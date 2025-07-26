from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('my-applications/', views.my_applications_view, name='my-applications'),
    path('', views.dashboard_view, name='dashboard'),
    path('dashboard/applicant/', views.applicant_dashboard, name='applicant-dashboard'),
    path('dashboard/employer/', views.employee_dashboard, name='employee-dashboard'),
    path('post-job/', views.post_job_view, name='post-job'),
    path('job/<int:job_id>/',views.job_detail,name='job-detail'),
    path('job/<int:job_id>/apply/', views.apply_to_job, name='apply-to-job'),
    path('register/',views.register_view,name='register'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='JobApp/login.html'),name='login'),
    path('accounts/logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('employer/applicants/', views.view_applicants, name='view-applicants'),
    path('job/<int:job_id>/delete/', views.delete_job, name='delete-job'),
]
