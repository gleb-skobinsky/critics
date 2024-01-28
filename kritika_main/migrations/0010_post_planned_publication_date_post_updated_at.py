# Generated by Django 4.2.4 on 2024-01-28 19:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("kritika_main", "0009_alter_kritikauser_role_delete_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="planned_publication_date",
            field=models.DateField(default=None, null=True),
        ),
        migrations.AddField(
            model_name="post",
            name="updated_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
