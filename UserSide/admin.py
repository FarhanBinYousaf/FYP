from django.contrib import admin
from .models import JobSeeker,ContactUs,PasswordResetOTP
# Register your models here.

admin.site.register(JobSeeker)
admin.site.register(ContactUs)
admin.site.register(PasswordResetOTP)
