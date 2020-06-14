from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives

# Create your views here.

def send_otl_email(request):
	text_content="Your one time link Email"
	subject="Request for your comment"
	template_name="email/otl.html"
	from_email=settings.EMAIL_HOST_USER
	users=User.objects.all()
	for user in users:
		recipients=[user.email]

		kwargs = {
			"uidb64":urlsafe_base64_encode(force_bytes(user.pk)),
			"token":default_token_generator.make_token(user)
		}

		the_url=reverse('user_comments', kwargs=kwargs)
		otl_url="{0}://{1}{2}".format(request.scheme, request.get_host(), the_url)

		context = {
			'user' : user,
			'otl_url': otl_url,
		}
		html_content = render_to_string(template_name, context)
		email=EmailMultiAlternatives(subject, text_content, from_email, recipients)
		email.attach_alternative(html_content, "text/html")
		email.send()
	return HttpResponse("All mails has been sent")

def comments(request, uidb64=None, token=None):
	return HttpResponse("Your link is active and your are back to server")
