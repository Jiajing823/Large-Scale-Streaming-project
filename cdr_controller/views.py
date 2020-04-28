import json
import logging
import threading
import time

from django.http import HttpResponse
from django.shortcuts import render
from django_redis import get_redis_connection

from . import data_generator

data_generator_exit_flag = 0
logger = logging.getLogger(__name__)


class dataGenThread(threading.Thread):
    def __init__(self, pick_type_distribution, rate_type_distribution,
                 pick_call_distribution, delta_distribution,
                 rate_place_distribution):
        threading.Thread.__init__(self)
        self.pick_type_distribution = pick_type_distribution
        self.rate_type_distribution = rate_type_distribution
        self.pick_call_distribution = pick_call_distribution
        self.delta_distribution = delta_distribution
        self.rate_place_distribution = rate_place_distribution

    def run(self):
        global data_generator_exit_flag
        while (1):
            if data_generator_exit_flag:
                exit(0)
            data_generator.people(
                pick_type_distribution=self.pick_type_distribution,
                rate_type_distribution=self.rate_type_distribution,
                pick_call_distribution=self.pick_call_distribution,
                delta_distribution=self.delta_distribution,
                rate_place_distribution=self.rate_place_distribution)


thread1 = dataGenThread(pick_type_distribution='default',
                        rate_type_distribution=0.3,
                        pick_call_distribution='default',
                        delta_distribution='default',
                        rate_place_distribution=0.7)


def hello_world(request):
    return render(request, 'hello_world.html', {})


def homepage(request):
    return render(request, 'homepage.html', {})


def index(request):
    global thread1
    if not thread1.isAlive():
        return render(request, 'homepage.html', {})
    return render(request, 'index.html', {})


def workload_generator(request):
    global thread1
    if not thread1.isAlive():
        return render(request, 'homepage.html', {})
    if request.method == 'POST':
        data_gen_stop(request)
        pick_type_distribution = request.POST['pick_type_distribution']
        rate_type_distribution = float(request.POST['rate_type_distribution'])
        pick_call_distribution = request.POST['pick_call_distribution']
        delta_distribution = request.POST['delta_distribution']
        rate_place_distribution = float(request.POST['rate_place_distribution'])

        logger.info("Start updating workload generator ... ")
        thread1 = dataGenThread(
            pick_type_distribution=pick_type_distribution,
            rate_type_distribution=rate_type_distribution,
            pick_call_distribution=pick_call_distribution,
            delta_distribution=delta_distribution,
            rate_place_distribution=rate_place_distribution)
        thread1.start()
        logger.info("Update workload generator successfully! ")
    elif request.method == 'GET':
        pass
    return render(request, 'workload_generator.html', {})


def page1_view(request):
    return HttpResponse("page1")


def page2_view(request):
    return HttpResponse("page2")


data = {"label": ["0:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00",
                  "7:00", "8:00", "9:00", "10:00", "11:00", "12:00"],
        "data": [1345, 1234, 433, 1234, 1432, 433, 1234, 1432, 433, 1234,
                 1432, 2193, 900]}

data2 = {"label": ['private',
                   'business',
                   'housing (including rental)',
                   'legal agency',
                   'school',
                   'hospital (including health care)',
                   'housekeeping and property management',
                   'clinic (including dentist)',
                   'financial agency',
                   'emergency',
                   'job',
                   'none',
                   'traveling',
                   'food (including takeaway)',
                   'dress code (booking and buying)',
                   'extracurricular training camp',
                   'banking'],
         "data": [19178, 3958, 3881, 3869, 3857, 3847, 3842, 3842, 3831, 3823,
                  3810, 3786, 3776, 3775, 3771, 3760, 3743]}

data3 = {
    "label": ['SC', 'ER', 'IO', 'TZ', 'CH', 'RU', 'CN', 'BW', 'CV', 'NG', 'AC',
              'NO', 'CI', 'MZ', 'NE', 'ZW', 'KE', 'SS', 'LS', 'FR'],
    "data": [235, 264, 255, 248, 237, 255, 216, 247, 254, 241, 235, 245, 239,
             221, 247, 247, 243, 227, 185, 221]}


# custom templates
def custom_template0(request):
    return render(request, 'filters/template_00.html', data)


def custom_template1(request):
    return render(request, 'filters/template_01.html', data2)

def custom_template3(request):
    return render(request, 'filters/template_03.html', data3)

# data source
def data_template0(request):
    return HttpResponse(json.dumps(data))


def data_template1(request):
    return HttpResponse(json.dumps(data2))

def data_template3(request):
    return HttpResponse(json.dumps(data3))

def show_info(request):
    html = '<div>' + "request method: " + request.method + '</div>'
    html += '<div>' + "request.GET: " + str(dict(request.GET)) + '</div>'
    html += '<div>' + "request.POST: " + str(dict(request.POST)) + '</div>'
    html += '<div>' + "request.COOKIES: " + str(request.COOKIES) + '</div>'
    html += '<div>' + "request.scheme: " + request.scheme + '</div>'
    html += '<div>' + "request.META['REMOTE_ADDR']: " + str(
        request.META['REMOTE_ADDR']) + '</div>'
    html += '<div>' + "request.META:" + str(request.META) + '</div>'
    return HttpResponse(html)


def data_gen_test(request):
    if request.method == 'POST':
        pick_type_distribution = request.POST['pick_type_distribution']
        rate_type_distribution = request.POST['rate_type_distribution']
        pick_call_distribution = request.POST['pick_call_distribution']
        delta_distribution = request.POST['delta_distribution']
        rate_place_distribution = request.POST['rate_place_distribution']
        p1 = data_generator.people(
            pick_type_distribution=pick_type_distribution,
            rate_type_distribution=rate_type_distribution,
            pick_call_distribution=pick_call_distribution,
            delta_distribution=delta_distribution,
            rate_place_distribution=rate_place_distribution)
        return HttpResponse('data_generator starts by post')
    elif request.method == 'GET':
        pick_type_distribution = request.GET['pick_type_distribution']
        rate_type_distribution = request.GET['rate_type_distribution']
        pick_call_distribution = request.GET['pick_call_distribution']
        delta_distribution = request.GET['delta_distribution']
        rate_place_distribution = request.GET['rate_place_distribution']
        p1 = data_generator.people(
            pick_type_distribution=pick_type_distribution,
            rate_type_distribution=rate_type_distribution,
            pick_call_distribution=pick_call_distribution,
            delta_distribution=delta_distribution,
            rate_place_distribution=rate_place_distribution)
        return HttpResponse('data_generator starts by get')
    else:
        return HttpResponse('wrong request method')


def data_gen_test_get_res(request):
    conn = get_redis_connection('default')
    res = conn.get('3aad3ac0-8731-11ea-9a51-14abc512967e')
    return HttpResponse(res)


def data_gen_start(request):
    global data_generator_exit_flag
    global thread1
    thread1 = dataGenThread(pick_type_distribution='default',
                            rate_type_distribution=0.3,
                            pick_call_distribution='default',
                            delta_distribution='default',
                            rate_place_distribution=0.7)
    data_generator_exit_flag = 0
    thread1.start()
    logger.info("Start data generator")
    return HttpResponse('Success')


def data_gen_stop(request):
    global data_generator_exit_flag
    global thread1
    data_generator_exit_flag = 1
    while (thread1.isAlive()):
        time.sleep(0.01)
        print('thread alive')
    logger.info('thread killed')
    return HttpResponse('Try to stop')
