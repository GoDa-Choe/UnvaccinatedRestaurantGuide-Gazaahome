from django.contrib import admin
from home.models import Corona, Statistics


@admin.register(Corona)
class CoronaAdmin(admin.ModelAdmin):
    list_display = ['id', 'state_date', 'decided_count', 'created_at', ]
    list_display_links = ['id', 'state_date', ]


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'state_date',

        'user_increment', 'calculator_increment',

        'user_count',
        'calculator_count', 'leave_count',
        'barracks_count', 'guest_book_count',
        'troop_count', 'review_count',
        'post_count', 'comment_count',
    ]

    list_display_links = ['id', 'state_date', ]
