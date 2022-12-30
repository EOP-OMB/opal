import logging

from django.conf import settings
from django.core.management import BaseCommand

from catalog.models import catalogs
from catalog.views import download_catalog
from common.models import props, metadata
from component.models import implemented_requirements
from ctrl_profile.models import profiles, imports

low = ['AC-01-00', 'AC-02-00', 'AC-03-00', 'AC-07-00', 'AC-08-00', 'AC-14-00', 'AC-17-00', 'AC-18-00', 'AC-19-00',
       'AC-20-00', 'AC-22-00', 'AT-01-00', 'AT-02-00', 'AT-02-02', 'AT-03-00', 'AT-04-00', 'AU-01-00', 'AU-02-00',
       'AU-03-00', 'AU-04-00', 'AU-05-00', 'AU-06-00', 'AU-08-00', 'AU-09-00', 'AU-11-00', 'AU-12-00', 'CA-01-00',
       'CA-02-00', 'CA-03-00', 'CA-05-00', 'CA-06-00', 'CA-07-00', 'CA-07-04', 'CA-09-00', 'CM-01-00', 'CM-02-00',
       'CM-04-00', 'CM-05-00', 'CM-06-00', 'CM-07-00', 'CM-08-00', 'CM-10-00', 'CM-11-00', 'CP-01-00', 'CP-02-00',
       'CP-03-00', 'CP-04-00', 'CP-09-00', 'CP-10-00', 'IA-01-00', 'IA-02-00', 'IA-02-01', 'IA-02-02', 'IA-02-08',
       'IA-02-12', 'IA-04-00', 'IA-05-00', 'IA-05-01', 'IA-06-00', 'IA-07-00', 'IA-08-00', 'IA-08-01', 'IA-08-02',
       'IA-08-04', 'IA-11-00', 'IR-01-00', 'IR-02-00', 'IR-04-00', 'IR-05-00', 'IR-06-00', 'IR-07-00', 'IR-08-00',
       'MA-01-00', 'MA-02-00', 'MA-04-00', 'MA-05-00', 'MP-01-00', 'MP-02-00', 'MP-06-00', 'MP-07-00', 'PE-01-00',
       'PE-02-00', 'PE-03-00', 'PE-06-00', 'PE-08-00', 'PE-12-00', 'PE-13-00', 'PE-14-00', 'PE-15-00', 'PE-16-00',
       'PL-01-00', 'PL-02-00', 'PL-04-00', 'PL-04-01', 'PL-10-00', 'PL-11-00', 'PS-01-00', 'PS-02-00', 'PS-03-00',
       'PS-04-00', 'PS-05-00', 'PS-06-00', 'PS-07-00', 'PS-08-00', 'PS-09-00', 'RA-01-00', 'RA-02-00', 'RA-03-00',
       'RA-03-01', 'RA-05-00', 'RA-05-02', 'RA-05-11', 'RA-07-00', 'SA-01-00', 'SA-02-00', 'SA-03-00', 'SA-04-00',
       'SA-04-10', 'SA-05-00', 'SA-08-00', 'SA-09-00', 'SA-22-00', 'SC-01-00', 'SC-05-00', 'SC-07-00', 'SC-12-00',
       'SC-13-00', 'SC-15-00', 'SC-20-00', 'SC-21-00', 'SC-22-00', 'SC-39-00', 'SI-01-00', 'SI-02-00', 'SI-03-00',
       'SI-04-00', 'SI-05-00', 'SI-12-00', 'SR-01-00', 'SR-02-00', 'SR-02-01', 'SR-03-00', 'SR-05-00', 'SR-08-00',
       'SR-10-00', 'SR-11-00', 'SR-11-01', 'SR-11-02', 'SR-12-00']
