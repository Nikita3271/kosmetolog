"""
Definition of models.
"""
from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models
from datetime import datetime  # добавлен импорт datetime

class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст новости')
    image = models.FileField(null=True)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Автор")
    def __str__(self):
        return self.title

admin.site.register(Blog)

class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментария")
    date = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Дата комментария")  # изменено
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Статья комментария")

    def __str__(self):
        return 'Комментрарий %d %s к %s' % (self.id, self.author, self.post)

    class Meta:
        db_table = "Comment"
        ordering = ["-date"]
        verbose_name = "Комментарий к статье блога"  # изменено
        verbose_name_plural = "Комментарии к статьям блога"

admin.site.register(Comment)
