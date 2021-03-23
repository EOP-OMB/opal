# Create your tests here.
from django.test import TestCase
from model_mommy import mommy
import json
from ssp.models.systems import *
from ssp.models.users import *


def test_creation(o):
    t = mommy.make(o)
    TestCase.assertTrue(isinstance(t,o))
    TestCase.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

def compare_model_instance_to_exported_json(json_dict,model_dict,i):
    errors = list()
    for key in json_dict:
        if 1 == 0:
            pass
        # for purposes of this unit test, the object should not have any
        # foreign keys defined so the length of any list objects should be 0
        elif isinstance(json_dict[key], list) and len(json_dict[key]) == 0:
            pass
        # unless, of course, the foreign key is a required field in which case
        # model_mommy will create a child object. In this case we need to fetch
        # the object and compare it's values to the json object
        elif isinstance(json_dict[key], list) and len(json_dict[key]) != 0:
            j_child_dict = json_dict[key]
            c = i._meta.get_field(key)
            c = c.related_model.objects.get(pk=j_child_dict['id'])
            d_child_dict = c.__dict__
            r = compare_model_instance_to_exported_json(j_child_dict,d_child_dict,c)
            if len(r) == 0:
                pass
        # special case for description field
        elif key == "description" and 'desc' in model_dict and str(model_dict['desc']) == str(json_dict[key]):
            pass
        # special case for short-name field
        elif key == "short-name" and 'short_name' in model_dict and str(model_dict['short_name']) == str(json_dict[key]):
            pass
        elif key in model_dict and str(model_dict[key]) == str(json_dict[key]):
            pass
        else:
            errors.append(key)
        return errors


def test_export(o):
    i = mommy.make(o)
    j = json.loads(i.get_serializer_json_OSCAL)[0]
    d = i.__dict__
    return compare_model_instance_to_exported_json(j,d,i)


# models test
class element_propertyTest(TestCase):
    def test_element_property_creation(self):
        t = mommy.make(element_property)
        self.assertTrue(isinstance(t, element_property))
        self.assertEqual(t.__str__(), t.name + ': ' + t.value)

    def test_element_property_export(self):
        errors = test_export(element_property)
        self.assertEqual(','.join(errors),"")


class hashed_valueTest(TestCase):
    def test_hashed_value_creation(self):
        t = mommy.make(hashed_value)
        self.assertTrue(isinstance(t, hashed_value))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(hashed_value)
        self.assertEqual(','.join(errors),"")

class linkTest(TestCase):
    def test_link_creation(self):
        t = mommy.make(link)
        self.assertTrue(isinstance(t, link))
        self.assertEqual(t.__str__(), t.text)

    def test_export(self):
        errors = test_export(link)
        self.assertEqual(','.join(errors),"")


class annotationTest(TestCase):
    def test_annotation_creation(self):
        t = mommy.make(annotation)
        self.assertTrue(isinstance(t, annotation))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(annotation)
        self.assertEqual(','.join(errors),"")


class statusTest(TestCase):
    def test_status_creation(self):
        t = mommy.make(status)
        self.assertTrue(isinstance(t, status))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')
    def test_export(self):
        errors = test_export(status)
        self.assertEqual(','.join(errors),"")

class information_typeTest(TestCase):
    def test_information_type_creation(self):
        t = mommy.make(information_type)
        self.assertTrue(isinstance(t, information_type))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(information_type)
        self.assertEqual(','.join(errors),"")

class attachmentTest(TestCase):
    def test_attachment_creation(self):
        t = mommy.make(attachment)
        self.assertTrue(isinstance(t, attachment))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(attachment)
        self.assertEqual(','.join(errors),"")

class user_functionTest(TestCase):
    def test_user_function_creation(self):
        t = mommy.make(user_function)
        self.assertTrue(isinstance(t, user_function))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(user_function)
        self.assertEqual(','.join(errors),"")

class user_privilegeTest(TestCase):
    def test_user_privilege_creation(self):
        t = mommy.make(user_privilege)
        self.assertTrue(isinstance(t, user_privilege))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(user_privilege)
        self.assertEqual(','.join(errors),"")

class user_roleTest(TestCase):
    def test_user_role_creation(self):
        t = mommy.make(user_role)
        self.assertTrue(isinstance(t, user_role))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(user_role)
        self.assertEqual(','.join(errors),"")

class addressTest(TestCase):
    def test_address_creation(self):
        t = mommy.make(address)
        self.assertTrue(isinstance(t, address))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(address)
        self.assertEqual(','.join(errors),"")

class emailTest(TestCase):
    def test_email_creation(self):
        t = mommy.make(email)
        self.assertTrue(isinstance(t, email))
        self.assertEqual(t.__str__(), t.type + ': ' + t.email)

    def test_export(self):
        errors = test_export(email)
        self.assertEqual(','.join(errors),"")

class telephone_numberTest(TestCase):
    def test_telephone_number_creation(self):
        t = mommy.make(telephone_number)
        self.assertTrue(isinstance(t, telephone_number))
        self.assertEqual(t.__str__(), t.type + ': ' + t.number)

    def test_export(self):
        errors = test_export(telephone_number)
        self.assertEqual(','.join(errors),"")


