from django.urls import path
from users.views import sign_up, sign_in, sign_out, activate_user, admin_dashboard, assign_role, create_group, group_list, CustomLoginView, ProfileView, CustomLogoutView, CustomChangePassword, CustomChangePasswordDone, CustomResetPassword, CustomResetPasswordConfirm, EditProfileView

urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    # path('sign-in/', sign_in, name='sign-in'),
    path('sign-in/', CustomLoginView.as_view(template_name='registration/sign_in.html'), name='sign-in'),
    # path('sign-out/', sign_out, name='sign-out'),
    path('sign-out/', CustomLogoutView.as_view(), name='sign-out'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate-user'),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/group-list/', group_list, name='group-list'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', CustomChangePassword.as_view(), name='change-password'),
    path('change-password/done/', CustomChangePasswordDone.as_view(), name='change-password-done'),
    path('reset-password/', CustomResetPassword.as_view(), name='reset-password'),
    path('reset-password/confirm/<uidb64>/<token>/', CustomResetPasswordConfirm.as_view(), name='password_reset_confirm'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
]
