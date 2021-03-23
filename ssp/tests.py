# Create your tests here.
from django.test import TestCase
from model_mommy import mommy

from ssp.models.systems import *
from ssp.models.users import *


# models test
class element_propertyTest(TestCase):

    def test_element_property_creation(self):
        t = mommy.make(element_property)
        self.assertTrue(isinstance(t, element_property))
        self.assertEqual(t.__str__(), t.name + ': ' + t.value)


class hashed_valueTest(TestCase):
    def test_hashed_value_creation(self):
        t = mommy.make(hashed_value)
        self.assertTrue(isinstance(t, hashed_value))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


class linkTest(TestCase):
    def test_link_creation(self):
        t = mommy.make(link)
        self.assertTrue(isinstance(t, link))
        self.assertEqual(t.__str__(), t.text)


class annotationTest(TestCase):
    def test_annotation_creation(self):
        t = mommy.make(annotation)
        self.assertTrue(isinstance(t, annotation))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


class statusTest(TestCase):
    def test_status_creation(self):
        t = mommy.make(status)
        self.assertTrue(isinstance(t, status))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


class information_typeTest(TestCase):
    def test_information_type_creation(self):
        t = mommy.make(information_type)
        self.assertTrue(isinstance(t, information_type))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


class attachmentTest(TestCase):
    def test_attachment_creation(self):
        t = mommy.make(attachment)
        self.assertTrue(isinstance(t, attachment))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


class user_functionTest(TestCase):
    def test_user_function_creation(self):
        t = mommy.make(user_function)
        self.assertTrue(isinstance(t, user_function))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


class user_privilegeTest(TestCase):
    def test_user_privilege_creation(self):
        t = mommy.make(user_privilege)
        self.assertTrue(isinstance(t, user_privilege))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


class user_roleTest(TestCase):
    def test_user_role_creation(self):
        t = mommy.make(user_role)
        self.assertTrue(isinstance(t, user_role))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


class addressTest(TestCase):
    def test_address_creation(self):
        t = mommy.make(address)
        self.assertTrue(isinstance(t, address))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


class emailTest(TestCase):
    def test_email_creation(self):
        t = mommy.make(email)
        self.assertTrue(isinstance(t, email))
        self.assertEqual(t.__str__(), t.type + ': ' + t.email)


class telephone_numberTest(TestCase):
    def test_telephone_number_creation(self):
        t = mommy.make(telephone_number)
        self.assertTrue(isinstance(t, telephone_number))
        self.assertEqual(t.__str__(), t.type + ': ' + t.number)


class locationTest(TestCase):
    def test_location_creation(self):
        t = mommy.make(location)
        self.assertTrue(isinstance(t, location))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


class organizationTest(TestCase):
    def test_organization_creation(self):
        t = mommy.make(organization)
        self.assertTrue(isinstance(t, organization))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


class personTest(TestCase):
    def test_person_creation(self):
        t = mommy.make(person)
        self.assertTrue(isinstance(t, person))
        self.assertEqual(t.__str__(), t.name)


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


class control_statementTest(TestCase):
    def test_control_statement_creation(self):
        t = mommy.make(control_statement)
        self.assertTrue(isinstance(t, control_statement))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


class control_parameterTest(TestCase):
    def test_control_parameter_creation(self):
        t = mommy.make(control_parameter)
        self.assertTrue(isinstance(t, control_parameter))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


class system_controlTest(TestCase):
    def test_system_control_creation(self):
        t = mommy.make(system_control)
        self.assertTrue(isinstance(t, system_control))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


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


class port_rangeTest(TestCase):
    def test_port_range_creation(self):
        t = mommy.make(port_range)
        self.assertTrue(isinstance(t, port_range))
        self.assertEqual(t.__str__(), str(t.start) + '-' + str(t.end) + ' ' + t.transport)


class protocolTest(TestCase):
    def test_protocol_creation(self):
        t = mommy.make(protocol)
        self.assertTrue(isinstance(t, protocol))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


class system_serviceTest(TestCase):
    def test_system_service_creation(self):
        t = mommy.make(system_service)
        self.assertTrue(isinstance(t, system_service))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


class system_interconnectionTest(TestCase):
    def test_system_interconnection_creation(self):
        t = mommy.make(system_interconnection)
        self.assertTrue(isinstance(t, system_interconnection))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


class inventory_item_typeTest(TestCase):
    def test_inventory_item_type_creation(self):
        t = mommy.make(inventory_item_type)
        self.assertTrue(isinstance(t, inventory_item_type))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


class system_inventory_itemTest(TestCase):
    def test_system_inventory_item_creation(self):
        t = mommy.make(system_inventory_item)
        self.assertTrue(isinstance(t, system_inventory_item))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


class system_userTest(TestCase):
    def test_system_user_creation(self):
        t = mommy.make(system_user)
        self.assertTrue(isinstance(t, system_user))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')


class system_security_planTest(TestCase):
    def test_system_security_plan_creation(self):
        t = mommy.make(system_security_plan)
        self.assertTrue(isinstance(t, system_security_plan))
        self.assertEqual(t.__str__(), t.title + ' (' + t.short_name + ')')
