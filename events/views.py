from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render,redirect         
from .forms import EventForm,CategoryForm,ParticipantForm   
from .models import Event,Participant ,Category ,RSVP
from django.utils import timezone
from django.db.models import Sum
from utils.auth import is_admin,is_organizer,is_participant
from django.contrib.auth.decorators import login_required,permission_required
# Create your views here.

def event_list(request):
    return render(request,"event-list.html")

def event_detail(request,id):
    event = Event.objects.select_related("category").get(id=id)
    print("event image url",event.event_img.url)
    return render(request,"event-detail.html",{"event":event})
    
def search(request):
    query = request.GET.get("q")
    if not query:
        return redirect("event-list")
    events = Event.objects.filter(Q(name__icontains=query) | Q(location__icontains=query)).select_related("category").prefetch_related("participant").all()
    return render(request,"search-result.html",{"events":events,"query":query})


# create event
@login_required(login_url="login")
@permission_required('events.add_event', login_url="no-permission")
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST,request.FILES)
        if form.is_valid(): 
            form.save()
            return redirect("event-detail",id=form.instance.id)
    else:
        form = EventForm()
    return render(request,"event-form.html",{"form": form, "title": "Create Event"})


# update event
@login_required(login_url="login")
@permission_required('events.change_event', login_url="no-permission")
def update_event(request,id):
    event = Event.objects.get(id=id)
    if not event:
        return redirect("event-list")
    form = EventForm(instance=event)
    if request.method == "POST":
        form_post = EventForm(request.POST,request.FILES,instance=event)   
        if form_post.is_valid():
            form_post.save()
            return redirect("event-detail",id=event.id)
    return render(request,"event-form.html",{"form":form,"title":"Update Event"})





# delete event
@login_required(login_url="login")
@permission_required('events.delete_event', login_url="no-permission")
def delete_event(request,id):
    event = Event.objects.get(id=id)
    if not event:
        return redirect("event-list")
    if request.method == "POST":
        event.delete()
        return redirect("event-list")
    return render(request,"event-delete.html",{"event":event})



# create category
@login_required(login_url="login")
@permission_required('events.add_category', login_url="no-permission")
def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect("category-list")
    else:
        form = CategoryForm()
    return render(request,"category-form.html",{"form":  form, "title": "Create Category"})

# update category
@login_required(login_url="login")
@permission_required('events.view_category', login_url="no-permission")
def category_list_view(request):
    categories = Category.objects.all()
    return render(request,"category-list.html",{"categories":categories})

@login_required(login_url="login")
@permission_required('events.change_category', login_url="no-permission")
def update_category(request,id):
    category = Category.objects.get(id=id)
    if not category:
        return redirect("category-list")
    form = CategoryForm(instance=category)
    if request.method == "POST":
        form_post = CategoryForm(request.POST,instance=category)   
        if form_post.is_valid():
            form_post.save()
            return redirect("category-list")
    return render(request,"category-form.html",{"form":form,"title":"Update Category"})


# delete category
@login_required(login_url="login")
@permission_required('events.delete_category', login_url="no-permission")
def delete_category(request,id):
    category = Category.objects.get(id=id)
    if not category:
        return redirect("category-list")
    if request.method == "POST":
        category.delete()
        return redirect("category-list")
    return render(request,"category-delete.html",{"category":category})


# create participant
@login_required(login_url="login")
@permission_required('events.add_participant', login_url="no-permission")
def create_participant(request):
    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect("participant-list")
    else:
        form = ParticipantForm()
    return render(request,"participant-form.html",{"form":form,"title":"Create Participant"})
    
# update participant
@login_required(login_url="login")
@permission_required('events.change_participant', login_url="no-permission")
def update_participant(request,id):
    participant = Participant.objects.get(id=id)
    if not participant:
        return redirect("participant-list")
    form = ParticipantForm(instance=participant)
    if request.method == "POST":
        form_post = ParticipantForm(request.POST,instance=participant)   
        if form_post.is_valid():
            form_post.save()
            return redirect("participant-list")
    return render(request,"participant-form.html",{"form":form,"title":"Update Participant"})

@login_required(login_url="login")
@permission_required('events.delete_participant', login_url="no-permission")
def delete_participant(request,id):
    participant = Participant.objects.get(id=id)
    if not participant:
        return redirect("participant-list")
    if request.method == "POST":
        participant.delete()
        return redirect("participant-list")
    return render(request,"participant-delete.html",{"participant":participant,"title":"Delete Participant"})








# rsvp user
@login_required(login_url="login")
def rsvp_user(request,id):
    event = Event.objects.get(id=id)
    expired = event.date < timezone.now().date()
    print("expired",expired)
    if not event:
        return redirect("event-list")
    try:
        user=request.user
        if request.method == "POST":
            if expired:
                messages.error(request,"Sorry! Event date expired")
            # check if user is not admin organizer or already registerd
            elif is_admin(request.user) or is_organizer(request.user):
                messages.error(request,"You are not allowed to RSVP")
            elif RSVP.objects.filter(event=event,participant=user).exists():
                messages.error(request,"You have already RSVP'd to this event")
            else:
                RSVP.objects.create(event=event,participant=user,rsvp=True)
                messages.success(request,"RSVP successfully added")
    except Exception as e:  
        messages.error(request,"Failed to RSVP")
    return render(request,"rsvp-form.html",{"event":event,"title":"RSVP","expired":expired})

@login_required(login_url="login")
def cancel_rsvp(request,id):
    event = Event.objects.get(id=id)
    expired = event.date < timezone.now().date()
    if not event:
        return redirect("event-list")
    try:
        user=request.user
        if request.method == "POST":
            if expired:
                messages.error(request,"Sorry! Event date expired")
            # check if user is not admin organizer or already registerd
            elif is_admin(request.user) or is_organizer(request.user):
                messages.error(request,"You are not allowed to cancel RSVP")
            elif RSVP.objects.filter(event=event,participant=user).exists():
                RSVP.objects.filter(event=event,participant=user).delete()
                messages.success(request,"RSVP successfully cancelled")
            else:
                messages.error(request,"You have not RSVP'd to this event")
    except Exception as e:  
        messages.error(request,"Failed to cancel RSVP")
    return render(request,"canceal-rsvp.html",{"event":event,"title":"Cancel RSVP","expired":expired})