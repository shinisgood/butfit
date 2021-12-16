from datetime import datetime, timedelta

from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response

from dj_rest_auth.registration.views import RegisterView

from .models import User, Credit, Reservation
from .serializers import (
    UserSerializer,
    UserCreditSerializer,
    UserReservationSerializer,
)

from rest_framework.permissions import AllowAny


class CustomRegisterViewSet(RegisterView):
    def create(self, request, *args, **kargs):
        # 핸드폰번호 중복 확인
        if User.objects.filter(phone_number=request.data["phone_number"]).exists():
            return Response(
                {"message": "already exist phone number"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        # 이메일 중복 확인
        if User.objects.filter(email=request.data["email"]).exists():
            return Response(
                {"message": "already exist email"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        # 입력 비밀번호 일치 확인
        elif not request.data["password1"] == request.data["password2"]:
            return Response(
                {
                    "message": "invalid_password",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 유저 생성
        response = super().create(request, *args, **kargs)

        user = get_object_or_404(User, email=request.data["email"])

        # 유저 핸드폰 번호 저장
        user.phone_number = request.data["phone_number"]
        user.save()
        response.data["user"]["phone_number"] = user.phone_number

        return Response(
            {
                "data": response.data,
            },
            status=status.HTTP_201_CREATED,
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreditViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    queryset = Credit.objects.all()
    serializer_class = UserCreditSerializer


class UserReservationViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    queryset = Reservation.objects.all()
    serializer_class = UserReservationSerializer

    def get_reservations(self, request):
        reservations = Reservation.objects.all()
        user = request.GET.get("user_id", None)
        is_canceled = request.GET.get("is_canceled", None)
        sort = request.GET.get("sort", "recent")

        # 솔팅
        sortby_mapping = {
            "recent": "-created",  # 예약 최신 순
        }
        reservations = reservations.order_by(sortby_mapping[sort])

        # 필터링
        filtering_criteria = {}

        # 유저 별 예약
        if is_canceled:
            filtering_criteria["is_canceled"] = is_canceled
            reservations = reservations.filter(**filtering_criteria).distinct()

        if user:
            filtering_criteria["user_id"] = user
            reservations = reservations.filter(**filtering_criteria).distinct()

        list = UserReservationSerializer(
            reservations, many=True, context={"request": request}
        ).data

        return Response(list)

    def put_reservation_cancel(self, request, pk):
        reservation = get_object_or_404(Reservation, id=pk)
        user_credit = get_object_or_404(Credit, user=reservation.user)

        if reservation.is_canceled == True:
            return Response(
                {
                    "message": "already canceled",
                },
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        # 수업 시작 기준 3일전 크레딧 전액 환불
        elif timezone.now().date() + timedelta(days=3) < reservation.course.date:
            user_credit.credit += reservation.course.credit
            user_credit.save()

        # 수업 시간 기준 1일전 크레딧 50% 환불
        elif timezone.now().date() + timedelta(days=1) < reservation.course.date:
            user_credit.credit += reservation.course.credit / 2
            user_credit.save()

        # 수업 당일 취소 불가
        elif timezone.now().date() == reservation.course.date:
            return Response(
                {
                    "message": "cannot be refunded",
                },
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        reservation.is_canceled = True
        reservation.save()
        data = UserReservationSerializer(reservation).data
        return Response(data)
