async def create_k8s_auth_engine():
    print("create_k8s_auth_engine")
    return "k8s_auth_engine"

async def configure_k8s_auth_engine():
    print("configure_k8s_auth_engine")
    return "configure_k8s_auth_engine"


k8s_authentication_methods = [ create_k8s_auth_engine, configure_k8s_auth_engine ]
