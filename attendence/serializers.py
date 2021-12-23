from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Attendence

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email","is_staff"]

class AttendenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendence
        fields = ['id', 'teacher', 'section',
                  'date', 'course_code', 'qr', 'student']

    def to_representation(self, instance):
        data = super(AttendenceSerializer, self).to_representation(instance)
        data["student"] = UserSerializer(instance.student,many=True).data
        return data
