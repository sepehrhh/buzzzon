from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django_eventstream import send_event

from . import models, serializers


class ListCreateRoom(generics.ListCreateAPIView):
    serializer_class = serializers.RoomSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return models.Room.objects.filter(callee=self.request.user)

    def create(self, request, *args, **kwargs):
        if models.Room.objects.filter(room_id=request.data.get('room_id'), callee=request.user).exists():
            return Response('room with this id already exists', status=status.HTTP_406_NOT_ACCEPTABLE)

        # create the room
        room = models.Room.objects.create(
            callee=self.request.user,
            room_id=request.data.get('room_id'),
        )
        # then add the callee himself/herself to participants
        room.participants.add(self.request.user.id)
        serializer = self.serializer_class(room)
        # send_event('navid', 'message', {'text': 'SSE Channel With Client for CreateRoom'})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyRoom(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.RoomSerializer
    queryset = models.Room.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(self.queryset, id=self.kwargs.get('pk'), callee=self.request.user)


class JoinRoom(generics.CreateAPIView):
    serializer_class = serializers.RoomSerializer
    queryset = models.Room.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        # get the room
        room = get_object_or_404(models.Room, room_id=request.data.get('room_id'))
        # add user to room participants
        room.participants.add(request.user.id)
        # change room status to "on_call"
        room.status = 2
        room.save()
        # serialize the data
        serializer = self.serializer_class(room)
        # send_event('test', 'message', {'text': 'SSE Channel With Client for JoinRoom'})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class ListCreateContact(generics.ListCreateAPIView):
    serializer_class = serializers.ContactSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return models.Contact.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(models.User, email=request.data.get('contact'))
        contact = models.Contact.objects.create(
            contact=user,
            owner=request.user,
            contact_name=request.data.get('contact_name'),
            detail=request.data.get('detail'),
        )
        serializer = self.serializer_class(contact)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class RetrieveUpdateDestroyContact(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ContactSerializer
    queryset = models.Contact.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(self.queryset, id=self.kwargs.get('pk'), owner=self.request.user)


def confirm_password_reset(request, first_token, password_reset_token):
    return redirect("/auth/#/resetPasswordConfirm/" + first_token + "/" + password_reset_token)


def confirm_email(request, key):
    return redirect("/auth/#/verifyEmail/" + key)


class ListMessage(generics.ListAPIView):
    serializer_class = serializers.MessageSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.Message.objects.all()

    def list(self, request, *args, **kwargs):
        receiver_id = request.query_params.get('user')
        if receiver_id:
            # if receiver id found in query params
            receiver_id = int(request.query_params.get('user'))
            messages = models.Message.objects.filter(
                Q(receiver_id=receiver_id, sender=request.user) | Q(receiver=request.user, sender_id=receiver_id))
        else:
            # if no receiver id found in query params
            messages = models.Message.objects.filter(sender=request.user)

        serializer = self.serializer_class(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserDetails(generics.ListAPIView):
    serializer_class = serializers.UserDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return models.User.objects.filter(id=self.request.user.id)


class Signaling(generics.CreateAPIView):
    serializer_class = serializers.RoomSerializer
    queryset = models.Room.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = request.data
        room = models.Room.objects.get(room_id=request.data.get('room'))
        for user in room.participants.all():
            if user != request.user:
                caller = user

        send_event(caller.email, 'message', data.get('data'))
        return HttpResponse("signaling received")
