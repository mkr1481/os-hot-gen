from os_hotgen import composer
from os_hotgen import heat

tmpl_a = heat.Template(
    description="Sample template generated using os-hot-gen")

param_a = heat.Parameter(name='param_1', type='string')
tmpl_a.add_parameter(param_a)

fn_get_param = heat.FnGetParam(param_a.name)
op_a = heat.Output(name="output_1", value=fn_get_param, description="sample")
tmpl_a.add_output(op_a)

rsc_a = heat.Resource('rsc_1', 'OS::Heat::TestResource')
rsc_a_prp_a = heat.ResourceProperty('value', fn_get_param)
rsc_a.add_property(rsc_a_prp_a)
tmpl_a.add_resource(rsc_a)
print composer.compose_template(tmpl_a)