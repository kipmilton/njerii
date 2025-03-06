from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Subject, Question, Submission
from .forms import QuestionForm, SubmissionForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Assignment, Submission
from .forms import AssignmentForm, GradeForm
from django.shortcuts import render, redirect
from .forms import SubjectForm, AssignmentForm

from django.shortcuts import render, redirect
from .forms import SubjectForm, AssignmentForm  # Ensure this matches the forms in forms.py
from .models import Subject, Assignment
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Subject, Assignment, Submission
from .forms import SubjectForm, AssignmentForm

def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('myapp:teachers_dashboard')
    else:
        form = SubjectForm()
    return render(request, 'teacher.html', {'subject_form': form})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Subject, Question, Submission, Assignment
from .forms import SubjectForm, AssignmentForm, GradeForm, SubmissionForm, RegisterForm




def add_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("teachers_dashboard")  # Redirect to the dashboard or any other page
    else:
        form = QuestionForm()

    context = {
        "form": form
    }
    return render(request, "add_question.html", context)




def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect('myapp:home_page')
        else:
            messages.error(request, "Invalid login credentials")
    return render(request, 'accounts/login.html')


from django.shortcuts import render
from myapp.models import Subject, Assignment

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



def logout_user(request):
    logout(request)
    return redirect('myapp:login_page')

def about(request):
    return render(request, 'about.html')

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

@login_required
def subjects(request):
    subjects = Subject.objects.all()
    return render(request, "subjects.html", {"subjects": subjects})

@login_required
def questions(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    questions = Question.objects.filter(subject=subject)
    return render(request, "questions.html", {"subject": subject, "questions": questions})

@login_required
def submit_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.question = question
            submission.status = "Attempted"
            submission.save()
            messages.success(request, "Submission successful!")
            return redirect('subjects')
    else:
        form = SubmissionForm()
    return render(request, "submit_answer.html", {"form": form, "question": question})

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
            return redirect('view_submissions')
    else:
        form = GradeForm(instance=submission)
    return render(request, "grade_submission.html", {"form": form, "submission": submission})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import SubjectForm, AssignmentForm
from .models import Submission


@login_required
@user_passes_test(lambda u: u.is_superuser)
def teachers_dashboard(request):
    if request.method == "POST":
        if 'add_subject' in request.POST:
            subject_form = SubjectForm(request.POST, request.FILES)
            if subject_form.is_valid():
                subject_form.save()
                return redirect('teachers_dashboard')

        elif 'upload_assignment' in request.POST:
            assignment_form = AssignmentForm(request.POST, request.FILES)
            if assignment_form.is_valid():
                assignment = assignment_form.save(commit=False)
                assignment.teacher = request.user  # Assign the logged-in teacher
                assignment.save()
                return redirect('teachers_dashboard')

    else:
        subject_form = SubjectForm()
        assignment_form = AssignmentForm()

    subjects = Subject.objects.all()  
    assignments = Assignment.objects.all().order_by('-created_at')  
    latest_done_assignments = Assignment.objects.filter(status='Completed').order_by('-updated_at')[:5] 

    return render(request, 'teachers.html', {
        'subject_form': subject_form,
        'assignment_form': assignment_form,
        'subjects': subjects,
        'assignments': assignments,
        'latest_done_assignments': latest_done_assignments, 
    })



@login_required
@user_passes_test(lambda u: u.is_superuser)
def upload_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)  # Don't save yet
            assignment.teacher = request.user  # Assign the logged-in teacher
            assignment.save()  # Now save
            return redirect('myapp:teachers_dashboard')  # Redirect after saving
    else:
        form = AssignmentForm()
    return render(request, 'teachers.html', {'assignment_form': form})



def is_teacher(user):
    return user.is_superuser  # Only superadmins are teachers



def home_page(request):
    subjects = Subject.objects.all()
    assignments = Assignment.objects.all().order_by('-created_at')
    latest_done_assignments = Assignment.objects.filter(status='Completed').order_by('-updated_at')[:5]
    
    print("🏠 Home page view is running!")
    print("Subjects:", subjects)  
    print("Assignments:", assignments)  
    print("Completed Assignments:", latest_done_assignments)  

    context = {
        'subjects': subjects,
        'assignments': assignments,
        'latest_done_assignments': latest_done_assignments,
    }
    return render(request, "index.html", context)



