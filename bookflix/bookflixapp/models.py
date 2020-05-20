from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, FileExtensionValidator
#los validator te ahorran tener que hardcodear algunas validaciones que django ya provee



class Autor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50, default='')

    def __str__(self):
        return '%s %s' % (self.apellido, self.nombre)

    class Meta:
        verbose_name_plural = "Autores"
        ordering = ["apellido","nombre"]


class Genero(models.Model):
    nombre = models.CharField(max_length=25,unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Generos"
        ordering = ["nombre"]


class Editorial(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Editoriales"
        ordering = ["nombre"]


class Capitulo(models.Model):
    libro = models.ForeignKey('Libro', on_delete=models.SET_NULL, null=True) #libro al cual pertenece el capitulo
    numero = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name='Numero del capitulo', null=True, blank=True)
    nropaginas = models.PositiveIntegerField(validators=[MinValueValidator(1)],verbose_name="Numero de paginas", null=True, blank=True)

    def __str__(self):
        return str(self.libro) + ' - Capitulo: ' + str(self.numero)

    class Meta:
        verbose_name_plural = "Capitulos"
        ordering = ["numero"]
        unique_together = ('libro', 'numero',) #no existen 2 capitulos 1 para el mismo libro

    def content_file_name(instance, filename):
        nombre = str(instance.numero) + '- ' + filename
        return '/'.join(['libros', instance.libro.titulo, nombre])


    pdf = models.FileField(upload_to=content_file_name ,validators=[FileExtensionValidator(['pdf'],'Solo se permiten archivos pdf')])

    

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    nropaginas = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Numero de paginas")
    nrocapitulos = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Numero de capitulos")
    isbn = models.CharField(max_length=13,unique=True,validators=[RegexValidator('^(\d{10}|\d{13})$', 'El numero debe tener 10 o 13 digitos numericos')],verbose_name="ISBN")
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    genero = models.ManyToManyField(Genero)
    agnoedicion = models.DateField(verbose_name="Año de edicion")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = "Libros"
        ordering = ["titulo"]



class Novedad(models.Model):
    titulo = models.CharField(max_length=100)
    texto = models.TextField()
    creacion = models.DateTimeField(auto_now_add=True,verbose_name="Creacion")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = "Novedades"
        ordering = ["-creacion"]


