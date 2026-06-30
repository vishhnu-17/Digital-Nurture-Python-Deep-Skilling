from django.contrib import admin
from .models import Department, Course, Student,Enrollment
class DepartmentAdmin(admin.ModelAdmin):
    list_display=('name','head_of_dept','budget')
    
admin.site.register(Department,DepartmentAdmin)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Enrollment)
# Register your models here.
