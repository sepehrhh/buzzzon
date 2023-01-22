from django.contrib import admin
from django.urls import path
from django.urls import include, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from dj_rest_auth.registration.views import VerifyEmailView
from allauth.account.views import confirm_email
import django_eventstream

from chat import views as chat_views

urlpatterns = [
    path('', TemplateView.as_view(template_name='auth.html')),
    path('userAuth/', TemplateView.as_view(template_name='auth.html')),
    path('contacts/', TemplateView.as_view(template_name='contacts.html')),
    path('rooms/', TemplateView.as_view(template_name='room.html')),
    path('chats/', TemplateView.as_view(template_name='chats.html')),
    path('groups/', TemplateView.as_view(template_name='groups.html')),
    path('rooms/<str:room_id>/callee/', TemplateView.as_view(template_name='video-chat-callee.html')),
    path('rooms/<str:room_id>/caller/', TemplateView.as_view(template_name='video-chat-caller.html')),
    path('admin/', admin.site.urls),
    path('api/', include(('chat.urls', 'chat'), namespace='chat')),
    path('events/', include(django_eventstream.urls)),
    # REST AUTH
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('rest-auth/', include('dj_rest_auth.urls')),
    path('rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    re_path(r'^account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^rest-auth/registration/account-confirm-email/(?P<key>\w+)/', confirm_email, name="confirm_email"),
    re_path(r'^account-confirm-email/(?P<key>\w+)/', confirm_email, name="confirm_email"),
    re_path(r'^reset/(?P<first_token>\w+)/(?P<password_reset_token>[-\w]+)/',
            chat_views.confirm_password_reset, name="confirm_password_reset"),
]

urlpatterns += staticfiles_urlpatterns()
