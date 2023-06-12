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
import os 
from django.core.paginator import Paginator
from django.conf import settings


import numpy as np
import pandas as pd
import nltk
# Text Vectorization using TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer

# cosine similarity
from sklearn.metrics.pairwise import cosine_similarity



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

def ocrCatJob(request,pk):
	categories = Category.objects.all()
	Cat = Category.objects.get(id=pk)
	jobs = OCRJobs.objects.filter(Category=Cat)
	context = {'jobs':jobs,'categories':categories}
	return render(request,'UserSide/ocr_cat_jobs.html',context)

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
	categories = Category.objects.all()
	Link = ""
	Contact = ""
	ocrjobs = OCRJobs.objects.all()
	context = {'ocrjobs':ocrjobs,'categories':categories}
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
	

def filterJobs(request):
	Title = ""
	Location = ""
	zipped_jobs  = ""
	Category = ""
	Qualification = ""
	Experience = ""
	file_path = os.path.join(settings.STATIC_ROOT, 'careerjobs.csv')
	jobs = pd.read_csv(file_path)
	# jobs = pd.read_csv("careerjobs")
	if request.method == "POST":
		Qualification = request.POST['qualification']
		Skills = request.POST['skills']
		Experience = request.POST['experience']
		jobs = jobs[['Title','Skills' , 'Qualification' , 'Category','Experience' , 'Location']]

		pd.set_option('display.max_columns', None)
		pd.set_option('display.max_rows', None)

		# Drop Duplicate
		jobs = jobs.drop_duplicates().reset_index(drop=True)


		# clean text
		def clean_text(text):
			cleaned_text = ''.join(char for char in text if char.isalnum() or char.isspace())
			return cleaned_text



		jobs['Skills'] = jobs['Skills'].apply(clean_text)
		jobs['Qualification'] = jobs['Qualification'].apply(clean_text)
		jobs['Category'] = jobs['Category'].apply(clean_text)
		jobs['Experience'] = jobs['Experience'].apply(clean_text)

		# Lowercase
		jobs['Skills'] = jobs['Skills'].apply(lambda x : x.lower())
		jobs['Qualification'] = jobs['Qualification'].apply(lambda x : x.lower())
		jobs['Category'] = jobs['Category'].apply(lambda x : x.lower())
		jobs['Experience'] = jobs['Experience'].apply(lambda x : x.lower())


		# Experience
		jobs['Experience'] = jobs['Experience'].apply(lambda x: x.replace(" ", ""))




		# Lemmitization

		lemmatizer = WordNetLemmatizer()



		def convert(text):
			# Tokenize the input text
			tokens = nltk.word_tokenize(text)
			
			# Lemmatize each token
			lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
			
			# Join the lemmatized tokens back into a string
			lemmatized_text = " ".join(lemmatized_tokens)
			
			return lemmatized_text

		jobs['Skills'] = jobs['Skills'].apply(convert)
		jobs['Qualification'] = jobs['Qualification'].apply(convert)
		jobs['Category'] = jobs['Category'].apply(convert)
		jobs['Experience'] = jobs['Experience'].apply(convert)


		#  job seeker data

		# user_qualification = "BSCS"
		# user_experience = "2 Year"
		# user_skills = "Backend Development  python"

		user_qualification = Qualification
		user_skills = Skills
		user_experience = Experience

		user_experience.replace(" ", "")
		user_data = f"{user_qualification} {user_skills} {user_experience}"
		user_data =   clean_text(user_data)
		user_data = user_data.lower()
		user_data = convert(user_data)




		vectorizer = TfidfVectorizer(stop_words = 'english')
		corpus = [user_data] + list(jobs['Qualification'] + ' '  + jobs['Skills'] + ' ' + jobs['Category'] +  ' ' + jobs['Experience'])
		tfidf_matrix = vectorizer.fit_transform(corpus)

		user_vector = tfidf_matrix[0]
		job_vectors = tfidf_matrix[1:]



		similarities = cosine_similarity(user_vector, job_vectors)
		sorted_indices = similarities.argsort()[0][::-1]
		num_recommendations = 20
		recommended_jobs = jobs.iloc[sorted_indices[:num_recommendations]]
		# print(recommended_jobs['Title'] + " " + recommended_jobs['Location'] + recommended_jobs['Category'] + recommended_jobs['Qualification'] + recommended_jobs['Experience'])
		print( recommended_jobs['Title'])
		Title = recommended_jobs['Title']
		Location = recommended_jobs['Location']
		Category = recommended_jobs['Category']
		Qualification = recommended_jobs['Qualification']
		Experience = recommended_jobs['Experience']
		zipped_jobs = zip(Title, Location, Category, Qualification, Experience)
	context = {'zipped_jobs': zipped_jobs}
	return render(request,'UserSide/filterJobs.html',context)