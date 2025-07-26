from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from .models import UserRole
from .forms import UserRegistrationForm,JobForm,ApplicationForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib import messages

@login_required
def delete_job(request,job_id):
    job = get_object_or_404(Job,id=job_id)
    if request.method == 'POST':
        job.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect('employee-dashboard')
    return render(request, 'JobApp/confirm_delete.html', {'job': job})
@login_required
def view_applicants(request):
    applications = Application.objects.filter(job__posted_by=request.user)
    context = {
        'applications' : applications
    }
    return render(request, 'JobApp/view_applicants.html', context)
@login_required
def apply_to_job(request,job_id):
    job = get_object_or_404(Job,id=job_id)
    try:
        if UserRole.objects.get(user=request.user).role != UserRole.Role.APPLICANT:
            messages.error(request,'Only applicants can aply to jobs.')
            return redirect('dashboard')
    except UserRole.DoesNotExist:
        messages.error(request,'Your role is not set')
        return redirect('dashboard')   
    if Application.objects.filter(job=job.id,applicant=request.user).exists():
        messages.info(request,'You have already applied to this job')
        return redirect('job-detail',job_id=job.id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST,request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request,'Application submitted succesfully!')
            return redirect('job-detail',job_id=job.id)
    else:
        form = ApplicationForm()   
     
    return render(request, 'JobApp/apply_to_job.html', {'form': form, 'job': job})    

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']
            UserRole.objects.create(user=user,role=role)
            login(request,user)
            if role == UserRole.Role.EMPLOYER:
                return redirect('employee-dashboard')
            elif role == UserRole.Role.APPLICANT:
                return redirect('applicant-dashboard')            
    else:
        form = UserRegistrationForm()
    return render(request,'JobApp/register.html',{'form':form})
@login_required        
def dashboard_view(request):
    try:
        user_role = UserRole.objects.get(user=request.user).role
    except ObjectDoesNotExist:
        return redirect('register')

    if user_role == UserRole.Role.EMPLOYER:
        return redirect('employee-dashboard')
    elif user_role == UserRole.Role.APPLICANT:
        return redirect('applicant-dashboard')
    else:
        return redirect('login')
@login_required    
def applicant_dashboard(request):
    query = request.GET.get('q','')
    if query:
        jobs = Job.objects.filter(
            title__icontains=query
        ) | Job.objects.filter(
            company_name__icontains=query
        ) | Job.objects.filter(
            location__icontains=query
        )
    else:
        jobs = Job.objects.all()  


    context = {
        'jobs':jobs,
        'query':query
    }    
    return render(request,'JobApp/applicant-dashboard.html',context)
@login_required    
def employee_dashboard(request):
    jobs = Job.objects.filter(posted_by=request.user)
    context = {
        'jobs':jobs
    }
    return render(request,'JobApp/employee-dashboard.html',context)
@login_required
def post_job_view(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        job = form.save(commit=False)
        job.posted_by = request.user
        job.save()
        return redirect('employee-dashboard')
    else:
        form = JobForm() 
    return render(request,'JobApp/post_job.html',{"form":form})    
@login_required
def job_detail(request,job_id):
    job = get_object_or_404(Job,id=job_id)
    return render(request,'JobApp/job_detail.html',{'job':job})
