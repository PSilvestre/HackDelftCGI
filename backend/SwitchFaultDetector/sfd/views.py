from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import SwitchModel
from .serializers import SwitchModelSerializer
from rest_framework import viewsets


@csrf_exempt
def get_data(request):
    data = SwitchModel.objects.all()
    if request.method == 'GET':
        serializer = SwitchModelSerializer(data, many=True)
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False)

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