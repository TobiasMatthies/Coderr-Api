from django.contrib import admin
from users.models import User, Profile

# Register your models here.
admin.site.register([User, Profile])
