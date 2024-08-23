from django.urls import path
from .api import SendInterestView, AcceptRejectInterestView, SendMessageView
from .views import chat_room

urlpatterns = [
    path('send-interest/<int:user_id>/', SendInterestView.as_view(), name='send-interest'),
    path('accept-reject-interest/<int:interest_id>/', AcceptRejectInterestView.as_view(), name='accept-reject-interest'),
    path('send-message/<int:user_id>/', SendMessageView.as_view(), name='send-message'),
    path('chat/<str:room_name>/', chat_room, name='chat-room'),
]
