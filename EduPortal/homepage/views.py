from django.shortcuts import render
from django.http import JsonResponse
import requests

def index(request):
    return render(request, 'homepage/index.html')

def register(request):
    return render(request, 'homepage/register.html')

def my_api(request):
    data = {
        'message': 'Hello, this is your API response!',
        'items': ['Item 1', 'Item 2', 'Item 3']
    }
    return JsonResponse(data)

def api_data(request):
    return render(request, 'homepage/api_data.html')
    # response = requests.get('http://127.0.0.1:8000/api/')  # URL of the API endpoint
    # data = response.json()
    # return render(request, 'homepage/api_data.html', {'data': data})