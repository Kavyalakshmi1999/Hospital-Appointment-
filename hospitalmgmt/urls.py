from django.contrib import admin
from django.urls import path

from bookings.views import Bookapp



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Bookapp.as_view(),name='request_appointment'),
    path('dbupdate/',Bookapp.as_view(),name='update_database'),
]