moderate = ['AC-01-00', 'AC-02-00', 'AC-02-01', 'AC-02-02', 'AC-02-03', 'AC-02-04', 'AC-02-05', 'AC-02-13', 'AC-03-00',
            'AC-04-00', 'AC-05-00', 'AC-06-00', 'AC-06-01', 'AC-06-02', 'AC-06-05', 'AC-06-07', 'AC-06-09', 'AC-06-10',
            'AC-07-00', 'AC-08-00', 'AC-11-00', 'AC-11-01', 'AC-12-00', 'AC-14-00', 'AC-17-00', 'AC-17-01', 'AC-17-02',
            'AC-17-03', 'AC-17-04', 'AC-18-00', 'AC-18-01', 'AC-18-03', 'AC-19-00', 'AC-19-05', 'AC-20-00', 'AC-20-01',
            'AC-20-02', 'AC-21-00', 'AC-22-00', 'AT-01-00', 'AT-02-00', 'AT-02-02', 'AT-02-03', 'AT-03-00', 'AT-04-00',
            'AU-01-00', 'AU-02-00', 'AU-03-00', 'AU-03-01', 'AU-04-00', 'AU-05-00', 'AU-06-00', 'AU-06-01', 'AU-06-03',
            'AU-07-00', 'AU-07-01', 'AU-08-00', 'AU-09-00', 'AU-09-04', 'AU-11-00', 'AU-12-00', 'CA-01-00', 'CA-02-00',
            'CA-02-01', 'CA-03-00', 'CA-05-00', 'CA-06-00', 'CA-07-00', 'CA-07-01', 'CA-07-04', 'CA-09-00', 'CM-01-00',
            'CM-02-00', 'CM-02-02', 'CM-02-03', 'CM-02-07', 'CM-03-00', 'CM-03-02', 'CM-03-04', 'CM-04-00', 'CM-04-02',
            'CM-05-00', 'CM-06-00', 'CM-07-00', 'CM-07-01', 'CM-07-02', 'CM-07-05', 'CM-08-00', 'CM-08-01', 'CM-08-03',
            'CM-09-00', 'CM-10-00', 'CM-11-00', 'CM-12-00', 'CM-12-01', 'CP-01-00', 'CP-02-00', 'CP-02-01', 'CP-02-03',
            'CP-02-08', 'CP-03-00', 'CP-04-00', 'CP-04-01', 'CP-06-00', 'CP-06-01', 'CP-06-03', 'CP-07-00', 'CP-07-01',
            'CP-07-02', 'CP-07-03', 'CP-08-00', 'CP-08-01', 'CP-08-02', 'CP-09-00', 'CP-09-01', 'CP-09-08', 'CP-10-00',
            'CP-10-02', 'IA-01-00', 'IA-02-00', 'IA-02-01', 'IA-02-02', 'IA-02-08', 'IA-02-12', 'IA-03-00', 'IA-04-00',
            'IA-04-04', 'IA-05-00', 'IA-05-01', 'IA-05-02', 'IA-05-06', 'IA-06-00', 'IA-07-00', 'IA-08-00', 'IA-08-01',
            'IA-08-02', 'IA-08-04', 'IA-11-00', 'IA-12-00', 'IA-12-02', 'IA-12-03', 'IA-12-05', 'IR-01-00', 'IR-02-00',
            'IR-03-00', 'IR-03-02', 'IR-04-00', 'IR-04-01', 'IR-05-00', 'IR-06-00', 'IR-06-01', 'IR-06-03', 'IR-07-00',
            'IR-07-01', 'IR-08-00', 'MA-01-00', 'MA-02-00', 'MA-03-00', 'MA-03-01', 'MA-03-02', 'MA-03-03', 'MA-04-00',
            'MA-05-00', 'MA-06-00', 'MP-01-00', 'MP-02-00', 'MP-03-00', 'MP-04-00', 'MP-05-00', 'MP-06-00', 'MP-07-00',
            'PE-01-00', 'PE-02-00', 'PE-03-00', 'PE-04-00', 'PE-05-00', 'PE-06-00', 'PE-06-01', 'PE-08-00', 'PE-09-00',
            'PE-10-00', 'PE-11-00', 'PE-12-00', 'PE-13-00', 'PE-13-01', 'PE-14-00', 'PE-15-00', 'PE-16-00', 'PE-17-00',
            'PL-01-00', 'PL-02-00', 'PL-04-00', 'PL-04-01', 'PL-08-00', 'PL-10-00', 'PL-11-00', 'PS-01-00', 'PS-02-00',
            'PS-03-00', 'PS-04-00', 'PS-05-00', 'PS-06-00', 'PS-07-00', 'PS-08-00', 'PS-09-00', 'RA-01-00', 'RA-02-00',
            'RA-03-00', 'RA-03-01', 'RA-05-00', 'RA-05-02', 'RA-05-05', 'RA-05-11', 'RA-07-00', 'RA-09-00', 'SA-01-00',
            'SA-02-00', 'SA-03-00', 'SA-04-00', 'SA-04-01', 'SA-04-02', 'SA-04-09', 'SA-04-10', 'SA-05-00', 'SA-08-00',
            'SA-09-00', 'SA-09-02', 'SA-10-00', 'SA-11-00', 'SA-15-00', 'SA-15-03', 'SA-22-00', 'SC-01-00', 'SC-02-00',
            'SC-04-00', 'SC-05-00', 'SC-07-00', 'SC-07-03', 'SC-07-04', 'SC-07-05', 'SC-07-07', 'SC-07-08', 'SC-08-00',
            'SC-08-01', 'SC-10-00', 'SC-12-00', 'SC-13-00', 'SC-15-00', 'SC-17-00', 'SC-18-00', 'SC-20-00', 'SC-21-00',
            'SC-22-00', 'SC-23-00', 'SC-28-00', 'SC-28-01', 'SC-39-00', 'SI-01-00', 'SI-02-00', 'SI-02-02', 'SI-03-00',
            'SI-04-00', 'SI-04-02', 'SI-04-04', 'SI-04-05', 'SI-05-00', 'SI-07-00', 'SI-07-01', 'SI-07-07', 'SI-08-00',
            'SI-08-02', 'SI-10-00', 'SI-11-00', 'SI-12-00', 'SI-16-00', 'SR-01-00', 'SR-02-00', 'SR-02-01', 'SR-03-00',
            'SR-05-00', 'SR-06-00', 'SR-08-00', 'SR-10-00', 'SR-11-00', 'SR-11-01', 'SR-11-02', 'SR-12-00']
