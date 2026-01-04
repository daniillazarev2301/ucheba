from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .ai_service import generate_presentation, generate_text_work, prepare_exam, solve_task
from .models import KnowledgeSource, SubscriptionPlan, TaskRequest, UserSubscription
from .serializers import (
    KnowledgeSourceSerializer,
    RegisterSerializer,
    SubscriptionPlanSerializer,
    TaskRequestSerializer,
    UserSerializer,
    UserSubscriptionSerializer,
)
from .tasks import generate_presentation_async, generate_text_work_async, solve_task_async

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {"refresh": str(refresh), "access": str(refresh.access_token)},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.check_password(password):
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({"refresh": str(refresh), "access": str(refresh.access_token)})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.select_related("user", "plan")
    serializer_class = UserSubscriptionSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=["post"], url_path="select")
    def select_plan(self, request):
        plan_id = request.data.get("plan_id")
        plan = SubscriptionPlan.objects.get(id=plan_id)
        subscription, _ = UserSubscription.objects.get_or_create(user=request.user, plan=plan)
        subscription.status = "active"
        subscription.started_at = timezone.now()
        subscription.ends_at = timezone.now() + timezone.timedelta(days=plan.duration_days)
        subscription.save()
        return Response(UserSubscriptionSerializer(subscription).data)


class TaskRequestViewSet(viewsets.ModelViewSet):
    queryset = TaskRequest.objects.select_related("user")
    serializer_class = TaskRequestSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(user=self.request.user)


class KnowledgeSourceViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeSource.objects.all()
    serializer_class = KnowledgeSourceSerializer
    permission_classes = [permissions.IsAdminUser]


class TaskSolveView(APIView):
    def post(self, request):
        payload = {
            "subject": request.data.get("subject"),
            "question": request.data.get("question"),
        }
        task_request = TaskRequest.objects.create(
            user=request.user,
            subject=payload["subject"],
            question=payload["question"],
            status="pending",
        )
        user_profile = {"specialty": request.user.specialty, "preferences": request.user.preferences}
        result = solve_task(payload, user_profile)
        task_request.steps = result.get("steps", [])
        task_request.answer = result.get("answer", "")
        task_request.status = "completed"
        task_request.save()
        solve_task_async.delay(task_request.id, payload, user_profile)
        return Response(result)


class WorkCreateView(APIView):
    def post(self, request):
        topic = request.data.get("topic")
        pages = int(request.data.get("pages", 1))
        user_profile = {"specialty": request.user.specialty, "preferences": request.user.preferences}
        result = generate_text_work(topic, pages, user_profile)
        generate_text_work_async.delay(request.user.id, topic, pages, user_profile)
        return Response(result)


class PresentationCreateView(APIView):
    def post(self, request):
        topic = request.data.get("topic")
        slides = int(request.data.get("slides", 5))
        user_profile = {"specialty": request.user.specialty, "preferences": request.user.preferences}
        result = generate_presentation(topic, slides, user_profile)
        generate_presentation_async.delay(request.user.id, topic, slides, user_profile)
        return Response(result)


class ExamPrepareView(APIView):
    def post(self, request):
        subjects = request.data.get("subjects", [])
        user_profile = {"specialty": request.user.specialty, "preferences": request.user.preferences}
        result = prepare_exam(subjects, user_profile)
        return Response(result)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def payment_webhook(request):
    external_id = request.data.get("payment_id")
    plan_id = request.data.get("plan_id")
    user_id = request.data.get("user_id")
    if not all([external_id, plan_id, user_id]):
        return Response({"detail": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST)
    plan = SubscriptionPlan.objects.get(id=plan_id)
    subscription, _ = UserSubscription.objects.get_or_create(user_id=user_id, plan=plan)
    subscription.status = "active"
    subscription.external_payment_id = external_id
    subscription.started_at = timezone.now()
    subscription.ends_at = timezone.now() + timezone.timedelta(days=plan.duration_days)
    subscription.save()
    return Response({"status": "ok"})
