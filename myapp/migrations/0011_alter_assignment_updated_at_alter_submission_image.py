# Generated by Django 5.1.6 on 2025-03-05 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_assignment_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='submissions/'),
        ),
    ]
