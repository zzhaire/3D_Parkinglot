from django.contrib import admin
from .models import Stake, Stall, User, Record


@admin.register(Stake)
class StakeManager(admin.ModelAdmin):
    list_display = ['status', 'start_time', 'finish_time', 'limit_time']
    search_fields = ['status , ''start_time', 'finish_time', 'limit_time']


# Register your models here.


@admin.register(Stall)
class StallManager(admin.ModelAdmin):
    list_display = ['stake_no', 'status', 'ph_no', 'car_no', 'start_time', 'end_time']
    search_fields = ['stake_no', 'status', 'ph_no', 'car_no', 'start_time', 'end_time']


@admin.register(Record)
class RecordManager(admin.ModelAdmin):
    list_display = ['status', 'ph_no', 'car_no', 'stall_no', 'stake_no', 'entry_no', 'exit_no', 'start_park_time',
                    'end_park_time', 'start_charge_time', 'finish_charge_time']
    search_fields = ['status', 'ph_no', 'car_no', 'stall_no', 'stake_no', 'entry_no', 'exit_no', 'start_park_time',
                     'end_park_time', 'start_charge_time', 'finish_charge_time']


@admin.register(User)
class UserManager(admin.ModelAdmin):
    list_display = ['ph_no', 'car_no', 'ip_no']
    search_fields = ['ph_no', 'car_no', 'ip_no']
