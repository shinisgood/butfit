from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser


from .models import Place, Course
from .serializers import (
    PlaceSerializer,
    CourseSerializer,
)
from courses.serializers import AdminReservationSerializer


class UserCourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class AdminPlaceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class AdminCourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class AdminReservationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Course.objects.all()
    serializer_class = AdminReservationSerializer

    def get_reservations(self, request):
        courses = Course.objects.all()
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        sort = request.GET.get("sort", "recent")

        # 필터링
        filtering_criteria = {}

        # 날짜별 필터링
        if start_date:
            filtering_criteria["date__gte"] = start_date
            courses = courses.filter(**filtering_criteria).distinct()
        if end_date:
            filtering_criteria["date__lte"] = end_date
            courses = courses.filter(**filtering_criteria).distinct()

        list = CourseSerializer(courses, many=True, context={"request": request}).data
        # for article in articles

        return Response(list)
