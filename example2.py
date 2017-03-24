from os_hotgen import composer
from os_hotgen import heat


baseline_name = 'Test1'
swift_url = 'http://swift:8080/v1/AUTH_abcd'
appdb_file_url = '{0}/{1}/appdb.json'.format(swift_url, baseline_name)
subtmpl_url = '{0}/Common/Subtemplate.yaml'.format(swift_url)
app_base_url = '{0}/{1}/application'.format(swift_url, baseline_name)

tmpl = heat.Template(description='Test')

# add app parameter
app_param = heat.Parameter(name='application', type='string')
app_constraint = heat.ParameterConstraint('allowed_values', ['A', 'B'])
app_param.add_constraint(app_constraint)
app_param.default = 'A'
tmpl.add_parameter(app_param)

# add resource section
subtmpl = heat.Resource('subtemplate', subtmpl_url)

app_db_prop= heat.ResourceProperty('appdb', heat.FnGetFile(appdb_file_url))
subtmpl.add_property(app_db_prop)

app_version_prop= heat.ResourceProperty('appversion', heat.FnGetParam('application'))
subtmpl.add_property(app_version_prop)

tmpl.add_resource(subtmpl)

# add output section

# get pn details for selected application parameter from appdb.json
app_label = heat.FnGetParam('application')
appdb_file = heat.FnGetFile(appdb_file_url)
app_details = heat.FnFuncSelect(app_label, appdb_file)

# extract app name from application details
app_name = heat.FnFuncSelect('url', app_details)

# construct app_url
app_url = heat.FnListJoin('/', [app_base_url, app_name])

# create app_output section
app_output = heat.Output('Application Download', app_url, '')
tmpl.add_output(app_output)

# ip attribute
ip_attr = heat.FnGetAttr('subtemplate', 'ip')
ip = heat.Output('ip', ip_attr, '')
tmpl.add_output(ip)


print composer.compose_template(tmpl)