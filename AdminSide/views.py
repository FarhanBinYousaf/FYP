from django.shortcuts import render, redirect,HttpResponse
from .forms import CustomUserCreationForm, UpdateUser
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from UserSide.models import JobSeeker
from .models import Jobs, Category, Company, Jobs,OCRJobs
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from django.core.paginator import Paginator
import pytesseract
from PIL import Image
import cv2
import numpy as np
import re
# Create your views here.


def AdminLogin(request):
	error = ""
	if request.method == "POST":
		username = request.POST['AdminUsername']
		password = request.POST['AdminPassword']
		try:
			user = User.objects.get(username=username)
		except:
			error = "User not exist"
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect("AdminHome")
		else:
			error = "Unable to login"
	context = {'error': error}
	return render(request, 'AdminSide/AdminLogin.html', context)


@login_required(login_url="AdminLogin")
def AdminHome(request):
	return render(request, 'AdminSide/AdminHome.html')


@login_required(login_url="AdminLogin")
def dashboard(request):
	return render(request, 'AdminSide/dashboard.html')


@login_required(login_url="AdminLogin")
def LogoutAdmin(request):
	logout(request)
	return redirect("AdminLogin")


@login_required(login_url="AdminLogin")
def AddAdmin(request):
	error = ""
	form = CustomUserCreationForm()
	active_users = User.objects.filter(is_active=True).count()
	if request.method == "POST":
		form = CustomUserCreationForm(request.POST)
		if active_users < 2:
			if form.is_valid():
			# admin = form.save(commit=False)
			# admin.username = form.cleaned_data['username']
			# admin.password = form.cleaned_data['password']
			# admin.save()
				form.save()
				return redirect("AllAdmins")
			else:
				messages.error(request, 'Data is not validated')
		else:
			messages.error(request, 'To add new admin delete previous first')
	else:
		form = CustomUserCreationForm()
	context = {'form': form, 'error': error, 'active_users': active_users}
	return render(request, 'AdminSide/AddAdmin.html', context)


@login_required(login_url="AdminLogin")
def AllAdmins(request):
	admins = User.objects.all()
	active_users = User.objects.filter(is_active=True).count()
	context = {'admins': admins, 'active_users': active_users}
	return render(request, 'AdminSide/AllAdmins.html', context)


@login_required(login_url="AdminLogin")
def UpdateAdmin(request, pk):
	error = ""
	form = ""
	admin = User.objects.get(id=pk)
	if admin.is_superuser:
		error = "Sorry! You cannot update Super Admin"
	else:
		form = UpdateUser(instance=admin)
		if request.method == "POST":
			form = UpdateUser(request.POST, instance=admin)
			if form.is_valid:
				admin = form.save(commit=False)
				admin.username = form.cleaned_data['username']
				if form.cleaned_data.get('update_password', False):
					password1 = form.cleaned_data['new_password1']
					password2 = form.cleaned_data['new_password2']
					if password1 == password2:
						admin.set_password(password1)
					else:
						error = "Password do not match"
				else:
					if not admin.has_usable_password():
						admin.set_unusable_password()
				admin.save()
				return redirect("AllAdmins")
		else:
			form = UpdateUser(instance=admin)
	context = {'form': form, 'error': error}
	return render(request, 'AdminSide/EditAdmins.html', context)


@login_required(login_url="AdminLogin")
def DeleteAdmin(request, pk):
	error = ""
	admin = ""
	admin = User.objects.get(id=pk)
	if admin.is_superuser:
		error = "Sorry! Super Admin cannot be deleted"
	else:
		if request.method == "POST":
			admin.delete()
			return redirect("AllAdmins")
	return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="AdminLogin")
def AllUsers(request):
	AllUsers = JobSeeker.objects.all()
	context = {'allUsers': AllUsers}
	return render(request, 'AdminSide/AllUsers.html', context)

@login_required(login_url="AdminLogin")
def ChangeUserStatus(request, pk):
	users = JobSeeker.objects.get(id=pk)
	if request.method == "POST":
		if users.is_active == True:
			users.is_active = False
		else:
			users.is_active = True
		users.save()
		return redirect("AllUsers")
	# print(users.is_active)
	return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="AdminLogin")
