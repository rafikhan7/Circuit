from django.contrib import admin
from .models import Event, Category, UserActivity, Bookmark, Review, Notification

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'category','event_type', 'cost', 'description', 'from_date', 'to_date', 'event_location', 'image')
    list_filter = ("event_name",)
    search_fields = ['event_name', 'category', '']
    prepopulated_fields = {'event_name': ('category',)}

  
admin.site.register(Event, EventAdmin)
admin.site.register(Category)
admin.site.register(UserActivity)
admin.site.register(Bookmark)
admin.site.register(Review)
admin.site.register(Notification)
