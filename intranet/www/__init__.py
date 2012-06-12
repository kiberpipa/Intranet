from django.contrib.comments.models import Comment
from django.core.mail import send_mail
from django.db.models import signals
from django.conf  import settings

def mail_comment(instance, **kwargs):
    subject = 'YAY! someone posted comment'
    msg = 'Comment text:\n\n%s\n\nComment url:%s\n\n' % (instance.comment, instance.get_absolute_url())
    #send_mail(subject, msg, 'webpage-comments@kiberpipa.org', ['dmulac@gmail.com'])

signals.post_save.connect(mail_comment, sender=Comment)
