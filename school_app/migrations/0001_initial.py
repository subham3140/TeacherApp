# Generated by Django 3.1.3 on 2020-11-26 17:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=100, unique=True)),
                ('about', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('teacher', 'Teacher'), ('student', 'Student')], default='choose status', max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('contact', models.BigIntegerField(null=True)),
                ('profile_pic', models.ImageField(default='default.jpg', upload_to='profile')),
                ('address', models.TextField()),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentGroupMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_app.studentgroup')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_app.usermodel')),
            ],
        ),
    ]
