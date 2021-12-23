from django.contrib import admin
from .models import Attendence, Student

class AttendenceAdmin(admin.ModelAdmin):
    list_display = ['date', 'course_code', 'section']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['studentID', 'user']

admin.site.register(Attendence, AttendenceAdmin)
admin.site.register(Student, StudentAdmin)
