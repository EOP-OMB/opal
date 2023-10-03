from django.urls import reverse
import pytest

from model_bakery import baker
# Add generators for custom field types
from model_bakery.random_gen import gen_m2m, gen_string, gen_text

from catalog.models import controls

baker.generators.add('common.models.ShortTextField', gen_string)
baker.generators.add('ckeditor.fields.RichTextField', gen_text)
baker.generators.add('common.models.properties_field', gen_m2m)

pytestmark = pytest.mark.django_db


def test_imports_model():
    imp = baker.make('ctrl_profile.imports',make_m2m=True, href="http://example.com/", import_type="catalog", include_all="True")
    # baker.make('catalog.controls',_quantity=10)
    assert type(imp.to_html()) is str
    assert imp.__str__() == 'http://example.com/'
    # test include only subset of controls
    imp2 = baker.make('ctrl_profile.imports',make_m2m=True,include_all="False")
    assert type(imp2.to_html()) is str
    # test exclude subset of controls
    imp3 = baker.make('ctrl_profile.imports',make_m2m=True, include_all="False",)
    for c in controls.objects.all():
        imp3.exclude_controls.add(c.id)
        imp3.save()
    assert type(imp3.to_html()) is str
    


def test_profiles_model():
    test_profile = baker.make('ctrl_profile.ctrl_profiles',make_m2m=True,_fill_optional=True)
    assert type(test_profile.list_all_controls()) is list
    assert type(test_profile.to_html()) is str



