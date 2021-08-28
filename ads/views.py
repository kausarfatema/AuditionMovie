from django.shortcuts import render, redirect, get_object_or_404
from .forms import Adform,ApplicationForm
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
import datetime
from .models import Ad, Application, ApplPictures
from accounts.models import Category, Talent
from .filters import AdFilter
from criteria.models import Result
import json
from django.contrib import messages
from accounts.task import send_email_task
from criteria.models import Result
from django.contrib.auth.decorators import login_required
# Create your views here.

def testview(request):
	if request.method == 'POST':
		a_form= Adform(request.POST)
		if a_form.is_valid():
			a_form.save()
			return redirect('home')
	else:
		a_form=Adform()
		context={
		'a_form':a_form
		}

	return render(request,'testad.html',context)


def testvalidate(request):
	
	date=request.POST.get('date',None)
	tr=datetime.datetime.strptime(date,'%m/%d/%Y').strftime('%Y-%m-%d')
	print(tr)
	data={
		'is_appoint': Ad.objects.filter(date=tr).exists()
	}
	return JsonResponse(data)


@login_required
def filteredAd(request):
	ad= Ad.objects.all().filter(start_application=True)
	appl = Application.objects.filter(talent = request.user.talent)
	res = Result.objects.filter(status ='F',talent= request.user.talent)
	ads = Ad.objects.exclude(application__in=appl).filter(start_application=True)
	print(ads)
	myfilter = AdFilter(request.GET, queryset=ads)
	ads=myfilter.qs

	context = {
		'ads': ads,
		'myfilter': myfilter,
	}
	return render (request,'adfilter.html', context)

@login_required
def updatead(request,pk):
	ad= Ad.objects.get(id=pk)
	a_form= Adform(instance=ad)
	if request.method == 'POST':
		a_form=Adform(request.POST, request.FILES, instance=ad)
		if a_form.is_valid():
			a_form.save()
			return redirect('recruter-dash')

	context = {
		'a_form':a_form
	}
	return render(request, 'addupdate.html',context)

@login_required
def updateadadmin(request,id,pk):
	ad= Ad.objects.get(id=pk)

	a_form= Adform(instance=ad)
	if request.method == 'POST':
		a_form=Adform(request.POST, request.FILES, instance=ad)
		if a_form.is_valid():
			a_form.save()
			return redirect(reverse ('horror', kwargs={"pk":id}))

	context = {
		'a_form':a_form
	}
	return render(request, 'horupdate.html',context)

@login_required
def deleteadadmin(request,id, pk):
	ad= Ad.objects.get(id=pk)
	cats = Category.objects.get(id=id)
	if request.method == 'POST':
		ad.delete()
		return redirect(reverse ('horror', kwargs={"pk":id}))
	context={
		'ad':ad,
		'cats':cats
	
	}
	return render(request,'hordelete.html',context)

@login_required
def deletead(request, pk):
	ad= Ad.objects.get(id=pk)
	if request.method == 'POST':
		ad.delete()
		return redirect('recruter-dash')
	context={'ad':ad}
	return render(request,'addelete.html',context)

def categorylist(request):
	category=Category.objects.all()
	context={
	'category':category
	}
	return render(request, 'producer.html', context)



def try_pks(request, pk,pk_alt):
	print(pk + pk_alt)
	return redirect('home')


@login_required
def apply(request,pk):
	ad=Ad.objects.get(pk=pk)
	result=Result.objects.filter(ad=pk, talent=request.user.talent)
	
	

	if not result:
		return redirect(reverse ('detailad', kwargs={"pk":ad.id}))
	if ad.is_past_due:
		return redirect('landing')
	
	else:
		if request.method=='POST':
			length=request.POST.get('length')
			thumbnail = request.FILES.get('display')
			vid = request.FILES.get('vids')
			app=Application.objects.create(name ="application",talent = request.user.talent, recruter = ad.recruter, thumbnail = thumbnail, ads =ad, video=vid)
			for filenum  in range(0, int(length)):
				ApplPictures.objects.create(
					appli=app,
					img=request.FILES.get(f'image{filenum}'),)
			
			messages.success(request, 'Thank you for applying! You will get notified by email your status')
			return redirect (reverse('detailad', kwargs={"pk":ad.id}))
		
		else:
			ap_form=ApplicationForm()
			context={
			'ap_form':ap_form,
			'pk':pk,
			
			}

			return render(request,'applyad.html',context)
	

@login_required
def detailad(request,pk):
	result=Result.objects.filter(ad=pk, talent=request.user.talent).first()
	ad = Ad.objects.get(id=pk)
	applications= Application.objects.filter(ads=pk, talent=request.user.talent)
	context = {
		'ad':ad,
		'result':result,
		'applications':applications
	}
	return render(request,'addetail.html',context)


@login_required
def allapplications(request, pk):

	ad = Ad.objects.get(id=pk)
	applications = Application.objects.filter(ads=ad)

	context = {
		'applications':applications
	}
	return render(request, "adapplication.html",context)

@login_required
def viewapplicationdetail(request, pk, pk_app, pk_u):

	app = Application.objects.get(id = pk_app)

	talent = Talent.objects.get(id= pk_u)

	ad =  Ad.objects.get(id = pk)

	result = Result.objects.filter(ad = ad, talent = talent)

	ph = ApplPictures.objects.filter(appli = app)
	context = {
		'app':app,
		'talent': talent,
		'result': result,
		'ad':ad,
		'ph':ph,
	}

	return render(request,"applicationdetail.html", context)



def accept(request,*args,**kwargs):

	id = request.POST.get('id')
	email = request.POST.get('email')
	print(id)
	app =   get_object_or_404(Application, id=id)
	app.application_status = 'Accepted'
	app.save()
	send_email_task.delay('Application status','Your Application has been accepted','kausarbhimani7@gmail.com',[email])
	response = {'status': 1, 'message': "bhhhvvg"} 
	return HttpResponse(json.dumps(response), content_type='application/json')


def regect(request, *args,**kwargs):
	
	id = request.POST.get('id')
	print(id)
	email = request.POST.get('email')
	app =   get_object_or_404(Application, id=id)
	app.application_status = 'Rejected'
	app.save()
	send_email_task.delay('Application status','Your Application has been Rejected','kausarbhimani7@gmail.com',[email])
	response = {'status': 1, 'message': "bhhhvvg"} 
	return HttpResponse(json.dumps(response), content_type='application/json')


def hold(request, *args,**kwargs):
	
	id = request.POST.get('id')
	print(id)
	email = request.POST.get('email')
	app =   get_object_or_404(Application, id=id)
	app.application_status = 'Hold'
	app.save()
	send_email_task.delay('Application status','Your Application has been put on Hold','kausarbhimani7@gmail.com',[email])
	response = {'status': 1, 'message': "bhhhvvg"} 
	return HttpResponse(json.dumps(response), content_type='application/json')


def startapplication(request, pk):
	ad = Ad.objects.get(id=pk)
	ad.start_application = True
	ad.save()
	messages.success(request,"You can now receive applications!")
	return redirect(reverse('view-question', kwargs={'pk':pk}))












