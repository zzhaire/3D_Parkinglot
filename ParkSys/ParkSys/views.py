from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from . import mapsolve
from DataPower.models import (
    User,
    Stall,
    Stake,
    Record,
)
from .forms import (
    Login,
    LocateCar1,
    LocateCar2,
    FindPath,
    RestCar,
    FetchCar,
    StartCharge,
    FinishCharge,
)

from django.views.decorators.csrf import csrf_exempt
from aip import AipOcr
import os


def m_test(request):
    return HttpResponse("Hello world!")


def m_map(request):
    return render(request, 'm_map.html')


def homepage(request):
    if request.method == 'GET':
        login_status, login_name = get_login_status(request)
        return render(request, 'homepage.html', {'login_status': login_status, 'login_name': login_name})

    elif request.method == 'POST':
        if "login" in request.POST:
            if submit_login(request):
                login_status, login_name = get_login_status(request)
                return render(request, 'homepage.html', {'login_status': 1, 'login_name': login_name})
            else:
                return HttpResponse(f"login failed")
        elif "logout" in request.POST:
            if submit_logout(request):
                return render(request, 'homepage.html', {'login_status': 0})
            else:
                return HttpResponse(f"logout failed")


def map(request):
    refresh_stake()
    stall_status = get_stall_status()
    stake_status = get_stake_status()
    login_status, login_name = get_login_status(request)
    user_status = get_user_status(request)
    # print(f" stall_status = ***{stall_status}*** ")
    # print(f" stall_status = ***{stall_status}*** ")
    # print(f" stall_status = ***{stall_status}*** ")
    print(f" user_status = ***{user_status}*** ")
    if request.method == 'GET':
        # print(stake_status)
        return render(request, 'map.html', {
            'stall_status': stall_status,
            'stake_status': stake_status,
            'login_status': login_status,
            'login_name': login_name,
            'user_status': user_status,
        })
    elif request.method == 'POST':
        print("test")
        if "login" in request.POST:
            if submit_login(request):
                return render(request, 'map.html', {
                    'stall_status': stall_status,
                    'stake_status': stake_status,
                    'login_status': login_status,
                    'login_name': login_name,
                    'user_status': user_status,
                })
            else:
                return HttpResponse(f"login failed")
        elif "logout" in request.POST:
            if submit_logout(request):
                return render(request, 'map.html', {
                    'stall_status': stall_status,
                    'stake_status': stake_status,
                    'login_status': 0,
                    'user_status': 0,
                })
            else:
                return HttpResponse(f"logout failed")
        elif "findpath" in request.POST:
            road_status = submit_render_path_lookup(request)
            if not road_status:
                return HttpResponse('Render Path Failed!')
            return render(request, 'map.html', {
                'stall_status': stall_status,
                'stake_status': stake_status,
                'road_status': road_status,
                'user_status': user_status,
                'login_status': login_status,
                'login_name': login_name,
            })


def showstallstatus(request):
    # print("greergger")
    if request.method == 'POST':
        no = request.POST.get('id')
        response = {'status': None}
        filter_result = Stall.objects.filter(stake_no=no)
        # print(no)
        if len(filter_result) > 0:
            response['status'] = Stall.objects.get(stake_no=no).status
        else:
            st = Stall.objects.create(p_row=int(no), p_col=int(no), stake_no=no, status='free', ph_no=no)
            st.save()
            response['status'] = 'free'
            # print('free')
        # print(response)
        return JsonResponse(response)


