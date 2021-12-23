from django.urls import path
from rest_framework import routers
from .api import AttendenceViewSet, GiveAttendenceView,StudentAttendance

router = routers.SimpleRouter()
router.register('', AttendenceViewSet, basename="attendence")
urlpatterns = [
    path('update/', GiveAttendenceView.as_view()),
    path('user/',StudentAttendance.as_view()),
]
urlpatterns += router.urls
