from django.db import models


# Create your models here.

class CommercialParking(models.Model):
    sr_no = models.AutoField(primary_key=True, editable=True)
    slot_no = models.IntegerField(editable=True, unique=True)
    number_plate = models.CharField(max_length=15, blank=True, null=True, editable=True)
    entry_time = models.TimeField(blank=True, null=True, editable=True)
    entry_date = models.DateField(blank=True, null=True, editable=True)
    image = models.BinaryField(null=True, editable=True)

    class Meta:
        db_table = 'commercial_parking'


class CommercialHistory(models.Model):
    sr_no = models.AutoField(primary_key=True, editable=True,)
    slot_no = models.IntegerField(blank=True, null=True)
    number_plate = models.CharField(max_length=15, blank=True, null=True)
    entry_time = models.TimeField(blank=True, null=True)
    entry_date = models.DateField(blank=True, null=True)
    image = models.BinaryField(blank=True, null=True)
    exit_time = models.TimeField(blank=True, null=True)


    class Meta:
        db_table = 'commercial_history'

class Resident(models.Model):
    sr_no = models.AutoField(primary_key=True)
    register_name = models.CharField(max_length=15, blank=True, null=True)
    number_plate = models.CharField(max_length=15, blank=True, null=True)
    mobile_no = models.CharField(max_length=10, blank=True, null=True)
    alloted_slot = models.IntegerField(blank=True, null=True)
    current_person_name = models.CharField(max_length=15, blank=True, null=True)
    current_person_mobile_no = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'resident'


class Visitor(models.Model):
    sr_no = models.AutoField(primary_key=True)
    number_plate = models.CharField(max_length=15, blank=True, null=True)
    entry_time = models.TimeField(blank=True, null=True)
    entry_date = models.DateField(blank=True, null=True)
    image = models.BinaryField(blank=True, null=True)
    visitor_name = models.CharField(max_length=30, blank=True, null=True)
    visitor_mob = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'visitor'
