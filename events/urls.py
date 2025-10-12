from os import name
from django.urls import path

from events.views import event_detail,event_list,search,create_event,create_category,update_event,delete_event,update_category,delete_category,update_participant,delete_participant,rsvp_user,category_list_view,cancel_rsvp

urlpatterns = [
    path("event-detail/<int:id>/",event_detail,name="event-detail"),
    path("search/",search,name="search"),

    # event section
    path("create-event/",create_event,name="create-event"),
    path("update-event/<int:id>/",update_event,name="update-event"),
    path("delete-event/<int:id>/",delete_event,name="delete-event"),
    path("rsvp/<int:id>/",rsvp_user,name="rsvp"),
    path("cancel-rsvp/<int:id>/",cancel_rsvp,name="cancel-rsvp"),

    # category section
    path("categories/",category_list_view,name="category-list"),
    path("create-category/",create_category,name="create-category"),
    path("update-category/<int:id>/",update_category,name="update-category"),
    path("delete-category/<int:id>/",delete_category,name="delete-category"),

]
