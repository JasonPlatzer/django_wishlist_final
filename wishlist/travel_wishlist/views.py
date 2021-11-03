from django.core.checks import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages


# Create your views here.


@login_required
def place_list(request):

    if request.method == 'POST':
        # creates a new place form object from data in form object
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False)
        place.user = request.user
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
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    # user=request.user gets user from request
    new_place_form = NewPlaceForm()
    # creates html
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})
    #'travel_wishlist/wishlist is the template
    # displays template with forms in the homepage

@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request , 'travel_wishlist/visited.html', {'visited': visited})
    # returns a templa
    #{'visited:visited} 'visited' is for visted.html it sets visited to visited in function

@login_required
# will reroute to a sign in page if one is available
def place_was_visited(request, place_pk):
    # place_pk must be the same variable used in url.py
    # pk- primary key
    if request.method == 'POST':
        #place = Place.objects.get(pk=place_pk)
        # pk is from database, gets object by pk
        place = get_object_or_404(Place, pk=place_pk)
        # returns 404 if page not found instead of error
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()

    return redirect('place_list')
    # place_list is name of path to homepage



 # this is for about page

@login_required
def about(request):
    author = 'Jason'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})

@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    #return render(request, 'travel_wishlist/place_detail.html', {'place':place})

    if place.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        # request.FILES are images uploaded, all stuff is sent with HTTP request, instance=place updates 
        # makes a form object
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
            # messages show a message to user
        else:
            messages.error(request, form.errors)
        
        return redirect('place_details', place_pk=place_pk) 
    
    # if a get request
    else:
        if place.visited:
            # from line 57
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        else:
             return render(request, 'travel_wishlist/place_detail.html', {'place': place})



@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        # you need to return a response
        return redirect('place_list')
    
    else:
        return HttpResponseForbidden

   