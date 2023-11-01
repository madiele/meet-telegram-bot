from django.contrib import admin
from django_admin_relation_links import AdminChangeLinksMixin
from letsMeetBot.models import (
    BotSettings,
    Chat,
    User,
    DailyStat,
    Message,
    ChatUser,
    Proposal,
)


# django admin pages
class BotSettingsAdmin(admin.ModelAdmin):
    exclude = ("instance",)
    pass


class ChatAdmin(admin.ModelAdmin):
    readonly_fields = (
        "chat_id",
        "chat_name",
        "last_welcome_message_id",
    )
    pass


class UserAdmin(admin.ModelAdmin):
    readonly_fields = (
        "user_id",
        "username",
        "message_count",
    )
    ordering = ["-message_count"]
    list_display = ("full_name", "username", "message_count", "user_id")
    search_fields = ("full_name", "username", "user_id")
    pass


class DailyStatAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    readonly_fields = (
        "members_count",
        "messages_count",
        "new_members_count",
        "date",
    )
    exclude = ("chat",)
    change_links = ("chat",)
    list_display = (
        "date",
        "members_count",
        "messages_count",
        "new_members_count",
        "chat_link",
    )
    ordering = ["-date"]
    pass


class MessageAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    readonly_fields = ("message_id", "date", "text", "pinned_message", "link")
    exclude = ("from_chat", "from_user")
    change_links = (
        "from_chat",
        "from_user",
    )
    list_display = ("message_id", "from_user_link", "from_chat_link", "date", "text")
    order_by = ["-date"]
    pass


class ChatUserAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    exclude = ("user", "chat")
    change_links = ("user", "chat")
    list_display = (
        "user",
        "chat_link",
        "can_do_automatic_pin",
        "instant_share_to_channel",
    )
    list_editable = ("can_do_automatic_pin", "instant_share_to_channel")
    pass


class ProposalAdmin(admin.ModelAdmin):
    pass


admin.site.register(BotSettings, BotSettingsAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(DailyStat, DailyStatAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(ChatUser, ChatUserAdmin)
admin.site.register(Proposal, ProposalAdmin)