class locationTest(TestCase):
    def test_location_creation(self):
        t = mommy.make(location)
        self.assertTrue(isinstance(t, location))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(location)
        self.assertEqual(','.join(errors),"")

class organizationTest(TestCase):
    def test_organization_creation(self):
        t = mommy.make(organization)
        self.assertTrue(isinstance(t, organization))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(organization)
        self.assertEqual(','.join(errors),"")


class personTest(TestCase):
    def test_person_creation(self):
        t = mommy.make(person)
        self.assertTrue(isinstance(t, person))
        self.assertEqual(t.__str__(), t.name)

    def test_export(self):
        errors = test_export(person)
        self.assertEqual(','.join(errors),"")

class nist_control_parameterTest(TestCase):
    def test_nist_control_parameter_creation(self):
        t = mommy.make(nist_control_parameter)
        self.assertTrue(isinstance(t, nist_control_parameter))
        self.assertEqual(t.__str__(), t.param_id)


class nist_control_statementTest(TestCase):
    def test_nist_control_statement_creation(self):
        t = mommy.make(nist_control_statement)
        self.assertTrue(isinstance(t, nist_control_statement))
        self.assertEqual(t.__str__(), t.nist_control.label + ' - ' + t.statement_type.capitalize())


class nist_controlTest(TestCase):
    def test_nist_control_creation(self):
        t = mommy.make(nist_control)
        self.assertTrue(isinstance(t, nist_control))
        self.assertEqual(t.__str__(), '(' + str(t.catalog) + ')' + t.long_title)


class control_baselineTest(TestCase):
    def test_control_baseline_creation(self):
        t = mommy.make(control_baseline)
        self.assertTrue(isinstance(t, control_baseline))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(control_baseline)
        self.assertEqual(','.join(errors),"")

class control_statementTest(TestCase):
    def test_control_statement_creation(self):
        t = mommy.make(control_statement)
        self.assertTrue(isinstance(t, control_statement))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(control_statement)
        self.assertEqual(','.join(errors),"")

class control_parameterTest(TestCase):
    def test_control_parameter_creation(self):
        t = mommy.make(control_parameter)
        self.assertTrue(isinstance(t, control_parameter))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(control_parameter)
        self.assertEqual(','.join(errors),"")


class system_controlTest(TestCase):
    def test_system_control_creation(self):
        t = mommy.make(system_control)
        self.assertTrue(isinstance(t, system_control))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(system_control)
        self.assertEqual(','.join(errors),"")


class continuous_monitoring_action_itemTest(TestCase):
    def test_continuous_monitoring_action_item_creation(self):
        t = mommy.make(continuous_monitoring_action_item)
        self.assertTrue(isinstance(t, continuous_monitoring_action_item))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


class import_catalogTest(TestCase):
    def test_import_catalog_creation(self):
        t = mommy.make(import_catalog)
        self.assertTrue(isinstance(t, import_catalog))
        self.assertEqual(t.__str__(), t.title)


class system_componentTest(TestCase):
    def test_system_component_creation(self):
        t = mommy.make(system_component)
        self.assertTrue(isinstance(t, system_component))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(system_component)
        self.assertEqual(','.join(errors),"")


class port_rangeTest(TestCase):
    def test_port_range_creation(self):
        t = mommy.make(port_range)
        self.assertTrue(isinstance(t, port_range))
        self.assertEqual(t.__str__(), str(t.start) + '-' + str(t.end) + ' ' + t.transport)

    def test_export(self):
        errors = test_export(port_range)
        self.assertEqual(','.join(errors),"")

class protocolTest(TestCase):
    def test_protocol_creation(self):
        t = mommy.make(protocol)
        self.assertTrue(isinstance(t, protocol))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(protocol)
        self.assertEqual(','.join(errors),"")

class system_serviceTest(TestCase):
    def test_system_service_creation(self):
        t = mommy.make(system_service)
        self.assertTrue(isinstance(t, system_service))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(system_service)
        self.assertEqual(','.join(errors),"")

class system_interconnectionTest(TestCase):
    def test_system_interconnection_creation(self):
        t = mommy.make(system_interconnection)
        self.assertTrue(isinstance(t, system_interconnection))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(system_interconnection)
        self.assertEqual(','.join(errors),"")

class inventory_item_typeTest(TestCase):
    def test_inventory_item_type_creation(self):
        t = mommy.make(inventory_item_type)
        self.assertTrue(isinstance(t, inventory_item_type))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(inventory_item_type)
        self.assertEqual(','.join(errors),"")


class system_inventory_itemTest(TestCase):
    def test_system_inventory_item_creation(self):
        t = mommy.make(system_inventory_item)
        self.assertTrue(isinstance(t, system_inventory_item))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(system_inventory_item)
        self.assertEqual(','.join(errors),"")


class system_userTest(TestCase):
    def test_system_user_creation(self):
        t = mommy.make(system_user)
        self.assertTrue(isinstance(t, system_user))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(system_user)
        self.assertEqual(','.join(errors),"")


class system_security_planTest(TestCase):
    def test_system_security_plan_creation(self):
        t = mommy.make(system_security_plan)
        self.assertTrue(isinstance(t, system_security_plan))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')

    def test_export(self):
        errors = test_export(system_security_plan)
        self.assertEqual(','.join(errors),"")