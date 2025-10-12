from django.shortcuts import render
from events.models import Category,Participant,Event
from django.shortcuts import redirect
from utils.auth import is_admin,is_organizer,is_participant
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views import View
from django.views.generic import TemplateView
from utils.auth import is_admin,is_organizer,is_participant

# def home_view(request):
#     events = Event.objects.prefetch_related("participant").select_related("category").all()
#     user_permitted = False
#     if request.user.is_authenticated:
#         if is_admin(request.user):
#             user_permitted = True
#     return render(request, "home.html", {"events": events,"title":"Events","user_permitted":user_permitted})
class HomeView(View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        events = Event.objects.prefetch_related("participant").select_related("category").all()
        user_permitted = request.user.is_authenticated and is_admin(request.user)
        context = {
            "events": events,
            "title": "Events",
            "user_permitted": user_permitted
        }
        return render(request, self.template_name, context)


# def event_list_view(request):
#     events = Event.objects.prefetch_related("participant").select_related("category").all()
#     user_permitted = False
#     if request.user.is_authenticated:
#         if is_admin(request.user):
#             user_permitted = True
#     return render(request, "events.html", {"events": events,"title":"All Events","user_permitted":user_permitted})

class EventListView(View):
    template_name = "events.html"

    def get(self, request, *args, **kwargs):
        events = Event.objects.prefetch_related("participant").select_related("category").all()
        user_permitted = request.user.is_authenticated and is_admin(request.user)
        context = {
            "events": events,
            "title": "All Events",
            "user_permitted": user_permitted
        }
        return render(request, self.template_name, context)
# def search_view(request):
#     return render(request, "search.html")
class SearchView(TemplateView):
    template_name = "search.html"

# def no_permission_view(request):
#     return render(request, "no-permission.html")

class NoPermissionView(TemplateView):
    template_name = "no-permission.html"






@login_required(login_url="login")
@permission_required('events.view_category', login_url="no-permission")
def category_list_view(request):
    categories = Category.objects.all() 
    return render(request, "categories.html", {"categories": categories})

@login_required(login_url="login")
@permission_required('events.view_participant', login_url="no-permission")
def participant_list_view(request):
    participants = Participant.objects.all()
    return render(request, "participants.html", {"participants": participants})

@login_required(login_url="login")
@permission_required('events.view_event', login_url="no-permission")
def dashboard_view(request):
    print(request.user.groups.all())
    if request.user.is_authenticated:
        if is_admin(request.user):
            return redirect("admin-dashboard")
        elif is_organizer(request.user):
            return redirect("organizer-dashboard")
        elif is_participant(request.user):
            return redirect("participant-dashboard")
        else:
            return redirect("home")