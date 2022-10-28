from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment


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


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentsAdmin)




