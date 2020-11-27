from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'school_app'

urlpatterns = [
 path('', views.IndexView, name = 'index'),
 path('signup/', views.SignUpView, name = 'signup'),
 path('login/', views.LogInView, name = 'login'),
 path('profileupdate/', views.UpdateProfile, name = 'updateprofile'),
 path('profile/', views.ProfileView, name = 'profile'),
 path('creategroup/', views.CreateGroupView, name = "creategroup"),
 path('logout/', auth_views.LogoutView.as_view(), name = "logout"),
 path('groupdetail/<int:pk>/', views.GroupDetailView, name = 'groupdetail'),
 path('grouplist/', views.GroupList, name = 'grouplist'),
 path('groupdelete/<int:pk>/', views.GroupDelete, name = 'groupdelete'),
 path('groupjoin/<int:pk>/<int:student_pk>/', views.GroupJoin, name = 'groupjoin'),
 path('studentlist/<int:pk>/', views.StudentList, name = 'studentlist')
]
