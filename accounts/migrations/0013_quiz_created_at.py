# Generated by Django 4.2.2 on 2024-05-03 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_resources_keywords'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
