from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'myapp'

urlpatterns = [
    path('', views.home_page, name='home_page'),  # Ensure this is correct
    path('accounts/login/', views.login_page, name='login_page'),
    path('accounts/register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('subjects/', views.subjects, name='subjects'),
    path('about/', views.about, name='about'),
    path('subjects/', views.subjects_assignments_view, name='subjects_page'),
    path('add-subject/', views.add_subject, name='add_subject'),
    path('subjects/<int:subject_id>/', views.questions, name='questions'),
    path('submit/<int:question_id>/', views.submit_answer, name='submit_answer'),
    path('submissions/', views.view_submissions, name='view_submissions'),
    path('grade/<int:submission_id>/', views.grade_submission, name='grade_submission'),
    path('teachers-dashboard/', views.teachers_dashboard, name='teachers_dashboard'),
    path('upload-assignment/', views.upload_assignment, name='upload_assignment'),
    path('grade-submission/<int:submission_id>/', views.grade_submission, name='grade_submission'),
    path('add-subject/', views.add_subject, name='add_subject'),
    path('add_question/', views.add_question, name='add_question'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





# from django.urls import path
# from . import views
# from django.conf import settings
# from django.conf.urls.static import static

# app_name = 'myapp'

# urlpatterns = [
#     path('', views.home_page, name='home_page'),
#     path('accounts/login/', views.login_page, name='login_page'),
#     path('accounts/register/', views.register, name='register'),
#     path('logout/', views.logout_user, name='logout'),
#     path('subjects/', views.subjects, name='subjects'),
#     path('about/', views.about, name='about'),
#     path('subjects/', views.subjects_assignments_view, name='subjects_page'),
#     path('add-subject/', views.add_subject, name='add_subject'),
#     path('subjects/<int:subject_id>/', views.questions, name='questions'),
#     path('submit/<int:question_id>/', views.submit_answer, name='submit_answer'),
#     path('submissions/', views.view_submissions, name='view_submissions'),
#     path('grade/<int:submission_id>/', views.grade_submission, name='grade_submission'),
#     path('teachers-dashboard/', views.teachers_dashboard, name='teachers_dashboard'),
#     path('upload-assignment/', views.upload_assignment, name='upload_assignment'),
#     path('grade-submission/<int:submission_id>/', views.grade_submission, name='grade_submission'),
#     path('add-subject/', views.add_subject, name='add_subject'),
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
