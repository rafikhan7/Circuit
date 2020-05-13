from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class Category(models.Model):
	category_name = models.CharField(max_length=200)
	slug = models.CharField(max_length=200)
	created_at = models.DateField()
	updated_at = models.DateField()

	def __str__(self):
		return self.category_name


class Event(models.Model):
    event_name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    event_type = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    event_location = models.CharField(max_length=50, default="")
    description = models.TextField()
    from_date = models.DateField()
    to_date = models.DateField()
    city  = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=10)
    status = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    created_at = models.DateField()
    updated_at = models.DateField()
    partner_tag = models.CharField(max_length = 200)
    partner_url = models.CharField(max_length = 200)
    image = models.ImageField(upload_to = 'event/images', default="")

    def __str__(self):
        return self.event_name

class UserActivity(models.Model):
    user_name = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200)
    event_name = models.CharField(max_length = 200)
    event_type = models.CharField(max_length = 200)
    event_url = models.CharField(max_length = 200)
    created_at = models.DateField()

    def __str__(self):
        return self.event_name

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    event_name = models.CharField(max_length = 200)
    created_at = models.DateField()

    def __str__(self):
        return str(self.event_name)

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.TextField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)
    pub_date = models.DateField('date published')
    
    def __str__(self):
        return str(self.event)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 250)
    description  = models.TextField()
    is_unread = models.BooleanField(default= False)
    created_at =models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.title)


