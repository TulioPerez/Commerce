from django import forms
from .models import *


# django form for auction listings - allows repopulation of fields when editing
class ListingForm(forms.ModelForm):
    class Meta:
        model = Auction_Listing
        fields = [
            "category",
            "image",
            "title",
            "description",
            "price",
            "quantity",
            "closing_time",
            "is_open",
        ]

    # initializes the form instance
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.all()
        self.fields["closing_time"].widget = forms.widgets.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control",
            }
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget.attrs.update(
            {"placeholder": "Add a comment", "rows": 5}
        )
        self.fields["content"].label = ""
