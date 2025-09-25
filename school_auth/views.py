from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.utils.crypto import get_random_string
from .models import PasswordResetRequest
from django.db import IntegrityError



User = get_user_model()

# Create your views here.
def signup_view(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST.get('role')


    #Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please log in or use a different email.")
            return redirect('signup')   # or re-render the same form template
        

        try:
            user = User.objects.create_user(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
        except IntegrityError:
            messages.error(request, "This email is already in use.")
            return redirect('signup')

        # Assign role flags
        if role == "student":
            user.is_student = True
        elif role == "teacher":
            user.is_teacher = True
        elif role == "admin":
            user.is_admin = True

        user.save()
        login(request, user)
        messages.success(request, 'Signed up Successfully!!')
        return redirect('index')

    return render(request, 'authentication/register.html')



def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Loggedin Successfully!!')

            if user.is_admin:
                return redirect('admin_dashboard')
            elif user.is_teacher:
                return redirect('teacher_dashboard')
            elif user.is_student:
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid user role')
                return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'authentication/login.html')



def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()

        if user:
            token = get_random_string(32)
            reset_request = PasswordResetRequest.objects.create(
                user = user,
                email = email,
                token = token
            )
            reset_request.send_reset_email()
            messages.success(request, 'Reset link sent to your email')
        else:
            messages.error(request, 'Email not found')
    return render(request, 'authentication/forgot-password.html')



def reset_password_view(request, token):
    reset_request = PasswordResetRequest.objects.filter(token=token).first()

    if not reset_request or not reset_request.is_valid():
        messages.error(request, 'Invalid or expired reset link')
        return redirect('index')
    
    if request.method == 'POST':
        new_password = request.POST['new_password']
        reset_request.user.set_password(new_password)
        reset_request.user.save()
        messages.success(request, 'Password reset successfully!!')
        return redirect('login')
    return render(request, 'authentication/reset-password.html', {'token':'token'})



def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out!!')
    return redirect('index')



