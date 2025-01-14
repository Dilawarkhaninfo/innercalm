# Generated by Django 4.2.2 on 2024-05-01 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_counselor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='counselor',
            name='f_name',
        ),
        migrations.AlterField(
            model_name='counselor',
            name='age',
            field=models.IntegerField(default='0'),
        ),
        migrations.AlterField(
            model_name='counselor',
            name='fees',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='counselor',
            name='gender',
            field=models.CharField(default='NA', max_length=10),
        ),
        migrations.AlterField(
            model_name='counselor',
            name='lang',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='counselor',
            name='location',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='counselor',
            name='phone',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='counselor',
            name='qualification',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AlterField(
            model_name='counselor',
            name='rating',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='counselor',
            name='specialization',
            field=models.CharField(default='NA', max_length=50),
        ),
    ]
