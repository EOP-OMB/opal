from ssp.models.controls import control_statement, system_control

def fix_short_name(id):
    obj = control_statement.objects.get(pk=id)
    sn = obj.short_name
    sl = sn.split('-')
    if len(sl[1].split('.')[0]) == 1:
        sl[1] = '0' + sl[1]
    return '-'.join(sl)

def update_short_names():
    for i in control_statement.objects.all():
        i.short_name = fix_short_name(i.id)
        i.save()

def link_statements_to_controls():
    for c in system_control.objects.all():
        for s in control_statement.objects.all():
            if '-'.join(s.short_name.split('-', 2)[0:2]) == c.short_name:
                c.control_statements.add(s)
                c.save()

def run():
    update_short_names()
    link_statements_to_controls()