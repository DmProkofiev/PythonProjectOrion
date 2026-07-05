from django.urls import path
from comments import views

app_name='comments'

urlpatterns = [
    path('comments/<int:publication_id>/', views.comment_add_view, name="comment_add"),
    path('comments/<int:pk>/delete/', views.comment_delete_view, name='comment_delete'),
]