# users/tests/test_consumers.py
from django.test import TestCase
from channels.testing import WebsocketCommunicator
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumer import ChatConsumer
from django.contrib.auth import get_user_model

User = get_user_model()

# Set up URL routing for testing
application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/chat/<str:room_name>/", ChatConsumer.as_asgi()),
        ])
    ),
})

class ChatConsumerTestCase(TestCase):
    async def test_chat_message(self):
        # Create test users
        user1 = await User.objects.create_user(username='user1', password='password')
        user2 = await User.objects.create_user(username='user2', password='password')

        communicator = WebsocketCommunicator(
            application,
            '/ws/chat/test_room/',
            user=user1
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.send_json_to({
            'message': 'Hello from user1'
        })
        response = await communicator.receive_json_from()
        self.assertEqual(response['message'], 'Hello from user1')
