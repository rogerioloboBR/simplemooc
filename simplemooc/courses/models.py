from django.db import models

from django.conf import settings


class CourseManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | \
            models.Q( description__icontains=query))


# Create your models here.
class Course(models.Model):

    name = models.CharField('Nome',max_length=100)
    slug = models.SlugField('Atalho')
    description = models.TextField('Descricao Simples', blank= True)
    about = models.TextField('Sobre o Curso' , blank=True)
    start_date = models.DateField('Data de Inicio', null=True, blank=True)
    image = models.ImageField(upload_to ='courses/images', verbose_name='Imagem', null=True,blank=True)
    created_at = models.DateTimeField('Criado em',auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em', auto_now=True)

    objects = CourseManager()

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('courses:details',(),{'slug':self.slug})
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['name']

class Enrollment(models.Model):

    STATUS_CHOICES =(
        (0,'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Usuario',
        related_name='enrollments'
    )

    course = models.ForeignKey(
        Course,
        verbose_name='Curso',
        related_name='enrollments'
    )
    status = models.IntegerField('Situacao', choices=STATUS_CHOICES, default=0, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em', auto_now=True)

    def active(self):
        self.status = 1
        self.save()

    def is_approved(self):
        return self.status == 1

    class Meta:
        verbose_name='Inscricao'
        verbose_name_plural ='Inscricoes'
        unique_together =(('user','course'),)


class Announcement(models.Model):
    course = models.ForeignKey(Course, verbose_name='Curso', related_name='announcements')
    title = models.CharField('Titulo', max_length=100)
    content = models.TextField('Conteudo')

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name= 'Anuncio'
        verbose_name_plural = 'Anuncios'
        ordering = ['-created_at']


class Comment(models.Model):

    announcement = models.ForeignKey(Announcement, verbose_name='Anuncio', related_name='comments'
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='usuario')
    comment = models.TextField('Comentario')

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['created_at']
