from django.contrib import admin
from .models import Jobs,Company,Category,OCRJobs
# Register your models here.

admin.site.register(Jobs)
admin.site.register(Company)
admin.site.register(Category)
admin.site.register(OCRJobs)