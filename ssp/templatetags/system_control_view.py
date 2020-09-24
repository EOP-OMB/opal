from django import template
from ssp.models import system_security_plan, nist_control

register = template.Library()

@register.simple_tag
def get_control_implementation(info_sys, nc):
    c = []
    ssp = system_security_plan.objects.get(pk=info_sys)
    nc = nist_control.objects.get(control_id=nc)
    if ssp.controls.filter(nist_control=nc).exists():
        print(nc.__str__() + ' exists for system')
        c.append({ssp.__str__() : ssp.controls.get(nist_control=nc)})
    if ssp.leveraged_authorization.exists():
        for leveraged_auth in ssp.leveraged_authorization.all():
            if leveraged_auth.controls.filter(nist_control=nc, inheritable=True).exists():
                print(nc.__str__() + ' exists for leveraged system')
                c.append({ssp.__str__() : ssp.controls.get(nist_control=nc)})
    return c