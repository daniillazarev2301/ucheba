from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import KnowledgeSource, SubscriptionPlan, TaskRequest, User, UserSubscription


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Profile", {"fields": ("specialty", "preferences")}),
    )
    list_display = ("username", "email", "specialty", "tasks_count", "subscriptions_count")

    def tasks_count(self, obj):
        return obj.task_requests.count()

    def subscriptions_count(self, obj):
        return obj.subscriptions.count()


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "duration_days", "is_active")


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "status", "started_at", "ends_at")


@admin.register(TaskRequest)
class TaskRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "subject", "status", "created_at")


@admin.register(KnowledgeSource)
class KnowledgeSourceAdmin(admin.ModelAdmin):
    list_display = ("title", "link", "created_at")
