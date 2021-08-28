from django.shortcuts import render, redirect, get_object_or_404
from .UserRegistration import UserRegisterForm, PhotographerForm, TalentForm, VideoForm,RecruterForm, UploadWork, PhotographerUpdateForm, FeedbackForm, RecruterappForm
from django.contrib.auth import authenticate, login
from .models import User, Province,District, Sector, PhotoImage, Category, Talent,RecruterApp
from django.http import JsonResponse, FileResponse
import os
import tempfile
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
import moviepy.editor as mp
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, admin_only
from .models import Photographer,User,PhotoImage, Appointment, Category, Photographerwork,WorkFolder, Feedback,CompanyBase, RecruterApp
from ads.models import Ad, Application
from ads.forms import Adform,ApplicationForm
from applications.models import PhotographerApplication
from django.core.mail import send_mail
from payment.models import Payment
from django.urls import reverse
from .apointments import AppointmentForm
from django.views.generic import View
from movieaudi.utils import render_to_pdf
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import Group
from django.contrib import messages
from .task import sleepy, send_email_task, delphoto, delrecruter
from django.contrib.auth.decorators import login_required
from payment.models import Payment

# Create your views here.
def home(request):
	return render(request,"registration.html")


@login_required
@admin_only
def admin_panel(request):
	photographer = Photographer.objects.all()
	labels = []
	data = []
	status =[]
	ads = Ad.objects.all().count()
	pho = Photographer.objects.filter(is_employed=True).count()
	phapp = PhotographerApplication.objects.filter(is_employed=False, is_rejected=False).count()
	adapp = Application.objects.all().count()
	accepted = Application.objects.filter(application_status = 'Accepted').count()
	rejected = Application.objects.filter(application_status = 'Rejected').count()
	hold = Application.objects.filter(application_status = 'Hold').count()
	notdec =  Application.objects.filter(application_status = 'Not Decided').count()
	status.append(accepted)
	status.append(rejected)
	status.append(hold)
	status.append(notdec)
	cat = Category.objects.all()
	context = {
		'cat':cat
	}
	


	
	for ph in photographer:

		pht = Payment.objects.filter(photographer = ph)
		amount = 0
		for am in pht:
			amount += am.ammount
		labels.append(ph.user.username)
		data.append(amount)
		
	print(data)
	print(labels)
	return render(request,"index.html",{'labels':labels,'data':data,'ads':ads, 'pho':pho, 'phapp':phapp,'adapp':adapp,'status':status,'cat':cat})


def trik(request):
	return render(request,'tri.html')

def landing(request):
	
	return render(request,"landing.html" )

@login_required
def recruterdashboard(request):
	ads= Ad.objects.all().filter(recruter=request.user.recruter)
	if request.method == 'POST':
		a_form= Adform(request.POST,request.FILES)
		
		if a_form.is_valid():
			a_form.instance.recruter = request.user.recruter
			a_form.save()
			
			return redirect('recruter-dash')
	else:
		a_form=Adform()
		context={
		'a_form':a_form,
		'ads': ads
		}
	
	return render(request, "blank.html",context)


@unauthenticated_user
def photographereg(request):
	if request.method=='POST':
		u_form=UserRegisterForm(request.POST)
		p_form=PhotographerForm(request.POST, request.FILES)
		if(u_form.is_valid() and p_form.is_valid()):
			u_form.instance.type_in_choices='PH'
			u_form.save()
			p_form.instance.user=u_form.instance
			p_form.save()
			new_user=authenticate(username=u_form.cleaned_data['username'],password=u_form.cleaned_data['password1'])
			login(request,new_user)
			
			return redirect('upload-apply')
		else:
			context={
		'u_form': u_form,
		'p_form': p_form 
		}

	else:
		u_form=UserRegisterForm()
		p_form=PhotographerForm()
		context={
		'u_form': u_form,
		'p_form': p_form 
		}
	return render(request,"registerphoto.html",context)