def Crawler(request):
	url_template = 'https://www.careerokay.com/jobs/index/page:{}'
	current_page = 1
	max_pages = 17
	while current_page <= max_pages:
		url = url_template.format(current_page)
		print('Scraping URL of :', url)
		response = requests.get(url)
		soup = BeautifulSoup(response.content, 'html.parser')
		divs = soup.find_all('div', class_='job-style1')
        # Link of website that will be combined to every job URL
		mylink = 'https://www.careerokay.com/'
        # Main divs for hiting HTML structure to crawl data
		for div in divs:
            # Main div of Job Content
			mydiv = div.find('div', class_='job-content')
			title = mydiv.find('h3').text.replace('\n', "")      # Job Title
			# Finding ancher(a) tag of every jobs to get URL
			aTag = mydiv.find('h3').find('a')
			link = aTag['href']                                 # Hyperlink of every job
			# complete link of every job after combining with URL of every job
			jobLink = mylink + link
			# Getting div of Company and Location
			CompanyAndLocation = mydiv.find('p')
			company = CompanyAndLocation.find('a').text
			FormatedCompany = company.replace(",","")
			         # Company Name
			location = CompanyAndLocation.find(
			    'span', class_='post-stats-line').text.replace('\n', "")       # Location Name (City Name)
            # Getting paragraph of Salar,Time,Date and Experience
			bar = mydiv.find('p', class_='post-stats-line')
			# Putting limit for getting span
			barr = bar.find_all('span', limit=4)
			date = barr[0].text                     # Getting Date
			experience = barr[1].text               # Getting Experience
			salary = barr[2].text                   # Getting Salary
			time = barr[3].text                     # Getting Time
            # Getting Apply Button
			applybutton = div.find('div', class_='col-sm-2')
			btn = applybutton.find('a')             # Getting Apply Button's ancher tag
			applyLink = mylink + btn['href']       # Apply Button Hyperlink

            # Using Requests for every jobs detail
			f = requests.get(jobLink)
			data = BeautifulSoup(f.content, 'html.parser')
			# Getting div of Every Job Detail which is on next page
			nextdiv = data.find('div', class_='job-details-wrap')
			# Getting Row under columns to get detail
			col = nextdiv.find('div', class_='col-sm-9').find('div', class_='row')
			firstCol = col.find_all('div', class_='col-md-6')
			FirstColDetail = firstCol[0].find('dl', class_='dl-horizontal')
			# Putting limit to find elements by indexing
			dd = FirstColDetail.find_all('dd', limit=9)
			category = dd[0].text       # Category
			careerLevel = dd[1].text    # Career Level
			Qualification = dd[3].text  # Qualification
			vacancies = dd[7].text      # Vacancies
            # skills = dd[8].find('div')
			skills = FirstColDetail.find_all('dd', class_='custom-tags')
			SkillsList = []
			for skill in skills:
				tags = skill.find_all('span', class_='custom-tag')
                # print(tags)
				for tag in tags:
					SkillsList.append(tag.text)
			if len(SkillsList) == 0:
				JobSkills = "None"
			else:
				JobSkills = ", ".join(SkillsList)
            # print(JobSkills)
            # print(SkillsList)
			ul = firstCol[1].find_all('ul', limit=2)
			des = ''
			if len(ul) == 0:
				des = "None"
			else:
				for u in ul:
					des += u.text
			res = firstCol[1].find_all('div')
			JobDescription_Cleaned = []
			JobDescription = []
			for element in res:
				JobDescription.append(element.text)
			for Desc in JobDescription:
				Desc_cleaned = Desc.replace('\n', '')
				if Desc_cleaned != '':
					JobDescription_Cleaned.append(Desc_cleaned)

			try:
				Db_Cat =  Category.objects.get(Name=category)
			except:
				category_obj = Category.objects.create(Name=category)
				Db_Cat = category_obj
				
			try:
				Db_Comp = Company.objects.get(Name=FormatedCompany)
			except Company.DoesNotExist:
				# Create a new Company object if it doesn't already exist
				company_obj = Company.objects.create(Name=FormatedCompany)
				Db_Comp = company_obj
				
			Jobs.objects.create(Title=title, Link=jobLink, Company=Db_Comp, Location=location, Experience=experience,
								Salary=salary, Time=time, ApplyLink=applyLink, Category=Db_Cat, CareerLevel=careerLevel,
								Qualification=Qualification, Vacancies=vacancies, Description=JobDescription_Cleaned,
								Skills=JobSkills)

            
		current_page += 1       # Increasing pages by one 
	return render(request,'AdminSide/JobsCrawler.html')