high = ['AC-01-00', 'AC-02-00', 'AC-02-01', 'AC-02-02', 'AC-02-03', 'AC-02-04', 'AC-02-05', 'AC-02-11', 'AC-02-12',
        'AC-02-13', 'AC-03-00', 'AC-04-00', 'AC-04-04', 'AC-05-00', 'AC-06-00', 'AC-06-01', 'AC-06-02', 'AC-06-03',
        'AC-06-05', 'AC-06-07', 'AC-06-09', 'AC-06-10', 'AC-07-00', 'AC-08-00', 'AC-10-00', 'AC-11-00', 'AC-11-01',
        'AC-12-00', 'AC-14-00', 'AC-17-00', 'AC-17-01', 'AC-17-02', 'AC-17-03', 'AC-17-04', 'AC-18-00', 'AC-18-01',
        'AC-18-03', 'AC-18-04', 'AC-18-05', 'AC-19-00', 'AC-19-05', 'AC-20-00', 'AC-20-01', 'AC-20-02', 'AC-21-00',
        'AC-22-00', 'AT-01-00', 'AT-02-00', 'AT-02-02', 'AT-02-03', 'AT-03-00', 'AT-04-00', 'AU-01-00', 'AU-02-00',
        'AU-03-00', 'AU-03-01', 'AU-04-00', 'AU-05-00', 'AU-05-01', 'AU-05-02', 'AU-06-00', 'AU-06-01', 'AU-06-03',
        'AU-06-05', 'AU-06-06', 'AU-07-00', 'AU-07-01', 'AU-08-00', 'AU-09-00', 'AU-09-02', 'AU-09-03', 'AU-09-04',
        'AU-10-00', 'AU-11-00', 'AU-12-00', 'AU-12-01', 'AU-12-03', 'CA-01-00', 'CA-02-00', 'CA-02-01', 'CA-02-02',
        'CA-03-00', 'CA-03-06', 'CA-05-00', 'CA-06-00', 'CA-07-00', 'CA-07-01', 'CA-07-04', 'CA-08-00', 'CA-08-01',
        'CA-09-00', 'CM-01-00', 'CM-02-00', 'CM-02-02', 'CM-02-03', 'CM-02-07', 'CM-03-00', 'CM-03-01', 'CM-03-02',
        'CM-03-04', 'CM-03-06', 'CM-04-00', 'CM-04-01', 'CM-04-02', 'CM-05-00', 'CM-05-01', 'CM-06-00', 'CM-06-01',
        'CM-06-02', 'CM-07-00', 'CM-07-01', 'CM-07-02', 'CM-07-05', 'CM-08-00', 'CM-08-01', 'CM-08-02', 'CM-08-03',
        'CM-08-04', 'CM-09-00', 'CM-10-00', 'CM-11-00', 'CM-12-00', 'CM-12-01', 'CP-01-00', 'CP-02-00', 'CP-02-01',
        'CP-02-02', 'CP-02-03', 'CP-02-05', 'CP-02-08', 'CP-03-00', 'CP-03-01', 'CP-04-00', 'CP-04-01', 'CP-04-02',
        'CP-06-00', 'CP-06-01', 'CP-06-02', 'CP-06-03', 'CP-07-00', 'CP-07-01', 'CP-07-02', 'CP-07-03', 'CP-07-04',
        'CP-08-00', 'CP-08-01', 'CP-08-02', 'CP-08-03', 'CP-08-04', 'CP-09-00', 'CP-09-01', 'CP-09-02', 'CP-09-03',
        'CP-09-05', 'CP-09-08', 'CP-10-00', 'CP-10-02', 'CP-10-04', 'IA-01-00', 'IA-02-00', 'IA-02-01', 'IA-02-02',
        'IA-02-05', 'IA-02-08', 'IA-02-12', 'IA-03-00', 'IA-04-00', 'IA-04-04', 'IA-05-00', 'IA-05-01', 'IA-05-02',
        'IA-05-06', 'IA-06-00', 'IA-07-00', 'IA-08-00', 'IA-08-01', 'IA-08-02', 'IA-08-04', 'IA-11-00', 'IA-12-00',
        'IA-12-02', 'IA-12-03', 'IA-12-04', 'IA-12-05', 'IR-01-00', 'IR-02-00', 'IR-02-01', 'IR-02-02', 'IR-03-00',
        'IR-03-02', 'IR-04-00', 'IR-04-01', 'IR-04-04', 'IR-04-11', 'IR-05-00', 'IR-05-01', 'IR-06-00', 'IR-06-01',
        'IR-06-03', 'IR-07-00', 'IR-07-01', 'IR-08-00', 'MA-01-00', 'MA-02-00', 'MA-02-02', 'MA-03-00', 'MA-03-01',
        'MA-03-02', 'MA-03-03', 'MA-04-00', 'MA-04-03', 'MA-05-00', 'MA-05-01', 'MA-06-00', 'MP-01-00', 'MP-02-00',
        'MP-03-00', 'MP-04-00', 'MP-05-00', 'MP-06-00', 'MP-06-01', 'MP-06-02', 'MP-06-03', 'MP-07-00', 'PE-01-00',
        'PE-02-00', 'PE-03-00', 'PE-03-01', 'PE-04-00', 'PE-05-00', 'PE-06-00', 'PE-06-01', 'PE-06-04', 'PE-08-00',
        'PE-08-01', 'PE-09-00', 'PE-10-00', 'PE-11-00', 'PE-11-01', 'PE-12-00', 'PE-13-00', 'PE-13-01', 'PE-13-02',
        'PE-14-00', 'PE-15-00', 'PE-15-01', 'PE-16-00', 'PE-17-00', 'PE-18-00', 'PL-01-00', 'PL-02-00', 'PL-04-00',
        'PL-04-01', 'PL-08-00', 'PL-10-00', 'PL-11-00', 'PS-01-00', 'PS-02-00', 'PS-03-00', 'PS-04-00', 'PS-04-02',
        'PS-05-00', 'PS-06-00', 'PS-07-00', 'PS-08-00', 'PS-09-00', 'RA-01-00', 'RA-02-00', 'RA-03-00', 'RA-03-01',
        'RA-05-00', 'RA-05-02', 'RA-05-04', 'RA-05-05', 'RA-05-11', 'RA-07-00', 'RA-09-00', 'SA-01-00', 'SA-02-00',
        'SA-03-00', 'SA-04-00', 'SA-04-01', 'SA-04-02', 'SA-04-05', 'SA-04-09', 'SA-04-10', 'SA-05-00', 'SA-08-00',
        'SA-09-00', 'SA-09-02', 'SA-10-00', 'SA-11-00', 'SA-15-00', 'SA-15-03', 'SA-16-00', 'SA-17-00', 'SA-21-00',
        'SA-22-00', 'SC-01-00', 'SC-02-00', 'SC-03-00', 'SC-04-00', 'SC-05-00', 'SC-07-00', 'SC-07-03', 'SC-07-04',
        'SC-07-05', 'SC-07-07', 'SC-07-08', 'SC-07-18', 'SC-07-21', 'SC-08-00', 'SC-08-01', 'SC-10-00', 'SC-12-00',
        'SC-12-01', 'SC-13-00', 'SC-15-00', 'SC-17-00', 'SC-18-00', 'SC-20-00', 'SC-21-00', 'SC-22-00', 'SC-23-00',
        'SC-24-00', 'SC-28-00', 'SC-28-01', 'SC-39-00', 'SI-01-00', 'SI-02-00', 'SI-02-02', 'SI-03-00', 'SI-04-00',
        'SI-04-02', 'SI-04-04', 'SI-04-05', 'SI-04-10', 'SI-04-12', 'SI-04-14', 'SI-04-20', 'SI-04-22', 'SI-05-00',
        'SI-05-01', 'SI-06-00', 'SI-07-00', 'SI-07-01', 'SI-07-02', 'SI-07-05', 'SI-07-07', 'SI-07-15', 'SI-08-00',
        'SI-08-02', 'SI-10-00', 'SI-11-00', 'SI-12-00', 'SI-16-00', 'SR-01-00', 'SR-02-00', 'SR-02-01', 'SR-03-00',
        'SR-05-00', 'SR-06-00', 'SR-08-00', 'SR-09-00', 'SR-09-01', 'SR-10-00', 'SR-11-00', 'SR-11-01', 'SR-11-02',
        'SR-12-00']
