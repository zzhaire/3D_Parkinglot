from django.db import models

# Create your models here.
# id is indeficitly defined
class Stall(models.Model):
    p_row       = models.IntegerField()                     # row no in map(start from 0)
    p_col       = models.IntegerField()                     # col no in map(start from 0)
    stake_no    = models.IntegerField()                     # associated with stake no
    status      = models.CharField(max_length=10)           # 'hold' or 'free'
    ph_no       = models.CharField(max_length=11)           # associated with phone number
    car_no      = models.CharField(max_length=10, null=True)# associated with car credential
    start_time  = models.DateTimeField(null=True)           # stark parking time
    end_time    = models.DateTimeField(null=True)           # end parking time

class Stake(models.Model):
    status      = models.CharField(max_length=10)           # 'on' or 'off'
    start_time  = models.DateTimeField(null=True)           # start charge time
    finish_time = models.DateTimeField(null=True)           # end charge time
    limit_time  = models.IntegerField(null=True)            # initialized charge time

class Record(models.Model):
    status      = models.CharField(max_length=10, null=True)# 'finished'(when fetch car) or null
    ph_no       = models.CharField(max_length=11)           # associated with phone number
    car_no      = models.CharField(max_length=10)           # associated with car credential
    stall_no    = models.IntegerField()                     # associated with stall no
    stake_no    = models.IntegerField(null=True)            # associated with stall no
    entry_no    = models.IntegerField(null=True)            # car entry port no
    exit_no     = models.IntegerField(null=True)            # car exit port no
    start_park_time     = models.DateTimeField(null=True)   # stark parking time
    end_park_time       = models.DateTimeField(null=True)   # end parking time
    start_charge_time   = models.DateTimeField(null=True)   # start charge time
    finish_charge_time  = models.DateTimeField(null=True)   # end charge time

class User(models.Model):
    ph_no       = models.CharField(max_length=11)           # associated with phone number
    car_no      = models.CharField(max_length=10)           # associated with car credential
    ip_no       = models.CharField(max_length=16, default='0.0.0.0')           # associated with user ip
    #status      = models.CharField(max_length=10, null=True)# 'auth' or 'unau'
