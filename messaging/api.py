from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Interest, ChatMessage
from users.models import CustomUser as User


class SendInterestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        """
        Handles sending an interest from the authenticated user to another user.

        Args:
            request: The HTTP request object.
            user_id: The ID of the user to whom the interest is being sent.

        Returns:
            Response: A response indicating whether the interest was successfully sent or if it already exists.
        """
        to_user = User.objects.get(id=user_id)
        if Interest.objects.filter(from_user=request.user, to_user=to_user).exists():
            return Response({'detail': 'Interest already sent.'}, status=status.HTTP_400_BAD_REQUEST)

        interest = Interest(from_user=request.user, to_user=to_user)
        interest.save()
        return Response({'detail': 'Interest sent successfully.'}, status=status.HTTP_201_CREATED)


class AcceptRejectInterestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, interest_id):
        """
        Handles accepting or rejecting an interest for the authenticated user.

        Args:
            request: The HTTP request object containing the action to perform.
            interest_id: The ID of the interest to be accepted or rejected.

        Returns:
            Response: A response indicating whether the interest was successfully accepted or rejected.
        """
        interest = Interest.objects.get(id=interest_id, to_user=request.user)
        action = request.data.get('action')

        if action == 'accept':
            interest.status = 'accepted'
        elif action == 'reject':
            interest.status = 'rejected'
        else:
            return Response({'detail': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

        interest.save()
        return Response(
            {'detail': f'Interest {interest.status} successfully.'},
            status=status.HTTP_200_OK)


class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        """
        Handles sending a message from the authenticated user to another user.

        Args:
            request: The HTTP request object containing the message to send.
            user_id: The ID of the user to whom the message is being sent.

        Returns:
            Response: A response indicating whether the message was
            successfully sent or if the users have not both accepted the interest.
        """
        recipient = User.objects.get(id=user_id)
        message = request.data.get('message')

        if not (
            Interest.objects.filter(
                from_user=request.user,
                to_user=recipient,
                status='accepted').exists() and Interest.objects.filter(
                        from_user=recipient,
                        to_user=request.user,
                        status='accepted'
                    ).exists()
            ):

            return Response(
                {
                    'detail': 'Both users must accept the interest to send messages.'
                }, status=status.HTTP_400_BAD_REQUEST)

        chat_message = ChatMessage(sender=request.user, recipient=recipient, message=message)
        chat_message.save()
        return Response({'detail': 'Message sent successfully.'}, status=status.HTTP_201_CREATED)
