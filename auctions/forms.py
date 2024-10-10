from django import forms 
from .models import *


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
            ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
