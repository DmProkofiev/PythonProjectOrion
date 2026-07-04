from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from orion import settings


class Tag(models.Model):
    name = models.CharField('название', max_length = 50, unique = True)
    slug = models.SlugField('slug', max_length = 60, unique = True)

    class Meta:
        ordering = ['name']
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField('название', max_length = 80, unique = True)
    slug = models.SlugField('slug', max_length = 90, unique = True)

    class Meta:
        ordering = ['name']
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name

class Publication(models.Model):
    STATUS_CHOICES = (
        ('active', 'Активно'),
        ('sold', 'Продано'),
        ('archived', 'Архивировано'),
    )
    # СВЯЗИ
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='publications',verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='publications', verbose_name='Категория')
    tags = models.ManyToManyField(Tag, blank=True, related_name='publications', verbose_name='Теги')
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('Слаг', max_length=220, unique=True, blank=True)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    image = models.ImageField('Изображение', upload_to='publications/', blank=True, null=True)
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default='active')
    views = models.PositiveIntegerField('Просмотры', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Publication.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Ссылка на страницу объявления."""
        return reverse('board:detail', kwargs={'slug': self.slug})

    def get_price_display(self):
        """Форматированный вывод цены."""
        return f'{self.price:.2f} ₽'
