from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
# Thêm bài viết mới
    path("new_post", views.CreateNewPost.as_view(), name="new_post"),
# Sửa bài viết 
    path("post/<int:pk>/update_post", views.UpdatePost.as_view(), name="update_post"),
    # Xoá bài viết
    path("post/<int:pk>/delete_post", views.DeletePost.as_view(), name="delete_post"),
    path('drafts/', views.draft_list, name='draft_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    re_path(r'^register/', views.register, name='register'),
    re_path(r'^/', views.user_login,name="user_login"),
    # Additional URL patterns
    re_path(r'^/',views.user_logout,name='logout'),
    
    # Duy: Public draft
    path('post/<int:pk>/publish/', views.publish_post, name='publish_post'),

]
