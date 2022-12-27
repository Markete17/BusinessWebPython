from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import EmailMessage
from .forms import ContactForm

# Create your views here.
def contact(request):
    contact_form = ContactForm()
    if request.method == 'POST':
        contact_form = ContactForm(data = request.POST)
        if contact_form.is_valid():
            name = request.POST['name']
            email = request.POST['email']
            content = request.POST['content']
            # Enviar correo con MailTrap y la libreria django.core.mail
            email = EmailMessage(
                "La Caffetiera: 'Nuevo mensaje de contacto'" 
                "De {} <{}>\n\nEscribió:\n\n{}".format(name, email, content), 
                "no-contestar@inbox.mailtrap.io",
                ["honopo5717@octovie.com"],
                reply_to = [email]
            )
            try:
                email.send()
                return redirect(reverse('contact')+'?ok')
            except:
                return redirect(reverse('contact')+'?fail')
    return render(request, 'contact/contact.html',{'form': contact_form})