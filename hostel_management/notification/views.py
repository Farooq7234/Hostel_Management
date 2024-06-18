from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from .models import Student,Attendance,Expenditure,Bill
from django.core.mail import send_mail
from django.conf import settings
#import pyrebase
config={
  "apiKey": "AIzaSyBY2HkpBR3PmsecYT0pH0Ezy111UVyDq4o",
  "authDomain": "hostel-management-ea786.firebaseapp.com",
  "databaseURL": "https://hostel-management-ea786-default-rtdb.firebaseio.com",
  "projectId": "hostel-management-ea786",
  "storageBucket": "hostel-management-ea786.appspot.com",
  "messagingSenderId": "145333777665",
  "appId": "1:145333777665:web:6907d4b75ac0ae272a5700",
}
#firebase=pyrebase.initialize_app(config)
#authe=firebase.auth()
#dtabase=firebase.database()


def home(request):
    return render(request,"app/index.html")

def contact(request):
    return render(request,"app/contact.html")
def index(request):
    return render(request,"app/index.html")

def about(request):
    return render(request,"app/about.html")

def is_student(user):
    return user.groups.filter(name="student").exists()

def is_admin(user):
    return user.groups.filter(name="admin").exists()


def student_dashboard(request):
    try: 
        if request.user.is_authenticated:
            student = Student.objects.get(reg_no=request.user)
            total_days = Attendance.objects.filter(reg_no__reg_no=request.user).count()
            present_days = Attendance.objects.filter(reg_no__reg_no=request.user, present=True).count()
            absent_days = Attendance.objects.filter(reg_no__reg_no=request.user, present=False).count()
            reduction_days = max(0, (absent_days - 6))

            last_month_expenditures = Expenditure.objects.filter(date__month=datetime.now().month-1)
            total_expenditure = sum(exp.total_expenditure for exp in last_month_expenditures)
            students_count = Student.objects.count()
            per_day = total_expenditure / students_count if students_count > 0 else 0
            mess_bill = present_days * per_day
            bill_summary = Bill.objects.filter(reg_no__reg_no=request.user)

            context = {
                'student': student,
                'total_days': total_days,
                'present_days': present_days,
                'reduction_days': reduction_days,
                'mess_bill': mess_bill,
                'bill_summary': bill_summary,
                'last_date': '10/06/2024',
            }
            return render(request, 'app/student/student_dashboard.html', context)
        else:
            messages.error(request, "login to access the page")
            return redirect('signin')
    except Student.DoesNotExist:
        return render(request, 'app/student/student_not_found.html')
def admin_dashboard(request):
    if request.user.is_authenticated:
        students = Student.objects.all()
        expenditures = Expenditure.objects.all()
        attendance=Attendance.objects.all()

        context = {
            'students': students,
            'expenditures': expenditures,
            'attendance': attendance,
        }
        return render(request, 'app/admin/admin_dashboard.html', context)
    else:
        messages.error(request, "login to access the page")
        return redirect('signin')

def signin(request):
    if request.user.is_authenticated:
        messages.info(request, "Already logged in")
        return redirect("home")
    
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            messages.success(request, "login success")
            if is_student(user):
                return redirect('student_dashboard')
            elif is_admin(user):
                return redirect('admin_dashboard')
            elif user.is_superuser:
                return redirect('superuser')
            return redirect("home")
        else:
            messages.error(request, "login failed")
            return redirect("signin")
    return render(request, "app/signin.html")

def signout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "logout sucess")
        return redirect("signin")
    return redirect('home')
def send_monthly():
    students = Student.objects.all()
    subject = "Monthly Update"
    message = "TIME TO PAY YOU MESS FEES "
    from_email = settings.DEFAULT_FROM_EMAIL
    
    recipient_list = [student.email for student in students]
    
    send_mail(subject, message, from_email, recipient_list)
def deleteData(request,id):
    newdata=Student.objects.get(id=id)
    newdata.delete()
    return redirect('admin_dashboard')

    
def send_monthly_emails(request):
    send_monthly()
    return redirect('/')

def updateData(request,id):
    newdata=Student.objects.get(id=id)
    if request.method=='POST':
        reg_no=request.POST['reg_no']
        name=request.POST['name']
        room_no=request.POST['room_no']
        course=request.POST['course']
        branch=request.POST['branch']
        hostel_name=request.POST['hostel_name']
        year_of_study=request.POST['year_of_study']
        email=request.POST['email']
        newdata.reg_no=reg_no
        newdata.name=name
        newdata.room_no=room_no
        newdata.course=course
        newdata.branch=branch
        newdata.hostel_name=hostel_name
        newdata.year_of_study=year_of_study
        newdata.email=email
        newdata.save()
        return redirect('admin_dashboard')
    return render(request,'app/update.html',{'data':newdata})


