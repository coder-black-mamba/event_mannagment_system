from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.http import HttpResponse
from users.forms import UserRegistrationForm,UserLoginForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import logout
from events.models import Event , RSVP
from django.contrib.auth.models import Group, Permission
from users.forms import AssignRoleForm, CreateGroupForm,EditProfileForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required,permission_required
from utils.auth import is_admin,is_organizer,is_participant
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from users.forms import EditProfileForm
from users.models import CustomUser
from users.forms import CustomPasswordChangeForm ,CustomPasswordResetForm , CustomPasswordResetConfirmForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView as DjangoPasswordChangeDoneView
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.views import PasswordResetView ,PasswordResetConfirmView,PasswordResetDoneView ,PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

# Create your views here.
def register(request):
    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request, "Confirmation Mail Sent ! Please Check Your Email")
            return redirect("login")
    return render(request,"register.html",{"form":form})
    

# def login_user(request):
#     form = UserLoginForm()
#     if request.method == "POST":
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect("dashboard") 
#             else:
#                 messages.error(request, "Invalid username or password")
#                 return redirect("login")
#     return render(request,"login.html",{"form":form})



def login_user(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        print(form.errors)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.success(request, "Login successful!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
                return redirect('login')
    return render(request, 'login.html', {'form': form})

    
def activate(request, id, token):
    try:
        user = CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        return HttpResponse("Invalid activation link")

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account activated successfully!")
        return redirect("login")
    else:
        messages.error(request, "Invalid activation link")
        return redirect("activate")

# @login_required(login_url="login")
# def logout_user(request):
#     logout(request)
#     return redirect("login")

class LogoutView(LoginRequiredMixin, View):
    login_url = "login"  # Redirect if not logged in

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


# dashboard er kahini
def participant_dashboard(request):
    rsvps = RSVP.objects.filter(participant=request.user).select_related("event").all()
    context = {
        "events":rsvps,
    }
    return render(request,"dashboard/participant-dashboard.html",context)

@login_required(login_url="login")
@user_passes_test(is_organizer,login_url="no-permission")
def organizer_dashboard(request):
    events = Event.objects.select_related("category").all()
    total_participants = RSVP.objects.all()
    print("total participants",total_participants)

    for event in events:
        event.participant_count = total_participants.filter(event=event).count()
    
    n_of_total_events=events.count()

    n_of_upcoming_events=events.filter(date__gt=timezone.now()).count()
    n_of_past_events=events.filter(date__lt=timezone.now()).count()
    today_events=events.filter(date=timezone.now())
    upcoming_events=events.filter(date__gt=timezone.now())
    past_events=events.filter(date__lt=timezone.now())  


    for event in today_events:
        event.participant_count = total_participants.filter(event=event).count()
    for event in upcoming_events:
        event.participant_count = total_participants.filter(event=event).count()
    for event in past_events:
        event.participant_count = total_participants.filter(event=event).count()

    if request.GET.get("type") == "today":
        events = today_events
    elif request.GET.get("type") == "upcoming":
        events = upcoming_events
    elif request.GET.get("type") == "past":
        events = past_events
    elif request.GET.get("type") == "all":
        events = events
    
    context = { 
        "events":events,
        "user_permitted":True,
        "total_participants":total_participants.count(),
        "n_of_total_events":n_of_total_events,
        "n_of_upcoming_events":n_of_upcoming_events,
        "n_of_past_events":n_of_past_events,
        "today_events":today_events,
        "upcoming_events":upcoming_events,
        "past_events":past_events
    }
    return render(request,"dashboard/organizer-dashboard.html",context)
@login_required(login_url="login")
@user_passes_test(is_admin,login_url="no-permission")
def admin_dashboard(request):
    events = Event.objects.select_related("category").all()
    total_participants = RSVP.objects.all()
    print("total participants",total_participants)

    for event in events:
        event.participant_count = total_participants.filter(event=event).count()
    
    n_of_total_events=events.count()

    n_of_upcoming_events=events.filter(date__gt=timezone.now()).count()
    n_of_past_events=events.filter(date__lt=timezone.now()).count()
    today_events=events.filter(date=timezone.now())
    upcoming_events=events.filter(date__gt=timezone.now())
    past_events=events.filter(date__lt=timezone.now())  


    for event in today_events:
        event.participant_count = total_participants.filter(event=event).count()
    for event in upcoming_events:
        event.participant_count = total_participants.filter(event=event).count()
    for event in past_events:
        event.participant_count = total_participants.filter(event=event).count()

    if request.GET.get("type") == "today":
        events = today_events
    elif request.GET.get("type") == "upcoming":
        events = upcoming_events
    elif request.GET.get("type") == "past":
        events = past_events
    elif request.GET.get("type") == "all":
        events = events
    
    context = { 
        "events":events,
        "user_permitted":True,
        "total_participants":total_participants.count(),
        "n_of_total_events":n_of_total_events,
        "n_of_upcoming_events":n_of_upcoming_events,
        "n_of_past_events":n_of_past_events,
        "today_events":today_events,
        "upcoming_events":upcoming_events,
        "past_events":past_events
    }
    return render(request,"dashboard/admin/admin-dashboard.html",context)
@login_required(login_url="login")
@user_passes_test(is_admin,login_url="no-permission")
def users(request):
    users = CustomUser.objects.all()
    return render(request,"dashboard/admin/users.html",{"users":users})
@login_required(login_url="login")
@user_passes_test(is_admin,login_url="no-permission")
def group_list(request):
    groups = Group.objects.all()
    return render(request,"dashboard/admin/group-list.html",{"groups":groups})


@login_required(login_url="login")
@user_passes_test(is_admin,login_url="no-permission")
def create_group(request):
    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            permissions = form.cleaned_data.get('permissions')
            group.permissions.set(permissions)
            return redirect("group-list")
    return render(request,"dashboard/admin/create-group.html",{"form":form})

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="no-permission")
def assign_role(request,id):
    user = CustomUser.objects.get(id=id)
    form = AssignRoleForm()
    if request.method == "POST":
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            group = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(group)
            return redirect("users")
    return render(request,"dashboard/admin/assign-role.html",{"form":form,"user":user})   
"""
def organizer_dashboard(request):
    events = Event.objects.prefetch_related("participant").select_related("category").all()
    total_participants = Participant.objects.count()
    n_of_upcoming_events=Event.objects.filter(date__gt=timezone.now()).count()
    n_of_past_events=Event.objects.filter(date__lt=timezone.now()).count()
    today_events=Event.objects.filter(date=timezone.now())
    upcoming_events=Event.objects.filter(date__gt=timezone.now())
    past_events=Event.objects.filter(date__lt=timezone.now())
    total_participants_across_all_events = Event.objects.aggregate(total=Sum("participant"))["total"]

    # default render events
    render_events=today_events

    if request.GET.get("type") == "today":
        render_events = today_events
    elif request.GET.get("type") == "upcoming":
        render_events = upcoming_events
    elif request.GET.get("type") == "past":
        render_events = past_events
    elif request.GET.get("type") == "all":
        render_events = events
    context = {
        "events_all":events,
        "total_participants":total_participants_across_all_events,
        "n_of_upcoming_events":n_of_upcoming_events,
        "n_of_past_events":n_of_past_events,
        "events":render_events,
        "user_permitted":True
        }
    return render(request,"organizer-dashboard.html",context)



"""
"""=======================  profile section ========================="""


# profile view
@login_required(login_url="login")
def profile(request):
    user = request.user
    return render(request,"profile.html",{"user":user})


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = EditProfileForm
    template_name = "edit-profile.html"
    success_url = reverse_lazy("profile")
    login_url = "login"
    
    def handle_no_permission(self): 
        return redirect('no-permission')
    
    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect(reverse_lazy("profile"))
# def edit_profile(request):
#     user = request.user
#     form = EditProfileForm(instance=user)
#     if request.method == "POST":
#         form = EditProfileForm(request.POST,request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect("profile")
#     return render(request,"edit-profile.html",{"form":form})



class ChangePassword(PasswordChangeView):
    template_name = 'password-change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("password-change-done")
    login_url = "login"
    
    def handle_no_permission(self): 
        return redirect('no-permission')



class PasswordChangeDoneView(LoginRequiredMixin, DjangoPasswordChangeDoneView):
    model = CustomUser
    form_class = CustomPasswordChangeForm
    template_name = "password-change-done.html"
    success_url = reverse_lazy("profile")
    login_url = "login"
    
    def handle_no_permission(self): 
        return redirect('no-permission')
    
    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect(reverse_lazy("profile"))
 

#  password reset
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'reset-password.html'
    success_url = reverse_lazy('password-reset-done')
    email_template_name = 'password_reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        context['site_name'] = 'Event Management System'
        print(context)
        return context

    def form_valid(self, form):
        messages.success(
        self.request, 'A Reset email sent. Please check your email')
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password-reset-done.html'
    success_url = reverse_lazy('password-reset-confirm')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'password-reset-confirm.html'

    def get_success_url(self):
        return reverse_lazy('password-reset-complete')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uidb64'] = self.kwargs.get('uidb64')
        context['token'] = self.kwargs.get('token')
        return context

    def form_valid(self, form):
        messages.success(
        self.request, 'Password reset successfully')
        return super().form_valid(form)

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password-reset-complete.html'
    success_url = reverse_lazy('login')