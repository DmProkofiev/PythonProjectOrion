from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

from board.models import Publication, Category, Tag


# главная страница
def index_view(request):
    publications = Publication.objects.filter(status='active').select_related('author', 'category')

    query = request.GET.get('q')
    if query:
        publications = publications.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    category_id = request.GET.get('category')
    if category_id:
        publications = publications.filter(category_id=category_id)

    tag_id = request.GET.get('tag')
    if tag_id:
        publications = publications.filter(tags__id=tag_id)

    sort = request.GET.get('sort', '-created_at')
    publications = publications.order_by(sort)

    paginator = Paginator(publications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'publications': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
        'query': query,
        'selected_category': category_id,
        'selected_tag': tag_id,
        'selected_sort': sort,
    }
    return render(request, 'board/board_list.html', context)