def parkin(request):
    ip_no = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    if request.method == 'POST':
        no = request.POST.get('id')
        response = {}
        if (no == '' or int(no) > 100):
            response['message'] = '未选择车位，请重新选择'
        else:
            filter_result = Stall.objects.filter(stake_no=no)
            # print(no)
            if len(filter_result) > 0:
                user = User.objects.get(ip_no=ip_no)
                ph_no = user.ph_no
                car_no = user.car_no
                current_stall = Stall.objects.get(stake_no=no)
                now = timezone.now()

                if current_stall.status == 'hold':
                    response['message'] = '该车位已有车，请重新选择'
                else:
                    try:
                        stall = Stall.objects.get(car_no=car_no,status='hold')
                        response['message'] = '请勿重复停车'
                    except ObjectDoesNotExist:
                        response['message'] = '停车成功'
                        current_stall.car_no = car_no
                        current_stall.ph_no = ph_no
                        current_stall.status = 'hold'
                        current_stall.start_time = now
                        current_stall.save()
                        rec = Record(
                            ph_no=ph_no,
                            car_no=car_no,
                            stall_no=no,
                            entry_no=1,
                            start_park_time=now,
                        )
                        rec.save()
        # print('free')
        # print(response)
    return JsonResponse(response)


def parkout(request):
    ip_no = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    response = {}
    if request.method == 'POST':
        user = User.objects.get(ip_no=ip_no)
        car_no = user.car_no
        stall = Stall.objects.get(car_no=car_no,status='hold')
        try:
            rec = Record.objects.get(car_no=car_no, status=None)
        # print(f"-----------------------{rec.status}---------------")
            stake_filter = Stake.objects.filter(id=rec.stake_no)
            not_exit_charge = 0
            if len(stake_filter) > 0:
                stake = Stake.objects.get(id=rec.stake_no)
                if stake.finish_time == null:
                    not_exit_charge = 1
                stake.status = 'off'
                stake.save()

            stall.status = 'free'
            now = timezone.now()
            stall.end_time = now
            stall.save()
            rec.status = 'finished'
            rec.exit_no = 2
            rec.end_park_time = now
            if len(stake_filter):
                rec.finish_charge_time = now if stake.finish_time == null else stake.finish_time
            rec.save()

            response['message'] = '取车成功,您的车位停放在' + str(stall.id) + '号'
            if not_exit_charge == 1:
                response['message'] = '取车成功,已为您默认断电,您的车位停放在' + str(stall.id) + '号'
            response['id'] = stall.id
        except ObjectDoesNotExist:
            response['message'] = '没有要取的车'
            response['id']=-1
        return JsonResponse(response)


def get_stakestatus(request):
    print('request')
    if request.method == 'POST':
        response = {}
        total = Stall.objects.all()
        total_num = len(total)
        # print(total_num)
        if total_num == 0:
            for i in range(1, 126):
                st = Stall(p_row=i, p_col=i, stake_no=i, status='free' if i % 2 == 0 else 'hold')
                st.save()
        # Manually convert the QuerySet to a list of dictionaries
        total = [{'id': obj.stake_no, 'status': obj.status} for obj in total]
        response['num'] = total_num
        response['status'] = total
        print(total)
        return JsonResponse(response)


#def charge(request):
#    return render(request, 'charge.html', {'login_status': login_status, 'login_name': login_name})

