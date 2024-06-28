from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.forms import formset_factory

from jobapp.models import *
from ckeditor.widgets import CKEditorWidget


    

class JobForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = "Job Title :"
        self.fields['location'].label = "Job Location :"
        self.fields['job_type'].label = "Skill Preference :"
        self.fields['salary'].label = "Salary :"
        self.fields['num_applicants_to_select'].label = "Number of Applicants to Select :"
        self.fields['description'].label = "Job Description :"
        self.fields['tags'].label = "Tags :"
        self.fields['last_date'].label = "Submission Deadline :"
        self.fields['company_name'].label = "Company Name :"
        self.fields['url'].label = "Website :"


        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'eg : Software Developer',
            }
        )        
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': 'eg : Harare',
            }
        )
        self.fields['job_type'].widget.attrs.update(
            {
                'placeholder': '1 For PROGRAMING, 2 FOR BUSINESS',
            }
        )
        self.fields['salary'].widget.attrs.update(
            {
                'placeholder': '$300 - $500',
            }
        )
        self.fields['num_applicants_to_select'].widget.attrs.update(
            {
                'placeholder': 'Number of Applicants to Select',
            }
        )
        
        self.fields['tags'].widget.attrs.update(
            {
                'placeholder': 'Use comma separated. eg: Python, JavaScript ',
            }
        )                        
        self.fields['last_date'].widget.attrs.update(
            {
                'placeholder': 'YYYY-MM-DD ',
                
            }
        )        
        self.fields['company_name'].widget.attrs.update(
            {
                'placeholder': 'Company Name',
            }
        )           
        self.fields['url'].widget.attrs.update(
            {
                'placeholder': 'https://example.com',
            }
        )    


    class Meta:
        model = Job

        fields = [
            "title",
            "location",
            "job_type",
            "salary",
            "num_applicants_to_select",
            "description",
            "tags",
            "last_date",
            "company_name",
            "company_description",
            "url"
            ]



    def save(self, commit=True):
        job = super(JobForm, self).save(commit=False)
        if commit:
            
            job.save()
        return job




class JobApplyForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['job']

class JobBookmarkForm(forms.ModelForm):
    class Meta:
        model = BookmarkJob
        fields = ['job']




class JobEditForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = "Job Title :"
        self.fields['location'].label = "Job Location :"
        self.fields['job_type'].label = "Skill Preference :"
        self.fields['salary'].label = "Salary :"
        self.fields['description'].label = "Job Description :"
        # self.fields['tags'].label = "Tags :"
        self.fields['last_date'].label = "Dead Line :"
        self.fields['company_name'].label = "Company Name :"
        self.fields['url'].label = "Website :"


        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'eg : Software Developer',
            }
        )        
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': 'eg : Harare',
            }
        )
        self.fields['job_type'].widget.attrs.update(
            {
                'placeholder': '1 For PROGRAMING, 2 FOR BUSINESS',
            }
        )
        self.fields['salary'].widget.attrs.update(
            {
                'placeholder': '$300 - $500',
            }
        )
                   
        self.fields['last_date'].widget.attrs.update(
            {
                'placeholder': 'YYYY-MM-DD ',
            }
        )        
        self.fields['company_name'].widget.attrs.update(
            {
                'placeholder': 'Company Name',
            }
        )           
        self.fields['url'].widget.attrs.update(
            {
                'placeholder': 'https://example.com',
            }
        )    

    
        last_date = forms.CharField(widget=forms.TextInput(attrs={
                    'placeholder': 'Service Name',
                    'class' : 'datetimepicker1'
                }))

    class Meta:
        model = Job

        fields = [
            "title",
            "location",
            "job_type", 
            "salary",
            "description",
            "last_date",
            "company_name",
            "company_description",
            "url"
            ]



    def save(self, commit=True):
        job = super(JobEditForm, self).save(commit=False)
      
        if commit:
            job.save()
        return job
    
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['reg_number', 'department', 'gpa', 'experience', 'phone_number', 'residentialaddress', 'nextofkin', 'nextofkincontact']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(StudentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(StudentForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance


class CourseResultForm(forms.ModelForm):
    class Meta:
        model = CourseResult
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CourseResultForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CourseResultForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance
    

class CourseResultForm(forms.ModelForm):
    course_id = forms.ModelChoiceField(queryset=Course.objects.all(),label='Course')
    class Meta:
        model = CourseResult
        fields = ['course_id', 'mark']


class AttachmentStudentForm(forms.ModelForm):
    class Meta:
        model = AttachmentStudent
        fields = ['attached_company', 'supervisor_at_work', 'period_of_attachment']
    def __init__(self, *args, **kwargs):
        super(AttachmentStudentForm, self).__init__(*args, **kwargs)
        self.fields['attached_company'].widget.attrs.update({'class': 'form-control'})
        self.fields['supervisor_at_work'].widget.attrs.update({'class': 'form-control'})
        self.fields['period_of_attachment'].widget.attrs.update({'class': 'form-control'})

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        exclude = ['student','supervisor']
        

      
class AttachmentStudentFilterForm(forms.Form):
    FILTER_CHOICES = (
        ('all', 'All Students'),
        ('registered', 'Registered Students'),
        ('attached', 'Attached Students'),
        ('department', 'Department'),
        ('have_supervisor', 'Students with Supervisor'),
        ('have_no_supervisor', 'Students without Supervisor'),
        ('assessments', 'Assessments'),
    )

    filter_by = forms.ChoiceField(choices=FILTER_CHOICES, required=False)
    department = forms.CharField(required=False)
    supervisor = forms.CharField(required=False)

class SchoolSupervisorForm(forms.ModelForm):
    class Meta:
        model = AttachmentStudent
        fields = ['supervisor_from_school']
        
    def __init__(self, *args, **kwargs):
        super(SchoolSupervisorForm, self).__init__(*args, **kwargs)
        self.fields['supervisor_from_school'].queryset = SchoolSupervisor.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        supervisor = cleaned_data.get("supervisor_from_school")
        if supervisor:
            cleaned_data['contact_details_school'] = supervisor.phone_number
        return cleaned_data
        
