# Generated by Django 2.2.5 on 2019-11-10 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0005_auto_20191028_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdog',
            name='status',
            field=models.CharField(choices=[('l', 'Liked'), ('d', 'Disliked'), ('u', 'Undecided')], default='u', max_length=1),
        ),
    ]
