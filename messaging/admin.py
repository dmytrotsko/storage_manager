from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django.urls import reverse
from .models import (
    EmailTemplate,
    EmailMessage,
)
from .forms import EmailTemplateForm


class EmailTemplateAdmin(admin.ModelAdmin):
    form = EmailTemplateForm
    list_display = ('name', 'subject')
    search_fields = ('name',)
    fields = ('name', 'subject', 'mjml_template', 'template_preview')
    readonly_fields = ('template_preview',)

    def template_preview(self, obj):
        TEMPLATE = '''
<div style="border:1px solid #ccc;">{html}</div>
<pre>
{text}
</pre>
'''
        context = {
            'html': obj.html_template,
            'text': obj.text_template,
        }
        result = mark_safe(TEMPLATE.format(**context))
        return result


admin.site.register(EmailTemplate, EmailTemplateAdmin)


class EmailMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'recipients', 'sender', 'sent', 'added')
    readonly_fields = ('message_preview', 'data')
    fields = ('template', 'sent', 'message_preview', 'data')
    actions = ['send_message']

    def send_message(self, request, queryset):
        for obj in queryset:
            obj.send()
    send_message.short_description = 'Send message'

    def message_preview(self, obj):
        TEMPLATE = '''
<strong>{To}:</strong> {to}<br>
<strong>{From}:</strong> {from}<br>
<strong>{Subject}:</strong> {subject}<br>
<div style="border:1px solid #ccc;">{html}</div>
<pre>
{text}
</pre>
'''
        context = {
            'To': 'To',
            'From': 'From',
            'Subject': 'Subject',
            'to': ', '.join(obj.recipients() or []),
            'from': obj.sender(),
            'subject': obj.subject(),
            'html': obj.html_body(),
            'text': obj.text_body(),
        }
        result = mark_safe(TEMPLATE.format(**context))
        return result


admin.site.register(EmailMessage, EmailMessageAdmin)
