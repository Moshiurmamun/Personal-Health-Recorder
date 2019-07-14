from django.urls import path, re_path, include
from .import views
from django.contrib.auth.views import (
    password_reset, password_reset_done, password_reset_confirm, password_reset_complete
)
from patient.views import story_list, story_create, story_detail, story_update, story_delete, about

app_name = 'accounts'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('registration/', views.Registration.as_view(), name='register'),
    path('logout/', views.logout_view, name="logout"),
    path('profile/about', about, name="about"),

    path('profile/edit', views.edit_profile, name="edit_profile"),
    path('profile/edit_basic', views.edit_info, name="edit_info"),
    path('profile/<username>', views.profile, name="profile"),
    path('profile/<username>/story_create', story_create, name="story_create"),


    re_path('profile/(?P<slug>[\w-]+)/', story_detail, name="story_detail"),
    re_path('edit/(?P<slug>[\w-]+)/', story_update, name="story_update"),
    re_path('delete/(?P<slug>[\w-]+)/', story_delete, name="story_delete"),

    path('change-password/', views.change_password, name='change_password'),

    path('reset-password/', password_reset, {'template_name': 'accounts/reset_password.html',
        'post_reset_redirect': 'accounts:password_reset_done', 'email_template_name': 'accounts/reset_password_email.html'},
        name='reset_password'),

    path('reset-password/done/', password_reset_done, {'template_name': 'accounts/reset_password_done.html'}, name='password_reset_done'),

    re_path('reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/', password_reset_confirm,
        {'template_name': 'accounts/password_reset_confirm.html' ,'post_reset_redirect': 'accounts:password_reset_complete'},
        name='password_reset_confirm'),

    path('reset-password/complete/', password_reset_complete, {'template_name': 'accounts/password_reset_complete.html'}, name='password_reset_complete'),


]
