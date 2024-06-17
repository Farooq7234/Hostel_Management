from django.urls import path

from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('contact',views.contact, name="contact"),
    path('email',views.send_monthly_emails,name='email'),
    path('about',views.about, name="about"),
    path('student-dashboard', views.student_dashboard, name='student_dashboard'),
    path('admin-dashboard', views.admin_dashboard, name='admin_dashboard'),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path("updateData/<int:id>",views.updateData,name='updateData'),
    path("deleteData/<int:id>",views.deleteData,name='deleteData'),
]

