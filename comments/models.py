from django.db import models
from board.models import Publication
from orion import settings
from users.models import User


class Comments(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='comments', verbose_name='Объявление')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author', verbose_name='Автор')
    text=models.TextField('Текст комментария')
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self):
        return f'Комментарий от {self.author.username}'