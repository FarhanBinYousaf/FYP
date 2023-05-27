from django.shortcuts import render,redirect
from UserSide.models import JobSeeker,ContactUs
from UserSide.forms import UserRegistrationForm
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.password_validation import validate_password,CommonPasswordValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import login,logout
from AdminSide.models import Jobs,Category,Company,OCRJobs
import re
import ast
from django.core.paginator import Paginator
# Create your views here.

def Index(request):
	job_query = request.GET.get('job_query')				# getting search_title from input field for searching
	if job_query:
		return redirect('search_job',query=job_query)		# Passing that title / query to query string 
	jobs = Jobs.objects.all()[:5]
	Categories = Category.objects.all()[:8]
	Companies = Company.objects.all()[:8]
	context = {'Categories':Categories,'Companies':Companies,'jobs':jobs}
	return render(request,'UserSide/index.html',context)

def search_result(request,query):
	error = ""
	jobs_list = []
	if query:
		jobs_list = Jobs.objects.filter(Q(Title__icontains=query))			# Applying Django Q technique to search through Title of job
	else:
		error = "Sorry"
		# print(jobs_list)
	context = {'jobs_list':jobs_list,'error':error}
	return render(request,'UserSide/search_job.html',context)

def UserRegister(request):
	if request.method  == "POST":
		username = request.POST['username']
		email = request.POST['email']
		password1 = request.POST['password']
		password2 = request.POST['confirmPassword']
		try:
			CheckEmail = JobSeeker.objects.get(Email=email)
			messages.error(request,'Email already exist')
		except:
			if len(password1) <8:
				messages.error(request,'Password must be at least 8 characters long')
			else:
				try:
					validate_password(password1,password_validators=[CommonPasswordValidator()])
				except ValidationError:
					messages.error(request,'password is too common')
				if(password1 == password2):
					encryptedPassword = make_password(password1)
					JobSeeker.objects.create(Username=username,Email=email,password=encryptedPassword)
					messages.success(request,'Your account has been created')
					return redirect('UserLogin')
				else:
					messages.error(request,'Password do not match')	
		
	return render(request,'UserSide/sign-up.html')

def UserLogin(request): 
	contactAdmin = ""
	if request.method == "POST":
		UserEmail = request.POST['email']
		UserPassword = request.POST['password']
		try:
			Job_seeker = JobSeeker.objects.get(Email=UserEmail)
			print("User Exist")
			if Job_seeker.is_active == True:
				if check_password(UserPassword,Job_seeker.password):
					request.session['job_seeker_id'] = Job_seeker.id
					return redirect('index')
					# print("User is loged in")
				else:
					messages.error(request,'Password do not match')
				# print("User is active")
			else:
				messages.error(request,'Sorry! You are blocked by admin')
				contactAdmin = "Blocked"
				# print("User is blocked")
		except:
			messages.error(request,'User does not exist')
	context = {'contactAdmin':contactAdmin}
	return render(request,'UserSide/sign-in.html',context)

def JobSeekerLogut(request):
	logout(request)
	return redirect('index')

def AllJobs(request):
	jobs = Jobs.objects.all()
	Companies = Company.objects.all()
	categories = Category.objects.all()

	paginator = Paginator(jobs,5)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {'jobs':jobs,'categories':categories,'Companies':Companies,'page_obj':page_obj}
	return render(request,'UserSide/jobs.html',context)

def AllCategories(request):
	Categories = Category.objects.all()
	context = {'categories':Categories}
	return render(request,'UserSide/categories.html',context)

def Companies(request):
	AllCompanies = Company.objects.all()
	context = {'companies':AllCompanies}
	return render(request,'UserSide/companies.html',context)

def CatJob(request,pk):
	categories = Category.objects.all()
	Cat = Category.objects.get(id=pk)
	jobs = Jobs.objects.filter(Category=Cat)
	context = {'categories':categories, 'jobs':jobs}
	return render(request,'UserSide/category_job.html',context)

def CompanyJob(request,pk):
	AllCompanies = Company.objects.all()
	Comp = Company.objects.get(id=pk)
	jobs = Jobs.objects.filter(Company=Comp)
	context = {'AllCompanies':AllCompanies,'jobs':jobs}
	return render(request,'UserSide/company_jobs.html',context)

def JobDetail(request,pk):
	job = Jobs.objects.get(id=pk)
	skills = job.Skills.split(',')
	# Description cleaning code start from here  
	text = ast.literal_eval(job.Description)
	text = [re.sub(r'[\r\xa0>]', '', sentence) for sentence in text]
	cleaned_description = ' '.join(text)
	# Description cleaning code ends here 
	# print(cleaned_description)
	context = {'job':job,'skills':skills,'cleaned_description':cleaned_description}
	return render(request,'UserSide/job_detail.html',context)

def ocrJobs(request):
	Link = ""
	Contact = ""
	ocrjobs = OCRJobs.objects.all()
	context = {'ocrjobs':ocrjobs}
	return render(request,'UserSide/ocrjobs.html',context)

def Contact(request):
	if request.method == "POST":
		username = request.POST['txtUsername']
		email = request.POST['txtEmail']
		subject = request.POST['txtSubject']
		message = request.POST['txtSubject']
		ContactUs.objects.create(Username=username,Email=email,Subject=subject,Query=message)
		messages.success(request,'Thanks for contact. We will respond you back soon')

		# print("Clicked")
	return render(request,'UserSide/contact.html')
	