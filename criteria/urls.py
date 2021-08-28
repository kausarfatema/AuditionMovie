from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('', views.addquestionview,name='questionadd'),
    path('takeaudition/<int:pk>/', views.start_exam_view, name='takeaudi'),
    path('calculate-marks/', csrf_exempt(views.calculate_marks_view),name='calculate-marks'),
    path('questionsview/<int:pk>/',views.allquestionview,name='view-question'),
    path('questiondeleteview/<int:pk>/',views.deletequestion, name='delete-question'),
    path('updatequestionview/<int:pk>/<int:alt_pk>/',views.updatequestion, name='update-question'),
    
    ]