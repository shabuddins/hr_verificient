# Generated by Django 2.2.9 on 2020-03-13 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miss_management', '0002_managers_associations'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team_goal_data_man',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_id', models.CharField(max_length=100)),
                ('dept', models.CharField(max_length=100)),
                ('goal_title', models.CharField(max_length=100)),
                ('goal_description', models.CharField(max_length=100)),
                ('due_date', models.CharField(default='NA', max_length=25)),
                ('employee_comment', models.CharField(default='NA', max_length=100)),
                ('employee_ratings', models.IntegerField(default=0)),
                ('manager_comment', models.CharField(default='NA', max_length=100)),
                ('manager_ratings', models.IntegerField(default=0)),
            ],
        ),
    ]