from rest_framework import serializers
from .models import Interest, ChatMessage


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'from_user', 'to_user', 'status', 'timestamp']


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'recipient', 'message', 'timestamp']
