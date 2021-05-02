from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Message(models.Model):
    head = models.ForeignKey('MessageHead', on_delete=models.CASCADE, related_name="messages")
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return self.message

    def get_json(self):
        json_data = {
            'message': self.message,
            'datetime': self.created.strftime("%m/%d/%Y, %H:%M:%S"),
            'userFrom': self.head.userFrom.username,
            'userTo': self.head.userTo.username
        }

        return json_data


class MessageHead(models.Model):
    userFrom = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, related_name="messages_sent")
    userTo = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="messages_received")

    def __str__(self):
        return f"from {self.userFrom} to {self.userTo}"

    
    