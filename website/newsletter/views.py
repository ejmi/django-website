from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from .forms import ContactForm, SignUpForm
from .models import SignUp

def home(request):
    title = 'Welcome'
    form = SignUpForm(request.POST or None)
    context = {
        "title": title,
        "form": form
    }


    if form.is_valid():
        instance = form.save(commit=False)
        full_name = form.cleaned_data.get("full_name")
        if not full_name:
            full_name = "New full name"
        instance.full_name = full_name
        instance.save()
        context = {
            "title": "Thank you"
        }


    if request.user.is_authenticated() and request.user.is_staff:
        # print(SignUp.objects.all())
        # i = 1
        # for instance in SignUp.objects.all():
        #     print(i)
        #     print(instance.full_name)
        #     i += 1
        queryset = SignUp.objects.all().order_by('-timestamp')
        context = {
            "queryset": queryset
        }

    return render(request, 'home.html', context)


def contact(request):
    title = "Contact us"
    title_align_center = True
    form = ContactForm(request.POST or None)
    if form.is_valid():
        #for key, value in form.cleaned_data.iteritems():
            #print key, value
        form_email = form.cleaned_data.get('email')
        form_message = form.cleaned_data.get('message')
        form_full_name = form.cleaned_data.get('full_name')
        subject = 'Hello!'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, 'lukasz.wojno@gmail.com']
        contact_message = "%s: %s via %s"%(
                form_full_name,
                form_message,
                form_email)

        send_mail(subject,
                contact_message, 
                from_email, 
                to_email, 
                fail_silently=False)
    context = {
        'form': form,
        'title': title,
        'title_align_center': title_align_center,
    }
    return render(request, 'forms.html', context)