from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm


# Create your views here.

def place_list(request):

    if request.method == 'POST':
        # creates a new place form object from data in form object
        form = NewPlaceForm(request.POST)
        place = form.save()
        # creates a model object form
        if form.is_valid():
            # uses database constraints
            place.save()
            # saves place to database
            return redirect('place_list')
            # redirects to homepage
            # reloads homepage


    #places = Place.objects.all()
    # gets all
    # this runs if request.method == POST does'nt run
    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    # creates html
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})
    #'travel_wishlist/wishlist is the template
    # displays template with forms in the homepage


def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request , 'travel_wishlist/visited.html', {'visited': visited})

def place_was_visited(request, place_pk):
    # place_pk must be the same variable used in url.py
    # pk- primary key
    if request.method == 'POST':
        #place = Place.objects.get(pk=place_pk)
        # pk is from database, gets object by pk
        place = get_object_or_404(Place, pk=place_pk)
        # returns 404 if page not found instead of error
        place.visited = True
        place.save()
    return redirect('place_list')
    # place_list is name of path to homepage



 # this is for about page
def about(request):
    author = 'Jason'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})

