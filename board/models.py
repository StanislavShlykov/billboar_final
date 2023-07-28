from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.cache import cache


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    cat_name = models.CharField(max_length=50, unique=True)
    users = models.ManyToManyField(User, through='UserCategory')

    def __str__(self):
        return f'{self.cat_name}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    time_in = models.DateTimeField(auto_now_add=True)
    post_name = models.CharField(max_length=100)
    post_text = models.TextField(default="Тут должен быть идиотский контент, а будет абракадабра, для проверки задания: дурак ываываываф идиот ыафыаываывфа мудак ываф ываф ывп фывп фвап фвп выа фывп фыва выа ыфвп выа фыв афвыа ывф.")
    category = models.ManyToManyField(Category, through='PostCategory')
    file = models.FileField(upload_to='my_downloads', blank=True)

    def preview(self):
        return self.post_text[:20] + '...'

    def __str__(self):
        return f'{self.post_name.title()} {self.time_in}: {self.preview()}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    #
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     cache.delete(f'news - {self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class UserCategory(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

class Response(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    resp_date = models.DateTimeField(auto_now_add=True)



