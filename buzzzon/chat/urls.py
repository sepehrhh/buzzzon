from django.urls import path
from . import views

urlpatterns = [
    path('getUser/', views.GetUserDetails.as_view(), name='get_user_details'),
    path('rooms/', views.ListCreateRoom.as_view(), name='list_room'),
    path('rooms/<int:pk>', views.RetrieveUpdateDestroyRoom.as_view(), name='room_detail'),
    path('rooms/join', views.JoinRoom.as_view(), name='join_room'),
    path('contacts', views.ListCreateContact.as_view(), name='list_contact'),
    path('contacts/<int:pk>', views.RetrieveUpdateDestroyContact.as_view(), name='contact_detail'),
    path('groups', views.ListCreateGroup.as_view(), name='list_group'),
    path('groups/<int:pk>', views.RetrieveUpdateDestroyGroup.as_view(), name='group_detail'),
    path('messages/', views.ListMessage.as_view(), name='list_messages'),
    path('signaling/', views.Signaling.as_view(), name='RTC_signaling')
]
