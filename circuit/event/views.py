from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from event.models import Event, Category, UserActivity, Bookmark, User, Review, Notification
from math import ceil
from datetime import date
import datetime
from urllib.parse import urlsplit, parse_qs
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from fcm_django.models import FCMDevice
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from django.conf import settings
from django.templatetags.static import static
from django.db.models.expressions import RawSQL
from celery import shared_task
from django.core import serializers
from django.core.paginator import Paginator, InvalidPage
from django.template.response import TemplateResponse
import os
import re

module_dir = os.path.dirname('static/')
file_path = os.path.join(module_dir, 'js/serviceAccountKey.json')
cred = credentials.Certificate(file_path)
default_app = firebase_admin.initialize_app(cred)
'''
Description:This function return the home page.
Args:
     **keyarg
Returns:
        Context Data 
Author: Rafi
Date: 2020-03-25
'''
def index(request):
	context = {}
	print(context)
	category = Category.objects.all()
	current_user_id = request.user.id
	params = {'category': category,}
	return TemplateResponse(request, 'events/home.html', context=context)

'''
Description:This function return the html page with filter event context data.
Args:
     **keyarg
Returns:
        Context Data 
Author: Rafi
Date: 2020-03-26
'''
def search_event(request):
	if 'category' in request.GET:
		category = request.GET.get('category')
		event_name = request.GET.get('event')
		events = Event.objects.filter(event_name__icontains=event_name)
		if category:
		    events = events.filter(category = category)
		page = request.GET.get('page', 1)
		paginator = Paginator(events, 2)
		try:
			events = paginator.page(page)
		except PageNotAnInteger:
			events = paginator.page(1)
		except EmptyPage:
			events = paginator.page(paginator.num_pages)
		if len(events) == 0:
			params = {'msg': "Please make sure to enter relevant search query"}
		params = {'events': events}
	return render(request, 'events/listing.html', params)



def get_locations_nearby_coords(latitude, longitude, max_distance=None):
    """
    Return objects sorted by distance to specified coordinates
    which distance is less than max_distance given in kilometers
    """
    # Great circle distance formula
    gcd_formula = "6371 * acos(least(greatest(\
    cos(radians(%s)) * cos(radians(latitude)) \
    * cos(radians(longitude) - radians(%s)) + \
    sin(radians(%s)) * sin(radians(latitude)) \
    , -1), 1))"
    distance_raw_sql = RawSQL(
        gcd_formula,
        (latitude, longitude, latitude)
    )
    qs = Event.objects.all() \
    .annotate(distance=distance_raw_sql)\
    .order_by('distance')
    if max_distance is not None:
        qs = qs.filter(distance__lt=max_distance)
    return qs

'''
Description:This function track user activity and store user selected event.
Args:
    user_id
Returns:
        Context Data 
Author: Rafi
Date: 2020-03-26
'''



@csrf_exempt
def user_activity(request):
    if request.method=="POST":
        event_name = request.POST.get('event_name')
        event_type = request.POST.get('event_type')
        event_url = '123'
        created_at =date.today()
        try:
        	username = request.user.username
        	email = request.user.email
        	activity = UserActivity(user_name=username, email=email, event_name=event_name, event_type=event_type, event_url=event_url, created_at=created_at)
        	activity.save()
        	response = json.dumps(updates, default=str)
        	return HttpResponse(response)
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'events/listing.html')




@csrf_exempt
def save_clientDevice(request):
	if request.method=="POST":
		registration_token  = request.POST.get('registration_id')
		name = request.user.username
		user_id = request.user.id
		date_created = date.today()
		try:
			client_devic = FCMDevice(name = name, active = 1, date_created = date_created, user_id=user_id, device_id = 1, registration_id= registration_token, type='Web')
			updates = client_devic.save()
			response = json.dumps(updates, default=str)
			return HttpResponse(response)
		except Exception as e:
			return HttpResponse('{}')





@shared_task
def push_notification(user_id, title, description):
	devices = FCMDevice.objects.all()
	title = 'New Notification fired'
	description = 'I just fired a new notification'
	data = {
			"title": title,
			"body": description
			}

	created_at = datetime.datetime.now()
	activity = Notification(user_id=user_id, title=title, description=description, is_unread=True, created_at=created_at)
	updates = activity.save()
	result =''
	for device in devices:
			registration_token = settings.FCM_DJANGO_SETTINGS['FCM_SERVER_KEY']
			message = messaging.Message(data, token=device.registration_id)
			response = messaging.send(message)
			result = 'Successfully sent message:'+response





def user_profile(request):
	user_id = request.user.id
	# import pdb; pdb.set_trace()
	bookmarks =Event.objects.filter(bookmark__user=1).all()

	# review = Review.objects.filter(user_id=user_id).select_related("event").all()
	data = {'bookmarks':bookmarks}
	return render(request, 'events/profile.html', data)




@csrf_exempt
def event_bookmark(request):
    if request.method=="POST":
        event_id = request.POST.get('event_id')
        event_name = request.POST.get('event_name')
        created_at = date.today()
        push_notification(1, "test", "test")
        try:
        	user_id = request.user.id
        	activity = Bookmark(user_id=user_id, event_id=event_id, event_name=event_name, created_at=created_at)
        	updates = activity.save()
        	response = json.dumps(updates, default=str)
        	return HttpResponse(response)
        except Exception as e:
            return HttpResponse('{}')




def event_review(request):
	if request.method=="POST":
		event_id = request.POST.get('event_id')
		rating = request.POST.get('rating')
		comment = request.POST.get('comment')
		created_at = date.today()
		user_id = request.user.id
		try:
			review = Review(comment=comment, rating=rating, pub_date=created_at, event_id=event_id, user_id=user_id)
			updates = review.save()
			response = json.dumps(updates, default=str)
			return HttpResponse(response)
		except Exception as e:
			return HttpResponse('{}')





# def get_notifictaion(request):
# 	# current_user_id = request.user.id
# 	# notification = Notification.objects.filter(user_id=current_user_id).all()
# 	# page = request.GET.get('page', 1)
# 	# paginator = Paginator(notification, 5)
# 	# try:
# 	# 	notification = paginator.page(page)
# 	# except PageNotAnInteger:
# 	# 	notification = paginator.page(1)
# 	# except EmptyPage:
# 	# 	notification = paginator.page(paginator.num_pages)
# 	# return render(request, 'events/notification.html', {'notifications': notification})

def notifictaion_pagination_index(request):
	current_user_id = request.user.id
	object_list = Notification.objects.filter(user_id=current_user_id).all()
	paginator = Paginator(object_list, 10)
	page_obj = paginator.page(1)
	context = {
				"object_list": page_obj.object_list,
				"page": page_obj,
			}
	template = 'events/notification.html'
	return render(request, template, context)

def get_latest_notifictaion(request):
	if request.method == "GET":
		current_user_id = request.user.id
		notification = Notification.objects.filter(user_id=current_user_id).all().order_by('created_at')[0:5]
		data = serializers.serialize('json', list(notification))
		return HttpResponse(data)


def notifictaion_detail(request, notification_id):
	try:
		detail_notification = Notification.objects.get(id=notification_id)
		Notification.objects.filter(id=notification_id).update(is_unread=False)
	except Notification.DoesNotExist:
		raise Http404("Notification does not exist")
	return render(request, 'events/notification_detail.html', data)


@csrf_exempt
def notifictaion_pagination_json(request):
	page = request.GET.get('page')
	current_user_id = request.user.id
	object_list = Notification.objects.filter(user_id=current_user_id).all()
	paginator = Paginator(object_list, 10)
	try:
		notification = paginator.page(page)
	except InvalidPage:
		raise Http404
	data = serializers.serialize('json', notification)
	return HttpResponse(data)
