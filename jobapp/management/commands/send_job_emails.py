from django.core.management.base import BaseCommand
from django.db.models import F
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from jobapp.models import Job  # Import your Job model

class Command(BaseCommand):
    help = 'Send emails to selected job applicants'

    def add_arguments(self, parser):
        parser.add_argument('job_id', nargs='?', type=int, help='ID of the job to select applicants for')

    def handle(self, *args, **options):
        job_id = options['job_id']
        while job_id is None:
            job_id = input("Enter the ID of the job to select applicants for: ")
            try:
                job_id = int(job_id)
            except ValueError:
                self.stdout.write(self.style.ERROR("Invalid input. Please enter a valid integer ID."))
                job_id = None
                continue

        try:
            # Fetch the specific job
            job = Job.objects.get(pk=job_id)
        except Job.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Job with ID '{job_id}' does not exist"))
            return

        # Check if the job is closed
        if job.is_closed:
            self.stdout.write(self.style.WARNING(f"Skipping job '{job.title}' as it is already closed"))
            return

        # Determine which average field to use based on job type
        average_field = 'programming_average' if job.job_type == '1' else 'business_average'

        # Select top applicants based on the highest average
        top_applicants = job.applicant_set.filter(
            user__student__programming_average__isnull=False if job.job_type == '1' else True,
            user__student__business_average__isnull=False if job.job_type == '2' else True,
        ).order_by(F('user__student__' + average_field).desc())[:job.num_applicants_to_select]

        # Send emails to selected applicants
        for applicant in top_applicants:
            subject = f'Congratulations! You have been selected for {job.title}'
            html_message = render_to_string('jobapp/applicant_selection.html', {'job': job, 'applicant': applicant})
            plain_message = strip_tags(html_message)
            from_email = 'hitattacheeassist@gmail.com'  # Set your email address here
            to_email = applicant.user.email
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
            self.stdout.write(self.style.SUCCESS(f"Email sent to applicant '{applicant.user.username}'"))

        # Mark the job as closed after sending emails
        job.is_closed = True
        job.save()
        self.stdout.write(self.style.SUCCESS(f"Job '{job.title}' is closed and emails have been sent to selected applicants"))
