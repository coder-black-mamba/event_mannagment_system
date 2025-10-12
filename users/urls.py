from django.urls import path
from .views import register,login_user,activate,participant_dashboard,organizer_dashboard,admin_dashboard,users,group_list,create_group,assign_role,profile,EditProfileView,ChangePassword,PasswordChangeDoneView,CustomPasswordResetView,CustomPasswordResetConfirmView,CustomPasswordResetDoneView,CustomPasswordResetCompleteView,LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activate/<int:id>/<str:token>/', activate, name='activate'),


    # profile 
    path('profile/', profile, name='profile'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
    path('password-change/', ChangePassword.as_view(), name='password-change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(), name='password-change-done'),
    # path('password-reset/', CustomPasswordResetView.as_view(), name='password-reset'),
    # path('reset-password/done/', PasswordResetDoneView.as_view(), name='reset-password-done'),
    # path('password-reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    # path('reset-password/complete/', PasswordResetCompleteView.as_view(), name='reset-password-complete'),

    # path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password-reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password-reset-done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password-reset-complete'),


    # dashboards
    path('participant-dashboard/', participant_dashboard, name='participant-dashboard'),
    path('organizer-dashboard/', organizer_dashboard, name='organizer-dashboard'),

    # admin
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/users/', users, name='users'),
    path('admin/group-list/', group_list, name='group-list'),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/assign-role/<int:id>/', assign_role, name='assign-role'),
]
