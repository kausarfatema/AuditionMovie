"""movieaudi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from accounts import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from ads import views as ad_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('home/',views.home,name='home'),
    path('custom-admin/',include('accounts.urls')),
    path('',views.landing,name='landing'),
    path('registerphoto/',views.photographereg,name='photoreg'),
    path('registertalent/',views.talentreg,name='talreg'),
    path('registerecruter/',views.recrutereg,name='recreg'),
    path('ajax/validate_username/',csrf_exempt(views.validate_username),name='validate_username'),
    
    path('ads/<int:pk>/<int:pk_alt>/',ad_view.try_pks,name='try-der'),
    path('test/',csrf_exempt(ad_view.testvalidate),name='test'),
    path('reset_password/', auth_views.PasswordResetView.as_view(),name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    path('ajax/load-cities',views.load_cities, name='ajax_load_cities'),
    path('ajax/load-districts/',views.load_districts,name='ajax_load_dictrict'),
    path('download/',views.downloadfile),
    path('ad/',include('ads.urls')),
    
    path('payment/',include('payment.urls')),
    path('application/',include('applications.urls')),
    path('add_questions/',include('criteria.urls')),
]



if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)