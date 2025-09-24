from celery import shared_task
from django.utils import timezone
from .models import Task
import logging

logger = logging.getLogger(__name__)

@shared_task
def check_due_tasks():
    now = timezone.now()
    due_tasks = Task.objects.filter(due_date__lte=now, due_date__isnull=False)
    for task in due_tasks:
        logger.info(f"Уведомление для задачи {task.id}: {task.title} просрочена!")