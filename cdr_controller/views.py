import logging
import threading

from django.http import HttpResponse
from django.shortcuts import render

from cdr_controller.filters.template_0 import template_0_main
from cdr_controller.filters.template_01 import template_1_main
from cdr_controller.filters.template_02 import template_2_main
from cdr_controller.filters.template_03 import template_3_main
from cdr_controller.filters.template_05 import template_05_main
from . import data_generator
from .get_result import *
from .queue_manage import *

data_generator_exit_flag = 0
logger = logging.getLogger(__name__)
logging.getLogger("py4j").setLevel(logging.ERROR)


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
        logging.info("Compute data generator data")
        global data_generator_exit_flag
        while (1):
            time.sleep(0.1)
            if data_generator_exit_flag:
                exit(0)

            logging.info("get data from data generator")
            data_generator.people(
                pick_type_distribution=self.pick_type_distribution,
                rate_type_distribution=self.rate_type_distribution,
                pick_call_distribution=self.pick_call_distribution,
                delta_distribution=self.delta_distribution,
                rate_place_distribution=self.rate_place_distribution)


thread0 = dataGenThread(pick_type_distribution='default',
                        rate_type_distribution=0.3,
                        pick_call_distribution='default',
                        delta_distribution='default',
                        rate_place_distribution=0.7)

qm0 = Process(target=queueStarter, args=(9000, "ID_0"))
qm1 = Process(target=queueStarter, args=(9001, "ID_01"))
qm2 = Process(target=queueStarter, args=(9002, "ID_02"))
qm3 = Process(target=queueStarter, args=(9003, "ID_03"))
qm5 = Process(target=queueStarter, args=(9005, "ID_05"))

qm0.start()
qm1.start()
qm2.start()
qm3.start()
qm5.start()

p0 = Process(target=template_0_main)
p1 = Process(target=template_1_main)
p2 = Process(target=template_2_main)
p3 = Process(target=template_3_main)
p5 = Process(target=template_05_main)
# template_pool = [p0, p1, p3, p5]
# template_pool = [p1]

p0.start()
p1.start()
p2.start()
p3.start()
p5.start()


def hello_world(request):
    return render(request, 'hello_world.html', {})


def homepage(request):
    return render(request, 'homepage.html', {})


def index(request):
    data_tmp0 = get_tmp0_data()
    data_tmp1 = get_tmp1_data()
    data_tmp3 = get_tmp3_data()
    data = {"chartBarHours": data_tmp0,
            "chartPieType": data_tmp1,
            "chartBarInternational": data_tmp3}
    return render(request, 'index.html', data)


def workload_generator(request):
    if request.method == 'POST':
        data_gen_stop(request)
        pick_type_distribution = request.POST['pick_type_distribution']
        rate_type_distribution = float(request.POST['rate_type_distribution'])
        pick_call_distribution = request.POST['pick_call_distribution']
        delta_distribution = request.POST['delta_distribution']
        rate_place_distribution = float(request.POST['rate_place_distribution'])

        logger.info("Start updating workload generator ... ")
        thread0 = dataGenThread(
            pick_type_distribution=pick_type_distribution,
            rate_type_distribution=rate_type_distribution,
            pick_call_distribution=pick_call_distribution,
            delta_distribution=delta_distribution,
            rate_place_distribution=rate_place_distribution)
        thread0.start()

        time.sleep(0.5)
        logger.info("Update workload generator successfully! ")
        data_tmp0 = get_tmp0_data()
        data_tmp1 = get_tmp1_data()
        data_tmp3 = get_tmp3_data()
        data = {"chartBarHours": data_tmp0,
                "chartPieType": data_tmp1,
                "chartBarInternational": data_tmp3}
        return render(request, 'index.html', data)
    elif request.method == 'GET':
        pass
    return render(request, 'workload_generator.html', {})


def plan_platform(request):
    if request.method == "POST":

        form_people_id = request.POST.get("form_people_id", "")
        form_tag = request.POST.getlist("form_tag", None)
        form_day = request.POST.get("form_day", "")
        form_clock = request.POST.get("form_clock", "")
        form_data = get_form_data(people_id=form_people_id, tags=form_tag,
                                  day=form_day, clock=form_clock)
        return render(request, "plan_platform.html",
                      {"datasetTable": form_data})
    return render(request, "plan_platform.html",
                  {"datasetTable": get_form_data()})


def page1_view(request):
    return HttpResponse("page1")


def page2_view(request):
    return HttpResponse("page2")


# custom templates
def custom_template0(request):
    data_tmp0 = get_tmp0_data()
    return render(request, 'filters/template_00.html', data_tmp0)


def custom_template1(request):
    data_tmp1 = get_tmp1_data()
    return render(request, 'filters/template_01.html', data_tmp1)


def custom_template3(request):
    data_tmp3 = get_tmp3_data()
    return render(request, 'filters/template_03.html', data_tmp3)


# data source
def data_template0(request):
    data_tmp0 = get_tmp0_data()
    return HttpResponse(json.dumps(data_tmp0))


def data_template1(request):
    data_tmp1 = get_tmp1_data()
    return HttpResponse(json.dumps(data_tmp1))


def data_template3(request):
    data_tmp3 = get_tmp3_data()
    return HttpResponse(json.dumps(data_tmp3))


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


def data_gen_start(request):
    global data_generator_exit_flag
    global thread0
    thread0 = dataGenThread(pick_type_distribution='default',
                            rate_type_distribution=0.3,
                            pick_call_distribution='default',
                            delta_distribution='default',
                            rate_place_distribution=0.7)
    data_generator_exit_flag = 0
    thread0.start()
    logger.info("Start data generator")

    return HttpResponse('Success')


def data_gen_stop(request):
    global data_generator_exit_flag
    global thread0, p0, p1, p3, p5, p2
    # global thread0, p0

    # restart template process
    p0.terminate()
    p1.terminate()
    p2.terminate()
    p3.terminate()
    p5.terminate()
    # del p0, p3, p5
    p0 = Process(target=template_0_main)
    p1 = Process(target=template_1_main)
    p2 = Process(target=template_2_main)
    p3 = Process(target=template_3_main)
    p5 = Process(target=template_05_main)

    p0.start()
    p1.start()
    p2.start()
    p3.start()
    p5.start()

    data_generator_exit_flag = 1
    while (thread0.isAlive()):
        time.sleep(0.01)
        print('thread alive')
    data_generator_exit_flag = 0
    logger.info('thread killed')
    return HttpResponse('Try to stop')
