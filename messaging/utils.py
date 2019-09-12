import subprocess
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def mjml_to_html(mjml_code):
    cmd_args = getattr(settings, 'MJML_COMMAND', './node_modules/.bin/mjml')
    if not isinstance(cmd_args, list):
        cmd_args = [cmd_args]
        cmd_args.extend(['-i', '-s'])

    try:
        p = subprocess.Popen(
            cmd_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        html = p.communicate(mjml_code.encode('utf8'))[0].decode('utf8')
    except (IOError, OSError) as e:
        raise RuntimeError(
            'Problem to run command "{}"\n'.format(' '.join(cmd_args)) +
            '{}\n'.format(e) +
            'Check that mjml is installed and allow permissions for execute.\n' +
            'See https://github.com/mjmlio/mjml#installation'
        )
    return html


def send_email(obj_id):
    from .models import EmailMessage
    message_obj = EmailMessage.objects.get(id=obj_id)
    mail = EmailMultiAlternatives(
        subject=message_obj.subject(),
        body=message_obj.text_body(),
        from_email=message_obj.sender(),
        to=message_obj.recipients(),
    )
    mail.attach_alternative(message_obj.html_body(), 'text/html')

    try:
        mail.send()
        message_obj.sent = True
        message_obj.save()
    except Exception as e:
        message_obj.data['error'] = str(e)
        message_obj.save()


def create_email_message(template_name, recipients, sender, context=None, request=None):
    from .models import EmailMessage, EmailTemplate
    from django.conf import settings

    if context is None:
        context = {}

    try:
        template = EmailTemplate.objects.get(name=template_name)

        data = {
            'recipients': recipients,
            'sender': sender,
            'subject': str(template.render_subject(context)),
            'html': template.render_html(context),
            'text': template.render_text(context),
        }

        message = EmailMessage(
            template=template,
            data=data,
        )
        message.save()
        return message
    except EmailTemplate.DoesNotExist:
        pass


def send_email_message(template_name, recipients, sender, context=None, request=None):
    msg = create_email_message(
        template_name, recipients, sender, context, request)
    if msg:
        msg.send()
