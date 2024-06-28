from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from phonenumber_field.modelfields import PhoneNumberField
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import F, Max

from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager


STRENGTH_IN = (
    ('1',"Programming"),
    ('2','Business'),
)
    
class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    company_TIN = models.CharField(max_length=12,primary_key=True)
    company_name = models.CharField(max_length = 35)
    trade_name = models.CharField(max_length = 35)
    industry = models.CharField(max_length = 35)
    location = models.CharField(max_length = 35)
    company_description = models.TextField()
    url = models.URLField(max_length=100)
    phone_number = PhoneNumberField()
    registration_status = models.BooleanField()
    
    def __str__(self):
        return self.company_name
    

class Job(models.Model):

    user = models.ForeignKey(User, related_name='User', on_delete=models.CASCADE) 
    title = models.CharField(max_length=300)
    job_type = models.CharField(choices=STRENGTH_IN, max_length=15)
    description = RichTextField()
    tags = TaggableManager()
    location = models.CharField(max_length=300)
    salary = models.CharField(max_length=30, blank=True)
    num_applicants_to_select = models.PositiveIntegerField(default=5)
    company_name = models.CharField(max_length=300)
    company_description = RichTextField(blank=True, null=True)
    url = models.URLField(max_length=200)
    last_date = models.DateField()
    is_published = models.BooleanField(default=True)
    is_closed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    

class Applicant(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job.title

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reg_number = models.CharField(max_length = 8)
    department = models.CharField(max_length = 3)
    gpa = models.DecimalField(max_digits=3, decimal_places=2)
    programming_average = models.FloatField(null=True, blank=True)
    business_average = models.FloatField(null=True, blank=True)
    experience = models.TextField()
    phone_number = PhoneNumberField()
    residentialaddress = models.TextField()
    nextofkin = models.CharField(max_length = 35)
    nextofkincontact = PhoneNumberField()
    registration_status = models.BooleanField(default=True)
    attatchment_status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.reg_number
        # return f"{self.user.get_full_name()} ({self.reg_number})"


class SchoolSupervisor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee_number = models.CharField(max_length=10)
    phone_number = PhoneNumberField()

    def __str__(self):
        return self.user.get_full_name()
    
class WorkSupervisor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    phone_number = PhoneNumberField()
    
    def __str__(self):
        return self.user.get_full_name()


class AttachmentStudent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reg_number = models.ForeignKey(Student, on_delete=models.CASCADE)
    attached_company = models.ForeignKey(Company, on_delete=models.CASCADE)
    supervisor_at_work = models.ForeignKey(WorkSupervisor, on_delete=models.CASCADE)
    registration_status = models.BooleanField(default=True)
    has_school_supervisor = models.BooleanField(default=False)
    supervisor_from_school = models.ForeignKey(SchoolSupervisor, on_delete=models.CASCADE, null=True, blank=True)
    period_of_attachment = models.CharField(max_length=100, null=True, blank=True)
    change_of_company = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.reg_number}"



class Assessment(models.Model):
    student = models.ForeignKey(AttachmentStudent, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE)
    assessment_number = models.IntegerField()
    assessment_details = models.TextField()
    marks = models.IntegerField()
    assessment_date = models.DateTimeField(auto_now=True)
    additional_comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - Visit {self.assessment_number} - Supervisor: {self.supervisor.get_full_name()}"


class Course(models.Model):
    course_id = models.CharField(max_length=7, primary_key=True)
    course_name = models.CharField(max_length=50)
    course_type = models.CharField(choices=STRENGTH_IN, max_length=15)
    def __str__(self):
        return self.course_name
    

class CourseResult(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    mark = models.IntegerField()

    def __str__(self):
        return f'{self.user} {self.course_id.course_name}'


class BookmarkJob(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)


    def __str__(self):
        return self.job.title
    

    