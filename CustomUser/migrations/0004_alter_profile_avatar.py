# Generated by Django 3.2.8 on 2022-03-18 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomUser', '0003_expert_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.FileField(blank=True, null=True, upload_to='avatar/'),
        ),
    ]