@login_required(login_url="AdminLogin")
def AllJobs(request):
	JobsAll = Jobs.objects.all()

	# paginator = Paginator(JobsAll,20)
	# page_number = request.GET.get('page')
	# page_obj = paginator.get_page(page_number)
	context = {"JobsAll":JobsAll}
	return render(request,'AdminSide/AllJobs.html',context)

@login_required(login_url="AdminLogin")
def DeleteJob(request,pk):
	JobDelete = Jobs.objects.get(id=pk)
	JobDelete.delete()
	
	return redirect(request.META.get('HTTP_REFERER'))


def generateFile(request):
    response = HttpResponse(content_type='text/csv')
    timestamp = datetime.now().strftime('%d-%m-%Y_%I-%M-%S-%p')
    filename = "Jobs Data"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow(['Title','Link','Company','Location','Experience','Salary','Time','ApplyLink','Category','CareerLevel','Qualification','Vacancies','Description','Skills'])
    JobsData = Jobs.objects.all()
    for job in JobsData:
        writer.writerow([job.Title,job.Link,job.Company,job.Location,job.Experience,job.Salary,job.Time,job.ApplyLink,job.Category,job.CareerLevel,job.Qualification,job.Vacancies,job.Description,job.Skills])
    return response

def JobsOCR(request):
	title = ""
	location = ""
	organization = ""
	Contact = ""
	Link = ""
	Date = ""
	if request.method == "POST":
		# image = request.FILES.get('img')
		# img = cv2.imread(image)
		image = request.FILES.get('img')
		img_bytes = image.read()  # Read the image bytes from the file object
		np_arr = np.frombuffer(img_bytes, np.uint8)  # Convert the bytes to a NumPy array
		img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # Decode the image array using OpenCV
		# Convert the image to grayscale
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		# Perform OCR
		text = pytesseract.image_to_string(gray, lang='eng', config='--psm 6')

		# Extract information using regex
		location_match = re.search(r"LOCATION: (.+)", text)
		if location_match:
		    location = location_match.group(1)
		else:
			location = ""

		title_match = re.search(r"JOB TITLE: (.+)", text)
		if title_match:
		    title = title_match.group(1)
		else:
		    title = ""

		organization_match = re.search(r"ORGANIZATION: (.+)", text)
		if organization_match:
		    organization = organization_match.group(1)
		else:
		    organization = ""


		Contact_match = re.search(r"CONTACT: (.+)", text)
		if Contact_match:
		    Contact = Contact_match.group(1)
		else:
		    Contact = ""

		Link_match = re.search(r"LINK: (.+)", text)
		if Link_match:
		    Link = Link_match.group(1)
		else:
		    Link = ""

		Date_match = re.search(r"DATE: (.+)", text)
		if Date_match:
		    Date = Date_match.group(1)
		else:
		    Date = ""

	context = {'title':title,'location':location,'organization':organization,'Link':Link,'Contact':Contact,'Date':Date}
	return render(request,'AdminSide/ocr.html',context)

def OCRData(request):
	if request.method == "POST":
		Job_Title = request.POST['job_title']
		Location = request.POST['job_location']
		Organization = request.POST['job_organization']
		Link = request.POST['job_link']
		Contact = request.POST['job_contact']
		Date = request.POST['job_date']
		if Job_Title:
			OCRJobs.objects.create(Title=Job_Title,Location=Location,Organization=Organization,Link=Link,Contact=Contact,Date=Date)
			messages.success(request,'Congratulations! OCR has been successfully')
		else:
			print("Something went wrong")
	return render(request,'AdminSide/ocr.html')
def practice(request):
	active_users = User.objects.filter(is_active=True).count()
	context = {'active_users':active_users}
	return render(request,'AdminSide/practice.html',context)