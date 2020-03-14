from django.forms import ModelForm
from .models import Emp_goal_data_man
from django import forms

class OrderForm(ModelForm):

    class Meta:
        model = Emp_goal_data_man
        fields = '__all__'
        widgets = {
            'employee_comment': forms.HiddenInput(),
            'employee_ratings': forms.HiddenInput(),
            'manager_comment': forms.HiddenInput(),
            'manager_ratings': forms.HiddenInput(),
        }


class EmployeeFeedback(ModelForm):
    class Meta:
        model = Emp_goal_data_man
        fields = '__all__'
        widgets = {
            'email': forms.TextInput(attrs={'readonly':'readonly'}),
            'goal_id': forms.HiddenInput(),
            'goal_title': forms.TextInput(attrs={'readonly':'readonly'}),
            'goal_description': forms.TextInput(attrs={'readonly':'readonly'}),
            'due_date': forms.TextInput(attrs={'readonly':'readonly'}),
            'manager_comment': forms.HiddenInput(),
            'manager_ratings': forms.HiddenInput(),
        }


class TeamGoalForm(ModelForm):

    class Meta:
        model = Emp_goal_data_man
        fields = '__all__'
        widgets = {
            'employee_comment': forms.HiddenInput(),
            'employee_ratings': forms.HiddenInput(),
            'manager_comment': forms.HiddenInput(),
            'manager_ratings': forms.HiddenInput(),
        }
