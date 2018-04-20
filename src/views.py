from rest_auth.registration.views import LoginView, VerifyEmailView, RegisterView
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import mixins, generics
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import AttachmentSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import simplejson
from . import constants
from .models import *
from .serializers import AttachmentSerializer, MessageSerializer, RecipientSerializer, \
    HeaderSerializer

class LoginViewCustom(LoginView):
    authentication_classes = (TokenAuthentication,)

class MessageView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, )

    def post(self, request):
        data = request.data
        user = request.user
        required_fields = ''
        body = data.get('body', None)
        if not body:
            required_fields += 'body,'
        to_address = data.get('to', None)
        if not to_address:
            required_fields += ' to,'
        subject = data.get('subject', None)
        if not subject:
            required_fields += ' subject,'
        if required_fields:
            return  Response({'error': {'required fields: %s' % (required_fields)}},
                             status=status.HTTP_400_BAD_REQUEST)
        draft = data.get('draft', False)
        reply_to = data.get('reply_to', None)
        msg_serializer = MessageSerializer(data={
            'subject': subject,
            'body': body,
            'created_by': user,
            'draft': draft,
            'reply_to': reply_to
        })
        if not msg_serializer.is_valid():
            return Response(msg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        attachments = data.get('attachments', None)
        attachment_serializer = AttachmentSerializer(data=attachments, many=True)
        if not attachment_serializer.is_valid():
            return Response(attachment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        message = Message.objects.create(body=body, created_by=user, draft=draft,
                                         subject=subject, reply_to=reply_to)
        to_address_es = to_address.split(',')
        for to in to_address_es:
            to  = to.strip()
            Recipient.objects.create(msg_id=message.msg_id, email=to, header='to')
        for attachment in attachments:
            file_path = attachment.get('file_path', None)
            file_name = attachment.get('file_name', None)
            attachment_obj = Attachment.objects.get(file_name=file_name,
                                                    file_path=file_path)
            attachment_obj.message = message
            attachment_obj.save()

        return Response(status=status.HTTP_201_CREATED)

    def update(self, request):
        data = request.data
        msg_id = data.get('message', None)
        try:
            message = Message.objects.get(pk=msg_id)
            message.update(data)
        except ObjectDoesNotExist:
            return Response({'error': {'message id is missing'}}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

def group_messages(messages):
    return messages


def sent_emails(request):
    user = request.user
    messages = Message.objects.filter(created_by=user).order_by('updated_at')
    paginator = Paginator(messages, constants.PAGINATION_MESSAGES)
    page = request.GET.get('page', 0)
    messages = paginator.get_page(page)
    grouped_messages = group_messages(messages)
    return HttpResponse(simplejson.dumps(grouped_messages), content_type='application/json')

def read_email(request):
    if request.method == 'POST':
        user = request.user
        msg_id = request.data.get('message', None)
        try:
            recipient = Recipient.objects.get(email=user.email, message=msg_id)
            recipient.read = True
            recipient.save()
        except ObjectDoesNotExist:
            return Response({'error': {'message does not exist'}}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


def received_emails(request):
    user = request.user
    messages = Recipient.objects.filter(email=user.email)
    paginator = Paginator(messages, constants.PAGINATION_MESSAGES)
    page = request.GET.get('page', 0)
    messages = paginator.get_page(page)
    grouped_messages = group_messages(messages)
    return HttpResponse(simplejson.dumps(grouped_messages), content_type='application/json')


class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, *args, **kwargs):
    file_serializer = AttachmentSerializer(data=request.data)
    if file_serializer.is_valid():
      file_serializer.save()
      return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)