import uuid
import datetime
from django.db import models

def current_year():
    return datetime.date.today().year

class Fund(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    chain_id = models.CharField(max_length=40)
    name = models.CharField(max_length=30, null=True, blank=True)
    year = models.CharField(max_length=4, default=str(datetime.date.today().year))
    fy_premium = models.DecimalField(max_digits=8, decimal_places=2)
    fy_allowable = models.DecimalField(max_digits=8, decimal_places=2)

class Subscriber(models.Model):
    id = models.AutoField(primary_key=True)
    pub_key = models.CharField(max_length=44, null=True, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)

class Enrollment(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    subscriber = models.ForeignKey(Subscriber, related_name='enrollments', on_delete=models.CASCADE, default=None)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, default=None)
    paid_in = models.DecimalField(max_digits=8, decimal_places=2)
    date_paid_in = models.DateTimeField(auto_now_add=True, editable=False)

class Claim(models.Model): 
    STATUS = [("A", "Approved"), ("P", "Pending"), ("I", "Need Info"), ("D", "Denied")]
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, default=None)
    enrollment = models.ForeignKey(Enrollment, related_name='claims', on_delete=models.CASCADE, default=None)
    file_support = models.URLField(max_length=200)
    claim_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    status = models.CharField(max_length=1, choices=STATUS, default="P")
    date = models.DateTimeField(auto_now_add=True, editable=False)
    subscriber_notes = models.CharField(max_length=400, null=True, blank=True)
    system_notes = models.CharField(max_length=400, null=True, blank=True)