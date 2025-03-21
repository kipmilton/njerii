# Generated by Django 5.1.6 on 2025-03-05 06:32

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_submission_assignment_alter_submission_question_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='created_at',
        ),
        migrations.AddField(
            model_name='assignment',
            name='due_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='assignment',
            name='subject',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.subject'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='teacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subject',
            name='description',
            field=models.TextField(default='CBC'),
        ),
        migrations.AddField(
            model_name='subject',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='subjects/'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='description',
            field=models.TextField(default='CBC'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='title',
            field=models.CharField(default='Our Subjects', max_length=200),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(default='Chemistry', max_length=100),
        ),
    ]
