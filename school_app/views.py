from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login
from django.conf import settings
from functools import wraps
import datetime
import jwt

# Create your views here.

# Here is the custom authentication by JWT token, so that only logged in user can access the end points
# i have used a decorator of this function which are then use as a permission just like a
# decorator "login_required" from django.contrib.auth.decorators import login_required
def Token_Required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = args[0].GET.get("token", None)
        if not token:
            messages.error(args[0], "Token Not Found, Unauthenticated!!")
            return redirect('school_app:login')
        else:
            try:
                data = jwt.decode(token, settings.SECRET_KEY)
            except:
                return redirect('school_app:login')
            return f(*args, **kwargs)
    return decorator

# Here i have this function which just give me the active user
def ActiveUser(request):
    return UserModel.objects.get(username__id = request.user.id)

# Here is the function which use to grab the token for every action so that the validated user can perform any task
def get_token(request):
    return request.GET.get("token", None)

# Here is the index view as a home view after a user LoggedIn
@Token_Required
def IndexView(request):
    context = {
     'token' : get_token(request)
    }
    return render(request, 'school_app/index.html', context)

# Here is the registration view
def SignUpView(request):
    signup_form = SignUpForm
    if request.method == "POST":
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            messages.success(request, "New User created!!")
            return redirect('school_app:updateprofile')
        else:
            messages.error(request, "Not in a proper format!1")
    context = {
    'form' : signup_form
    }
    return render(request, 'school_app/signup.html', context)

# Here is the custom LogInView with jst token
def LogInView(request):
    login_form = AuthenticationForm
    if request.method == "POST":
        login_form = AuthenticationForm(request = request, data = request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username = username,
                                password = password)
            login(request, user)
            if user:
                 token = jwt.encode({"username" : username,
                                    "user_id" : UserModel.objects.get(username = user).id,
                                    "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)},
                                    settings.SECRET_KEY)
                 messages.success(request, f"You are successfully LoggedIn as {username}!")
                 return render(request, 'school_app/index.html', {"token" : token.decode("UTF-8")})
            else:
                 messages.error(request, "Invalid username or password!!")
        else:
              messages.error(request, "Invalid username or password!!")
    context = {
        'form' : login_form
       }
    return render(request, 'school_app/login.html', context)


# Here is the update profile which should be fill just after the registration
def UpdateProfile(request):
    profile_form = ProfileForm
    if request.method == "POST":
        profile_form = ProfileForm(request.POST,request.FILES)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, f"Profile updated successfully!!")
            return redirect('school_app:login')
        else:
            messages.error(request, "Invalid form!")
    return render(request, 'school_app/updateprofile.html', {'form' : profile_form})

# Here is the profile view
@Token_Required
def ProfileView(request):
    context = {
     'profile' : ActiveUser(request),
     'token' : get_token(request)
    }
    return render(request, 'school_app/profile.html', context)

# Here is the create group view which can be done only by the teachers
@Token_Required
def CreateGroupView(request):
    group_form = StudentGroupForm
    if request.method == "POST":
        group_form = StudentGroupForm(request.POST)
        if group_form.is_valid():
            group_name = group_form.cleaned_data["group_name"]
            created_by = User.objects.get(id = ActiveUser(request).username.id)
            about = group_form.cleaned_data["about"]
            if ActiveUser(request).status == "teacher":
               new_group = StudentGroup(group_name = group_name, created_by = created_by, about = about)
               new_group.save()
               messages.success(request, "You have created a group successfully!!")
               return render(request, 'school_app/groupdetail.html', {"token" : get_token(request), "pk" : new_group.id,"group" : get_object_or_404(StudentGroup, pk = new_group.id)})
            else:
               messages.info(request, "Since you are not a faculty or a Teacher so you can't form the group!")
    context = {
        'form' : group_form,
        'token' : get_token(request)
    }
    return render(request, 'school_app/creategroup.html', context)


# Here is the group detail which can be see by any user
@Token_Required
def GroupDetailView(request, pk):
    group = get_object_or_404(StudentGroup, pk = pk)
    Mystudents = StudentGroupMember.objects.filter(group = group)
    context = {
     'group' : group,
     'token' : get_token(request),
     'students' : Mystudents,
     'pk' : pk
    }
    return render(request, 'school_app/groupdetail.html', context)

# Here is the group list which can be see by any user
@Token_Required
def GroupList(request):
    groups = StudentGroup.objects.all()
    return render(request, 'school_app/grouplist.html', {"groups" : groups, "token" : get_token(request)})

# Here are the group deletion option which can be done by only the teacher who created this group of student
@Token_Required
def GroupDelete(request, pk):
    group = get_object_or_404(StudentGroup, pk = pk)
    if group.created_by == ActiveUser(request).username:
        group.delete()
        messages.success(request, "Group deleted successfully!!")
    else:
        messages.error(request, "You are not a creator of this group!!")
    return render(request, 'school_app/index.html', {'token' : get_token(request)})

# Here are the group join view, here a teacher (having a existing group) can join any student he want
@Token_Required
def GroupJoin(request, pk, student_pk):
    group = get_object_or_404(StudentGroup, pk = pk)
    Mystudents = StudentGroupMember.objects.filter(group = group)
    if group.created_by == ActiveUser(request).username:
          try:
            student = StudentGroupMember.objects.get(member__id=student_pk, group = group)
            messages.info(request, f"{UserModel.objects.get(id=student_pk).username} is already in this group!!")
            return render(request, 'school_app/groupdetail.html', {"token" : get_token(request), "group" : group, "pk" : pk, 'students' : Mystudents})
          except:
             StudentGroupMember.objects.create(group = group, member = UserModel.objects.get(id = student_pk))
             messages.success(request, f"You have added your student {UserModel.objects.get(id = student_pk).username} successfully!!")
    else:
        messages.error(request, "You are not a creator of this group!!")
    return render(request, 'school_app/groupdetail.html', {"token" : get_token(request), "group" : group, "pk" : pk, 'students' : Mystudents})


# here are the student list which can be see by any teacher so that the teacher can add the particular student he want
@Token_Required
def StudentList(request, pk):
    students = UserModel.objects.filter(status = "student")
    return render(request, 'school_app/studentlist.html', {"token" : get_token(request), 'students' : students,"pk" : pk})
