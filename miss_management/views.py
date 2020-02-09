from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .utility import *
from .models import Emp_goal_data_man, EmpData
from django.http import HttpResponse
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
            if staff.username == 'usha@verificient.com':
                return render(request, "miss_management/register_employees.html")
            if emp_type == 'Manager':
                return render(request, "miss_management/goal_setting_form.html")
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
            print(fname,  email, password)

            obj = User(username=email, password=password, first_name=type)
            obj.save()
            obj = EmpData(fname=fname, email=email,job_title=job_title,doj=doj,last_ap_date=last_ap_date,
                    evalute_by=evalute_by,reporting_mail=reporting_mail)
            obj.save()
            return HttpResponse("Added employee successfully")
        except:

            return HttpResponse("Employee registration failed")


class save_emp_goal_Data(View):  # for saving employee data into database
    # if (request.method=='POST'):
    def post(self, request, *args, **kwargs):  # save data if request is post
        try:
            emp_id = request.POST.get('emp_id', 'NA')
            goal_title = request.POST.get('goal_title', 'NA')
            goal_description = request.POST.get('goal_description', 'NA')
            due_date = request.POST.get('due_date', 'NA')

            print(emp_id, goal_title, goal_description, due_date)

            if emp_id and goal_title and goal_description and due_date:
                if not is_integer(emp_id):
                    return render(request, "miss_management/goal_setting_form.html",
                                  {'error': 'Employee id must be number'})

                if not validate(due_date):
                    return render(request, "miss_management/goal_setting_form.html",
                                  {'error': 'please enter date in proper format, e.g. 2003-12-30'})
                obj = Emp_goal_data_man(emp_id=emp_id, goal_title=goal_title, goal_description=goal_description,
                                        due_date=due_date)  # database object

                obj.save()
                return redirect("DisplayEmpData")
            else:
                return render(request, "miss_management/goal_setting_form.html", {'error': 'Please fill all the fields'})

        except Exception as e:
            print(e)
            return render(request, "miss_management/goal_setting_form.html", {'error': "Please fill all the fields"})

    def get(self, request, *args, **kwargs):  # get request
        return redirect(setting_form)


class DisplayEmpData(View):
    def get(self, request, *args, **kwargs):  # for displaying employee detail from database get request
        all_emp_data = Emp_goal_data_man.objects.all()
        SerNo = len(all_emp_data)
        # return all employee data which will be stored till now
        return render(request, "miss_management/show_goal_setting_data.html", {'emp_goal_setting_data': all_emp_data, 'serno': SerNo})


@login_required(login_url="Login")  # decorator foruser is login or not
def create_form(request):
    return render(request, "miss_management/registration.html")


@login_required(login_url="Login")
def setting_form(request):
    return render(request, "miss_management/goal_setting_form.html")


def logout_page(request):  # for logout
    login_emp_details = {'user_name': None, 'emp_type':None, 'login_status': False}
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


#
# def employee_details(request):
#     if login_emp_details:
#








