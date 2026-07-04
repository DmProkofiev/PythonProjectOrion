from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.defaultfilters import title
from board.forms import PublicationForm


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

def remove_blog_view(request):
    pass

def edite_blog_view(request):
    pass


