from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from corona.models import Restaurant, RestaurantComment, RestaurantCategory, RestaurantTag, UnvaccinatedPass


@admin.register(Restaurant)
class RestaurantAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'latitude', 'longitude', 'unvaccinated_pass', 'verifieded', 'created_at']
    list_display_links = ['id', 'name', ]


@admin.register(RestaurantComment)
class RestaurantCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'restaurant', 'is_anonymous', 'created_at']
    list_display_links = ['id', 'restaurant', ]


@admin.register(RestaurantCategory)
class RestaurantCategoryAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ['id', 'name', ]
    list_display_links = ['id', 'name', ]


@admin.register(UnvaccinatedPass)
class UnvaccinatedPassAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ['id', 'type', ]
    list_display_links = ['id', 'type', ]


@admin.register(RestaurantTag)
class RestaurantTagAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ['id', 'name', ]
    list_display_links = ['id', 'name', ]
