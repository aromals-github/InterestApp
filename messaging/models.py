# models.py
from django.db import models
from django.conf import settings


class Interest(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_interests')
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_interests')
    status = models.CharField(
        choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')],
        default='Pending',
        max_length=10
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}"


class ChatMessage(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}"

    def save(self, *args, **kwargs):
        # Check if both users have accepted the interest before allowing the message to be saved
        if not (Interest.objects.filter(from_user=self.sender, to_user=self.recipient, status='accepted').exists() and
                Interest.objects.filter(from_user=self.recipient, to_user=self.sender, status='accepted').exists()):
            raise ValueError("Cannot send a message unless both users have accepted the interest.")
        super().save(*args, **kwargs)

