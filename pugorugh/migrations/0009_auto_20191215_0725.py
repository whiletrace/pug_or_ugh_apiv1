# Generated by Django 2.2.7 on 2019-12-15 07:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pugorugh', '0008_auto_20191214_0915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdog',
            name='dog',
        ),
        migrations.AddField(
            model_name='userdog',
            name='dog',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_dog', related_query_name='user_dogs_query', to='pugorugh.Dog'),
        ),
        migrations.RemoveField(
            model_name='userdog',
            name='user',
        ),
        migrations.AddField(
            model_name='userdog',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dogs_user', related_query_name='dogs_user_query', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='age',
            field=models.CharField(blank=True, choices=[('b', 'Baby'), ('y', 'Young'), ('a', 'Adult'), ('s', 'Senior')], default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='gender',
            field=models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female'), ('u', 'Unknown')], default='', max_length=4),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='size',
            field=models.CharField(blank=True, choices=[('s', 'Small'), ('m', 'Medium'), ('l', 'Large'), ('xl', 'Extra Large'), ('u', 'Unknown')], default='', max_length=10),
        ),
    ]