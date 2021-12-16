from django.db import models

program_name = (
    ("펑셔널", "펑셔널"),
    ("웨이트", "웨이트"),
    ("바디디자인", "바디디자인"),
    ("팻버닝", "팻버닝"),
    ("그룹요가", "그룹요가"),
    ("그룹복싱", "그룹복싱"),
    ("그룹필라테스", "그룹필라테스"),
)

credit = (
    ("99000", "99000"),
    ("190000", "190000"),
    ("290000", "290000"),
    ("390000", "390000"),
)
pass_count = (
    ("10", "10"),
    ("20", "20"),
    ("30", "30"),
)


class Place(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    center_name = models.CharField(max_length=50, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "places"
        app_label = "courses"


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    place = models.ForeignKey("Place", models.DO_NOTHING, null=False, blank=True)
    program_name = models.CharField(
        max_length=20, choices=program_name, null=True, blank=True
    )
    pass_count = models.CharField(
        max_length=20, choices=pass_count, null=True, blank=True
    )
    credit = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    closing_number = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    start_at = models.TimeField(null=True, blank=True)
    end_at = models.TimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "courses"
        app_label = "courses"