def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('subjects')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    return redirect('login_page')

@login_required
def subjects(request):
    subjects = Subject.objects.all()
    return render(request, "subjects.html", {"subjects": subjects})

@login_required
def questions(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    questions = Question.objects.filter(subject=subject)
    return render(request, "questions.html", {"subject": subject, "questions": questions})

@login_required
def submit_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.question = question
            submission.status = "Attempted"
            submission.save()
            messages.success(request, "Submission successful!")
            return redirect('subjects')
    else:
        form = SubmissionForm()
    return render(request, "submit_answer.html", {"form": form, "question": question})

@login_required
@user_passes_test(is_teacher)
def view_submissions(request):
    submissions = Submission.objects.all()
    return render(request, "view_submissions.html", {"submissions": submissions})

@login_required
@user_passes_test(is_teacher)
def grade_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    if request.method == "POST":
        grade = request.POST.get("grade")
        submission.grade = f"{grade}%"
        submission.save()
        messages.success(request, "Grade updated!")
        return redirect('view_submissions')
    return render(request, "grade_submission.html", {"submission": submission})




def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect('myapp:home_page')
        else:
            messages.error(request, "Invalid login credentials")
    return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    return redirect('myapp:login_page')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                login(request, user)
                messages.success(request, "Account created successfully.")
                return redirect('myapp:home_page')
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, 'accounts/register.html')


































































# @login_required
# @user_passes_test(lambda u: u.is_superuser)  # Or use a custom teacher check
# def teachers_dashboard(request):
#     if request.method == "POST":
#         if 'add_subject' in request.POST:
#             subject_form = SubjectForm(request.POST, request.FILES)
#             if subject_form.is_valid():
#                 subject_form.save()
#                 return redirect('teachers_dashboard')  # ✅ Corrected redirect

#         elif 'upload_assignment' in request.POST:
#             assignment_form = AssignmentForm(request.POST, request.FILES)
#             if assignment_form.is_valid():
#                 assignment = assignment_form.save(commit=False)
#                 assignment.teacher = request.user  # Assign logged-in teacher
#                 assignment.save()
#                 return redirect('teachers_dashboard')  #  Corrected redirect

#     else:
#         subject_form = SubjectForm()
#         assignment_form = AssignmentForm()

#     submissions = Submission.objects.all()  # Fetch all submissions

#     return render(request, 'teachers.html', {  #  Fixed template name
#         'subject_form': subject_form,
#         'assignment_form': assignment_form,
#         'submissions': submissions
#     })





# @login_required
# def upload_assignment(request):
#     if request.method == 'POST':
#         form = AssignmentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('teachers_dashboard')  #  Corrected redirect
#     else:
#         form = AssignmentForm()
#     return render(request, 'teachers.html', {'assignment_form': form})  #  Fixed template name



# @login_required
# def teachers_dashboard(request):
#     """View for teachers to upload assignments and view submissions."""
#     assignments = Assignment.objects.all()
#     submissions = Submission.objects.filter(assignment__isnull=False)  # Only submissions related to assignments
#     form = AssignmentForm()

#     if request.method == 'POST':
#         form = AssignmentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('myapp:teachers_dashboard')

#     context = {
#         'assignments': assignments,
#         'submissions': submissions,
#         'form': form
#     }
#     print(context)  # Debugging: Print context to console
#     return render(request, 'teachers.html', context)


# @login_required
# def upload_assignment(request):
#     """Handles assignment uploads by teachers."""
#     if request.method == 'POST':
#         form = AssignmentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('myapp:teachers_dashboard')

#     return redirect('myapp:teachers_dashboard')


# @login_required
# def grade_submission(request, submission_id):
#     """Allows teachers to grade student submissions."""
#     submission = get_object_or_404(Submission, id=submission_id)

#     if request.method == 'POST':
#         form = GradeForm(request.POST, instance=submission)
#         if form.is_valid():
#             form.save()
#             return redirect('myapp:teachers_dashboard')

#     else:
#         form = GradeForm(instance=submission)

#     return render(request, 'grade_submission.html', {'form': form, 'submission': submission})
