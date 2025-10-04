from django.shortcuts import render
from django.http import HttpResponseForbidden, JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required
from school.models import Notification


# Create your views here.
def index(request):
    return render(request, "authentication/login.html")


@login_required
def dashboard(request):
    unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    unread_notification_count = unread_notification.count()
    return render(request, 'students/student-dashboard.html', {
        'unread_notification_count': unread_notification_count,
        'unread_notifications': unread_notification
    })


@login_required
def mark_notifications_as_read(request):
    if request.method == 'POST':
        notification = Notification.objects.filter(user=request.user, is_read=False)
        notification.update(is_read=True)
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden()


@login_required
def clear_all_notifications(request):
    if request.method == 'POST':
        notification = Notification.objects.filter(user=request.user)
        notification.delete()
        return JsonResponse({'status':'success'})
    return HttpResponseForbidden()



def create_notification(user, message):
    """
    Creates a notification for the given user.
    """
    Notification.objects.create(user=user, message=message)

