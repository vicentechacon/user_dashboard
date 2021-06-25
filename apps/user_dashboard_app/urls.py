from django.urls import path, include
from . import views

urlpatterns = [
        #--------------------------------> LOGIN PATHS <--------------------------------
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout/', views.logout),
        #--------------------------------> ADMIN PATHS <--------------------------------
    path('dashboard/admin', views.admin_dashboard),
    path('admin/users/edit/<int:user_id>', views.admin_edit),
    path('admin/users/change_password/<int:user_id>', views.admin_edit),
    path('users/<int:user_id>/delete', views.admin_delete),
    path('users/new', views.admin_add_new),
        #--------------------------------> USER PATHS <--------------------------------
    path('dashboard/', views.dashboard),
    path('users/edit/<int:user_id>', views.user_edit),
    path('users/edit/description/<int:user_id>', views.user_edit_description),
    path('users/<int:user_id>', views.show_user),
    path('users/<int:user_id>/post_message', views.post_message),
    path('users/<int:message_id>/post_comment', views.post_comment),
    path('delete/<int:message_id>', views.delete_message),
    path('delete/comment/<int:comment_id>', views.delete_comment),
    path('change_password/<int:user_id>', views.change_password),
]