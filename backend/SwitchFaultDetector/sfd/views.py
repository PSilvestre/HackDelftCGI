from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import SwitchModel
from .serializers import SwitchModelSerializer
from rest_framework import viewsets
from django.http import HttpResponse
import dateutil.parser
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np

@csrf_exempt
def get_data(request):
    data = SwitchModel.objects.all()
    if request.method == 'GET':
        serializer = SwitchModelSerializer(data, many=True)
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def getimage(request):
    path = str(request.GET.get('path'))
    with open(path, 'rb') as f:
        blob = f.read()

        return HttpResponse(blob, content_type="image/png")


@csrf_exempt
def getarrow(request):
    data = list(SwitchModel.objects.all())
    dates = [x.timestamp for x in data]
    lowest_ts = min(dates)
    highest_ts = max(dates)

    plt.figure()
    plt.hlines(1,lowest_ts,highest_ts)
    plt.eventplot(dates, orientation='horizontal', colors='r')
    plt.axis('off')
    plt.savefig("time.png")
    plt.close()
    with open("time.png", 'rb') as f:
        blob = f.read()

        return HttpResponse(blob, content_type="image/png")


class SwitchViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SwitchModel.objects.all()
    serializer_class = SwitchModelSerializer


def get_switch(request, s_id):
    switch_values = SwitchModel.objects.filter(switch_id=s_id)
    template = loader.get_template('sfd/switch.html')
    context = {
        'switch_values': switch_values,
    }
    return HttpResponse(template.render(context, request))
