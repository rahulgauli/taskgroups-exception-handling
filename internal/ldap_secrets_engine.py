async def create_ldap_auth_engine():
    print("create_ldap_auth_engine")

    return "ldap_auth_engine"

async def configure_ldap_auth_engine():
    print("configure_ldap_auth_engine")
    return "configure_ldap_auth_engine"

ldap_secrets_engine_methods = [ create_ldap_auth_engine, configure_ldap_auth_engine ]