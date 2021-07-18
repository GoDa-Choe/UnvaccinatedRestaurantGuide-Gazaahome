from django.contrib import admin
from barracks.models import Barracks, Invitation, GuestBook
from django.contrib import admin


class GuestBookInline(admin.TabularInline):
    model = GuestBook
    extra = 0


class InvitationInline(admin.TabularInline):
    model = Invitation
    extra = 0


class MembershipInline(admin.TabularInline):
    model = Barracks.members.through
    extra = 0


@admin.register(Barracks)
class BarracksAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at', 'host', ]
    list_display_links = ['id', 'name', ]
    inlines = [
        GuestBookInline,
        InvitationInline,
        MembershipInline,
    ]

    exclude = ('members',)


@admin.register(GuestBook)
class GuestBookAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'calculator', 'barracks', 'content', 'created_at']
    list_display_links = ['id', 'author', ]


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['id', 'barracks', 'inviter', 'inviter_calculator', 'invitee', 'created_at', ]
    list_display_links = ['id', 'barracks', ]
