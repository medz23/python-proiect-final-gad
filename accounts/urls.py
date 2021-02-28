from django.urls import re_path, path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    re_path(r"^login/$", auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    re_path(r"^logout/$", auth_views.LogoutView.as_view(), name="logout"),
    re_path(r"^signup/$", views.SignUp.as_view(), name="signup"),
    re_path(r"^home/$", views.home, name=""),
    path('profile-update/',views.updateProfile, name='profile-update'),
    path('follow-unfollow/<int:pk>/',views.userFollowUnfollow, name="follow-unfollow"),
    path('<str:username>/', views.profile, name='profile'),
    path('search/asame/', views.search_view, name='search'),
    path('<str:username>/notifications/',views.notifications_view,name='notifications'),
    path('<str:username>/notifications/update/', views.notifications_update_view, name='notifications-update'),
    path('<str:username>/notifications/count/', views.notifications_unread_count_view, name='notifications-count'),
    path('like/post',views.like_view,name='like'),
    path('p/<slug:slug>/', views.post_detail_view, name="post-detail"),
    path('post/new/',views.post_create_view,name='post-create'),
    path('post/<int:pk>/update/', views.post_update_view, name='post-update'),
    path('post/<int:pk>/delete/',views.post_delete_view, name='post-delete'),
]
