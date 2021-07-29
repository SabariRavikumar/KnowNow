from django.db import models
from django.contrib.auth.models import User
from myblog.models import Post
from django.utils import timezone

class Notification(models.Model):
    NOTIFICATION_TYPE =((1,'like'),(2,'comment'),(3,'follow'),(4,'add post'),(5,'update post'),(0,'fav cat'))

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post", blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciver')
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPE)
    date = models.DateTimeField(default=timezone.now)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return  f"Notification to {self.user}"

