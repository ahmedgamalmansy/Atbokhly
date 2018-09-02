from django.contrib import admin
from .models import *

admin.site.register(Meal)
admin.site.register(Ingredient)
admin.site.register(Category)
admin.site.register(Feedback)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(ReactValues)
admin.site.register(LikeComment)
admin.site.register(Rate)
admin.site.register(UserRate)
admin.site.register(UserLike)