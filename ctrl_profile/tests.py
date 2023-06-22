from django.urls import reverse
import pytest

from model_bakery import baker
# Add generators for custom field types
from model_bakery.random_gen import gen_m2m, gen_string, gen_text
baker.generators.add('common.models.ShortTextField', gen_string)
baker.generators.add('ckeditor.fields.RichTextField', gen_text)
baker.generators.add('common.models.properties_field', gen_m2m)

pytestmark = pytest.mark.django_db


def test_imports_model():
    imp = baker.make('ctrl_profile.imports',make_m2m=True, href="http://example.com/", import_type="catalog", include_all="True",)
    assert type(imp.to_html()) is str
    assert imp.__str__() == 'http://example.com/'


def test_profiles_model():
    test_profile = baker.make('ctrl_profile.profiles',make_m2m=True,_fill_optional=True)
    assert type(test_profile.list_all_controls()) is list
    assert type(test_profile.to_html()) is str
    assert test_profile.__str__ == test_profile.metadata.title



