# Generated by Django 3.2.8 on 2022-01-20 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomUser', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expert',
            name='field',
        ),
        migrations.AddField(
            model_name='expert',
            name='field',
            field=models.ManyToManyField(blank=True, null=True, to='CustomUser.Fields'),
        ),
    ]