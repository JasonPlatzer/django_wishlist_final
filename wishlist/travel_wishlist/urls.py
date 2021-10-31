from django.urls import path
from . import views


urlpatterns = [
   path('', views.place_list, name='place_list'),
    # '' matches to 127.0.0.1:8000 the homepage
    path ('place/<int:place_pk>/was_visited', views.place_was_visited, name='place_was_visited'),
    # sets a path based on primary key
    path('visited', views.places_visited, name='places_visited'),
    path('about', views.about, name='about'),
    path('place/<int:place_pk>', views.place_details, name='place_details'),
    path('place/<int:place_pk>/delete', views.delete_place, name='delete_place')
]