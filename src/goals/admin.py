from django.contrib import admin

from goals.models import BoardParticipant
from goals.models.board import Board
from goals.models.goal_category import GoalCategory
from goals.models.goal import Goal
from goals.models.goal_comment import GoalComment


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "created", "updated")
    search_fields = ("title", "user")


class GoalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "category",
        "title",
        "description",
        "status",
        "priority",
        "due_date",
        "created",
        "updated",
    )
    search_fields = ("title", "user")
    list_filter = ('status', 'priority')
    readonly_fields = ('created', 'updated')
    list_display_links = ('title', )


class GoalCommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text')
    search_fields = ("text",)
    readonly_fields = ('created', 'updated')


class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', "is_deleted")
    search_fields = ("title",)
    readonly_fields = ('created', 'updated')


class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', "board", "role")
    list_filter = ("role",)
    readonly_fields = ('created', 'updated')
    list_display_links = ('board', 'user')


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentsAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(BoardParticipant, BoardParticipantAdmin)
