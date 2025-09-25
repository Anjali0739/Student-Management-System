from django.shortcuts import render
from django.http import HttpResponseForbidden, JsonResponse
from .models import *


# Create your views here.
def index(request):
    return render(request, "authentication/login.html")


def dashboard(request):
    unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    unread_notification_count = unread_notification.count()
    return render(request, 'students/student-dashboard.html')


def mark_notifications_as_read(request):
    if request.method == 'POST':
        notification = Notification.objects.filter(user=request.user, is_read=False)
        notification.update(is_read=True)
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden()



def clear_all_notifications(reuqest):
    if reuqest.method == 'POST':
        notification = Notification.objects.filter(user=reuqest.user)
        notification.delete()
        return JsonResponse({'status':'success'})
    return HttpResponseForbidden