def charge(request):
    refresh_stake()
    login_status, login_name = get_login_status(request)
    park_status = get_park_status(request)
    charge_status = get_charge_status(request)
    print(login_status)
    print(park_status)
    statuss = {
            'login_status': login_status, 
            'login_name': login_name, 
            'park_status': park_status,
            'charge_status': charge_status,  
            'remain_time' : 0, # need to calculate
            'actual_time' : 0, # need to calculate
            }
    if request.method == 'GET':
        if login_status and park_status and charge_status:
            ip_no = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
            user = User.objects.get(ip_no=ip_no)
            ph_no = user.ph_no
            car_no = user.car_no
            stall = Stall.objects.get(car_no=car_no, ph_no=ph_no, status='hold')
            stake = Stake.objects.get(id=stall.id)
            now = timezone.now()
            statuss['actual_time'] = (now - stake.start_time).total_seconds()
            statuss['remain_time'] = int(stake.limit_time - statuss['actual_time'])
            ach = (statuss['actual_time'] / 3600 * 7)
            ach = "{:.2f}".format(ach)
            rth = int(statuss['remain_time'] / 3600)
            rtm = int(int(int(statuss['remain_time']) % 3600) / 60)
            rts = int(int(statuss['remain_time']) % 3600) % 60
            money = stake.limit_time*0.55*7/3600
            money = "{:.2f}".format(money)
            statuss.update({'sno': stake.id, 'ach':ach, 'rth':rth, 'rtm':rtm,'rts':rts,'money':money})

        elif login_status and park_status and not charge_status:
            ip_no = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
            user = User.objects.get(ip_no=ip_no)
            ph_no = user.ph_no
            car_no = user.car_no
            stall = Stall.objects.get(car_no=car_no, ph_no=ph_no, status='hold')
            stake = Stake.objects.get(id=stall.id)
            statuss.update({'sno': stake.id,})
            return render(request, 'charge.html', statuss)

    # the follows are post requests 

    elif login_status and park_status and charge_status==0 :
        money = request.POST['money']
        limit_time = int(money) / 0.55 / 7 * 3600;
        print(limit_time)
        ip_no = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
        user = User.objects.get(ip_no=ip_no)
        ph_no = user.ph_no
        car_no = user.car_no
        stall = Stall.objects.get(car_no=car_no, ph_no=ph_no, status='hold')
        stake = Stake.objects.get(id=stall.id)
        now = timezone.now()

        stake.status = 'on'
        stake.start_time = now
        stake.end_time = None
        # TODO
        stake.limit_time = limit_time
        stake.save()
        statuss['charge_status'] = 1
        statuss['remain_time'] = stake.limit_time 
        statuss['actual_time'] = 0
        statuss['actual_time'] = (now - stake.start_time).total_seconds()
        statuss['remain_time'] = int(stake.limit_time - statuss['actual_time'])
        ach = (statuss['actual_time'] / 3600 * 7)
        ach = "{:.2f}".format(ach)
        rth = int(statuss['remain_time'] / 3600)
        rtm = int(int(int(statuss['remain_time']) % 3600) / 60)
        rts = int(int(statuss['remain_time']) % 3600) % 60
        money = stake.limit_time*0.55*7/3600
        money = "{:.2f}".format(money)
        statuss.update({'sno': stake.id, 'ach':ach, 'rth':rth, 'rtm':rtm,'rts':rts,'money':money})

        return render(request, 'charge.html', statuss)

    elif login_status and park_status and charge_status==1 and "stopcharge" in request.POST:
        ip_no = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
        user = User.objects.get(ip_no=ip_no)
        ph_no = user.ph_no
        car_no = user.car_no
        stall = Stall.objects.get(car_no=car_no, ph_no=ph_no, status='hold')
        stake = Stake.objects.get(id=stall.id)
        now = timezone.now()

        stake.status = 'off'
        stake.finish_time = now
        stake.save()
        statuss['charge_status'] = 0
        statuss['actual_time'] = (now - stake.start_time).total_seconds()
        statuss['remain_time'] = 0

    return render(request, 'charge.html', statuss)

# TODO
def charge_qzx(request):
    # name 是手机号
    status, name = get_login_status(request)

    # if request.method == 'POST':
    #    if "start_time" in request.POST:
    #        now1 = datetime.datetime.now()
    #       return render(request, 'charge.html', {"start_time":now1})
    #    elif "finish_time" in request.POST:
    #        now2 = datetime.datetime.now()
    #        return render(request, 'charge.html', {"finish_time":now2})
    #    else
    #        return render(request, 'charge.html',)

    # statuss={
    #    'login_status': login_status,
    #    'park_status': park_status,
    #    'charge_status': charge_status,
    #   'remain_time':0,
    #   'actual_time':0,
    # }
    return render(request, 'charge.html')


def contact(request):
    login_status, login_name = get_login_status(request)
    return render(request, 'contact.html', {'login_status': login_status, 'login_name': login_name})


