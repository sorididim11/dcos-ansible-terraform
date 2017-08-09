
curl -X PUT --cacert dcos-ca.crt -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:mesos:master:framework:role:dev-role2/groups/hpe/create
curl -X PUT --cacert dcos-ca.crt -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:mesos:master:reservation:role:dev-role2/groups/hpe/create
curl -X PUT --cacert dcos-ca.crt -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:mesos:master:volume:role:dev-role2/groups/hpe/create
curl -X PUT --cacert dcos-ca.crt -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:mesos:master:task:user:nobody/groups/hpe/create
curl -X PUT --cacert dcos-ca.crt -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:mesos:master:reservation:principal:hpc/groups/hpe/delete
curl -X PUT --cacert dcos-ca.crt -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:mesos:master:task:app_id:%252F/groups/hpe/create
curl -X PUT --cacert dcos-ca.crt -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:mesos:master:volume:principal:hpc/groups/hpe/delete
