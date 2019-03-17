from django.db import models

class Writer(models.Model):
    '''
        Writers should have id, name, age, email, address. (All fields are required)
    '''
    name = models.CharField(max_length=64,)
    age = models.PositiveIntegerField()
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=128)

    class Meta:
        ordering = ('name',)


class Article(models.Model):
    '''
        Articles should have id, title, excerpt, text, date created, date updated, writer, image. (Image is optional, the rest are required)
    '''
    title = models.CharField(max_length=100)
    excerpt = models.TextField(max_length=512)
    text = models.TextField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(
        Writer, on_delete=models.CASCADE)
    image = models.ImageField(blank=True)

    class Meta:
        ordering = ('update_at',)


class Blog(models.Model):
    '''
        Blogs should have id, title, articles. (articles are optional, the rest required).
    '''
    title = models.CharField(max_length=100, blank=False, default='')
    content = models.CharField(max_length=512, blank=False, default='')
    articles = models.ManyToManyField(
        Article, blank=True)

    class Meta:
        ordering = ('id',)
