from django.contrib import admin
from rank.models import RankingChart


@admin.register(RankingChart)
class CalculatorAdmin(admin.ModelAdmin):
    list_display = ['calculator', 'num_remaindays', 'num_workdays', 'percent', 'workday_percent', 'num_leaves',
                    'start_date', 'end_date', 'end_workday', 'updated_at']
    list_display_links = ['calculator']
