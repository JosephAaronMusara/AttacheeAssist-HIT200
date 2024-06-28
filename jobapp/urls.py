from django.urls import path
from jobapp import views

app_name = "jobapp"


urlpatterns = [

    path('', views.home_view, name='home'),
    path('jobs/', views.job_list_View, name='job-list'),
    path('job/create/', views.create_job_View, name='create-job'),
    path('job/<int:id>/', views.single_job_view, name='single-job'),
    path('apply-job/<int:id>/', views.apply_job_view, name='apply-job'),
    path('bookmark-job/<int:id>/', views.job_bookmark_view, name='bookmark-job'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('result/', views.search_result_view, name='search_result'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/employer/job/<int:id>/applicants/', views.all_applicants_view, name='applicants'),
    path('dashboard/employer/job/edit/<int:id>', views.job_edit_view, name='edit-job'),
    path('dashboard/employer/applicant/<int:id>/', views.applicant_details_view, name='applicant-details'),
    path('dashboard/employer/close/<int:id>/', views.make_complete_job_view, name='complete'),
    path('dashboard/employer/delete/<int:id>/', views.delete_job_view, name='delete'),
    path('dashboard/employee/delete-bookmark/<int:id>/', views.delete_bookmark_view, name='delete-bookmark'),
    path('dashboard/employee/createcv/', views.create_student, name='createcv'),
    path('dashboard/employee/attachment-details/', views.create_attachment_student, name='attachment_details'),
    path('dashboard/employee/studentresults/', views.add_course_results, name='studentresults'),
    #testing the coordinator view functionality we recently added
    path('dashboard/coordinator/', views.coordinator_view, name='coordinator'),
    path('dashboard/coordinator/student/attatched/<int:id>/', views.coordinator_attatched_student_details, name='coordinator-attatched-student-details'),
    path('dashboard/coordinator/student/<int:id>/',views.coordinator_all_students, name='coordinator-all-students'),
    path('dashboard/coordinator/assign-supervisor/<int:id>/', views.assign_supervisor, name='assign-supervisor'),
    path('dashboard/supervisor/attachment-student-details/<int:id>/', views.supervisor_attachment_student_details, name='supervisor_attachment_student_details'),
    path('dashboard/supervisor/attachement-student-details-worksupervisor/<int:id>/', views.worksupervisor_attachment_student_details, name='supervisor_attachment_student_details_worksupervisor'),
    path('dashboard/supervisor/assessment/<int:id>', views.supervisor_student_assessment, name='student_assessment'),
    path('dashboard/supervisor/school-assessment-record/', views.assessment_list,name='school_student_assessment_records'),
    path('assessment/', views.assessment_list, name='assessment'),
]
