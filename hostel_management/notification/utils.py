from twilio.rest import Client
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from .models import Student, Attendance, Expenditure
from datetime import datetime

def send_bulk_sms(request):
    if request.method == 'POST':
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)

        students = Student.objects.all()
        successful_count = 0
        failed_count = 0
        failed_students = []

        # Calculate total expenditure for the previous month
        last_month_expenditures = Expenditure.objects.filter(date__month=datetime.now().month - 1)
        total_expenditure = sum(exp.total_expenditure for exp in last_month_expenditures)
        students_count = Student.objects.count()
        per_day = total_expenditure / students_count if students_count > 0 else 0

        for student in students:
            if student.phone_number:
                try:
                    # Calculate attendance details for the student
                    total_days = Attendance.objects.filter(reg_no=student.reg_no).count()
                    present_days = Attendance.objects.filter(reg_no=student.reg_no, present=True).count()
                    absent_days = Attendance.objects.filter(reg_no=student.reg_no, present=False).count()
                    reduction_days = max(0, (absent_days - 6))

                    # Calculate mess bill
                    mess_bill = present_days * per_day
                    mess_bill = f"{mess_bill:.2f}"

                    # Create message content
                    message_content = f"Name: {student.name}, Reg No: {student.reg_no}, Bill: {mess_bill}"
                    
                    # Send SMS
                    sent_message = client.messages.create(
                        body=message_content,
                        from_=settings.TWILIO_PHONE_NUMBER,
                        to=student.phone_number
                    )
                    successful_count += 1
                    print(f"SMS sent to {student.name} at {student.phone_number}")
                except Exception as e:
                    failed_count += 1
                    failed_students.append(student.name)
                    print(f"Failed to send SMS to {student.name}: {str(e)}")

        if successful_count > 0:
            messages.success(request, f"SMS sent successfully to {successful_count} students.")
        if failed_count > 0:
            messages.warning(request, f"Failed to send SMS to {failed_count} students: {', '.join(failed_students)}")

        return redirect('admin_dashboard')
    else:
        return redirect('admin_dashboard')
