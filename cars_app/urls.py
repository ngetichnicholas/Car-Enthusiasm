from django.urls import path
from cars_app import views as app_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',app_views.index,name='index'),
    path('contact',app_views.contact,name='contact'),
    path('register/',app_views.signup_view,name='register'),
    path('accounts/login/',app_views.login,name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'index.html'),name='logout'),
    path('accounts/profile/',app_views.profile,name='profile'),
    path('update/',app_views.update_profile,name='update_profile'),
    path('add_car',app_views.add_car,name='add_car'),
    path('car_view/<int:car_id>',app_views.car_view,name='car_view')

]
if settings.DEBUG:
  urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)