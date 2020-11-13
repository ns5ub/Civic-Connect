from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField

## For emails
from django import template
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
#from django.db import models
from django.template import Context
## For Emails



interests = [('1', "Cybersecurity"), ('2', "Police Brutality")]

class Interest(models.Model):
    description = models.CharField(max_length=300)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    address = models.CharField(max_length=30, blank=True)
    interests = models.ManyToManyField(Interest, default=[])


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class TemplateSubmission(models.Model):
    topic = MultiSelectField(choices=interests, max_choices=3)
    template = models.CharField(max_length=5000, default="Write Template Here")
    def __str__(self):
        return self.template


class EmailTemplate(models.Model):
    """
    Email templates get stored in database so that admins can
    change emails on the fly
    """
    
    subject = models.CharField(max_length=255, blank=True, null=True)
    to_email = models.CharField(max_length=255, blank=True, null=True)
    from_email = models.CharField(max_length=255, blank=True, null=True)
    html_template = models.TextField(blank=True, null=True)
    plain_text = models.TextField(blank=True, null=True)
    is_html = models.BooleanField(default=False)
    is_text = models.BooleanField(default=False)

    # unique identifier of the email template
    template_key = models.CharField(max_length=255, unique=True)

    def get_rendered_template(self, tpl, context):
        return self.get_template(tpl).render(context)

    def get_template(self, tpl):
        return template.Template(tpl)

    def get_subject(self, subject, context):
        return subject or self.get_rendered_template(self.subject, context)

    def get_body(self, body, context):
        return body or self.get_rendered_template(self._get_body(), context)

    def get_sender(self):
        return self.from_email or settings.DEFAULT_FROM_EMAIL

    def get_recipient(self, emails, context):
        return emails or [self.get_rendered_template(self.to_email, context)]

    @staticmethod
    def send(*args, **kwargs):
        EmailTemplate._send(*args, **kwargs)

    @staticmethod
    def _send(template_key, context, subject=None, body=None, sender=None,
        emails=None, bcc=None, attachments=None):
        mail_template = EmailTemplate.objects.get(template_key=template_key)
        context = Context(context)
        subject = mail_template.get_subject(subject, context)
        body = mail_template.get_body(body, context)
        sender = sender or mail_template.get_sender()
        emails = mail_template.get_recipient(emails, context)

        if mail_template.is_text:
            return send_mail(subject, body, sender, emails, fail_silently=not settings.DEBUG)
        msg = EmailMultiAlternatives(subject, body, sender, emails, alternatives=((body, 'text/html'),), bcc=bcc)
        if attachments:
            for name, content, mimetype in attachments:
                msg.attach(name, content, mimetype)
        return msg.send(fail_silently=not (settings.DEBUG or settings.TEST))

        
    def _get_body(self):
        if self.is_text:
            return self.plain_text
        return self.html_template

        
    def __str__(self):
    
        return "<{}> {}".format(self.template_key, self.subject)
