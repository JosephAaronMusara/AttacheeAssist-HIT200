from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CourseResult, Student

@receiver(post_save, sender=CourseResult)
def update_averages(sender, instance, created, **kwargs):
    if created:
        student = instance.user
        course = instance.course_id
        if course.course_type == 'Programming':
            student.programming_average = student.courseresult_set.filter(course_id__course_type='Programming').aggregate(avg_score=models.Avg('score'))['avg_score']
        elif course.course_type == 'Business':
            student.business_average = student.courseresult_set.filter(course_id__course_type='Business').aggregate(avg_score=models.Avg('score'))['avg_score']
        student.save()