def talentreg(request):
	if request.method=='POST':
		u_form=UserRegisterForm(request.POST)
		t_form=TalentForm(request.POST,request.FILES)
		if(u_form.is_valid() and t_form.is_valid()):
			u_form.instance.type_in_choices='TL'
			talent = u_form.save()
			group = Group.objects.get(name='talents')
			talent.groups.add(group)
			t_form.instance.user=u_form.instance

			t_form.save()
			return redirect('account_login')
		else:
			context={
		'u_form': u_form,
		't_form': t_form,
		}

	else:
		u_form=UserRegisterForm()
		t_form=TalentForm()
		context={
		'u_form': u_form,
		't_form': t_form ,
		}
	return render(request,"registertalent.html",context)

def recrutereg(request):
	if request.method=='POST':
		u_form=UserRegisterForm(request.POST)
		t_form=RecruterForm(request.POST)
		if(u_form.is_valid() and t_form.is_valid()):
			u_form.instance.type_in_choices='RC'
			recruter =u_form.save()
			group = Group.objects.get(name='recruter')
			recruter.groups.add(group)
			t_form.instance.user=u_form.instance
			t_form.save()
			messages.success(request, 'Recruter has been created')
			return redirect('admin-panel')
		else:
			context={
		'u_form': u_form,
		't_form': t_form,
		}

	else:
		u_form=UserRegisterForm()
		t_form=RecruterForm()
		context={
		'u_form': u_form,
		't_form': t_form ,
		}
	return render(request,"registerecruter.html",context)

@login_required
def recruterprofile(request):
	u_form=UserRegisterForm(instance=request.user)
	p_form=RecruterForm(instance=request.user.recruter)

	if request.method == 'POST':
		u_form=UserRegisterForm(request.POST,instance=request.user)
		p_form=RecruterForm(request.POST,request.FILES,instance=request.user.recruter)
		if(u_form.is_valid() and p_form.is_valid()):
			u_form.save()
			p_form.save()
			messages.success(request, 'Profile has been update')
			return redirect ('recruter-dash')
	
	context={
		'u_form':u_form,
		'p_form':p_form,
	}
	return render(request,'uprecruter.html',context)

@login_required
def talentprofile(request):
	u_form=UserRegisterForm(instance=request.user)
	p_form=TalentForm(instance=request.user.talent)

	if request.method == 'POST':
		u_form=UserRegisterForm(request.POST,instance=request.user)
		p_form=PhotographerForm(request.POST,request.FILES,instance=request.user.talent)
		if(u_form.is_valid() and p_form.is_valid()):
			u_form.save()
			p_form.save()
			messages.success(request, 'Profile has been updated')
			return redirect ('filter-ad')
	
	context={
		'u_form':u_form,
		'p_form':p_form,
	}
	return render(request,'uptalent.html',context)




def validate_username(request):
    username = request.POST.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    print(username)
    return JsonResponse(data)

def load_cities(request):
	province_id=request.GET.get('province_id')
	districts=District.objects.filter(province_id=province_id)
	return render(request,'dis_dropdown.html',{'districts':districts})


def load_districts(request):
	district_id=request.GET.get('district_id')
	sectors=Sector.objects.filter(district_id=district_id)
	return render(request,'sec_dorpdown.html',{'sectors':sectors})

def downloadfile(request):
	if request.method=='POST':
		fs=FileSystemStorage(location='/media')
		v_form=VideoForm(request.POST, request.FILES)
		vid=request.FILES['video']
		file_name1=default_storage.save(vid.name,vid)
		file1=default_storage.open(file_name1)
		file_url1=default_storage.url(file_name1)
		print(file_url1)
		url1_now="http://127.0.0.1:8000"+file_url1
		clip=mp.VideoFileClip(url1_now)
		clip_mp4=clip.write_videofile("F:\\Audition\\media\\test.mp4")



	else:
		v_form=VideoForm()	
	context={
			'v_form':v_form
		}
	return render(request,'edit.html',context)


def create_phto(request,pk):
	pht=PhotographerApplication.objects.get(id=pk)
	if request.method=='POST':
		length=request.POST.get('length')
	
		
		for filenum  in range(0, int(length)):
			PhotoImage.objects.create(
				appl=pht,
				image=request.FILES.get(f'image{filenum}'))
		
	return render(request,'upload_file.html',{"pk":pk})


