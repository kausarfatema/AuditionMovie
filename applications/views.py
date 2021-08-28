from django.shortcuts import render, redirect
from .models import PhotographerApplication
from .forms import AppForm
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
# Create your views here.

def ApplicationForm(request):
    num=0
    if request.method =='POST':
        app_form=AppForm(request.POST)
        if app_form.is_valid():
            exp=app_form.cleaned_data['experience_in_month_or_year']
            type_work=app_form.cleaned_data['Type_of_Work']
            num_exp=app_form.cleaned_data['experience']
            if exp == '2':
                num +=2
            
            if exp == '1':
                if int(num_exp) > 6:
                    num +=1
                
            if type_work == 'CP':
                num +=2

            if type_work == 'FR':
                num +=1
            
            if num >= 3:

                app_form.instance.is_rejected=False
                app=app_form.save()
                
                send_mail(
                    'Link Application Continues',
                    f"http://127.0.0.1:8000/custom-admin/upld/{app.id}",
                    'kausarbhimani7@gmail.com',
                    [app.email],
                    fail_silently=False,
                )
                messages.success(request, 'Congratulations you have passed the Fiest Stage of selection ')
                return redirect(reverse ('upload-file', kwargs={"pk":app.id}))
            
            else:
                app_form.instance.is_rejected=True
                app_form.save()
                app_form=AppForm()

                context={
                    'app_form':app_form
                }
                
                        

    else:
        app_form=AppForm()
        context={
            'app_form':app_form
        }
        return render(request,'applicat.html',context)

