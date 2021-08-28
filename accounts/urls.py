from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('tables/', views.viewphotographerapplications,name='phototable'),
    path('tables/<int:id>',views.viewphotodetail, name="photogr"),
    path('',views.admin_panel,name='admin-panel'),
    path('recruter/',views.recruterdashboard, name='recruter-dash'),
    path('recruter/updateprofile/',views.recruterprofile, name='update-recruter'),
    path('adfilter/updateprofile/',views.talentprofile, name='update-profile'),
    path('upld/<int:pk>/', views.create_phto,name="upload-file"),
    path('delete/',csrf_exempt(views.deletephototgrapher) , name="delete-ph"),
    path('recdelete/',csrf_exempt(views.deleterecruter),name="deleterec"),
    path('appointments/',views.photograherappointment,name="appointment"),
    path('appointments/<int:id>/',views.viewphotodetailapp, name="photog"),
    path('applications/',views.viewapplicationresult, name='applications'),
    path('appoints/',views.appointmentstalent, name='talappoint'),
    path('horror/<int:pk>/', views.horrorads, name='horror'),
    path('phappointment/',views.photoappoint,name='photoappoint'),
    path('phappointment/<int:pk>',views.deleteAppointment,name='canap'),
    path('updateappointment/<int:pk>',views.updateAppointment, name='updateappoint'),
    path('uploadwork/',views.uploadwork, name="upload-work"),
    path('collections/',views.viewfolder, name="view-folder"),
    path('gallery/<int:pk>/', views.viewfoldertalent,name="gallery"),
    path('collections/<int:pk>/', views.viewpictures, name="view-pic"),
    path('gallerypictures/<int:pk>/',views.viewpicturestalent, name="view-gallery"),
    path('collections/addpictures/<int:pk>/', views.addpictures, name='ad-pic'),
    path('collections/picture/<int:pk>/<int:pk_alt>/',views.deletepicture, name="del-pic"),
    path('photopdf/',views.GeneratePdf.as_view(),name="pdfphoto"),
    path('moviepdf/',views.GeneratePdfMovie.as_view(),name="pdfmovie"),
    path('givefeedback/<int:pk>/<int:alt_pk>/',views.givefeedback,name='givefeeds'),
    path('recruterapp/',views.createrecruterapplication,name='recruterapp'),
    path('viewrecruterapp/',views.viewrecruterapplication,name='viewrecruterapp'),
    path('view/feedback/<int:pk>/',views.viewfeedback,name='viewfeedback'),
    path('paymentreport/', views.generatepaymentpdf.as_view(),name='paymentreport'),
    path('try/', views.trik, name='tricks')
    
    
    ]