def createrecruterapplication(request):
	form = RecruterappForm()
	if request.method =='POST':
		form = RecruterappForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('landing')

	context ={
		'form' : form
	}
	return render (request,'recruterappform.html',context)
		 	
	

@login_required
def viewrecruterapplication(request):
	applications = RecruterApp.objects.filter(is_rejected=False, is_employed=False)
	company = CompanyBase.objects.all()
	u_form = UserRegisterForm()
	r_form = RecruterForm()
	if request.method == 'POST':
		u_form = UserRegisterForm(request.POST)
		r_form =  RecruterForm(request.POST)
		if(u_form.is_valid() and r_form.is_valid()):
			app_id = r_form.cleaned_data['appid']
			em = u_form.cleaned_data['email']
			application = RecruterApp.objects.get(id=app_id)
			application.is_employed = True
			application.save()
			u_form.instance.type_in_choices='RC'
			u_form.save()
			r_form.instance.user=u_form.instance
			r_form.instance.rec_application = application
			r_form.save()
			messages.success(request, 'Recruter Has been Registered')

	context ={
		'applications':applications,
		'u_form' : u_form,
		'r_form': r_form,
		'company': company,

	}
	return render(request,'recruter_application.html',context)

@login_required
def viewphotographerapplications(request):
	
	applications = PhotographerApplication.objects.filter(is_rejected=False, is_employed=False)
	u_form= UserRegisterForm()
	p_form= PhotographerForm()
	if request.method == 'POST':
		u_form=UserRegisterForm(request.POST)
		p_form=PhotographerForm(request.POST)
		if(u_form.is_valid() and p_form.is_valid()):
			app_id= p_form.cleaned_data['appid']
			em= u_form.cleaned_data['email']
			application = PhotographerApplication.objects.get(id=app_id)
			application.is_employed=True
			
			application.save()
			u_form.instance.type_in_choices='PH'
			
			u_form.save()
			p_form.instance.user=u_form.instance
			p_form.instance.application=application
			p_form.save()
			send_mail(
				'Photographer application',
				'your application has been accepted',
				'kausarbhimani7@gmail.com',
				[em],
				fail_silently=False,
			)
			
	context={
		'applications':applications,
		'u_form': u_form,
		'p_form': p_form,

	}
	return render(request,'tables.html',context)



def viewphotodetail(request,id):
	photographer=get_object_or_404(PhotographerApplication,pk=id)
	photo=PhotoImage.objects.filter(appl=photographer)

	return render(request,'viewphotodetail.html',{'photo':photo,'photographer':photographer})


def viewphotodetailapp(request,id):
	photographer=get_object_or_404(PhotographerApplication,pk=id)
	photo=PhotoImage.objects.filter(appl=photographer)
	#feeds = Feedback.objects.filter()

	return render(request,'viewphotodetailapp.html',{'photo':photo,'photographer':photographer})





def deletephototgrapher(request, *args,**kwargs):
	if request.method == 'POST':
		app_id=request.POST.getlist('id[]')
		delphoto.delay(app_id)

		
		return redirect('phototable')

def deleterecruter(request, *args, **kwargs):
	if request.method == 'POST':
		app_id=request.POST.getlist('id[]')
		delrecruter.delay(app_id)
	
		return redirect('recruterapp')



def photograherappointment(request):
	ph =  Photographer.objects.all()
	context ={
		'ph': ph,
	}
	return render(request, 'appointmentph.html',context )


def viewapplicationresult(request):
	application = Application.objects.filter(talent=request.user.talent)
	context = {
		'application': application,
	}

	return render(request, 'viewapp.html', context)


def appointmentstalent(request):
	app =  Appointment.objects.filter(talent= request.user.talent)

	context = {
		'app':app,
	}

	return render(request, 'allapp.html', context)

def horrorads(request, pk):
	cat = Category.objects.get(id=pk)
	cats = Category.objects.all()
	ads = Ad.objects.filter(category = cat)
	context = {
		'ads':ads,
		'cat':cat,
		'cats':cats,
	}
	return render(request,'horror.html', context)