privacy = ['AC-01-00', 'AC-03-14', 'AT-01-00', 'AT-02-00', 'AT-03-00', 'AT-03-05', 'AT-04-00', 'AU-01-00', 'AU-02-00',
           'AU-03-03', 'AU-11-00', 'CA-01-00', 'CA-02-00', 'CA-05-00', 'CA-06-00', 'CA-07-00', 'CA-07-04', 'CM-01-00',
           'CM-04-00', 'IR-01-00', 'IR-02-00', 'IR-02-03', 'IR-03-00', 'IR-04-00', 'IR-05-00', 'IR-06-00', 'IR-07-00',
           'IR-08-00', 'IR-08-01', 'MP-01-00', 'MP-06-00', 'PE-08-03', 'PL-01-00', 'PL-02-00', 'PL-04-00', 'PL-04-01',
           'PL-08-00', 'PL-09-00', 'PM-03-00', 'PM-04-00', 'PM-05-01', 'PM-06-00', 'PM-07-00', 'PM-08-00', 'PM-09-00',
           'PM-10-00', 'PM-11-00', 'PM-13-00', 'PM-14-00', 'PM-17-00', 'PM-18-00', 'PM-19-00', 'PM-20-00', 'PM-20-01',
           'PM-21-00', 'PM-22-00', 'PM-24-00', 'PM-25-00', 'PM-26-00', 'PM-27-00', 'PM-28-00', 'PM-31-00', 'PS-06-00',
           'PT-01-00', 'PT-02-00', 'PT-03-00', 'PT-04-00', 'PT-05-00', 'PT-05-02', 'PT-06-00', 'PT-06-01', 'PT-06-02',
           'PT-07-00', 'PT-07-01', 'PT-07-02', 'PT-08-00', 'RA-01-00', 'RA-03-00', 'RA-07-00', 'RA-08-00', 'SA-01-00',
           'SA-02-00', 'SA-03-00', 'SA-04-00', 'SA-08-33', 'SA-09-00', 'SA-11-00', 'SC-07-24', 'SI-01-00', 'SI-12-00',
           'SI-12-01', 'SI-12-02', 'SI-12-03', 'SI-18-00', 'SI-18-04', 'SI-19-00']


