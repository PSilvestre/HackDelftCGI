from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ExampleModel
from .serializers import ExampleModelSerializer


@csrf_exempt
def get_data(request):
    data = ExampleModel.objects.all()
    if request.method == 'GET':
        serializer = ExampleModelSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
