from django.db import models
from django.utils import timezone

# Create your models here.

class JobSeeker(models.Model):
    Username = models.CharField(max_length=100,blank=False,null=False)
    Email = models.EmailField(max_length=100,blank=False,null=False)
    password = models.CharField(max_length=100,blank=False,null=False)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.Username
    

class ContactUs(models.Model):
    Username = models.CharField(max_length=100,null=False,blank=False)
    Email = models.CharField(max_length=100,null=False,blank=False)
    Subject = models.CharField(max_length=100,null=True,blank=True)
    Query = models.TextField(max_length=1000,null=True,blank=True)

    def __str__(self):
        return self.Email
    
class PasswordResetOTP(models.Model):
    Job_seeker = models.ForeignKey(JobSeeker,on_delete=models.CASCADE,null=True)
    OTP = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

