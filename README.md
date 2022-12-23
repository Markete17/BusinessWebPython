# BusinessWebPython

Toda la información en: [Información](https://docs.hektorprofe.net/django/web-empresarial/)

**Índice**   
1. [Personalizar panel Administrador](#id1)
2. [Template Tag: _set.all (Related name) Filtrar Inversa](#id2)
3. [Procesadores de Contexto](#id3)
4. [Crear Templates Tags - Alternativa a los procesadores de contextos](#id4)
5. [Ordenación](#id5)
6. [Template Tag Auth - Mostrar usuario sesión](#id6)
7. [URL del panel de administrador en las vistas](#id7)
8. [Ck Editor](#id8)
9. [Formularios y validaciones](#id9)

## Personalizar panel Administrador<a name="id1"></a>

En <b>admin.py</b>, antes de registrar el modelo en el panel de administrador, para modificar la vista de los registros del model, es necesario crear
una clase que herede de <b>admin.modelAdmin</b>.
Este clase tiene varios métodos que hará que cambie la vista del administrador en ese modelo pudiendo poner filtros, buscadores, ordenaciones, etc.

- <b>readonly_fields</b>: Indica qué campos son solo de lectura para el panel admin (no se pueden ni eliminar ni modificar)

<a href="https://ibb.co/h848N9k"><img src="https://i.ibb.co/x5B5bLy/Captura.png" alt="Captura" border="0"></a>

- <b>ordering</b>: Para crear un filtro de ordenación por campos
- <b>search_fields</b>: Incluye una barra de búsqueda para poder buscar por los campos seleccionados
- <b>date_hierarchy</b>: Crea una jerarquía ordenada según una fecha del campo seleccionado
- <b>list_filter</b>: Crea un filtro a la derecha para poder buscar por los campos indicados
- <b>fields</b>: Indica los campos que se quieren ser modificados en el panel admin para editar y crear
- <b>fieldsets</b>: Es una tupla que permite crear una sección en el registro que contenga varios campos.
- <b>list_display</b>: Se indican los campos del objeto que se quiere mostrar en el panel. Para poder mostrar relaciones ManyToMany, OneToMany, etc.

Es necesario crear una función auxiliar que devuelva un string con las categorías que lo forman.
Para cambiar el nombre del campo en el panel de administrador, se usa la propiedad del método: <b>short_description</b>

Para más campos de <b>admin.ModelAdmin</b>: [Doc Django ModelAdmin](https://docs.djangoproject.com/es/4.0/ref/contrib/admin/#modeladmin-options)

<pre><code>
from django.contrib import admin
from .models import Post, Category

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated') # Indicar los campos de solo lectura para el admin
    list_display = ('title', 'author', 'published', 'post_categories') # Indica los campos que se muestran
    
    ordering = ('author', 'published') # Si se quiere ordenar por 1 la tupla debería tener la coma ('author',)
    search_fields = ('title', 'content','author__username') ## Agrega una barra de búsqueda. Para los objetos es necesario indicar su propiedad con la doble barra baja __
    date_hierarchy = 'published' # Se crea una jerarquía por fecha
    list_filter = ('author__username','categories__name') # Añade filtros por propiedades
	
	fieldsets = (
        (None, {
            'fields': ('title', 'content', 'published', 'image', 'author', 'categories')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('created', 'updated'),
        }),
    )

    # Los campos ManyToMany ni se pueden mostrar con list_display
    # para que se muestre es necesario crear una función

    def post_categories(self, obj):
        categories_list = [c.name for c in obj.categories.all()]
        return ', '.join(categories_list)
    
    post_categories.short_description = 'Categorías'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
</code></pre>


<h2><b>El panel de administrador quedaría de la siguiente manera: </b></h2>

<a href="https://ibb.co/1mdsZ4p"><img src="https://i.ibb.co/6W1vYqp/Captura2.png" alt="Captura2" border="0"></a>

## Filtrar a la inversa una relación ManyToMany/OneToMany con el Template Tag: _set.all (Related name)<a name="id2"></a>

Django permite hacer filtros a la inversa mediante template tag. Por ejemplo, teniendo esta un modelo Post que tiene una relación ManyToMany
con el modelo Category. Se quiere filtrar los post que tengan X categoría. Teniendo la URL:

<pre><code>

urlpatterns = [
    path('', views.blog, name='blog'),
    path('category/<int:category_id>/', views.category, name='category')
]

</code></pre>

Donde la vista views.py es:

<pre><code>
def category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    """
    En vez de hacer esto, usar template tag
    posts = Post.objects.filter(categories=category)

    result = {
        'category': category,
        'posts': posts
    }
    """
    return render(request, 'blog/category.html', {'category': category})

</code></pre>

En vez de pasar los posts filtrados por la categoría a la vista con el método filter y render, se puede hacer de una forma más sencilla en la vista
con el template tag <b><nombre_del_modelo>_set_all</b> y recorrer el modelo con un FOR.

<pre><code>
{% for post in category.post_set.all%}
</code></pre>

Para personalizar el nombre por defecto <b>_set.all</b>, es necesario cambiar el modelo añadiendo el parámetro <b>related_name</b>

<pre><code>
class Post(models.Model):
	.....
    categories = models.ManyToManyField(Category, verbose_name = 'Categorías', related_name='get_posts')
</code></pre>

<pre><code>
{% for post in category.get_posts.all%}
</code></pre>

## Procesadores de Contexto<a name="id3"></a>

El contexto es el diccionario que se envía desde el views.py a la vista (el result). Los procesadores de contextos permiten que ese diccionario se pueda
enviar a diferentes vistas. 
1. Para crear esto, es necesario crear un fichero llamado <b>processors.py</b> (aunque el nombre no importa) en la app correspondiente.
2. En este fichero, se va a definir el diccionario a devolver, por ejemplo: 

<b>processors.py</b> 
<pre><code>
def ctx_dict(request):
    ctx = {'test': 'hola'}
    return ctx
</code></pre>

3. <b>Ir a settings.py</b> y en la lista context_processors, añadir el método creado:

<b>processors.py</b> 
        'OPTIONS': {
            'context_processors': [
				.....
                'social.processors.ctx_dict'
            ],
</code></pre>

4. Ya está, ahora la variable <b>test</b> definida en el método <b>ctx_dict()</b> se puede utilizar en todas las vistas html.

## Crear Templates Tags - Alternativa a los procesadores de contextos (consume más)<a name="id4"></a>

1. Crear un paquete dentro de la app. Como todo paquete necesita tener dentro un archivo <b>__init__.py</b>
2. Crear un archivo <b>[nombre_fichero_creado].py</b> que contenga la variable register que será quien registre la nueva template tage que se quiere crear.
3. Se define el método para obtener la variable deseada para compartirlo entre todas las templates.
4. Este método se anota con la anotación <b>@register.simple_tag</b> para que sea registrada en la biblioteca de tags del proyecto.

Ejemplo:

<pre><code>
from django import template
from pages.models import Page

register = template.Library()

@register.simple_tag
def get_page_list():
    pages = Page.objects.all()
    return pages
</code></pre>

5. Con esto ahora en cualquier vista se puede insertar la variable creada con una template tag que será el nombre del método. 
Se tiene que cargar con el template tag <b>{%load [nombre_fichero_creado]%}</b> y a continuación usar la template tag almacenada:

<b>Cabe destacar que se puede renombrar la variable con la palabra as [nombre]</b>
<pre><code>
            {% load pages_extras %}
            {% get_page_list as page_list %}
            {% for page in page_list %}
              a href="{% url 'page' page.id %}" class="link">{{page.title}} /a> {% if not forloop.last %}·{% endif %}
            </p>
</code></pre>

## Ordenación<a name="id5"></a>

Una herramienta para ordenar las listas es incluir un campo en el modelo llamado order que sea un models.SmallIntegerField(verbose_name='Orden', default=0).
Y en el Meta, ordering = ["order","title"] que ordene por ese número.

## Template Tag Auth - Mostrar usuario sesión<a name="id6"></a>

En settings.py, en 'context_processors' existe un procesador de contexto llamado auth, que contiene toda la información del usuario.
Por lo tanto, en cualquier vista, al poner {{user}} se mostrará el nombre del usuario conectado a la sesión.

Entonces, en la vista se puede mostrar el usuario y comprobar si está autenticado, por ejemplo:

<pre><code>
      {% if user.is_authenticated %}
      <span {{user}} /span>
      {% endif %}
</code></pre>

## URL del panel de administrador en las vistas<a name="id7"></a>

Gracias a Django, con el template tag Url, se puede redirigir al panel de administrador en cualquier vista para poder crear, eliminar, modificar algún
registro del modelo de datos.

<b>PLANTILLA:</b>
admin:[APP]_[MODELO]_[ACCION] [OBJ.ID]

<b>EJEMPLO:</b>
<pre><code>
a> href="{% url 'admin:pages_page_change' page.id %}">Editar /a>
</code></pre>

<a name="id1"></a>

## Ck Editor<a name="id8"></a>

Por ejemplo, para mejorar los cuadros de texto TextField y sean editables modo Word, es necesario instalar la biblioteca <b>django-ckeditor</b>
1. pipenv shell
2. pip install django-ckeditor
3. En settings, incluir en INSTALLED_APPS la app 'ckeditor'
4. En el modelo, incluir la biblioteca from ckeditor.fields import RichTextField
5. Definir el campo que sea un RichTextField: content = RichTextField(verbose_name="Contenido")
6. Para modificar la configuración del CkEditor, se tiene que poner en <b>settings.py</b> una constante llamada CKEDITOR_CONFIGS para establecer la configuración:

Con esta se abre todo lo que se puede hacer con ckeditor
<pre><code>
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None
    }
}
</code></pre>

Pero quizás sea mejor incluir un aspecto más sencillo:

<pre><code>
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Basic'
    }
}
</code></pre>
https://docs.hektorprofe.net/django/web-empresarial/personalizando-panel-administrador-parte-3/
Más información en: [Link CkEditor Docs](https://github.com/django-ckeditor/django-ckeditor)

## Formularios y validaciones<a name="id9"></a>

1. Crear una app contact que va a contener el formulario de contacto.
2. Crear un fichero <b>forms.py</b> que contenga una clase forms.Form

<pre><code>
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label="Nombre", required=True)
    email = forms.EmailField(label="Email", required=True)
    content = forms.CharField(label="Contenido", required=True, widget=forms.Textarea())
</code></pre>

A diferencia del modelo, forms tiene diferentes campos. Más documentación en

[Link Forms Doc](https://docs.djangoproject.com/en/4.0/topics/forms/)
[Link Forms Doc](https://docs.djangoproject.com/en/4.0/ref/forms/fields/#built-in-field-classes)

3. Insertar el formulario en la vista. En views.py incluir el método que renderizará y mandará el formulario a la vista:

<pre><code>
def contact(request):
    contact_form = ContactForm()
    return render(request, 'contact/contact.html',{'form': contact_form})
</code></pre>

4. Añadir el form a la vista

Con la variable nombrada: {{form.as_table}} y se le puede dar formato as_ table, ul, p etc.
              