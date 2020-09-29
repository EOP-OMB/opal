from ssp.models import system_control

for i in system_control.objects.all():
    for r in i.control_implementation.control_responsible_roles.all():
        i.control_responsible_roles.add(r)
    for p in i.control_implementation.control_parameters.all():
        i.control_parameters.add(p)
    for s in i.control_implementation.control_statements.all():
        i.control_statements.add(s)

