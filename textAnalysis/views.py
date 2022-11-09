import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def text_analysis(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        return JsonResponse({"message": data}, status=200)
    else:
        return JsonResponse({"message": "error"}, status=400)