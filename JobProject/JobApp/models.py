from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserRole(models.Model):
    class Role(models.TextChoices):
        EMPLOYER = 'employer','EMPLOYER'
        APPLICANT = 'applicant','APPLICANT'
    user = models.OneToOneField(User,on_delete=models.CASCADE)    
    role = models.CharField(max_length=10,choices=Role.choices)
class Job(models.Model):
    title = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    description = models.TextField()
    posted_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey(Job,models.CASCADE)
    applicant = models.ForeignKey(User,models.CASCADE)
    resume = models.FileField()
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)
