from django.db.models.signals import post_save
from django.dispatch import receiver
from ssp.models import system_control


"""
Catch the post_save signal from the system_control and call the save method on 
each of it's parts to update title and short_name
"""
@receiver(post_save, sender=system_control)
def update_statements_and_parameters(sender, instance, **kwargs):
    for s in instance.control_statements.all():
        s.save()
    for p in instance.control_parameters.all():
        p.save()