from django.db import models

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='teacher_photos/')
    joining_date = models.DateField()

    def __str__(self):
        return self.name
