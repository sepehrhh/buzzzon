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

class ContactRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return UserSerializer(value).data


class ContactSerializer(serializers.ModelSerializer):
    contact = ContactRelatedField(queryset=models.Contact.objects.all())

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

    def to_internal_value(self, data):
        data._mutable = True
        if self.instance is None:
            data['owner'] = self.context.get('request').user.id
        else:
            data['owner'] = None
        return super(ContactSerializer, self).to_internal_value(data)


class GroupSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        fields = (
            'id',
            'owner',
            'participants',
            'share_code',
            'name',
        )
        model = models.Group

    def to_internal_value(self, data):
        data._mutable = True
        if self.instance is None:
            data['owner'] = self.context.get('request').user.id
        else:
            data['owner'] = None
        return super(GroupSerializer, self).to_internal_value(data)

    def to_representation(self, instance):
        representation = super(GroupSerializer, self).to_representation(instance)
        representation['owner'] = UserSerializer(instance.owner).data
        return representation


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'sender',
            'receiver',
            'content',
            'created',
            'type',
        )
        model = models.Message
