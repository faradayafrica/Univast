# Generated by Django 4.1.1 on 2023-08-20 14:07

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academia', '0021_accreditationbody_ranking_programme_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_current_session', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='programme',
            field=models.ManyToManyField(blank=True, related_name='department_programmes', to='academia.programme'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='programme',
            field=models.ManyToManyField(blank=True, related_name='faculty_programmes', to='academia.programme'),
        ),
        migrations.AddField(
            model_name='programme',
            name='parent_programme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_programmes', to='academia.programme'),
        ),
        migrations.AlterField(
            model_name='programme',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='programme',
            name='prerequisites',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_current_semester', models.BooleanField(default=False)),
                ('academic_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semesters', to='academia.academicsession')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semesters', to='academia.school')),
            ],
        ),
        migrations.AddField(
            model_name='academicsession',
            name='programme',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='program_academic_sessions', to='academia.programme'),
        ),
        migrations.AddField(
            model_name='academicsession',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school_academic_sessions', to='academia.school'),
        ),
        migrations.CreateModel(
            name='AcademicCalendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('event_description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('event_title', models.CharField(max_length=200)),
                ('academic_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calendar_events', to='academia.academicsession')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calendar_events', to='academia.school')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calendar_events', to='academia.semester')),
            ],
            options={
                'ordering': ['-end_date'],
            },
        ),
        migrations.AddField(
            model_name='school',
            name='academic_sessions',
            field=models.ManyToManyField(blank=True, related_name='all_school_academic_sessions', to='academia.academicsession'),
        ),
    ]
