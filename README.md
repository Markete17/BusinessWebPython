# BusinessWebPython

## Personalizar panel Administrador

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

## Filtrar a la inversa una relación ManyToMany/OneToMany con el Template Tag: _set.all (Related name)

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