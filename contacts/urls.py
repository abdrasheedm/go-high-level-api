from django.urls import path
from . import views

urlpatterns = [
    path('fetch-contacts/', views.fetch_contacts, name="fetch_contacts"),
    path('check/', views.fetch, name="check"),
]
