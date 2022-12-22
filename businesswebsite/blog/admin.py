from django.contrib import admin
from .models import Post, Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

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