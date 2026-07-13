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
from django.db.models import Q
from django.http import Http404
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
    
    def create(self,request):
        response=super().create(request)
        response['location']=f"api/v1/courses/{response.data['id']}/"
        return response
    
    def list(self,request):
        page=int(request.query_params.get("page",1))
        page_size=int(request.query_params.get("page_size",2))
        search=request.query_params.get("search")
        start=(page-1)*page_size
        end=start+page_size
        # courses=Course.objects.all()[start:end] # or courses= self.get_queryset()[start:end]
        queryset=Course.objects.all()
        if search:
            queryset=queryset.filter(Q(name__icontains=search)|Q(code__icontains=search))
        courses=queryset[start:end]    
        total=queryset.count()
        serializer=CourseSerializer(courses,many=True)
        next_page=None
        if end<total:
            next_page=f"/api/v1/courses/?search={search}&page={page+1}&page_size={page_size}"
        prev_page=None
        if page>1:
             prev_page=f"/api/v1/courses/?search={search}&page={page-1}&page_size={page_size}"
        return Response({
            "count":total,
            "next":next_page,
            "previous": prev_page,
            "results": serializer.data
        })
    
    def error_response(self,code,message,field=None,status_code=400):
        return Response(
            {
                "code":code,
                "message":message,
                "field":field,
                
            },
            status=status_code
        )
    def retrieve(self,request,*args,**kwargs):
        try:
            super().retrieve(request,*args,**kwargs)
        except Http404:
            return self.error_response(
                code="NOT FOUND",
                message=f"Course with id {kwargs['pk']} does not exist",
                status_code=status.HTTP_404_NOT_FOUND
                )  
                            
        
# A ModelViewSet already contains:

# list()
# retrieve()
# create()
# update() ← PUT
# partial_update() ← PATCH
# destroy()        

class StudentViewSet(viewsets.ModelViewSet):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset=Enrollment.objects.all()
    serializer_class=EnrollmentSerializer
            
    