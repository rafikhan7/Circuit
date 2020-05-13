from django.http import HttpResponse
from django.shortcuts import render
from event.models import Event, Category
from math import ceil
import json

def index(request):
	# products = Product.objects.all() 
	# params = {'product': products}
	return render(request, 'events/home.html')