from celery import shared_task

from .ai_service import generate_presentation, generate_text_work, solve_task
from .models import TaskRequest


@shared_task
def solve_task_async(task_request_id, payload, user_profile):
    result = solve_task(payload, user_profile)
    TaskRequest.objects.filter(id=task_request_id).update(
        steps=result.get("steps", []),
        answer=result.get("answer", ""),
        status="completed",
    )
    return result


@shared_task
def generate_text_work_async(user_id, topic, pages, user_profile):
    return generate_text_work(topic, pages, user_profile)


@shared_task
def generate_presentation_async(user_id, topic, slides, user_profile):
    return generate_presentation(topic, slides, user_profile)
