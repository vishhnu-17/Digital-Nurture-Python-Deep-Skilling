from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .serializers import *
from rest_framework.views import APIView  
from rest_framework.response import Response 
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
# Create your views here.
def hello_view(request):
    return HttpResponse("Course Management API is running")
class CourseView(APIView):
    def get(self,request):
        courses=Course.objects.all()
        serializer=CourseSerializer(courses,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class CourseDetailView(APIView):
    def get(self,request,pk):
        course=get_object_or_404(Course,pk=pk)
        serializer=CourseSerializer(course)
        return Response(serializer.data)  
    def put(self,request,pk):
        course=get_object_or_404(Course,pk=pk)
        serializer=CourseSerializer(course,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        print("delete called")
        course=get_object_or_404(Course,pk=pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CourseViewSet(viewsets.ModelViewSet):
    queryset=Course.objects.all() # these are attributes defined 
    serializer_class=CourseSerializer    # So those attribute names are part of the framework's API (its expected interface).
    @action(detail=True)
    def students(self,request,pk=None):
        course=self.get_object()
        students=Student.objects.filter(enrollment__course=course)
        serializer=StudentSerializer(students,many=True)
        return Response(serializer.data)
        
   
class StudentViewSet(viewsets.ModelViewSet):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset=Enrollment.objects.all()
    serializer_class=EnrollmentSerializer
            
    