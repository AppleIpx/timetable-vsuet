from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import inline_serializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from timetable.users.api.response_schemes import StudentResponseSerializer
from timetable.users.api.response_schemes import TeacherResponseSerializer
from timetable.users.api.response_schemes import UnknownResponseSerializer
from timetable.users.api.serializers import BaseTeacherSerializer
from timetable.users.api.serializers import StudentSerializer


@extend_schema(
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="UserInfoResponse",
                fields={
                    "student": StudentResponseSerializer(),
                    "teacher": TeacherResponseSerializer(),
                    "unknown": UnknownResponseSerializer(),
                },
            ),
            description="User info based on role",
        ),
    },
)
class UserInfoView(APIView):
    """
    # Возвращает информацию о текущем авторизованном пользователе и его роли в системе.

    В зависимости от типа пользователя (студент или преподаватель), возвращается соответствующая структура данных:
    - Если пользователь является студентом, возвращаются его данные в формате `StudentSerializer`.
    - Если пользователь является преподавателем, возвращаются его данные в формате `BaseTeacherSerializer`.
    - Если пользователь не привязан ни к студенту, ни к преподавателю — возвращается роль `unknown`..
    """

    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user

        if hasattr(user, "student"):
            data = StudentSerializer(user.student).data
            return Response({"role": "student", "data": data})

        if hasattr(user, "teacher"):
            data = BaseTeacherSerializer(user.teacher).data
            return Response({"role": "teacher", "data": data})

        return Response({"role": "unknown", "user": "Anonymous"})
