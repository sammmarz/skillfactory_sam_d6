from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post
@receiver(m2m_changed, sender=Post.textCategory.through)
# @receiver(post_save, sender=Post)
def notify(sender, instance, action, **kwargs):
	if action == "post_add":
		ca = []
		newtitle = instance.header
		newtext = instance.postText
		categs = instance.textCategory
		for categ in categs.all():
			for sub in categ.subscribers.all():
				print(sub.username)
				if sub not in ca:
					ca.append(sub)
					username = sub.username
					id = instance.id
					html_content = render_to_string(
						'tomail.html', {'newtitle': newtitle, 'newtext': newtext, 'username':username, 'id':id}
					)
					ca.append(sub)
					msg = EmailMultiAlternatives(
						subject=f'{newtitle}',
						body=f'Привет, {sub.username}',
						from_email='petrovskill23@yandex.ru',
						to=[f'{sub.email}'],
						)
					msg.attach_alternative(html_content, "text/html")
					msg.send()