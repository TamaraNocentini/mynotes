from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', RedirectView.as_view(url='/my_notes/')),
    path('admin/', admin.site.urls),
    path('my_notes/', include('my_notes.urls')),
    path('accounts/login/',
         LoginView.as_view(template_name='my_notes/login.html'),
         name='login'),
    path('accounts/logout/',
         LogoutView.as_view(template_name='my_notes/logout.html'),
         name='logout'),
]
