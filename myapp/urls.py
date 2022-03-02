from django.urls import path
from django.contrib.auth import views as auth_views
from .import views
from django.conf import settings
from django.conf.urls.static import static
from .views import VideoCreateView,VideoUpdateView,VideoDeleteView,CommentUpdateView,CommentDeleteView


urlpatterns = [
    path('',auth_views.LoginView.as_view(),name='login'),
    path('register/',views.register,name='register'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('profile/password-reset/',auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),name='password_reset'),
    path('profile/password-resset/done/',auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('profile/password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
    path('profile/password-resset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
    path('home/',views.home,name='home'),
    path('s/',views.search,name='search'),
    path('home/category/<int:pk>/',views.category_page,name='category_page'),
    path('home/video/<int:pk>/',views.vdodetail,name='vdodetail'),
    path('home/video/<int:pk>/#',views.vlikes,name='vlikes'),
    path('home/video/<int:pk>/update/',VideoUpdateView.as_view(),name='vdoupdate'),
    path('home/video/<int:pk>/cupdate/',CommentUpdateView.as_view(),name='cupdate'),
    path('home/video/<int:pk>/delete/',VideoDeleteView.as_view(),name='vdodelete'),
    path('home/video/<int:pk>/cdelete/',CommentDeleteView.as_view(),name='cdelete'),
    path('home/video/post/',VideoCreateView.as_view(),name='vdocreate'),
    # path('profile/',views.profile,name='profile'),
    path('userprofile/<int:pk>/',views.profile_user,name='profile_user'),
    path('update/<int:pk>/',views.update,name='update'),
    path('watchlist/',views.watchlist,name='watchlist'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)































