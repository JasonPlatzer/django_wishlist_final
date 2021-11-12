from django import forms
from django.forms import fields, widgets
from .models import Place

# creating a form object to store data from input
# into a database
class NewPlaceForm(forms.ModelForm):
   class Meta:
       model = Place
       fields = ('name', 'visited') 

class DateInput(forms.DateInput):
    input_type = 'date'
# used with widget to make a calender date picker

class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('notes', 'date_visited', 'photo')
        widgets = {
            'date_visited': DateInput()
        }
