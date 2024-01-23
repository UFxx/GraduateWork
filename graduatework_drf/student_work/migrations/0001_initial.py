# Generated by Django 5.0.1 on 2024-01-21 13:11

import autoslug.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student_performance', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quest_name', models.CharField(max_length=100, verbose_name='Задание')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('file_link', models.FileField(blank=True, null=True, upload_to='quest/%Y/%m/%d/')),
                ('date_added', models.DateField(auto_now_add=True, verbose_name='Дата Добавления')),
                ('date_pass', models.DateField(auto_now_add=True, verbose_name='Дата сдачи')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='quest_name', unique=True, verbose_name='URL')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quest_group', to='student_performance.group', verbose_name='Группа')),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='quest_lecturer', to='student_performance.lecturer', verbose_name='Преподаватель')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quest_subject', to='student_performance.subject', verbose_name='Дисциплина')),
            ],
            options={
                'verbose_name': 'Задание',
                'verbose_name_plural': 'Задания',
            },
        ),
        migrations.CreateModel(
            name='UserQuest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Статус')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('file_link', models.FileField(blank=True, null=True, upload_to='user_quest/%Y/%m/%d/')),
                ('date_added', models.DateField(auto_now_add=True)),
                ('quest', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='student_work.quest', verbose_name='Задание')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_quest_student', to=settings.AUTH_USER_MODEL, verbose_name='Студент')),
            ],
            options={
                'verbose_name': 'Готовая работа',
                'verbose_name_plural': 'Готовые работы',
            },
        ),
    ]