def comedyads(request,pk):
	cat = Category.objects.get(id=pk)
	ads = Ad.objects.filter(category = cat)
	context = {
		'ads':ads,
	}
	return render(request,'comedy.html', context)


def photoappoint(request):
	app = Appointment.objects.filter(photographers = request.user.photographer)

	context ={
		'app':app
	}
	return render(request,'phappointment.html',context)


def uploadwork(request):
	
	pht = request.user.photographer
	if request.method=='POST':
		length=request.POST.get('length')
		foldername = request.POST.get('foldername')
		img = request.FILES.get('display')
		print(img)
		w = WorkFolder.objects.create(
			photographer =pht,
			display_image = img,
			name = foldername
		)
		
		for filenum  in range(0, int(length)):
			Photographerwork.objects.create(
				photographer=pht,
				image=request.FILES.get(f'image{filenum}'),
				fold= w),
				
		
	return render(request,'uploadwork.html')



def viewfolder(request):

	folder = WorkFolder.objects.filter(photographer=request.user.photographer)
	context = {
		'folder' : folder
	}

	return render (request, "collection.html", context)


def viewfoldertalent(request,pk):
	ph =Photographer.objects.get(id=pk)
	folder = WorkFolder.objects.filter(photographer=ph)
	context = {
		'folder' : folder
	}

	return render (request, "viewfolder.html", context)

def viewpictures(request, pk):
	w = WorkFolder.objects.get(id=pk)

	ph = Photographerwork.objects.filter(fold=w)
	
	return render(request,"collectionph.html",{'ph':ph,'id':pk})

def viewpicturestalent(request,pk):
	w = WorkFolder.objects.get(id=pk)

	ph = Photographerwork.objects.filter(fold=w)
	
	return render(request,"talentpictures.html",{'ph':ph,'id':pk})




def addpictures(request,pk):
	w = WorkFolder.objects.get(id=pk)
	pht = request.user.photographer
	length=request.POST.get('length')
	if request.method == 'POST':
		for filenum  in range(0, int(length)):
			Photographerwork.objects.create(
				photographer=pht,
				image=request.FILES.get(f'image{filenum}'),
				fold= w)

	return render(request,"addpictures.html",{'id':pk})


def deletepicture(request,pk,pk_alt):
	w = WorkFolder.objects.get(id=pk)
	ph = Photographerwork.objects.get(id=pk_alt)
	ph.delete()
	messages.success(request, 'Picture has been deleted')
	return redirect(reverse ('view-pic', kwargs={"pk":pk}))




def deleteAppointment(request,pk):
	app = Appointment.objects.filter(id = pk)
	app.delete()
	return redirect(photoappoint)


def recruterprofile(request):
	u_form=UserRegisterForm(instance=request.user)
	p_form=RecruterForm(instance=request.user.recruter)

	if request.method == 'POST':
		u_form=UserRegisterForm(request.POST,instance=request.user)
		p_form=RecruterForm(request.POST,request.FILES,instance=request.user.recruter)
		if(u_form.is_valid() and p_form.is_valid()):
			u_form.save()
			p_form.save()
			messages.success(request, 'Profile has been updated')
			return redirect ('recruter-dash')
	
	context={
		'u_form':u_form,
		'p_form':p_form,
	}
	return render(request,'uprecruter.html',context)


def updateAppointment(request,pk):
	appt = Appointment.objects.get(id=pk)
	form = AppointmentForm(instance=appt)
	if request.method =='POST':
		form = AppointmentForm(request.POST,instance=appt)
		if(form.is_valid()):
			
			v=form.save()
			appdate = v.date
			apptimeslot = v.timeslot
			serv = v.request_service
			em = v.talent.user.email
			msg = f'hello, Your requested service {serv} has been updated to {appdate}  at {apptimeslot}'
			send_email_task.delay("Appointment",msg,'kausarbhimani7@gmail.com',[em])
			print(v.talent)
			
			return redirect(photoappoint)
	
	context={
		'form':form,
	}
	return render(request, 'upphoto.html', context)


