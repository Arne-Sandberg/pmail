from rest_framework import serializers
from .models import Attachment, Message, Header, Recipient

class AttachmentSerializer(serializers.ModelSerializer):
  class Meta():
    model = Attachment
    fields = ('message', 'file_name', 'file_path', 'created_at', 'updated_at')

class MessageSerializer(serializers.ModelSerializer):
    class Meta():
        model = Message
        fields = ('message', 'created_by', 'body', 'created_at', 'updated_at', 'status')

class RecipientSerializer(serializers.ModelSerializer):
    class Meta():
        model = Recipient
        fields = ('message', 'seen', 'header', 'email', 'created_at', 'updated_at')

class HeaderSerializer(serializers.ModelSerializer):
    class Meta():
        model = Header
        fields = ('message', 'name', 'value', 'created_at', 'updated_at')