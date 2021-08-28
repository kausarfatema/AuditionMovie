
from django.urls import path, include
from . import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('<int:pk>/', views.index,name='make-appointment'),
    path('test/',csrf_exempt(views.test)),
    path('pay/',csrf_exempt(views.payappointment),name='pay'),
    ]