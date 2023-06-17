from django import forms

# base form class
class MyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['autocomplete'] = 'off'

class Login(MyForm):
    phone_no = forms.CharField(label='手机号', max_length=11)
    car_no = forms.CharField(label='车牌号', max_length=10)

class LocateCar1(MyForm):
    stall_no = forms.IntegerField(label='车位号')

class LocateCar2(MyForm):
    phone_no = forms.CharField(label='手机号', max_length=11)
    car_no = forms.CharField(label='车牌号', max_length=10)

class FindPath(MyForm):
    start_pos_r = forms.IntegerField(label='起始位置行号')
    start_pos_c = forms.IntegerField(label='起始位置列号')
    end_pos_r = forms.IntegerField(label='结束位置行号')
    end_pos_c = forms.IntegerField(label='结束位置列号')

class RestCar(MyForm):
    phone_no = forms.CharField(label='手机号', max_length=11)
    car_no = forms.CharField(label='车牌号', max_length=10)
    stall_no = forms.IntegerField(label='车位号')
    entry_no = forms.IntegerField(label='入口')

class FetchCar(MyForm):
    phone_no = forms.CharField(label='手机号', max_length=11)
    car_no = forms.CharField(label='车牌号', max_length=10)
    exit_no = forms.IntegerField(label='出口')

class StartCharge(MyForm):
    stake_no = forms.IntegerField(label='充电桩号')

class FinishCharge(MyForm):
    stake_no = forms.IntegerField(label='充电桩号')
