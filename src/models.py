import base64
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    subject = models.CharField(max_length=300, null=True)
    body = models.TextField(max_length=5000, blank=True)
    mime_text = models.TextField(max_length=10000, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    draft = models.BooleanField(default=False)
    reply_to = models.ForeignKey('Message', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Attachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True)
    file_path = models.FileField(null=True)
    file_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('file_name', 'file_name', 'message')


class Recipient(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    header = models.CharField(max_length=100) # to, cc etc
    email = models.CharField(max_length=300, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
         unique_together = ('message', 'email')

class Header(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    value = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('message', 'name',)




