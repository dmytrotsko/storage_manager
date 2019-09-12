from django.db import models
from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from indussystem.models import User
import uuid


class EmailTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Name', max_length=255, unique=True)

    subject = models.CharField('Subject', max_length=255)
    mjml_template = models.TextField(
        'MJML template', default='', blank=True)
    html_template = models.TextField(
        'HTML template', default='', blank=True)
    text_template = models.TextField(
        'Text template', default='', blank=True)

    added = models.DateTimeField('Added', auto_now_add=True)
    changed = models.DateTimeField('Changed', auto_now=True)

    class Meta:
        verbose_name = 'Email template'
        verbose_name_plural = 'Email templates'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        import re
        from .utils import mjml_to_html
        from .html2text import html2text
        self.html_template = mjml_to_html(self.mjml_template)
        self.text_template = html2text(self.html_template)
        super(EmailTemplate, self).save(*args, **kwargs)

    def _template_header(self):
        CODE = '{% load static %}\n'
        return CODE

    def _render_template(self, template, context={}):
        from django.template import Context, Template
        template = self._template_header() + template
        t = Template(template)
        c = Context(context)
        return t.render(c)

    def render_subject(self, context={}):
        return self._render_template(self.subject, context).replace('\n', '')

    def render_html(self, context={}):
        context.update({
            'format': 'html',
        })
        return self._render_template(self.html_template, context)

    def render_text(self, context={}):
        context.update({
            'format': 'text',
        })
        return self._render_template(self.text_template, context)


class EmailMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    template = models.ForeignKey(
        EmailTemplate, verbose_name='Template', related_name='email_messages', on_delete=models.PROTECT)
    data = JSONField('Data', default=dict, blank=True)

    sent = models.BooleanField('Sent', default=False)
    added = models.DateTimeField('Added', auto_now_add=True)
    changed = models.DateTimeField('Changed', auto_now=True)

    class Meta:
        verbose_name = 'Email message'
        verbose_name_plural = 'Email messages'
        ordering = ('-added',)

    def __str__(self):
        return self.subject()

    def subject(self):
        return self.data.get('subject').replace('\n', '')

    def recipients(self):
        return self.data.get('recipients')

    def sender(self):
        return self.data.get('sender')

    def html_body(self):
        return self.data.get('html')

    def text_body(self):
        return self.data.get('text')

    def send(self):
        from .utils import send_email
        send_email(self.id)
