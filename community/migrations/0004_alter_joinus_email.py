# Generated by Django 3.2.3 on 2021-07-08 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0003_alter_joinus_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joinus',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]