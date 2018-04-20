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
    path('')

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns