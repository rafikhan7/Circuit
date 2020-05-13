from django.http import HttpResponse
from event.models import Notification
import json
class NotificationMiddleware(object):
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		current_user_id = request.user.id
		notifications = Notification.objects.filter(user_id=current_user_id, is_unread=True).all()
		request.notifications = notifications.count()
		# context = json.dumps({
		# 		'notifications': notifications.count()
		# 		})
		response = self.get_response(request)
		return response