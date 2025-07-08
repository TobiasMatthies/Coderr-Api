from django.contrib import admin
from  offers.models import Offer, OfferDetail

# Register your models here.
admin.site.register([Offer, OfferDetail])
