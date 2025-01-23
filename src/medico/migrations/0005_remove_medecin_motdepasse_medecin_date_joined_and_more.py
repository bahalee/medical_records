# Generated by Django 5.1.4 on 2025-01-18 00:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('medico', '0004_alter_medecin_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medecin',
            name='motDePasse',
        ),
        migrations.AddField(
            model_name='medecin',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='medecin',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='medecin_set_permissions', to='auth.permission', verbose_name='user permissions'),
        ),
    ]