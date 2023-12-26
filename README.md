# taskgroups-exception-handling
Simple POC for the python 3.11 task-group and exceptions handling for a recognized api responses

Sample Payload 

```json
payload = {
    "primary_requirements": {
        "hashicorp_vault_namespace_name":"namespace_name",
        "ad_group_admins": "admin_group_name",
        "ad_group_reader": "reader_group_name"},
    "add_on_services": {
        "auth_methods": {
            "kubernetes_auth_engine": {"cluster_names":["cluster_name_1", "cluster_name_2"], "kubernetes_namespace": "namespace_name"},
            "ad_auth_engine": True,
            "github_oidc_auth": False,
        },
        "secrets_engines": {
            "ldap_secrets_engine": True
            }
    }
}
```