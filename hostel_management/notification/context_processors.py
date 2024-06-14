
from django.contrib.auth.models import Group

def student_group(request):
    if request.user.is_authenticated:
        is_student = request.user.groups.filter(name='student').exists()
    else:
        is_student = False
    return {'is_student': is_student}
