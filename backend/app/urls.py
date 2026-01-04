from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ExamPrepareView,
    KnowledgeSourceViewSet,
    LoginView,
    PresentationCreateView,
    RegisterView,
    SubscriptionPlanViewSet,
    TaskRequestViewSet,
    TaskSolveView,
    UserSubscriptionViewSet,
    UserViewSet,
    WorkCreateView,
    payment_webhook,
)

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("plans", SubscriptionPlanViewSet)
router.register("subscriptions", UserSubscriptionViewSet)
router.register("subscription", UserSubscriptionViewSet, basename="subscription")
router.register("tasks", TaskRequestViewSet)
router.register("knowledge", KnowledgeSourceViewSet)

urlpatterns = [
    path("auth/register", RegisterView.as_view(), name="register"),
    path("auth/login", LoginView.as_view(), name="login"),
    path("task/solve", TaskSolveView.as_view(), name="solve"),
    path("work/create", WorkCreateView.as_view(), name="work-create"),
    path("presentation/create", PresentationCreateView.as_view(), name="presentation-create"),
    path("exam/prepare", ExamPrepareView.as_view(), name="exam-prepare"),
    path("subscription/webhook", payment_webhook, name="payment-webhook"),
    path("", include(router.urls)),
]
