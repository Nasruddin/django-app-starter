from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from .forms import ContactForm, SignUpForm

# Create your views here.
def home(request):
	title = "Welcome"
	#Add form
	form = SignUpForm(request.POST or None)

	if request.user.is_authenticated():
		title = "My Title %s" %(request.user)

	context = {
		"template_title": title,
		"form": form
	}

	if form.is_valid():
		#request.POST['email'] #Not recommended
		instance = form.save(commit= False)

		full_name = form.cleaned_data.get("full_name")

		if not full_name:
			full_name = "new full name"
			instance.full_name = full_name
		instance.save()
		print instance.email	
		print instance.timestamp
		context = {
			"template_title"	: "Thank you"
		}
	return render(request, "home.html", context)


def contact(request):

	title = 'Contact Us'
	title_align_center = True
	form = ContactForm(request.POST or None)

	if form.is_valid():
		form_email = form.cleaned_data.get("email")
		form_full_name = form.cleaned_data.get("full_name")
		form_message = form.cleaned_data.get("message")

		subject = 'Site info'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email, 'webo.geeky@gmail.com']
		contact_message = "%s: %s via %s"%(
				form_full_name, 
				form_message, 
				form_email)

		send_mail(subject, 
				contact_message, 
				from_email, 
				to_email, 
				fail_silently=False)
		#print form.cleaned_data
		#print email, full_name, message

	context = {
		"form": form,
		"title": title,
		"title_align_center": title_align_center
	}
	return render(request, "forms.html", context)
