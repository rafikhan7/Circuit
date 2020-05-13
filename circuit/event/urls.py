from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [

    path("", views.index, name="index"),
    path("search_event/", views.search_event, name="search_event"),
    path("user_activity/", views.user_activity, name="user_activity"),
    path("user_profile/", views.user_profile, name="user_profile"),
    path("push_notification/", views.push_notification, name="push_notification"),
    path("save_clientDevice/", views.save_clientDevice, name="save_clientDevice"),
    path("event_bookmark/", views.event_bookmark, name="event_bookmark"),
    path("search_event/review/", views.event_review, name="event_review"),
    path("get_latest_notifictaion/", views.get_latest_notifictaion, name="get_latest_notifictaion"),
    #path("notifictaion/", views.get_notifictaion, name="get_notifictaion")
    path("notifictaion/", views.notifictaion_pagination_index, name="notifictaion_pagination_index"),
    path("notification_paginate/", views.notifictaion_pagination_json, name="notifictaion_pagination_json")
]