from django.db import models

# Create your models here.

class Jobs(models.Model):
    Title = models.CharField(null=True,blank=True,max_length=50)
    Link  = models.CharField(null=True,blank=True,max_length=100)
    Company = models.ForeignKey('Company',on_delete=models.CASCADE,null=True)
    Location = models.CharField(null=True,blank=True,max_length=100)
    Experience = models.CharField(null=True,blank=True,max_length=100)
    Salary = models.CharField(null=True,blank=True,max_length=100)
    Time = models.CharField(null=True,blank=True,max_length=100)
    ApplyLink = models.CharField(null=True,blank=True,max_length=100)
    Category = models.ForeignKey('Category',on_delete=models.CASCADE,null=True)
    CareerLevel = models.CharField(null=True,blank=True,max_length=100)
    Qualification = models.CharField(null=True,blank=True,max_length=100)
    Vacancies = models.CharField(null=True,blank=True,max_length=100)
    Description = models.TextField(null=True,blank=True,max_length=1000)
    Skills = models.TextField(null=True,blank=True,max_length=500)

    def __str__(self):
        return self.Title
    
class Company(models.Model):
    Name = models.CharField(null=True,blank=True,max_length=100)

    def __str__(self):
        return self.Name

class Category(models.Model):
    Name = models.CharField(null=True,blank=True,max_length=100)

    def __str__(self):

        return self.Name
    


class OCRJobs(models.Model):
    Category = models.ForeignKey(Category,null=True,on_delete=models.CASCADE)
    Title = models.CharField(max_length=50,null=True,blank=True)
    Location = models.CharField(max_length=50,null=True,blank=True)
    Organization = models.CharField(max_length=50,null=True,blank=True)
    Link = models.CharField(max_length=50,null=True,blank=True)
    Contact = models.CharField(max_length=50,null=True,blank=True)
    Date = models.CharField(max_length=50,null=True,blank=True)
    
    def __str__(self):
        return self.Title