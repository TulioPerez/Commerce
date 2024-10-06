from django.contrib import admin
from .models import Auction_Listing, Bid, Category, Comment 

# register models for use in admin portal 
# registered via the python shell

admin.site.register(Auction_Listing)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Comment)
