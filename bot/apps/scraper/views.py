from django.shortcuts import render
from .models import *

def test(request):
    channel = Channel.objects.get(id=1)
    print(channel.get_profiles())
    return render(request, 'base.html')
