from twilio.rest import Client
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from .models import Student

def send_bulk_sms(request):
    if request.method == 'POST':
        message_content = request.POST.get('message', '')
        
        if not message_content:
            messages.error(request, "Message cannot be empty.")
            return redirect('admin_dashboard')

        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)
        
        students = Student.objects.all()
        successful_count = 0
        failed_count = 0
        failed_students = []

        for student in students:
            if student.phone_number:
                try:
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
