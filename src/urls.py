"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from django.conf import settings
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from django.urls import include, path, re_path
from src import views
from django.contrib import admin
schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view),
    path('rest-auth/login/', views.LoginViewCustom.as_view(), name='rest_login'),
    path('message/', views.MessageView.as_view, name='message_view'),
    path('sent_emails/', views.sent_emails, name='sent_emails'),
    path('received_emails/', views.received_emails, name='received_emails'),
    path('upload_file/', views.FileView.as_view(), name='file_upload'),
    path('message/read/', views.read_email, name='read_email'),
    # get message details
    path('message_details/<str:msg_id>/', views.MessageDetailsApiView.as_view(), name='message_details')
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns