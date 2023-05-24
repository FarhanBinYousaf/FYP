from django.urls import path
from . import views 

urlpatterns = [
	path('AdminLogin',views.AdminLogin,name="AdminLogin"),
	path('AdminHome',views.AdminHome,name="AdminHome"),
	path('LogoutAdmin',views.LogoutAdmin,name="LogoutAdmin"),
	path('AllAdmins',views.AllAdmins,name="AllAdmins"),
	# path('EditAdmins/<str:pk>/',views.EditAdmins,name="EditAdmins"),
	path('DeleteAdmin/<str:pk>/',views.DeleteAdmin,name="DeleteAdmin"),
	path('AddAdmin',views.AddAdmin,name="AddAdmin"),
	path('UpdateAdmin/<str:pk>/',views.UpdateAdmin,name="UpdateAdmin"),
	path('practice',views.practice,name="practice"),
	path('dashboard',views.dashboard,name="dashboard"),
    path('AllUsers',views.AllUsers,name="AllUsers"),
    path('ChangeUserStatus/<str:pk>/',views.ChangeUserStatus,name="ChangeUserStatus"),
    path('JobsCrawler',views.Crawler,name="JobsCrawler"),
    path('AllJobs',views.AllJobs,name="AllJobs"),
    path('DeleteJob/<str:pk>/',views.DeleteJob,name="DeleteJob"),
    path('generateFile',views.generateFile,name="generateFile"),
    path('jobsOCR',views.JobsOCR,name="jobsOCR"),
    path('ocrData',views.OCRData,name="ocrData",)
]