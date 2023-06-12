from django.urls import path
from . import views

urlpatterns = [
	path('',views.Index,name="index"),
	path('UserLogin',views.UserLogin,name="UserLogin"),
	path('UserRegister',views.UserRegister,name="UserRegister"),
	path('logout',views.JobSeekerLogut,name="logout"),
    path('jobs',views.AllJobs,name="jobs"),
    path('jobDetail/<str:pk>/',views.JobDetail,name="jobDetail"),
    path('companies',views.Companies,name="companies"),
    path('categories',views.AllCategories,name="categories" ),
    path('contact',views.Contact,name="contact"),
    path('catJob/<str:pk>/',views.CatJob,name="catJob"),
    path('ocrCatJob/<str:pk>/',views.ocrCatJob,name="ocrCatJob"),
    path('compJob/<str:pk>/',views.CompanyJob,name="compJob"),
    path('OCRjobs',views.ocrJobs,name="OCRjobs"),
    path('search_job/<str:query>/',views.search_result,name="search_job"),
    path('filter_jobs',views.filterJobs,name="filter_jobs"),
]