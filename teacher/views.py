from django.shortcuts import render, get_object_or_404, redirect
from .models import Teacher, Department
from django.contrib import messages
# Create your views here.



def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher/teachers.html', {'teachers': teachers})

def teacher_detail(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    return render(request, 'teacher/teacher-details.html', {'teacher': teacher})


def add_teacher(request):
    departments = Department.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        department_id = request.POST['department']
        joining_date = request.POST['joining_date']
        photo = request.FILES.get('photo')

        department = get_object_or_404(Department, id=department_id)

        Teacher.objects.create(
            name=name,
            email=email,
            phone=phone,
            department=department,
            joining_date=joining_date,
            photo=photo
        )

        messages.success(request, "Teacher added successfully!")
        return redirect('teacher_list')

    return render(request, 'teacher/teacher_form.html', {
        'departments': departments,
        'teacher': None
    })


def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    departments = Department.objects.all()

    if request.method == 'POST':
        teacher.name = request.POST['name']
        teacher.email = request.POST['email']
        teacher.phone = request.POST['phone']
        teacher.department = get_object_or_404(Department, id=request.POST['department'])
        teacher.joining_date = request.POST['joining_date']

        if 'photo' in request.FILES:
            teacher.photo = request.FILES['photo']

        teacher.save()
        messages.success(request, "Teacher updated successfully!")
        return redirect('teacher_detail', teacher_id=teacher.id)

    return render(request, 'teacher/teacher_form.html', {
        'teacher': teacher,
        'departments': departments
    })
