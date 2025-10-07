from django.db import models
from django.utils import timezone


class Student(models.Model):
    roll_number = models.CharField(max_length=20, unique=True, primary_key=True)  # Changed from 8 to 20
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=150)  # Increased from 50 to 150
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.roll_number} - {self.name}"
    
    class Meta:
        ordering = ['roll_number']


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-date', '-time']


class Attendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    marked_at = models.DateTimeField(auto_now_add=True)
    is_present = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('event', 'student')
        ordering = ['-marked_at']
    
    def __str__(self):
        return f"{self.student.roll_number} - {self.event.name}"