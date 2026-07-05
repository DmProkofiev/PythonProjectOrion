from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import title
from board.forms import PublicationForm
from board.models import Tag, Publication, Category


@login_required
def board_form_view(request):
    title = 'Создать объявление'
    if request.method == 'POST':
        form = PublicationForm(request.POST, request.FILES)
        if form.is_valid():
            publication = form.save(commit=False)
            publication.author = request.user
            publication.save()
            form.save_m2m()
    else:
        form = PublicationForm()
    return render(request, 'board/board_form.html', {'form': form, 'title': title})

@login_required
def board_detail_view(request, slug):
    publication = get_object_or_404(Publication,slug=slug, status='active')
    publication.views += 1
    publication.save(update_fields=['views'])

    comments = publication.comments.select_related('author').all()

    context = {
        'publication': publication,
        'comments': comments,
    }
    return render(request, 'board/board_detail.html', context)

@login_required
def board_confirm_delete_view(request, slug):
    publication = get_object_or_404(Publication, slug=slug, author=request.user)
    if request.method == 'POST':
        publication.delete()
        return redirect('board:index')
    return render(request, 'board/board_confirm_delete.html', {'publication': publication})

@login_required
def blog_edite_view(request, slug):
    publication = get_object_or_404(Publication, slug=slug, author=request.user)
    if request.method == 'POST':
        form = PublicationForm(request.POST, request.FILES, instance=publication)
        if form.is_valid():
            form.save()
            return redirect('board:detail', slug=publication.slug)
    else:
        form = PublicationForm(instance=publication)
    return render(request, 'board/board_form.html', {
        'form': form,
        'title': 'Редактировать объявление',
    })


