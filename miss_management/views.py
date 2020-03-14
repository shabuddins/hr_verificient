from django.shortcuts import render, redirect
from django.views import View
from .forms import OrderForm, EmployeeFeedback, TeamGoalForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .utility import *
from .models import Emp_goal_data_man, EmpData, Managers_associations
from django.http import HttpResponse
import uuid

# Created views here.


class Login(View):  # login class
    def get(self, request, *args, **kwargs):  # if request is get
        return render(request, "miss_management/login.html")

    def post(self, request, *args, **kwargs):  # if request is post
        uname = request.POST.get('username')
        password = request.POST.get('password')
        # print(uname,password)
        staff = authenticate(request, username=uname, password=password)

        if staff:
            login(request, staff)

            # print(uname,password)
            # emp_login_status, emp_type = verify_user_using_csv_data('employee_details.csv', uname, password)
            print(staff.first_name)
            emp_type = staff.first_name
            if staff.username == 'usha@verificient.com' or staff.get_username() == 'prabodh':
                return render(request, "miss_management/register_employees.html")
            if emp_type == 'Manager':
                return render(request, "miss_management/goal_setting_form.html")
            if emp_type == 'Employee':
                all_emp_data = Emp_goal_data_man.objects.filter(email=uname)
                SerNo = len(all_emp_data)
                # return all employee data which will be stored till now
                return render(request, "miss_management/get_employee_feedback.html",
                       {'emp_goal_setting_data': all_emp_data, 'serno': SerNo})

            return HttpResponse("Employee successfully login")  # redirect page to home page or registration page

        else:
            # Check in csv users name id
            return render(request, "miss_management/login.html", {'error': "Wrong username or password"})
            # return same page if invalid credential


@login_required(login_url="Login")  # decorator foruser is login or not
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, "miss_management/goal_setting_form.html")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


class save_emp_Data(View):
    def get(self, request, *args, **kwargs):  # if request is get
        return render(request, "miss_management/login.html")

    def post(self, request, *args, **kwargs):
        try:
            type = request.POST.get('type', 'NA')
            fname = request.POST.get('fname', 'NA')
            email = request.POST.get('email', '00')
            password = request.POST.get('password', 'NA')
            job_title = request.POST.get('job_title', 'NA')
            doj = request.POST.get('doj', 'NA')
            last_ap_date = request.POST.get('last_ap_date', 'NA')
            evalute_by = request.POST.get('evalute_by', 'NA')
            reporting_mail = request.POST.get('reporting_mail', 'NA')
            print(fname, email, password)

            obj = User(username=email, first_name=type)
            obj.set_password(password)
            obj.save()
            obj = EmpData(fname=fname, email=email, job_title=job_title, doj=doj, last_ap_date=last_ap_date,
                          evalute_by=evalute_by, reporting_mail=reporting_mail)
            obj.save()
            return HttpResponse("Added employee successfully")
        except:

            return HttpResponse("Employee registration failed")


class save_emp_goal_Data(View):  # for saving employee data into database
    # if (request.method=='POST'):
    def post(self, request, *args, **kwargs):  # save data if request is post
        try:
            goal_id = uuid.uuid4()
            emp_id = request.POST.get('emp_id', 'NA')
            goal_title = request.POST.get('goal_title', 'NA')
            goal_description = request.POST.get('goal_description', 'NA')
            due_date = request.POST.get('due_date', 'NA')

            print(emp_id, goal_title, goal_description, due_date)

            if len(Emp_goal_data_man.objects.filter(goal_id=goal_id)) > 0:
                return render(request, "miss_management/goal_setting_form.html",
                              {'error': 'Goal id exist..'})
            if goal_id and emp_id and goal_title and goal_description and due_date:
                if not validate(due_date):
                    return render(request, "miss_management/goal_setting_form.html",
                                  {'error': 'please enter date in proper format, e.g. 2003-12-30'})

                # Validation for goal_id already in DB.
                obj = Emp_goal_data_man(goal_id=goal_id, email=emp_id, goal_title=goal_title,
                                        goal_description=goal_description,
                                        due_date=due_date)  # database object

                obj.save()
                return redirect("EditDisplayEmpData")
            else:
                return render(request, "miss_management/goal_setting_form.html",
                              {'error': 'Please fill all the fields'})

        except Exception as e:
            print(e)
            return render(request, "miss_management/goal_setting_form.html", {'error': "Please fill all the fields"})

    def get(self, request, *args, **kwargs):  # get request
        return render(request, "miss_management/goal_setting_form.html")


