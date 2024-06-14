from django.contrib import admin
from .models import Student, Attendance, Bill, Expenditure

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('reg_no', 'name', 'room_no', 'course', 'branch', 'hostel_name', 'year_of_study', 'email')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('reg_no', 'date', 'present')

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('reg_no', 'amount', 'date_issued', 'due_date', 'paid', 'reference_number')

@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    list_display = ('date', 'milk', 'gas', 'groceries', 'vegetables', 'total_expenditure')