def photographerprofile(request):
	u_form=UserRegisterForm(instance=request.user)
	p_form=PhotographerUpdateForm(instance=request.user.photographer)

	if request.method == 'POST':
		u_form=UserRegisterForm(request.POST,instance=request.user)
		p_form=PhotographerUpdateForm(request.POST,request.FILES,instance=request.user.photographer)
		if(u_form.is_valid() and p_form.is_valid()):
			u_form.save()
			p_form.save()
			return redirect ('filter-ad')
	
	context={
		'u_form':u_form,
		'p_form':p_form,
	}
	return render(request,'uptalent.html',context)


class GeneratePdf(View):
	def get(self, request, *args, **kwargs):
		app = Appointment.objects.filter(photographers = request.user.photographer)
		
		print(request.user)

		data = {
			
			"app" :app
		}
		pdf = render_to_pdf('photoreport.html', data)
		return HttpResponse(pdf, content_type='application/pdf')

class generatepaymentpdf(View):
	def get(self, request, *args, **kwargs):
		app = Payment.objects.all()

		

		data = {
			
			"app" :app
		}
		pdf = render_to_pdf('paymentreport.html', data)
		return HttpResponse(pdf, content_type='application/pdf')

class GeneratePdfMovie(View):
	def get(self, request, *args, **kwargs):
		app=[]
		tal_male=[]
		com=[]
		ct=[]
		lt=[]
		finl=[]
		cat = Category.objects.get(name='comedy')
		ads =Ad.objects.filter(recruter = request.user.recruter)
		male =User.objects.filter(gender="Male")
		
		for male in male:
			tal_m=Talent.objects.filter(user=male)
			
			tal_male.append(tal_m)
		
		applications = Application.objects.filter(recruter=request.user.recruter)
		adds = Ad.objects.filter(recruter=request.user.recruter)
		for adds in adds:
			print(adds.application_set.all().count())
		
		
		
		for ad  in ads :
			lit = Application.objects.filter(ads = ad, )
			app.append(list(lit))
		for m in tal_male:
			for n in m:
				ap = Application.objects.filter(recruter=request.user.recruter,talent=n)
				com.append(ap)

		for cmd in com:
			adcomedy=Ad.objects.filter(application__in =cmd,category=cat)
			finl.append(adcomedy)
		
		print(finl)
		#for ap in app:
		#	adcomedy=Ad.objects.filter(application__in =ap,category=cat)
		#	com.append(adcomedy)

		
		
			
		

		#male = Application.objects.filter(ads = Ad.objects.filter(recruter = request.user.recruter),talent=Talent.objects.filter(user=User.objects.filter(gender='Male'))).count()
		#print(male)
		#total = Application.objects.filter(ads = Ad.objects.filter(recruter = request.user.recruter)).count()
		#total_comedy = Application.objects.filter(ads = Ad.objects.filter(recruter = request.user.recruter,category=cat))
		
		print(request.user)
		

		data = {
			
			"app" : app,
			
		}
		pdf = render_to_pdf('moviereport.html', data)
		return HttpResponse(pdf, content_type='application/pdf')


def feedbackview(request,pk):
	phg = Photographer.objects.get(id = pk)
	feedbacks = Feedback.objects.filter(photographer = phg)

	context = {
		'feedbacks': feedbacks
	}

	return render(request,'viewfeedback.html',context)

def givefeedback(request,pk,alt_pk):
	phg = Photographer.objects.get(id = pk)
	app = Appointment.objects.get(id=alt_pk)
	feedback_form = FeedbackForm()
	if request.method == "POST":
		feedback_form = FeedbackForm(request.POST)
		if feedback_form.is_valid():
			feedback_form.instance.talent=request.user.talent
			feedback_form.instance.photographer=phg
			feedback_form.instance.appointment = app
			feedback_form.save()
			return redirect('talappoint')

	context ={
		'feedback_form':feedback_form
	}
	return render(request,'feedback.html',context)


def viewfeedback(request,pk):
	ph = Photographer.objects.get(id=pk)
	feeds = Feedback.objects.filter(photographer = ph)
	context = {
		'feeds': feeds
	}
	return render(request, 'viewfeedback.html', context)





























	

