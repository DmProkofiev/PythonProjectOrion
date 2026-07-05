from django.urls import path
from board import views

app_name = 'board'

urlpatterns = [
    path('form/', views.board_form_view, name='board_form'),
    path('form/<slug:slug>/', views.blog_edite_view, name='board_edite'),
    path('<slug:slug>/', views.board_detail_view, name='detail'),
    path('delete/<slug:slug>/', views.board_confirm_delete_view, name='confirm_delete')
]