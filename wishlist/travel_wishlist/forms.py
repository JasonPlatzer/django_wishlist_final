from django import forms
from .models import Place

# creating a form object to store data from input
# into a database
class NewPlaceForm(forms.ModelForm):
   class Meta:
       model = Place
       fields = ('name', 'visited') 
