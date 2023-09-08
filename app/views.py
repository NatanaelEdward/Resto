from django.shortcuts import render
import json
# Create your views here.
def Login(request):
    return render(request, 'Login.html')

def index(request):
    return render(request, 'index.html')