from django.dispatch import receiver
from django.db.models.signals import post_save
from users.models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import Group

@receiver(post_save, sender=CustomUser)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"

        subject = 'Activate Your Account'
        message = f'Hi {instance.username},\n\nPlease activate your account by clicking the link below:\n{activation_url}\n\nThank You!\n Built with 💔 by Abu Sayed'
        recipient_list = [instance.email]

        try:
            send_mail(subject, message,
                      settings.EMAIL_HOST_USER, recipient_list)
            print("Email sent to", instance.email)
            print("Activation URL:", activation_url)
        except Exception as e:
            print(f"Failed to send email to {instance.email}: {str(e)}")

@receiver(post_save, sender=CustomUser)
def assign_role(sender, instance, created, **kwargs):
    if created:
        user_group, created = Group.objects.get_or_create(name='participant')
        instance.groups.add(user_group)
        instance.save()