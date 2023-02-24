import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
	from news.models import Category, Post
	from datetime import datetime, timedelta
	cat = Category.objects.all()
	now = datetime.now()-timedelta(days=7)
	print(now)
	for c in cat:
		posts = Post.objects.filter(textCategory=c, creationTime__gte=now)
		list_email = []
		for sub in c.subscribers.all():
			print("пользователь", sub, posts)
			list_email.append(sub.email)
		subject, from_email = f'Новости за неделю в категории {c}', 'petrovskill23@yandex.ru'
		to = list_email
		text_content = f'Привет! Новости за неделю в категории {c}'
		list_a=[]
		for post in posts:
			list_a.append(f'<a href="http://127.0.0.1:8000/news/{post.id}">{post.header}</a>')
		html_content = f'<p>{list_a}</p>'
		msg = EmailMultiAlternatives(subject, text_content, from_email, to)
		msg.attach_alternative(html_content, "text/html")
		msg.send()
	print('hello from job',)


# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
	"""This job deletes all apscheduler job executions older than `max_age` from the database."""
	DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
	help = "Runs apscheduler."


	def handle(self, *args, **options):
		scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
		scheduler.add_jobstore(DjangoJobStore(), "default")

		# добавляем работу нашему задачнику
		scheduler.add_job(
			my_job,
			trigger=CronTrigger(day_of_week="sun"), 
			id="my_job",  # уникальный айди
			max_instances=1,
			replace_existing=True,
		)
		logger.info("Added job 'my_job'.")

		scheduler.add_job(
			delete_old_job_executions,
			trigger=CronTrigger(
				day_of_week="mon", hour="00", minute="00"
			),
			# Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
			id="delete_old_job_executions",
			max_instances=1,
			replace_existing=True,
		)
		logger.info(
			"Added weekly job: 'delete_old_job_executions'."
		)

		try:
			logger.info("Starting scheduler...")
			scheduler.start()
		except KeyboardInterrupt:
			logger.info("Stopping scheduler...")
			scheduler.shutdown()
			logger.info("Scheduler shut down successfully!")