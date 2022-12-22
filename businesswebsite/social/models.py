from django.db import models

# Create your models here.
class Link(models.Model):
    key = models.SlugField(verbose_name="Nombre Clave", max_length=100) # Asegura que una cadena es una cadena slug, que es una cadena que sólo contiene letras, números, guiones bajos o guiones
    name = models.CharField(verbose_name="Red Social", max_length=200)
    url = models.URLField(verbose_name="Enlace", max_length=200, blank=True, null=True)
    created = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Fecha de modificación", auto_now=True)

    class Meta:
        verbose_name = ("Enlace")
        verbose_name_plural = ("Enlaces")
        ordering = (['name'])

    def __str__(self):
        return self.name
