from rest_framework import viewsets, views, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from django.utils.dateparse import parse_date
from .serializers import AttendenceSerializer, UserSerializer
from .models import Attendence

User = get_user_model()


class AttendenceViewSet(viewsets.ModelViewSet):
    
    serializer_class = AttendenceSerializer

    def get_queryset(self):
        queryset = Attendence.objects.all()
        teacherID = self.request.query_params.get("teacher")
        teacher = User.objects.filter(id=teacherID).first()
        if teacher:
            queryset = Attendence.objects.filter(teacher=teacher)
        return queryset

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class GiveAttendenceView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        result_string = request.data.get("result")
        user = request.user
        if result_string:
            import ast
            result = ast.literal_eval(result_string)
            attendence = Attendence.objects.filter(
                section=result['section'],
                course_code=result['course_code'],
                date=parse_date(result['date'])).first()
            if user not in attendence.student.all():
                attendence.student.add(user)
                attendence.save()
                return Response({"message": "Success"})
            else:
                return Response({"message": "You have already given attendance."}, status=status.HTTP_423_LOCKED)
        return Response({"message": "Something went wrong, try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignupAPIView(views.APIView):
    def post(self, request):
        print(request.data)
        first_name = request.data.get('fname')
        last_name = request.data.get('lname')
        email = request.data.get('email')
        studentID = request.data.get('studentID')
        password = request.data.get('password')

        user = User.objects.create_user(studentID, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        user_data = UserSerializer(user).data

        return Response(user_data)


class LoginAPIView(views.APIView):
    def post(self, request):
        user = authenticate(username=request.data.get(
            "studentID"), password=request.data["password"])
        if not user:
            return Response({"message": "Please enter correct info"}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)

        user_data = UserSerializer(user).data

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            "user": user_data,
        })


class GetUserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = UserSerializer(request.user).data
        return Response(user)


class StudentAttendance(views.APIView):
    permission_classes = []

    def get(self,request):
        user = request.user
        # user = User.objects.get(id=1)
        attendence = Attendence.objects.filter(student__pk=user.id)
        attendenceAll = Attendence.objects.all()

        print(attendence)
        attendence_serializer = AttendenceSerializer(attendence,many=True)
        all_attendenceserizer = AttendenceSerializer(attendenceAll, many=True)
        return Response({"student":attendence_serializer.data, "all":all_attendenceserizer.data})

