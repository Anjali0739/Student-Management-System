from django.shortcuts import render, get_object_or_404
from .models import Teacher
# Create your views here.



def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher/teachers.html', {'teachers': teachers})

def teacher_detail(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    return render(request, 'teacher/teacher-details.html', {'teacher': teacher})
