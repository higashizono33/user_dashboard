from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard', UserView.as_view(), name='dashboard'),
    path('new', UserCreateView.as_view(), name='new'),
    path('edit/<int:pk>', UserEditView.as_view(), name='edit_user'),
    path('password_update/<int:pk>', password_update, name='password_update'),
    path('delete/<int:pk>', UserDeleteView.as_view(), name='delete_user'),
    path('edit/profile/<int:pk>', ProfileEditView.as_view(), name='edit_profile'),
    path('password_update/profile', profile_pass_update, name='profile_pass_update'),
    path('description_update/profile', profile_desc_update, name='profile_desc_update'),
    path('show/<int:user_id>', ProfileView.as_view(), name='profile'),
    path('post_message', post_message, name='post_message'),
    path('post_comment/<int:message_id>', post_comment, name='post_comment'),
    path('delete_message/<int:message_id>', delete_message, name='delete_message'),
    path('delete_comment/<int:comment_id>', delete_comment, name='delete_comment'),
    path('edit_message/<int:message_id>', edit_message, name='edit_message'),
    path('edit_comment/<int:comment_id>', edit_comment, name='edit_comment'),
]