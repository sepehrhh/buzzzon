from rest_framework import serializers
from . import models

from django.contrib.auth import settings

from allauth.account.models import EmailAddress
from allauth.account.forms import ResetPasswordForm
from dj_rest_auth.serializers import (
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    PasswordChangeSerializer,
    UserDetailsSerializer
)
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(UserDetailsSerializer, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')
        read_only_fields = ('email', 'id',)


class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField()


class PasswordSerializer(PasswordResetSerializer):
    password_reset_form_class = ResetPasswordForm


class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    def save(self):
        if not EmailAddress.objects.filter(user=self.user).exists():
            EmailAddress.objects.create(user=self.user, email=self.user.email, verified=True, primary=True)
        return self.set_password_form.save()


class CustomPasswordChangeSerializer(PasswordChangeSerializer):
    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = getattr(
            settings, 'OLD_PASSWORD_FIELD_ENABLED', False
        )
        self.logout_on_password_change = getattr(
            settings, 'LOGOUT_ON_PASSWORD_CHANGE', False
        )
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

        self.empty_old_password = True if self.user.password == '' else False

        if not self.old_password_field_enabled or self.empty_old_password:
            self.fields.pop('old_password')

    def save(self):
        super().save()
        if self.empty_old_password:
            if not EmailAddress.objects.filter(user=self.user).exists():
                EmailAddress.objects.create(user=self.user, email=self.user.email, verified=True, primary=True)


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'callee',
            'participants',
            'created',
            'status',
            'room_id',
        )
        model = models.Room
        validators = []  # remove default validation


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'owner',
            'contact',
            'contact_name',
            'detail',
            'created',
        )
        model = models.Contact


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'sender',
            'receiver',
            'message',
            'created',
        )
        model = models.Message