class save_man_asso_Data(View):  # for saving employee data into database
    # if (request.method=='POST'):
    def post(self, request, *args, **kwargs):  # save data if request is post
        try:
            email = request.POST.get('email', 'NA')
            team = request.POST.get('team', 'NA')

            if len(Managers_associations.objects.filter(email=email)) > 0:
                return render(request, "miss_management/register_managers.html",
                              {'error': 'Email id exist..'})
            if email and team:
                # Validation for goal_id already in DB.
                obj = Managers_associations(email=email, dept=team)  # database object
                obj.save()
                return redirect("EditDisplayManAsso")
            else:
                return render(request, "miss_management/register_managers.html",
                              {'error': 'Please fill all the fields'})

        except Exception as e:
            print(e)
            return render(request, "miss_management/register_managers.html", {'error': "Please fill all the fields"})

    def get(self, request, *args, **kwargs):  # get request
        return render(request, "miss_management/register_managers.html")

class EditDisplayManAsso(View):
    def get(self, request, *args, **kwargs):  # for displaying employee detail from database get request
        all_emp_data = Managers_associations.objects.all()
        SerNo = len(all_emp_data)
        # return all employee data which will be stored till now
        return render(request, "miss_management/show_managers.html",
                      {'manager_data': all_emp_data, 'serno': SerNo})


class DisplayEmpData(View):
    def get(self, request, *args, **kwargs):  # for displaying employee detail from database get request
        all_emp_data = Emp_goal_data_man.objects.all()
        SerNo = len(all_emp_data)
        # return all employee data which will be stored till now
        return render(request, "miss_management/show_goal_setting_data.html",
                      {'emp_goal_setting_data': all_emp_data, 'serno': SerNo})



class search_emp_goal_Data(View):
    def get(self, request, *args, **kwargs):  # get request
        return render(request, "miss_management/search_emp_goals_details.html")
    def post(self, request, *args, **kwargs):  # for displaying employee detail from database get request
        email_id = request.POST.get('email_id', 'NA')
        all_emp_data = Emp_goal_data_man.objects.filter(email=email_id)
        SerNo = len(all_emp_data)
        # return all employee data which will be stored till now
        return render(request, "miss_management/show_goal_setting_data.html",
                      {'emp_goal_setting_data': all_emp_data, 'serno': SerNo})



class EditDisplayEmpData(View):
    def get(self, request, *args, **kwargs):  # for displaying employee detail from database get request
        all_emp_data = Emp_goal_data_man.objects.all()
        SerNo = len(all_emp_data)
        # return all employee data which will be stored till now
        return render(request, "miss_management/edit_goal_details_emp.html",
                      {'emp_goal_setting_data': all_emp_data, 'serno': SerNo})


def DisplayTeamData(request, pk):
    all_emp_data = EmpData.objects.filter(reporting_mail=pk)
    print (all_emp_data)
    SerNo = len(all_emp_data)
    # return all employee data which will be stored till now
    if SerNo != 0:
        return render(request, "miss_management/show_team_members.html",
                      {'emp_goal_setting_data': all_emp_data, 'serno': SerNo})
    else:

        return HttpResponse("No one is reporting to you...")