def admin(request):
    refresh_stake()
    if request.method == 'GET':
        if "initstake" in request.GET:
            mapsolve.init_stake()
            return HttpResponse("Init Stake DB success!")

        elif "initstall" in request.GET:
            mapsolve.init_stall()
            return HttpResponse("Init Stall DB success!")

        elif "initrecord" in request.GET:
            mapsolve.init_record()
            return HttpResponse("Init Record DB success!")

        elif "inituser" in request.GET:
            mapsolve.init_user()
            return HttpResponse("Init User DB success!")

        # get admin page
        else:
            rest_car_form = RestCar()
            fetch_car_form = FetchCar()
            lc_car1_form = LocateCar1()
            lc_car2_form = LocateCar2()
            find_path_form = FindPath()
            start_charge_form = StartCharge()
            finish_charge_form = FinishCharge()
            forms = {
                'rest_car_form': rest_car_form,
                'fetch_car_form': fetch_car_form,
                'lc_car1_form': lc_car1_form,
                'lc_car2_form': lc_car2_form,
                'find_path_form': find_path_form,
                'start_charge_form': start_charge_form,
                'finish_charge_form': finish_charge_form,
            }

            return render(request, 'a_admin.html', forms)

    elif request.method == 'POST':
        if "locate_car1" in request.POST:
            r, c = submit_locate_car1(request)

            if (r, c) == (-1, -1):
                return HttpResponse('locate_car1 failed!')

            return HttpResponse(f"locate_car1 success!<br> row: {r} col: {c}")

        elif "locate_car2" in request.POST:
            r, c = submit_locate_car2(request)

            if (r, c) == (-1, -1):
                return HttpResponse('locate_car2 failed!')

            return HttpResponse(f"locate_car2 success!<br> row: {r} col: {c}")

        elif "find_path" in request.POST:
            path = submit_find_path(request)
            if not path:
                return HttpResponse('Find Path Failed!')

            return render(request, 'a_coordinates.html', {'coordinates': path})

        elif "render_path" in request.POST:
            stall_status = get_stall_status()
            road_status = submit_render_path(request)
            if not road_status:
                return HttpResponse('Render Path Failed!')

            return render(request, 'map.html', {'stall_status': stall_status, 'road_status': road_status})

        elif "rest_car" in request.POST:
            success, path = submit_rest_car(request)
            if success:
                # return HttpResponse('Rest Car Success!')
                return render(request, 'a_response_restcar.html', {'coordinates': path})
            else:
                return HttpResponse('Rest Car Failed!')

        elif "fetch_car" in request.POST:
            success, path, park_time = submit_fetch_car(request)
            if success:
                # return HttpResponse('Fetch Car Success!')
                return render(request, 'a_response_fetchcar.html', {'coordinates': path, 'park_time': park_time})
            else:
                return HttpResponse('Fetch Car Failed!')

        elif "start_charge" in request.POST:
            # print("test s")
            success = submit_start_charge(request)
            if success:
                return HttpResponse('Start Charge Success!')
            else:
                return HttpResponse('Start Charge Failed!')

        elif "finish_charge" in request.POST:
            success, charge_time = submit_finish_charge(request)
            if success:
                return HttpResponse(f'Fetch Car Success! <br> Total Charge time: {charge_time}')
            else:
                return HttpResponse('Start Charge Failed!')


def submit_locate_car1(request):
    form = LocateCar1(request.POST)

    if form.is_valid():
        stall_no = form.cleaned_data['stall_no']
        stall = Stall.objects.get(id=stall_no)
        row = stall.p_row
        col = stall.p_col
        return (row, col)

    return (-1, -1)


def submit_locate_car2(request):
    form = LocateCar2(request.POST)

    if form.is_valid():
        phone_no = form.cleaned_data['phone_no']
        car_no = form.cleaned_data['car_no']

        try:
            stall = Stall.objects.get(car_no=car_no, ph_no=phone_no, status='hold')
            row = stall.p_row
            col = stall.p_col
            return (row, col)

        except ObjectDoesNotExist:
            print("find no corresponding stall")
            return (-1, -1)

        except MultipleObjectsReturned:
            print("find multiple corresponding stall")
            return (-1, -1)

    return (-1, -1)


