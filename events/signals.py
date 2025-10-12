from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.core.mail import send_mail
from .models import RSVP


# send email to participant when they RSVP for an event
@receiver(post_save, sender=RSVP)
def send_rsvp_email(sender, instance, created, **kwargs):
    if created:
        event=instance.event
        participant = instance.participant
        subject = f'RSVP Confirmation for {event.name}'
        message = f'Hi {participant.username},\n\nYou have successfully RSVP for the event {event.name}.\n\nThank You! Please arrive on {event.date} at {event.time}.\n\nLocation: {event.location}\n\nDescription: {event.description}\n\nThank You!\n Built with 💔 by Abu Sayed'
        recipient_list = [participant.email]

        try:
            send_mail(subject, message,
                      settings.EMAIL_HOST_USER, recipient_list)
            print("Email sent to", participant.email)
            print("RSVP MESSAGE:", message)
        except Exception as e:
            print(f"Failed to send email to {participant.email}: {str(e)}")


# add rsvp cancel email
@receiver(post_delete, sender=RSVP)
def send_rsvp_cancel_email(sender, instance, **kwargs):
    event=instance.event
    participant = instance.participant
    subject = f'RSVP Cancellation for {event.name}'
    message = f'Hi {participant.username},\n\nYou have successfully cancelled your RSVP for the event {event.name}.\n\nThank You!\n Built with 💔 by Abu Sayed'
    recipient_list = [participant.email]

    try:
        send_mail(subject, message,
                  settings.EMAIL_HOST_USER, recipient_list)
        print("Email sent to", participant.email)
        print("RSVP CANCEL MESSAGE:", message)
    except Exception as e:
        print(f"Failed to send email to {participant.email}: {str(e)}")
    