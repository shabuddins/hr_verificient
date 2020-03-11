from django.forms import ModelForm
from .models import Emp_goal_data_man, Emp_goal_feedback


class OrderForm(ModelForm):
    class Meta:
        model = Emp_goal_data_man
        fields = '__all__'


class EmployeeFeedback(ModelForm):
    class Meta:
        model = Emp_goal_feedback
        fields = '__all__'
