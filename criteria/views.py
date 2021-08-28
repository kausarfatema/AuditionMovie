from django.shortcuts import render, redirect
from .forms import QuestionForm, QuestForm
# Create your views here.
from ads.models import Ad
from django.http import HttpResponseRedirect
from .models import CriteriaQuestions, Result, SavedResult
from accounts.models import User
from django.contrib import messages
from django.urls import reverse

def addquestionview(request):
    recruter = request.user.recruter
    print(recruter)
    questionForm=QuestionForm(recruter=recruter)
    if request.method=='POST':
        questionForm=QuestionForm(request.POST, recruter=recruter)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            ad=Ad.objects.get(id=request.POST.get('ad'))
            question.ad=ad
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/')
    return render(request,'addquestion.html',{'questionForm':questionForm})

def allquestionview(request,pk):
    ad= Ad.objects.get(id=pk)
    
    questions = CriteriaQuestions.objects.all().filter(ad=ad)
    questionForm=QuestForm()
    if request.method=='POST':
        questionForm=QuestForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            
            question.ad=ad
            question.save()  
            return redirect ('recruter-dash')     
        else:
            print("form is invalid")
        
    context={
        'ad':ad,
        'questions':questions,
        'questionForm':questionForm,
    }
    return render(request,"questionsview.html",context)

def deletequestion(request,pk):
    question=CriteriaQuestions.objects.get(id=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('view-question')
    context={'question':question}
        
    return render(request,'questiondelete.html',context)

def updatequestion(request,pk,alt_pk):
    print(pk)
    print(alt_pk)
   
    
    ad= Ad.objects.get(id=pk)
    question= CriteriaQuestions.objects.get(id=alt_pk)
    questionForm= QuestForm(instance=question)
    if request.method == 'POST':
        questionForm=QuestForm(request.POST, instance=question)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            question.ad=ad
            question.save() 
            return redirect('recruter-dash')
    context = {
        'questionForm':questionForm
    }
    return render(request, 'questionupdate.html',context)
    

def take_audition(request,pk):
    ad=Ad.objects.get(id=pk)
    total_questions=CriteriaQuestions.objects.all().filter(ad=ad).count()
    questions=CriteriaQuestions.objects.all().filter(ad=ad)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'take_audition.html',{'ad':ad,'total_questions':total_questions,'total_marks':total_marks})

def start_exam_view(request,pk):
    result=Result.objects.filter(ad=pk, talent=request.user.talent)
    print(result)
    if not result :
        ad=Ad.objects.get(id=pk)
        total_questions=CriteriaQuestions.objects.all().filter(ad=ad).count()
        questions=CriteriaQuestions.objects.all().filter(ad=ad)
        if request.method=='POST':
            pass
        response= render(request,'start_exam.html',{'ad':ad,'questions':questions})
        response.set_cookie('ad_id',ad.id)
        return response

    return redirect('filter-ad')
   

def calculate_marks_view(request):
    
    ad_id = request.COOKIES.get('ad_id')
   
    user = User.objects.get(id=request.user.id)
    talent=user.talent

    ad=Ad.objects.get(id=ad_id)
    total_mark =0
    total_marks=0
    questions=CriteriaQuestions.objects.all().filter(ad=ad)
    
    for q in questions:
        total_mark=total_mark + q.marks
    for i in range(len(questions)):
        savedResult = SavedResult()
        selected_ans = request.COOKIES.get(str(i+1))
        slt = selected_ans.split()
        print(slt)
        selected_ans = slt[0]
        ans = slt[1]
        print(selected_ans)

        actual_answer = questions[i].answer
        act = actual_answer.lower()
        
        if actual_answer == 'Option1':
            savedResult.actual_answer = questions[i].option1

        elif actual_answer == 'Option2':
            savedResult.actual_answer = questions[i].option2

        elif actual_answer == 'Option3':
            savedResult.actual_answer = questions[i].option3

        else:
            savedResult.actual_answer = questions[i].option4

        savedResult.question = questions[i].question
        savedResult.answer = ans
        savedResult.ad = ad
        savedResult.talent = talent
        
        if selected_ans == actual_answer:
            total_marks = total_marks + questions[i].marks
            savedResult.is_correct = True
        
        
        savedResult.save()
    
    result=Result()
    res_mark=total_marks/total_mark
    result.marks=res_mark
    if res_mark > 0.75:
        result.status = "P"
        result.ad=ad
        result.talent=talent
        result.save()
        print(result)
        messages.success(request, 'You have passed the first stage of Auditions')
        return redirect(reverse('detailad', kwargs={'pk':ad_id}))
    else:
        result.status = "F"
        messages.error(request, 'Sorry you havent passed the first stage of audition')
        result.ad=ad
        result.talent=talent
        result.save()
        print(result)
        return redirect('filter-ad')
    
    

    