def import_800_53():
    logger = logging.getLogger('django')
    link = 'https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json'
    catalog_dict = download_catalog(link)
    new_catalog = catalogs()
    oscal_data = catalog_dict
    new_catalog = new_catalog.import_oscal(oscal_data)
    logger.info('Creating implemented_requirement objects for all controls in the import')
    ctrl_list = new_catalog.list_all_controls()
    for ctrl in ctrl_list:
        implemented_requirements.objects.get_or_create(control_id=ctrl)
        ctrl.sort_id = ctrl._get_sort_id
    logger.info('Creating profiles for FISMA baselines')
    create_profile(new_catalog, 'Low', low)
    create_profile(new_catalog, 'Moderate', moderate)
    create_profile(new_catalog, 'High', high)
    create_profile(new_catalog, 'Privacy', privacy)


def create_profile(new_catalog, fips_level, ctrl_list):
    logger = logging.getLogger('django')
    new_metadata, created = metadata.objects.get_or_create(title='SP 800-53 rev 5 FISMA %s Controls' % fips_level)
    new_profile, created = profiles.objects.get_or_create(metadata=new_metadata)
    new_profile.save()
    host = settings.HOST_NAME
    url = "https://" + host + new_catalog.get_permalink()
    new_import, created = imports.objects.get_or_create(href=url, import_type="catalog")
    new_profile.imports.add(new_import)
    new_profile.save()
    for ctrl in ctrl_list:
        i = ctrl.lower()
        if i[6:8] == '00':
            i = i[:5]
        else:
            i = i[:5] + '.' + i[6:8]
        if props.objects.filter(name='sort-id', value=i).count() > 0:
            p = props.objects.filter(name='sort-id', value=i).get()
            if p.controls_set.count() == 1:
                c = p.controls_set.first()
                new_import.include_controls.add(c)
            elif p.controls_set.count() == 0:
                logger.warning("sort-id %s is not assigned to any controls!" % i)
            else:
                logger.warning("No matching property found for sort-id %s" % i)
        else:
            logger.warning("sort-id %s is assigned to more than one control!" % i)


class Command(BaseCommand):
    help = 'Import all 800-53 Rev 5 controls and create profiles for FISMA Low, Moderate, High and for the privacy controls'

    def handle(self, *args, **options):
        import_800_53()
