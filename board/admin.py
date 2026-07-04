from django.contrib import admin

# apps/board/admin.py
from django.contrib import admin
from .models import Tag, Category, Publication


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Настройка отображения тегов в админке."""
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка отображения категорий в админке."""
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    """Настройка отображения объявлений в админке."""
    list_display = (
        'title',
        'author',
        'price',
        'category',
        'status',
        'views',
        'created_at',
    )

    list_filter = (
        'status',
        'category',
        'tags',
        'created_at',
        'author',
    )

    search_fields = (
        'title',
        'description',
        'author__username',
        'author__email',
        'category__name',
    )

    readonly_fields = ('views', 'created_at', 'updated_at')
    filter_horizontal = ('tags',)
    fieldsets = (
        (None, {
            'fields': ('author', 'title', 'slug', 'description', 'price', 'category', 'tags', 'image')
        }),
        ('Статус и статистика', {
            'fields': ('status', 'views', 'created_at', 'updated_at')
        }),
    )
    actions = ['make_active', 'make_sold', 'make_archived']

    def make_active(self, request, queryset):
        queryset.update(status='active')
        self.message_user(request, f'Статус {queryset.count()} объявлений изменён на "Активно".')

    make_active.short_description = 'Изменить статус на "Активно"'

    def make_sold(self, request, queryset):
        queryset.update(status='sold')
        self.message_user(request, f'Статус {queryset.count()} объявлений изменён на "Продано".')

    make_sold.short_description = 'Изменить статус на "Продано"'

    def make_archived(self, request, queryset):
        queryset.update(status='archived')
        self.message_user(request, f'Статус {queryset.count()} объявлений изменён на "Архивировано".')

    make_archived.short_description = 'Изменить статус на "Архивировано"'
