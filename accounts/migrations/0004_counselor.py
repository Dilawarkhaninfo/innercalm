# Generated by Django 4.2.2 on 2024-05-01 21:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counselor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('f_name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('phone', models.IntegerField()),
                ('location', models.CharField(max_length=50)),
                ('lang', models.CharField(max_length=50)),
                ('specialization', models.CharField(max_length=50)),
                ('qualification', models.IntegerField()),
                ('rating', models.FloatField()),
                ('fees', models.FloatField()),
            ],
        ),
    ]
