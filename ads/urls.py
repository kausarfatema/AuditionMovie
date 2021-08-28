from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns=[
	path('producer/',views.categorylist, name='category-list'),
	path('updatead/<int:pk>/',views.updatead,name='update-ad'),
	path('deletead/<int:pk>/',views.deletead, name='delete-ad'),
	path('ad_filter',views.filteredAd, name='filter-ad'),
	path('detailad/<int:pk>/',views.detailad,name='detailad'),
	path('apply/<int:pk>/',views.apply, name='apply'),
	path('applications/<int:pk>/',views.allapplications,name='ad-apply'),
	path('applicationdetail/<int:pk>/<int:pk_app>/<int:pk_u>/',views.viewapplicationdetail, name= 'app-detail'),
	path('applicationdetail/delete/',csrf_exempt(views.regect), name="regect-appl"),
	path('applicationdetail/accept/',csrf_exempt(views.accept), name="accept-appl"),
	path('applicationdetail/hold/',csrf_exempt(views.hold), name="hold-appl"),
	path('updateadmin/<int:id>/<int:pk>/', views.updateadadmin, name="upad"),
	path('deleteadmin/<int:id>/<int:pk>/', views.deleteadadmin, name="delad"),
	path('startapplication/<int:pk>/',views.startapplication, name="start"),
]