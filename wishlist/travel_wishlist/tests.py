from django.http import response
from django.test import TestCase
from django.urls import reverse


from .models import Place

# Create your tests here.

class TestHomePage(TestCase):

    def test_home_page_shows_empty_list_message_for_empty_database(self):
        home_page_url = reverse('place_list') 
        # looks up url from url.py
        response = self.client.get(home_page_url)
        # makes request to web app server
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'You have no places in your wishlist')

class TestWishlist(TestCase):
    fixtures = {'test_places'}
    # gets data from test_places.json

    def test_wishlist_contains_not_visited(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')

class TestVisited(TestCase):
    fixtures = {'test_places'}

   

    def test_visited_page_only_places_visited_are_shown(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'Moab')
        self.assertContains(response, 'San Francisco')
        self.assertNotContains(response, 'Tokyo')
        self.assertNotContains(response, 'New York')

class TestVisitedPage(TestCase):

    def test_visited_page_shows_message_if_no_places_visted(self):
        visited_page_url = reverse('places_visited')
        response = self.client.get(visited_page_url)
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'You have not visited any places yet')

class TestAddNewPlace(TestCase):

    def test_add_new_unvisited_place(self):
        add_place_url = reverse('place_list')
        new_place_data = {'name': 'Tokyo', 'visited': False}
        response = self.client.post(add_place_url, new_place_data, follow=True)
        # follow=true means if another request is made after first request it will follow redirect
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        response_places = response.context['places']
        # returns a dictionary from what views.py is containing with template
        self.assertEqual(1, len(response_places))
        tokyo_from_reponse = response_places[0]
        tokyo_from_database = Place.objects.get(name='Tokyo', visited=False)
        self.assertEqual(tokyo_from_database, tokyo_from_reponse)

class TestVisitedPlace(TestCase):
    fixtures = ['test_places']

    def test_visit_place(self):
        visit_place_url = reverse('place_was_visited', args=(2, ))
        # args = 2 gets the database object with 2 as primary key
        response = self.client.post(visit_place_url, follow=True)
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertNotContains(response, 'New York')
        self.assertContains(response, 'Tokyo')
        
        # testing db
        new_york = Place.objects.get(pk=2)
        self.assertTrue(new_york.visited)

    def test_non_existent_place(self):
        visit_non_existent_place_url = reverse('place_was_visited', args=(123456, ))
        response = self.client.post(visit_non_existent_place_url, follow=True)
        self.assertEqual(404, response.status_code)