def submit_find_path(request):
    form = FindPath(request.POST)

    if form.is_valid():
        sr = form.cleaned_data['start_pos_r']
        sc = form.cleaned_data['start_pos_c']
        er = form.cleaned_data['end_pos_r']
        ec = form.cleaned_data['end_pos_c']
        return mapsolve.grid.search((sr, sc), (er, ec))

    return []


def submit_render_path(request):
    form = FindPath(request.POST)

    if form.is_valid():
        sr = form.cleaned_data['start_pos_r']
        sc = form.cleaned_data['start_pos_c']
        er = form.cleaned_data['end_pos_r']
        ec = form.cleaned_data['end_pos_c']

        path_coord = mapsolve.grid.search((sr, sc), (er, ec))
        road_coord = mapsolve.get_road()
        road_status = [0] * len(road_coord)

        for c in path_coord:
            if c in road_coord:
                road_status[road_coord.index(c)] = 1

        return road_status

    return []


def submit_render_path_lookup(request):
    ip_no = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    user = User.objects.get(ip_no=ip_no)
    car_no = user.car_no
    ph_no = user.ph_no
    stall = Stall.objects.get(car_no=car_no, ph_no=ph_no, status='hold')

    sr = 2
    sc = 0
    er = stall.p_row
    ec = stall.p_col

    path_coord = mapsolve.grid.search((sr, sc), (er, ec))
    road_coord = mapsolve.get_road()
    road_status = [0] * len(road_coord)

    for c in path_coord:
        if c in road_coord:
            road_status[road_coord.index(c)] = 1

    print(road_status)
    return road_status


def submit_rest_car(request):
    form = RestCar(request.POST)

    if form.is_valid():
        # get submit data
        phone_no = form.cleaned_data['phone_no']
        car_no = form.cleaned_data['car_no']
        stall_no = form.cleaned_data['stall_no']
        entry_no = form.cleaned_data['entry_no']

        # lookup matching stall record
        stall = Stall.objects.get(id=stall_no)

        # retur false if the stall is hold
        if stall.status != 'free':
            print("submit_rest_car: the stall has been parked")
            return False, []

        # get current time
        now = timezone.now()

        # update Stall table 
        stall.car_no = car_no
        stall.ph_no = phone_no
        stall.status = 'hold'
        stall.start_time = now
        stall.save()

        # update Record table 
        rec = Record(
            ph_no=phone_no,
            car_no=car_no,
            stall_no=stall_no,
            entry_no=entry_no,
            start_park_time=now,
        )
        rec.save()

        # get path
        start = mapsolve.port[entry_no - 1]
        end = (stall.p_row, stall.p_col)
        path = mapsolve.grid.search(start, end)
        # adjust path a little
        path = [mapsolve.port[entry_no - 1]] + path[:-1]

        return True, path

    return False, []


def submit_fetch_car(request):
    form = FetchCar(request.POST)

    if form.is_valid():
        phone_no = form.cleaned_data['phone_no']
        car_no = form.cleaned_data['car_no']
        exit_no = form.cleaned_data['exit_no']

        # lookup matching record
        try:
            stall = Stall.objects.get(car_no=car_no, ph_no=phone_no)
            stake = Stake.objects.get(id=stall.stake_no)
            print(stake.id)
            try:
                rec = Record.objects.get(car_no=car_no, ph_no=phone_no, status=None)

                # check status
                if stall.status != 'hold':
                    print('submit_fetch_car: The Stall is already parked')
                    return False, [], None
                if stake.status != 'off':
                    print("submit_fetch_car: The Stake hasn't been discharged!")
                    return False, [], None

                # get current time
                now = timezone.now()

                # update Stall's record
                stall.status = 'free'
                stall.end_time = now
                stall.save()

                # update Record's record
                rec.exit_no = exit_no
                rec.end_park_time = now
                rec.status = 'finished'
                rec.save()

                # get path
                start = (stall.p_row, stall.p_col)
                end = mapsolve.port[exit_no - 1]
                path = mapsolve.grid.search(start, end)

                # get park time 
                time = stall.end_time - stall.start_time

                return True, path, time.total_seconds()

            except ObjectDoesNotExist:
                print("submit_fetch_car: find no corresponding parking record")
                return False, [], None

            except MultipleObjectsReturned:
                print("submit_fetch_car: find multiple corresponding parking record")
                return False, [], None

        except ObjectDoesNotExist:
            print("submit_fetch_car: find no corresponding stall")
            return False, [], None

        except MultipleObjectsReturned:
            print("submit_fetch_car: find multiple corresponding stall")
            return False, [], None

    return False, [], None


