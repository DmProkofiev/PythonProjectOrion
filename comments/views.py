from . import models
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from board.models import Publication
from .models import Comments


@login_required
def comment_add_view(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id, status='active')
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Comments.objects.create(publication=publication,author=request.user,text=text)
    return redirect('board:detail', slug=publication.slug)

@login_required
def comment_delete_view(request, pk):
    comment = get_object_or_404(Comments, pk=pk)
    if not (request.user == comment.author or request.user.is_staff):
        return redirect('board:detail', slug=comment.publication.slug)
    publication_slug = comment.publication.slug
    comment.delete()
    return redirect('board:detail', slug=publication_slug)