def save_team_goal_Data(request, pk):
    if request.method == 'POST': # save data if request is post
        try:
            goal_id = uuid.uuid4()
            goal_title = request.POST.get('goal_title', 'NA')
            goal_description = request.POST.get('goal_description', 'NA')
            due_date = request.POST.get('due_date', 'NA')
            print(goal_id, goal_title, goal_description, due_date)

            if len(Emp_goal_data_man.objects.filter(goal_id=goal_id)) > 0:
                return render(request, "miss_management/team_goal_setting_form.html",
                              {'error': 'Goal id exist..'})
            if goal_id and goal_title and goal_description and due_date:
                if not validate(due_date):
                    return render(request, "miss_management/team_goal_setting_form.html",
                                  {'error': 'please enter date in proper format, e.g. 2003-12-30'})
                all_emp_data = EmpData.objects.filter(reporting_mail=pk)
                for emp_data in all_emp_data:
                    # Validation for goal_id already in DB.
                    obj = Emp_goal_data_man(goal_id=goal_id, email=emp_data.email, goal_title=goal_title,
                                            goal_description=goal_description,
                                            due_date=due_date)  # database object

                    obj.save()
                return redirect("EditDisplayEmpData")
            else:
                return render(request, "miss_management/team_goal_setting_form.html",
                              {'error': 'Please fill all the fields'})

        except Exception as e:
            print(e)
            return render(request, "miss_management/team_goal_setting_form.html", {'error': "Please fill all the fields"})


class DisplayTeamGoalData(View):
    def get(self, request, *args, **kwargs):  # for displaying employee detail from database get request
        all_emp_data = Team_goal_data_man.objects.all()
        SerNo = len(all_emp_data)
        # return all employee data which will be stored till now
        return render(request, "miss_management/edit_team_goal_details.html",
                      {'emp_goal_setting_data': all_emp_data, 'serno': SerNo})


def updateTeamGoals(request, goal_id):
    order = Team_goal_data_man.objects.get(goal_id=goal_id)
    form = TeamGoalForm(instance=order)

    if request.method == 'POST':
        form = TeamGoalForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("DisplayTeamGoalData")

    context = {'form': form}
    return render(request, 'miss_management/update_goal_form.html', context)


def deleteTeamGoals(request, goal_id):
    order = Emp_goal_data_man.objects.get(goal_id=goal_id)
    if request.method == "POST":
        order.delete()
        return redirect('DisplayEmpData')

    context = {'item': order}
    return render(request, 'miss_management/delete.html', context)


def updateOrder(request, pk):
    order = Emp_goal_data_man.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("DisplayEmpData")

    context = {'form': form}
    return render(request, 'miss_management/update_goal_form.html', context)


def add_emp_feedback(request, pk, email):
    order = Emp_goal_data_man.objects.get(id=pk)
    form = EmployeeFeedback(instance=order)

    if request.method == 'POST':
        form = EmployeeFeedback(request.POST, instance=order)
        if form.is_valid():
            form.save()
            all_emp_data = Emp_goal_data_man.objects.filter(email=email)

            SerNo = len(all_emp_data)
            # return all employee data which will be stored till now
            return render(request, "miss_management/get_employee_feedback.html",
                          {'emp_goal_setting_data': all_emp_data, 'serno': SerNo})

    context = {'form': form}
    return render(request, 'miss_management/update_goal_employee_form.html', context)


def deleteOrder(request, pk, goal_id):
    order = Emp_goal_data_man.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('DisplayEmpData')

    context = {'item': order}
    return render(request, 'miss_management/delete.html', context)


@login_required(login_url="Login")  # decorator foruser is login or not
def create_form(request):
    return render(request, "miss_management/registration.html")


@login_required(login_url="Login")
def setting_form(request):
    return render(request, "miss_management/goal_setting_form.html")

@login_required(login_url="Login")
def team_setting_form(request):
    return render(request, "miss_management/team_goal_setting_form.html")

def logout_page(request):  # for logout
    login_emp_details = {'user_name': None, 'emp_type': None, 'login_status': False}
    return redirect("login")


@login_required(login_url="Login")  # decorator
def logout_user(request):  # for logout
    logout(request)
    return redirect("Login")


def login_details(request):
    return render(request, "miss_management/hr_home_page.html")


@login_required(login_url="Login")  # decorator foruser is login or not
def register_emp(request):
    return render(request, "miss_management/register_employees.html")

@login_required(login_url="Login")  # decorator foruser is login or not
def register_man(request):
    return render(request, "miss_management/register_managers.html")

#
# def employee_details(request):
#     if login_emp_details:
#
