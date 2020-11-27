from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# Here i have two choice to be as a user
Status_Choice = (
      ('teacher' , 'Teacher'),
      ('student' , 'Student')
)

# Here is the Custom user model
class UserModel(models.Model):
    username = models.ForeignKey(User, on_delete = models.CASCADE)
    status = models.CharField(choices = Status_Choice, max_length = 50, default = 'choose status')
    email = models.EmailField(max_length = 50, null = False)
    contact = models.BigIntegerField(null = True)
    profile_pic = models.ImageField(upload_to = 'profile', default = 'default.jpg')
    address = models.TextField()


    def __str__(self):
        return f'{self.username}'


# Here is the Group of student which can be form only by the Teaches
class StudentGroup(models.Model):
    group_name = models.CharField(max_length = 100, null = False, unique = True)
    created_by = models.ForeignKey(User, on_delete = models.CASCADE)
    about = models.TextField()
    created_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'{self.group_name}'

# Here are the members of the particular group
class StudentGroupMember(models.Model):
    group = models.ForeignKey(StudentGroup, on_delete = models.CASCADE)
    member = models.ForeignKey(UserModel, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.member.username}"
