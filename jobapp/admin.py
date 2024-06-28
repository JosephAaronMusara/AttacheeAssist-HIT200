from django.contrib import admin
from .models import *


class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('job','user','timestamp')
    
admin.site.register(Applicant,ApplicantAdmin)


class JobAdmin(admin.ModelAdmin):
    list_display = ('title','is_published','is_closed','timestamp')

admin.site.register(Job,JobAdmin)

class BookmarkJobAdmin(admin.ModelAdmin):
    list_display = ('job','user','timestamp')
admin.site.register(BookmarkJob,BookmarkJobAdmin)


admin.site.register(AttachmentStudent)
admin.site.register(Student)
admin.site.register(Company)
admin.site.register(CourseResult)
admin.site.register(Course)
admin.site.register(SchoolSupervisor)
admin.site.register(WorkSupervisor)
admin.site.register(Assessment)


