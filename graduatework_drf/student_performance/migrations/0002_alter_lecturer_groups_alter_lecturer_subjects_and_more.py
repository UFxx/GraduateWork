# Generated by Django 5.0.1 on 2024-01-10 14:58

import django.db.models.deletion
import sortedm2m.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_performance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturer',
            name='groups',
            field=sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, to='student_performance.group', verbose_name='Группы'),
        ),
        migrations.AlterField(
            model_name='lecturer',
            name='subjects',
            field=sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, to='student_performance.subject', verbose_name='Предметы'),
        ),
        migrations.AlterField(
            model_name='lecturer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]