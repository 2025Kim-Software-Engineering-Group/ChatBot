
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from ChatBot.MessageHandle.handle import handleMessage
@csrf_exempt
def reportMessage(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        handleMessage(raw_data)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)