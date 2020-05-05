from django.shortcuts import render
from django.http import HttpResponse
from .optimizer import get_nutrion

def index(request):
    return render(request, 'index.html')

def result(request):
    result_list,finish_food,required_list = get_nutrion(request.POST['eat1'],request.POST['eat2'],request.POST['eat3'],request.POST['eat4'])
    contents = {
        'result_list': result_list,
        'finish_food': finish_food,
        'required_list': required_list,
    }
    return render(request, 'result.html', contents)
