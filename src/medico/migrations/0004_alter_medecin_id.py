# Generated by Django 5.1.4 on 2025-01-17 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medico', '0003_medecin_groups_medecin_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medecin',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]