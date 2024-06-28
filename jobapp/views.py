from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.core.serializers import serialize
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.core.mail import send_mail

from account.models import User
from jobapp.forms import *
from jobapp.models import *
from jobapp.permission import *
User = get_user_model()


def home_view(request):

    published_jobs = Job.objects.filter(is_published=True).order_by('-timestamp')
    jobs = published_jobs.filter(is_closed=False)
    total_candidates = User.objects.filter(role='employee').count()
    total_companies = User.objects.filter(role='employer').count()
    paginator = Paginator(jobs, 3)
    page_number = request.GET.get('page',None)
    page_obj = paginator.get_page(page_number)

    if request.is_ajax():
        job_lists=[]
        job_objects_list = page_obj.object_list.values()
        for job_list in job_objects_list:
            job_lists.append(job_list)
        

        next_page_number = None
        if page_obj.has_next():
            next_page_number = page_obj.next_page_number()

        prev_page_number = None       
        if page_obj.has_previous():
            prev_page_number = page_obj.previous_page_number()

        data={
            'job_lists':job_lists,
            'current_page_no':page_obj.number,
            'next_page_number':next_page_number,
            'no_of_page':paginator.num_pages,
            'prev_page_number':prev_page_number
        }    
        return JsonResponse(data)
    
    context = {

    'total_candidates': total_candidates,
    'total_companies': total_companies,
    'total_jobs': len(jobs),
    'total_completed_jobs':len(published_jobs.filter(is_closed=True)),
    'page_obj': page_obj
    }
    print('ok')
    return render(request, 'jobapp/index.html', context)

