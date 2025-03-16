from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Assignment, Submission
from .models import Subject
from .models import Subject, Assignment, Submission
from .forms import SubjectForm, AssignmentForm, GradeForm, SubmissionForm, RegisterForm



def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('myapp:home_page')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('myapp:login_page')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect('myapp:login_page')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})







from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from myapp.models import Subject, Assignment, Submission  # Ensure Submission is imported
from myapp.forms import SubjectForm, AssignmentForm

@login_required
@user_passes_test(lambda u: u.is_superuser)
def teachers_dashboard(request):
    if request.method == "POST":
        if 'add_subject' in request.POST:
            subject_form = SubjectForm(request.POST, request.FILES)
            if subject_form.is_valid():
                subject_form.save()
                return redirect('myapp:teachers_dashboard')

        elif 'upload_assignment' in request.POST:
            assignment_form = AssignmentForm(request.POST, request.FILES)
            if assignment_form.is_valid():
                assignment = assignment_form.save(commit=False)
                assignment.teacher = request.user  # Assign the logged-in teacher
                assignment.save()
                return redirect('myapp:teachers_dashboard')

    else:
        subject_form = SubjectForm()
        assignment_form = AssignmentForm()

    subjects = Subject.objects.all()
    assignments = Assignment.objects.all().order_by('-created_at')
    latest_done_assignments = Assignment.objects.filter(status='Completed').order_by('-updated_at')[:5]

    # **Fix: Fetch submitted assignments**
    submissions = Submission.objects.all().order_by('-submitted_at')  # Adjust as needed

    return render(request, 'teachers.html', {
        'subject_form': subject_form,
        'assignment_form': assignment_form,
        'subjects': subjects,
        'assignments': assignments,
        'latest_done_assignments': latest_done_assignments,
        'submissions': submissions,  # **Pass submissions to the template**
    })














# @login_required
# @user_passes_test(lambda u: u.is_superuser)
# def teachers_dashboard(request):
#     if request.method == "POST":
#         if 'add_subject' in request.POST:
#             subject_form = SubjectForm(request.POST, request.FILES)
#             if subject_form.is_valid():
#                 subject_form.save()
#                 return redirect('myapp:teachers_dashboard')

#         elif 'upload_assignment' in request.POST:
#             assignment_form = AssignmentForm(request.POST, request.FILES)
#             if assignment_form.is_valid():
#                 assignment = assignment_form.save(commit=False)
#                 assignment.teacher = request.user  # Assign the logged-in teacher
#                 assignment.save()
#                 return redirect('myapp:teachers_dashboard')

#     else:
#         subject_form = SubjectForm()
#         assignment_form = AssignmentForm()

#     subjects = Subject.objects.all()
#     assignments = Assignment.objects.all().order_by('-created_at')
#     latest_done_assignments = Assignment.objects.filter(status='Completed').order_by('-updated_at')[:5]

#     return render(request, 'teachers.html', {
#         'subject_form': subject_form,
#         'assignment_form': assignment_form,
#         'subjects': subjects,
#         'assignments': assignments,
#         'latest_done_assignments': latest_done_assignments,
#     })



@login_required
def subjects(request):
    subjects = Subject.objects.all()
    return render(request, "subjects.html", {"subjects": subjects})


@login_required
def subjects_assignments_view(request):
    subjects = Subject.objects.all()
    assignments = Assignment.objects.all()
    latest_done_assignments = Assignment.objects.filter(status='Completed')

    context = {
        'subjects': subjects,
        'assignments': assignments,
        'latest_done_assignments': latest_done_assignments,
    }
    return render(request, 'index.html', context)



@login_required
@user_passes_test(lambda u: u.is_superuser)
def view_submissions(request):
    submissions = Submission.objects.all()
    return render(request, "view_submissions.html", {"submissions": submissions})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def grade_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    if request.method == "POST":
        form = GradeForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, "Grade updated!")
            return redirect('myapp:teachers_dashboard')
    else:
        form = GradeForm(instance=submission)
    return render(request, "grade_submission.html", {"form": form, "submission": submission})




def home_page(request):
    subjects = Subject.objects.all()
    assignments = Assignment.objects.all().order_by('-created_at')

    # Fetch latest completed submissions with grades
    latest_done_assignments = Submission.objects.filter(
        status='Completed'
    ).select_related('assignment__subject').order_by('-submitted_at')[:5]

    context = {
        'subjects': subjects,
        'assignments': assignments,
        'latest_done_assignments': latest_done_assignments, 
    }
    return render(request, "index.html", context)









# def home_page(request):
#     subjects = Subject.objects.all()
#     assignments = Assignment.objects.all().order_by('-created_at')
#     latest_done_assignments = Assignment.objects.filter(status='Completed').order_by('-updated_at')[:5]

#     context = {
#         'subjects': subjects,
#         'assignments': assignments,
#         'latest_done_assignments': latest_done_assignments,
#     }
#     return render(request, "index.html", context)


def about(request):
    return render(request, 'about.html')


def subject_detail(request, id):
    subject = get_object_or_404(Subject, id=id)
    return render(request, 'subject_detail.html', {'subject': subject})


def assignment_detail(request, id):
    assignment = get_object_or_404(Assignment, id=id)
    return render(request, 'assignment_detail.html', {'assignment': assignment})

@login_required 
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submission, created = Submission.objects.get_or_create(student=request.user, assignment=assignment)

    if request.method == "POST":
        image = request.FILES.get("image")
        if image:
            submission.image = image  
            submission.status = "Submitted"
            submission.save()
            messages.success(request, "Assignment submitted successfully!")
            return redirect("myapp:assignment_detail", id=assignment.id)  

    return render(request, "submit_assignment.html", {"assignment": assignment, "submission": submission})


# def add_subject(request):
#     if request.method == 'POST':
#         form = SubjectForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('myapp:teachers_dashboard')
#     else:
#         form = SubjectForm()
#     return render(request, 'teacher.html', {'subject_form': form})


# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required, user_passes_test
# from .models import Subject, Assignment
# from .forms import SubjectForm, AssignmentForm

# Add subject
@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('myapp:teachers_dashboard')
    else:
        form = SubjectForm()
    return render(request, 'teacher.html', {'subject_form': form})

# Delete subject
@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    return redirect('myapp:teachers_delete')

# Upload assignment
@login_required
@user_passes_test(lambda u: u.is_superuser)
def upload_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = request.user
            assignment.save()
            return redirect('myapp:teachers_dashboard')
    else:
        form = AssignmentForm()
    return render(request, 'teachers.html', {'assignment_form': form})

# Delete assignment
@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    assignment.delete()
    return redirect('myapp:teachers_delete')

# View all subjects and assignments in dashboard
@login_required
@user_passes_test(lambda u: u.is_superuser)
def teachers_delete(request):
    subjects = Subject.objects.all()
    assignments = Assignment.objects.all()
    return render(request, 'teachers_delete.html', {
        'subjects': subjects,
        'assignments': assignments
    })
