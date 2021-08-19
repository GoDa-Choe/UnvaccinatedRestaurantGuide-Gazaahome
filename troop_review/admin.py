from django.contrib import admin
from troop_review.models import Troop, Review


@admin.register(Troop)
class TroopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', ]
    list_display_links = ['id', 'name', ]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'troop', 'reviewer', 'star_rating', 'duty_assignment', 'year', 'month', 'created_at']
    list_display_links = ['id', 'troop', ]
