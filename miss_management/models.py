from django.db import models

# Create your models here.


class EmpData(models.Model):  # database name is EmpData,for storing Employee details
    fname = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    job_title = models.CharField(max_length=25, default="NA")
    last_ap_date = models.CharField(max_length=100)
    reporting_mail = models.EmailField(max_length=50)
    doj = models.CharField(max_length=100)
    evalute_by = models.CharField(max_length=100)
    dept = models.CharField(max_length=50)


class Emp_goal_data_man(models.Model):  # database name is Emp_goal_data_man,for storing goals details
    email = models.EmailField(max_length=50)
    goal_id = models.CharField(max_length=100)
    goal_title = models.CharField(max_length=100)
    goal_description = models.CharField(max_length=100)
    due_date = models.CharField(max_length=25, default="NA")
    employee_comment = models.CharField(max_length=100, default="NA")
    employee_ratings = models.IntegerField(default=00)
    manager_comment = models.CharField(max_length=100, default="NA")
    manager_ratings = models.IntegerField(default=00)


class Managers_associations(models.Model):
    email = models.EmailField(max_length=50)
    dept = models.CharField(max_length=50)