def submit_start_charge(request):
    refresh_stake()
    form = StartCharge(request.POST)

    if form.is_valid():
        stake_no = form.cleaned_data['stake_no']

        # retrieve records
        stall = Stall.objects.get(stake_no=stake_no)
        stake = Stake.objects.get(id=stake_no)
        try:
            rec = Record.objects.get(stall_no=stall.id, status=None)

            # check status
            if stall.status != 'hold':
                # print('submit_start_charge: Not yet Parked!')
                return False
            if stake.status != 'off':
                # print('submit_start_charge: Already Charging!')
                return False

            now = timezone.now()
            # update stake
            stake.status = 'on'
            stake.start_time = now
            stake.save()
            # update rec 
            rec.stake_no = stake.id
            rec.start_charge_time = now
            rec.save()

            return True

        except ObjectDoesNotExist:
            # print("submit_start_charge: find no corresponding record")
            return False

        except MultipleObjectsReturned:
            # print("submit_start_charge: find multiple corresponding record")
            return False

    return False


def submit_finish_charge(request):
    refresh_stake()
    form = FinishCharge(request.POST)

    if form.is_valid():
        stake_no = form.cleaned_data['stake_no']

        # retrieve records
        stall = Stall.objects.get(stake_no=stake_no)
        stake = Stake.objects.get(id=stake_no)

        try:
            rec = Record.objects.get(stall_no=stall.id, status=None)

            # check status
            if stall.status != 'hold':
                # print('submit_finish_charge: Not yet Parked!')
                return False, None
            if stake.status != 'on':
                # print('submit_finish_charge: Not Charging!')
                return False, None

            now = timezone.now()
            # update stake
            stake.status = 'off'
            stake.finish_time = now
            stake.save()
            # update rec 
            rec.finish_charge_time = now
            rec.save()
            # get charge time
            time = stake.finish_time - stake.start_time

            return True, time.total_seconds()

        except ObjectDoesNotExist:
            # print("submit_finish_charge: find no corresponding record")
            return False, None

        except MultipleObjectsReturned:
            # print("submit_finish_charge: find multiple corresponding record")
            return False, None

    return False, None


def get_stall_status():
    status = []
    stalls = Stall.objects.filter().count()

    for i in range(stalls):
        stall = Stall.objects.get(id=i + 1)
        if stall.status == 'free':
            status += [0]
        else:
            status += [1]

    # print(status)
    return status


def get_stake_status():
    refresh_stake()
    status = []
    stakes = Stake.objects.filter().count()

    for i in range(stakes):
        stake = Stake.objects.get(id=i + 1)
        if stake.status == 'off':
            status += [0]
        else:
            status += [1]

    # print(status)
    return status


def get_login_status(request):
    ip_no = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    try:
        user = User.objects.get(ip_no=ip_no)
        name = user.ph_no
        return 1, name
    except ObjectDoesNotExist:
        return 0, None


def get_user_status(request):
    ip_no = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    try:
        user = User.objects.get(ip_no=ip_no)
        ph_no = user.ph_no
        car_no = user.car_no
        try:
            stall = Stall.objects.get(car_no=car_no, ph_no=ph_no, status='hold')
            return 1
        except ObjectDoesNotExist:
            return 0

    except ObjectDoesNotExist:
        return 0


