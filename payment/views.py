from django.shortcuts import render
from django.http import HttpResponse
from .task import sleepy
from accounts.models import Photographer, Appointment
from django.http import JsonResponse, HttpResponse
# Create your views here.
from accounts.apointments import AppointmentForm
import datetime
from accounts.models import Appointment
from .models import Payment
import json
from django.contrib.auth.decorators import login_required

@login_required
def index(request,pk):
	ph= Photographer.objects.get(id=pk)


	form = AppointmentForm()
	return render(request, 'appointment_form.html', {'form': form,'ph':ph})


def test(request, *args,**kwargs):
	ph= request.POST.get('ph')
	date= request.POST.get('date')
	date =datetime.datetime.strptime(date,'%m/%d/%Y').strftime('%Y-%m-%d')
	ph = Photographer.objects.get(id=ph)
	appt= Appointment.objects.filter(photographers = ph, date=date ).first()
	app= Appointment.objects.filter(photographers = ph, date=date ).values('timeslot')
	print(app)
	if not appt:
		data ={
			'choices' : ""
		}
		return JsonResponse(data)
	
	data = {
		'choices': appt.timeslot
	}
	app=list(app)
	return JsonResponse(app, safe=False)

def validate_username(request):
    username = request.POST.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    print(username)
    return JsonResponse(data)


def payappointment(request):
	user= request.user
	talen = user.talent
	body = json.loads(request.body)
	date= body['date']
	date = datetime.datetime.strptime(date,'%m/%d/%Y').strftime('%Y-%m-%d')
	serv = body['sev']
	ph_id=body['ph']
	pho= Photographer.objects.get(id=ph_id)
	appointment = Appointment()
	appointment.date=date
	appointment.timeslot= body['timeslot']
	appointment.talent=talen
	appointment.photographers=pho
	appointment.request_service = serv
	appointment.save()
	payment = Payment()
	payment.txt_ref=body['txt']
	payment.talent=talen
	payment.photographer=pho
	payment.appointment=appointment
	payment.transaction_id=body['tr_id']
	payment.status = body['status']
	payment.save()

	print("body: " ,body)
	return JsonResponse("payment completed ", safe=False)


