from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Categoría')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Fecha de modificación')

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['-created']
    
    def __str__(self):
        return self.name

class Post(models.Model):

    title = models.CharField(max_length=200, verbose_name = 'Título')
    content = models.TextField(verbose_name='Contenido')
    published = models.DateTimeField(verbose_name='Fecha de publicación', default=now)
    image = models.ImageField(verbose_name='Imagen', upload_to='blog', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'Autor')
    categories = models.ManyToManyField(Category, verbose_name = 'Categorías', related_name='get_posts')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Fecha de modificación')

    class Meta:
        verbose_name = ("Publicación")
        verbose_name_plural = ("Publicaciones")
        ordering = ['-created']

    def __str__(self):
        return self.title