@cache_page(60 * 15)
def job_list_View(request):
    """

    """
    job_list = Job.objects.filter(is_published=True,is_closed=False).order_by('-timestamp')
    paginator = Paginator(job_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {

        'page_obj': page_obj,

    }
    return render(request, 'jobapp/job-list.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def create_job_View(request):
    """
    Provide the ability to create job post
    """
    user = request.user
    print("Logged-in user:", user)
    company = Company.objects.filter(company_name=user.first_name).first()
    print("Company:", company)
    if company:
        initial_data = {
            'company_name': company.company_name,
            'company_description': company.company_description,
            'url': company.url,
        }
        form = JobForm(request.POST or None, initial=initial_data)
    else:
        form = JobForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            form.save_m2m()
            messages.success(
                request, 'You have successfully posted your job! Please wait for review.')
            #email sending
            email_addresses = Student.objects.values_list('email', flat=True)
            subject = 'AttacheeAssist Vacancy Alert'
            message = f'Available Vacancy from {instance.company_name} company. Login to your portal to check'
            from_email = 'hitattacheeassist@gmail.com'

            # Iterate through each email address and send the email
            for email_address in email_addresses:
                send_mail(subject, message, from_email, [email_address])
            
            return redirect(reverse("jobapp:single-job", kwargs={'id': instance.id}))

    context = {'form': form}
    return render(request, 'jobapp/post-job.html', context)



def single_job_view(request, id):
    """
    Provide the ability to view job details
    """
    if cache.get(id):
        job = cache.get(id)
    else:
        job = get_object_or_404(Job, id=id)
        cache.set(id,job , 60 * 15)
    related_job_list = job.tags.similar_objects()

    paginator = Paginator(related_job_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'job': job,
        'page_obj': page_obj,
        'total': len(related_job_list)

    }
    return render(request, 'jobapp/job-single.html', context)


def search_result_view(request):
    """
        User can search job with multiple fields

    """

    job_list = Job.objects.order_by('-timestamp')

    # Keywords
    if 'job_title_or_company_name' in request.GET:
        job_title_or_company_name = request.GET['job_title_or_company_name']

        if job_title_or_company_name:
            job_list = job_list.filter(title__icontains=job_title_or_company_name) | job_list.filter(
                company_name__icontains=job_title_or_company_name)

    # location
    if 'location' in request.GET:
        location = request.GET['location']
        if location:
            job_list = job_list.filter(location__icontains=location)


    paginator = Paginator(job_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {

        'page_obj': page_obj,

    }
    return render(request, 'jobapp/result.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def apply_job_view(request, id):

    form = JobApplyForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = Applicant.objects.filter(user=user, job=id)

    if not applicant:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.id = user.id
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully applied for this job!')
                return redirect(reverse("jobapp:single-job", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("jobapp:single-job", kwargs={
                'id': id
            }))

    else:

        messages.error(request, 'You already applied for the Job!')

        return redirect(reverse("jobapp:single-job", kwargs={
            'id': id
        }))


@login_required(login_url=reverse_lazy('account:login'))
def dashboard_view(request):
    """
    """
    jobs = []
    savedjobs = []
    appliedjobs = []
    total_applicants = {}
    students = []
    if request.user.role == 'employer':

        jobs = Job.objects.filter(user=request.user.id)
        for job in jobs:
            count = Applicant.objects.filter(job=job.id).count()
            total_applicants[job.id] = count

    if request.user.role == 'employee':
        savedjobs = BookmarkJob.objects.filter(user=request.user.id)
        appliedjobs = Applicant.objects.filter(user=request.user.id)
        
    if request.user.role == 'supervisor':
        supervisor = get_object_or_404(SchoolSupervisor, user=request.user)
        students = AttachmentStudent.objects.filter(supervisor_from_school=supervisor)
        
    if request.user.role == 'worksupervisor':
        supervisor = get_object_or_404(WorkSupervisor, user=request.user)
        students = AttachmentStudent.objects.filter(supervisor_at_work=supervisor)
    context = {

        'jobs': jobs,
        'savedjobs': savedjobs,
        'appliedjobs':appliedjobs,
        'total_applicants': total_applicants,
        'students': students
    }

    return render(request, 'jobapp/dashboard.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def delete_job_view(request, id):

    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:

        job.delete()
        messages.success(request, 'Your Job Post was successfully deleted!')

    return redirect('jobapp:dashboard')




@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def delete_job_view(request, id):

    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:

        job.delete()
        messages.success(request, 'Your Job Post was successfully deleted!')

    return redirect('jobapp:dashboard')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def make_complete_job_view(request, id):
    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:
        try:
            job.is_closed = True
            job.save()
            messages.success(request, 'Your Job was marked closed!')
        except:
            messages.success(request, 'Something went wrong !')
            
    return redirect('jobapp:dashboard')



@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def all_applicants_view(request, id):

    all_applicants = Applicant.objects.filter(job=id)

    context = {

        'all_applicants': all_applicants
    }

    return render(request, 'jobapp/all-applicants.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def delete_bookmark_view(request, id):

    job = get_object_or_404(BookmarkJob, id=id, user=request.user.id)

    if job:

        job.delete()
        messages.success(request, 'Saved Job was successfully deleted!')

    return redirect('jobapp:dashboard')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def applicant_details_view(request, id):
    applicant = get_object_or_404(User, id=id)
    applicant_instance = get_object_or_404(Applicant, user=applicant)

    # to get the associated student for the applicant
    appdetails = get_object_or_404(Student, user=applicant_instance.user)

    context = {
        'applicant': applicant_instance.user,
        'appdetails': appdetails
    }

    return render(request, 'jobapp/applicant-details.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def job_bookmark_view(request, id):

    form = JobBookmarkForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = BookmarkJob.objects.filter(user=request.user.id, job=id)

    if not applicant:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully save this job!')
                return redirect(reverse("jobapp:single-job", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("jobapp:single-job", kwargs={
                'id': id
            }))

    else:
        messages.error(request, 'You already saved this Job!')

        return redirect(reverse("jobapp:single-job", kwargs={
            'id': id
        }))


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def job_edit_view(request, id=id):
    """
    Handle Job Update

    """

    job = get_object_or_404(Job, id=id, user=request.user.id)
    form = JobEditForm(request.POST or None, instance=job)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # for save tags
        # form.save_m2m()
        messages.success(request, 'Your Job Post Was Successfully Updated!')
        return redirect(reverse("jobapp:single-job", kwargs={
            'id': instance.id
        }))
    context = {

        'form': form,
    }

    return render(request, 'jobapp/job-edit.html', context)

@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user  # Associate with the current user
            student.email = request.user.email
            student.save()
            messages.success(request, 'CV created successfully')
            return redirect(reverse_lazy('jobapp:dashboard'))
    else:
        form = StudentForm()
    return render(request, 'jobapp/createcv.html', {'form': form})


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def add_course_results(request):
    if request.method == 'POST':
        form = CourseResultForm(request.POST)
        if form.is_valid():
            course_result = form.save(commit=False)
            student = Student.objects.get(user=request.user)
            course_result.user = student
            course_result.save()
            
            # Calculate and update programming_average and business_average for the student
            student.programming_average = CourseResult.objects.filter(user=student, course_id__course_type='1').aggregate(avg_score=Avg('mark'))['avg_score']
            student.business_average = CourseResult.objects.filter(user=student, course_id__course_type='2').aggregate(avg_score=Avg('mark'))['avg_score']
            student.save()

            messages.success(request, 'Course result added successfully')
            return redirect('jobapp:studentresults')
    else:
        form = CourseResultForm()
    return render(request, 'jobapp/add_course_results.html', {'form': form})


def about(request):
    return render(request, 'jobapp/about.html')

def contact(request):
    return render(request, 'jobapp/contact.html')

@login_required(login_url=reverse_lazy('account:login'))
@user_is_coordinator
def coordinator_view(request):
    filter_choice = request.GET.get('filter_choice', 'all')
    selected_tab = filter_choice  # This will hold the selected tab name
    current_user = request.user
    students_all = Student.objects.all()
    students_attached = AttachmentStudent.objects.all()
    students_registered = Student.objects.filter(registration_status=True)
    students_by_department = Student.objects.order_by('department')
    students_with_supervisor = AttachmentStudent.objects.exclude(has_school_supervisor=False)
    students_without_supervisor = AttachmentStudent.objects.filter(has_school_supervisor=False)
    assessments = Assessment.objects.all()
    context = {
        'selected_tab': selected_tab,
        'students_all': students_all,
        'students_attached': students_attached,
        'students_registered': students_registered,
        'students_by_department': students_by_department,
        'students_with_supervisor': students_with_supervisor,
        'students_without_supervisor': students_without_supervisor,
        'current_user': current_user,
        'assessments': assessments,
    }
    return render(request, 'jobapp/tab_view.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_coordinator
def coordinator_attatched_student_details(request, id):
    student_details = get_object_or_404(AttachmentStudent, id = id)
    return render(request, 'jobapp/coordinator_attatched_student.html', {'student_details': student_details})

@login_required(login_url=reverse_lazy('account:login'))
@user_is_coordinator
def coordinator_all_students(request, id):
    student_details = get_object_or_404(Student,user=id)
    return render(request, 'jobapp/coordinator_all_student.html', {'student_details': student_details})

@login_required(login_url=reverse_lazy('account:login'))
@user_is_coordinator
def assign_supervisor(request, id):
    student = get_object_or_404(AttachmentStudent, id=id)
    if request.method == "POST":
        form = SchoolSupervisorForm(request.POST, instance=student)
        if form.is_valid():
            attachment_student = form.save(commit=False)
            supervisor = form.cleaned_data['supervisor_from_school']
            if supervisor:
                attachment_student.contact_details_school = supervisor.phone_number
                attachment_student.has_school_supervisor = True
                attachment_student.save()
                messages.success(request, 'Supervisor assigned successfully')
                return redirect('jobapp:coordinator')
    else:
        form = SchoolSupervisorForm(instance=student)
    return render(request, 'jobapp/assign_supervisor.html', {'form': form, 'student': student})


@login_required(login_url=reverse_lazy('account:login'))
@user_is_supervisor
def supervisor_attachment_student_details(request, id):
    supervisor = get_object_or_404(SchoolSupervisor, user=request.user)
    student_details = get_object_or_404(AttachmentStudent, user=id, supervisor_from_school=supervisor)
    return render(request, 'jobapp/coordinator_attatched_student.html', {'student_details': student_details})

@login_required(login_url=reverse_lazy('account:login'))
@user_is_worksupervisor
def worksupervisor_attachment_student_details(request, id):
    supervisor = get_object_or_404(WorkSupervisor, user=request.user)
    student_details = get_object_or_404(AttachmentStudent, user=id, supervisor_at_work=supervisor)
    return render(request, 'jobapp/coordinator_attatched_student.html', {'student_details': student_details})


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def create_attachment_student(request):
    student = Student.objects.get(user=request.user)
    if request.method == 'POST':
        form = AttachmentStudentForm(request.POST)
        if form.is_valid():
            attachment_student = form.save(commit=False)
            attachment_student.user = request.user
            attachment_student.reg_number = student
            attachment_student.save()
            messages.success(request, 'Attachment details saved successfully')
            return redirect('jobapp:dashboard')
    else:
        form = AttachmentStudentForm()
    return render(request, 'jobapp/create_attachment_student.html', {'form': form})


@login_required(login_url=reverse_lazy('account:login'))
#@user_is_supervisor 
def supervisor_student_assessment(request, id):
    supervisor = request.user
    attachment_student = AttachmentStudent.objects.get(user=id)
    print(attachment_student)
    print(supervisor)
    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.supervisor = supervisor
            assessment.student = attachment_student
            assessment.save()
            messages.success(request, 'Assessment saved successfully')
            return redirect('jobapp:dashboard')
    else:
        form = AssessmentForm()
    return render(request, 'jobapp/supervisor_student_assessment.html', {'form': form})

@login_required(login_url=reverse_lazy('account:login'))
def assessment_list(request):
    print(request.user)
    assessments = Assessment.objects.filter(supervisor=request.user)
    print(assessments)
    return render(request, 'jobapp/assessments.html', {'assessments': assessments})

#upload employers assesment form---- coordinator--- to all employers-----supervisor at work
#That has been addressed and can be used a a plus point during the presentation halala
