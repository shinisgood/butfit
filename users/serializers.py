from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable

from .models import User, Credit, Reservation

from courses.serializers import CourseSerializer


class UserSerializer(serializers.ModelSerializer):
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


class UserCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data["user"]
        user_credit = Credit.objects.get_or_create(user=user)[0]

        # 유저가 구매한 크래딧 추가
        user_credit.credit = user_credit.credit + validated_data["credit"]

        # 보유 금액이 100000 보다 작을 시 use_days 는 30일
        if user_credit.credit < 100000:
            user_credit.use_days = 30

        # 보유 금액이 100000 같거나 크고, 200000 보다 작다면 use_days 는 60일
        elif 100000 <= user_credit.credit < 200000:
            user_credit.use_days = 60

        # 보유 금액이 200000 같거나 크고, 300000 보다 작다면 use_days 는 90일
        elif 200000 <= user_credit.credit < 300000:
            user_credit.use_days = 90

        # 보유 금액이 300000 같거나 크면 use_days 는 120일
        elif 300000 <= user_credit.credit:
            user_credit.use_days = 120

        user_credit.save()
        return user_credit


class UserReservationSerializer(serializers.ModelSerializer):
    reservation_id = serializers.SerializerMethodField()
    user_info = serializers.SerializerMethodField()
    course_info = serializers.SerializerMethodField()
    credit_status = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = [
            "reservation_id",
            "is_canceled",
            "user",
            "user_info",
            "course",
            "course_info",
            "created",
            "updated",
            "credit_status",
        ]

    def get_reservation_id(self, obj):
        return obj.id

    def get_user_info(self, obj):
        user = UserSerializer(obj.user).data
        return user

    def get_course_info(self, obj):
        course = CourseSerializer(obj.course).data
        return course

    def get_credit_status(self, obj):
        # 예약 취소 시 크래딧 증가
        if obj.is_canceled == True:
            data = obj.course.credit
        # 예약 시 크래딧 감소
        else:
            data = obj.course.credit * -1
        return int(data)

    def create(self, validated_data):
        user = validated_data["user"]
        course = validated_data["course"]
        data = Reservation.objects.filter(user=user, course=course)

        # 중복 예약 확인
        if data.filter(is_canceled=False).exists():
            raise NotAcceptable("already exists")

        # 취소 후 재신청의 경우
        elif data.filter(is_canceled=True).exists():
            data = data[0]
            data.is_canceled = False
            data.save()

        # 첫번째 신청
        else:
            data = Reservation.objects.create(**validated_data)

        # 유저의 보유 크레딧 감소
        user_credit = get_object_or_404(Credit, user=user)
        if user_credit.credit < course.credit:

            # 크레딧 부족 시 에러
            raise NotAcceptable("not enough credit")
        user_credit.credit = user_credit.credit - course.credit
        user_credit.save()

        return data
