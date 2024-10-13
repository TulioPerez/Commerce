from django import forms 
from .models import *

# django form for auction listings - allows repopulation of fields when editing
class ListingForm(forms.ModelForm):
    class Meta:
        model = Auction_Listing
        fields = [
            'category', 
            'image',
            'title', 
            'description',
            'price',
            'quantity',
            'closing_time',
            'is_open'
            ]
    
    # initializes the form instance
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['closing_time'].widget = forms.widgets.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
        })
