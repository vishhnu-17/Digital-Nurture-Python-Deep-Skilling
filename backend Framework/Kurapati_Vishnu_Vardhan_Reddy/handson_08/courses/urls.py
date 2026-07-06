from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . views import *
router=DefaultRouter()
router.register('courses',CourseViewSet)
router.register('enrollments',EnrollmentViewSet)
router.register('students',StudentViewSet)
urlpatterns = [
    # path("", hello_view),
    # path("courses/", CourseView.as_view(), name="courses_with_slash"),
    # path("courses/<int:pk>/",CourseViewSet.as_view())
    path("",include(router.urls))
]
