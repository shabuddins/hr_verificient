from . import views
from django.urls import path

urlpatterns = [
    path('', views.Login.as_view(), name="Login"),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('reg_emp/', views.register_emp, name="reg_emp"),
    path('setting_form/', views.setting_form, name="setting_form"),
    path('save_emp_Data/', views.save_emp_Data.as_view(), name="save_emp_Data"),
    path('save_emp_goal_Data/', views.save_emp_goal_Data.as_view(), name="save_emp_goal_Data"),
    path('DisplayEmpData/', views.DisplayEmpData.as_view(), name="DisplayEmpData"),
    path('EditDisplayEmpData/', views.EditDisplayEmpData.as_view(), name="EditDisplayEmpData"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/<str:goal_id>/', views.deleteOrder, name="delete_order"),
    path('add_emp_feedback/<str:goal_id>/', views.add_emp_feedback, name="add_emp_feedback"),
    path('search_emp_goal_Data/', views.search_emp_goal_Data.as_view(), name="search_emp_goal_Data"),

]