def submit_login(request):
    ip_no = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))

    form = Login(request.POST)
    # print(request.POST)
    # print(ip_no)

    if form.is_valid():
        ph_no = form.cleaned_data['phone_no']
        car_no = form.cleaned_data['car_no']

        try:
            user = User.objects.get(ip_no=ip_no)
            return False

        except ObjectDoesNotExist:
            user = User(ph_no=ph_no, car_no=car_no, ip_no=ip_no)
            user.save()
            return True

        # print("valid")

    return False


def submit_login2(request):
    ip_no = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))

    ph_no = request.POST['login']
    car_no = request.POST['plate-number']

    try:
        user = User.objects.get(ip_no=ip_no)
        return 0

    except ObjectDoesNotExist:
        user = User(ph_no=ph_no, car_no=car_no, ip_no=ip_no)

        user.save()
        return 1


def submit_logout(request):
    ip_no = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    # print(ip_no)

    try:
        user = User.objects.get(ip_no=ip_no)
        user.delete()
        return True

    except ObjectDoesNotExist:
        return False


def submit_logout2(request):
    ip_no = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    # print(ip_no)

    try:
        user = User.objects.get(ip_no=ip_no)
        user.delete()
        return 1

    except ObjectDoesNotExist:
        return 0


# 替换为你的 API Key 和 Secret Key
APP_ID = '32596722'
API_KEY = 'GYGdulO8clxfdviMYbKHMfVe'
SECRET_KEY = 'wnTf6a1Io9wX4S0WNZhIUdE5h7D6Ay6Q'

# 初始化 AipOcr 对象
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


@csrf_exempt
def recognize(request):
    if request.method == 'POST':
        file = request.FILES['image-upload']
        file_path = save_uploaded_file(file)
        result = recognize_text(file_path)
        plate_number = result['words_result'][0]['words'] if result.get('words_result') else ''
        print(plate_number)
        return JsonResponse({'plate_number': plate_number})


@csrf_exempt
def login(request):
    print(request)
    if request.method == 'POST':
        success = submit_login2(request)
        # 这里是你的登录/注册逻辑

        # ...
        return JsonResponse({'status': success})
    else:
        return render(request, 'login.html')


def logout(request):
    submit_logout2(request)
    login_status, login_name = get_login_status(request)
    return render(request, 'homepage.html', {'login_status': login_status, 'login_name': login_name})


def save_uploaded_file(f):
    file_name = f.name
    directory = os.path.join('static', 'car_num')
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path


def recognize_text(file_path):
    with open(file_path, 'rb') as fp:
        image = fp.read()
    result = client.basicGeneral(image)
    return result

def get_charge_status(request):
    refresh_stake()
    ip_no = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    try:
        user = User.objects.get(ip_no=ip_no)
        ph_no = user.ph_no
        car_no = user.car_no

        try:
            stall = Stall.objects.get(car_no=car_no, ph_no=ph_no, status='hold')
            try:
                stake = Stake.objects.get(id=stall.id, status='on')
                return 1
            except ObjectDoesNotExist:
                return 0

        except ObjectDoesNotExist:
            return 0

    except ObjectDoesNotExist:
        return 0

def get_park_status(request):
    ip_no = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    try:
        user = User.objects.get(ip_no=ip_no)
        ph_no = user.ph_no
        car_no = user.car_no
        try:
            stall = Stall.objects.get(car_no=car_no, ph_no=ph_no, status='hold')
            return 1
        except ObjectDoesNotExist:
            return 0

    except ObjectDoesNotExist:
        return 0

# must call before any page containing stake_status
def refresh_stake():
    on_stakes = Stake.objects.filter(status='on')
    now = timezone.now()
    for s in on_stakes: 
        start_time = s.start_time 
        limit_time = s.limit_time
        intval = int((now - start_time).total_seconds()) 
        if limit_time <= intval:
            s.status = 'off'
            s.finish_time = start_time +  timedelta(seconds=limit_time)
            s.save()
