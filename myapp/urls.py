from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'myapp'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('accounts/login/', views.login_page, name='login_page'),
    path('accounts/register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('subjects/', views.subjects_assignments_view, name='subjects_page'),
    path('about/', views.about, name='about'),
    path('add-subject/', views.add_subject, name='add_subject'),
    path('submissions/', views.view_submissions, name='view_submissions'),
    path('grade/<int:submission_id>/', views.grade_submission, name='grade_submission'),
    path('teachers-dashboard/', views.teachers_dashboard, name='teachers_dashboard'),
    path('upload-assignment/', views.upload_assignment, name='upload_assignment'),
    path('subjects/<int:id>/', views.subject_detail, name='subject_detail'),
    path('assignments/<int:id>/', views.assignment_detail, name='assignment_detail'),
    path('assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

