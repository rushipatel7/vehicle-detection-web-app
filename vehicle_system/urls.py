"""vehicle_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, reverse
from django.conf.urls import url
from accounts import views as ac
# from plate_api import views as pa
# from plate_api.video_stream import index
from vehicle_detect.video_stream import index
from vehicle_detect import views as vd
from plate_api import views as plate_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', ac.register, name='register'),
    path('login/', ac.userlogin, name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='parking management/park_login.html', redirect_field_name='login'),
         name='logout'),
    path('index/', vd.index, name='index'),
    path('', vd.landing, name='landing'),
    path('result/', vd.yolo_backend, name='yolo_backend'),
    path('streaming/', index, name='streaming'),
    path('error-404/', vd.error_404, name="error404"),
    path('error-500/', vd.error_500, name="error500"),
    path('error-validation/', vd.error_validation, name="errorvalidation"),
    path('api/', plate_view.plateApi, name="api"),
    path('park_commercial', vd.commercial_history, name='commercial_history'),
    path('stream/', vd.streaimg, name="stream"),
    path('park_resident/',vd.resident_history, name="resident_history"),
    path('chat/',vd.chat,name="chat"),
    path('result-second/', vd.btnSecondModel, name='yolo_crnet'),
]
