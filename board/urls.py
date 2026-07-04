from django.urls import path
from board import views

app_name = 'board'

urlpatterns = [
    path('form/', views.board_form_view, name='board_form')
]