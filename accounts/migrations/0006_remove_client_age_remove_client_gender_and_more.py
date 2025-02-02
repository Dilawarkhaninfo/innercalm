# Generated by Django 4.2.2 on 2024-05-01 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_counselor_f_name_alter_counselor_age_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='age',
        ),
        migrations.RemoveField(
            model_name='client',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='client',
            name='lang',
        ),
        migrations.RemoveField(
            model_name='client',
            name='location',
        ),
        migrations.RemoveField(
            model_name='counselor',
            name='age',
        ),
        migrations.RemoveField(
            model_name='counselor',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='counselor',
            name='lang',
        ),
        migrations.RemoveField(
            model_name='counselor',
            name='location',
        ),
        migrations.RemoveField(
            model_name='counselor',
            name='phone',
        ),
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(default='0'),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(default='NA', max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='lang',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.IntegerField(default='0', max_length=12),
        ),
    ]
