from django.shortcuts import get_object_or_404

from rest_framework import serializers

from courses.models import Place, Course
from users.models import User, Credit, Reservation


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ["name", "center_name"]


class CourseSerializer(serializers.ModelSerializer):
    course_id = serializers.SerializerMethodField()
    place_info = serializers.SerializerMethodField()
    reservation_status = serializers.SerializerMethodField()
    reservation_detail = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "course_id",
            "place",
            "place_info",
            "program_name",
            "pass_count",
            "credit",
            "closing_number",
            "date",
            "start_at",
            "end_at",
            "created",
            "updated",
            "reservation_status",
            "reservation_detail",
        ]

    def get_course_id(self, obj):
        return obj.id

    def get_place_info(self, obj):
        data = PlaceSerializer(obj.place).data
        return data

    def get_reservation_status(self, obj):
        reservations = obj.reservation_set.all()
        data = {
            "total": reservations.count(),
            "canceled": reservations.filter(is_canceled=True).count(),
            "reserved": reservations.filter(is_canceled=False).count(),
            "credits": int(reservations.filter(is_canceled=False).count() * obj.credit),
        }
        return data

    def get_reservation_detail(self, obj):
        reservations = obj.reservation_set.all()
        data = AdminReservationSerializer(reservations, many=True).data
        return data


class AdminReservationSerializer(serializers.ModelSerializer):
    reservation_id = serializers.SerializerMethodField()
    user_info = serializers.SerializerMethodField()
    credit_status = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = [
            "reservation_id",
            "is_canceled",
            "user",
            "user_info",
            "created",
            "updated",
            "credit_status",
        ]

    def get_reservation_id(self, obj):
        return obj.id

    def get_user_info(self, obj):
        user = BrifUserSerializer(obj.user).data
        return user

    def get_credit_status(self, obj):
        # 예약 취소 시 크래딧 증가
        if obj.is_canceled == True:
            data = obj.course.credit
        # 예약 시 크래딧 감소
        else:
            data = obj.course.credit * -1
        return int(data)


class BrifUserSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    credit = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["user_id", "email", "phone_number", "credit"]

    def get_user_id(self, obj):
        return obj.id

    def get_credit(self, obj):
        credit = Credit.objects.filter(user=obj)
        if credit.exists():
            data = credit[0].credit
        else:
            data = 0
        return int(data)
