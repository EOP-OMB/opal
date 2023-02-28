import json
import pytest
from model_bakery import baker

from component.models import components, control_implementations, implemented_requirements
from catalog.models import controls

# Add generators for custom field types
from model_bakery.random_gen import gen_string, gen_text
baker.generators.add('common.models.ShortTextField', gen_string)
baker.generators.add('ckeditor.fields.RichTextField', gen_text)

pytestmark = pytest.mark.django_db

def test_component_model():
    test_cmp = components.objects.create(type='hardware',title='A computer',description='A computer is a machine or device that performs processes, calculations and operations based on instructions provided by a software or hardware program.', purpose='computing',status='other')
    assert test_cmp.to_html() == "<h1>A computer</h1><a href='/admin/component/components/%s/change/'>Edit</a><div>Purpose: computing</div><div>Type: hardware</div><div>A computer is a machine or device that performs processes, calculations and operations based on instructions provided by a software or hardware program.</div>" % test_cmp.id
    test_ctrl = controls.objects.get(control_id='s1.1.1')
    test_ir = implemented_requirements.objects.create(control_id=test_ctrl)
    test_ci = control_implementations.objects.create(description='test control implementation',component=test_cmp)
    test_ci.implemented_requirements.add(test_ir)
    assert test_cmp.list_implemented_controls() == [test_ctrl]
    assert test_cmp.to_html() == "<h1>A computer</h1><a href='/admin/component/components/%s/change/'>Edit</a><div>Purpose: computing</div><div>Type: hardware</div><div>A computer is a machine or device that performs processes, calculations and operations based on instructions provided by a software or hardware program.</div><div class='container' style='margin-left: 0; margin-right: 0; background-color: greenyellow;'><div class='row justify-content-start'><div class='col-sm-10' style='text-align: start;'><h2>Implemented Controls</h2></div></div></div><div class='control_implementation'><h3>test control implementation</h3><div class='implemented_requirement'><a id=s1.1.1><h4>S1.1.1 - Information security roles and responsibilities ()</h4>All information security responsibilities should be defined and allocated.\n\nA value has been assigned to {{ insert: param, s1.1.1-prm11 }}.\n\nA cross link has been established with a choppy syntax: [(choppy)](#s1.2).<br>\n<h5>Guidance</h5><p></p>&nbsp;&nbsp;Allocation of information security responsibilities should be done in accordance with the information security policies. Responsibilities for the protection of individual assets and for carrying out specific information security processes should be identified. Responsibilities for information security risk management activities and in particular for acceptance of residual risks should be defined. These responsibilities should be supplemented, where necessary, with more detailed guidance for specific sites and information processing facilities. Local responsibilities for the protection of assets and for carrying out specific security processes should be defined.<br>\n&nbsp;&nbsp;Individuals with allocated information security responsibilities may delegate security tasks to others. Nevertheless they remain accountable and should determine that any delegated tasks have been correctly performed.<br>\n&nbsp;&nbsp;Areas for which individuals are responsible should be stated. In particular the following should take place:\n\n1. the assets and information security processes should be identified and defined;\n1. the entity responsible for each asset or information security process should be assigned and the details of this responsibility should be documented;\n1. authorization levels should be defined and documented;\n1. to be able to fulfil responsibilities in the information security area the appointed individuals should be competent in the area and be given opportunities to keep up to date with developments;\n1. coordination and oversight of information security aspects of supplier relationships should be identified and documented.\n<br>\n<div><strong>Related Controls:</strong><br></div><p><strong>References:</strong> </p></div></div>" % test_cmp.id




