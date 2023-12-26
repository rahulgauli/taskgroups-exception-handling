

from pydantic import BaseModel, ConfigDict, Field, constr, field_validator
from typing import ClassVar, List, Union
from internal.kubernetes_auth import k8s_authentication_methods
from internal.github_oidc_auth import github_oidc_methods
from internal.ad_auth_engine import ad_auth_engine_methods
from internal.ldap_secrets_engine import ldap_secrets_engine_methods


class TaskGroup:
    add_on_services_task_list = {}

    @staticmethod
    def clean_task_group():
        TaskGroup.add_on_services_task_list = {} 
    
class KubernetesAuthEngineSchema(BaseModel):
    cluster_names: List[str]
    kubernetes_namespace: str
    
    @field_validator('cluster_names')
    def check_cluster_names_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError('cluster_names must contain at least one value')
        return v
    

class GithubOidcAuthSchema(BaseModel):
    url_pattern: ClassVar[str] =r'^https://github.com/RRInternal/'
    repository_url: constr = Field(..., pattern=url_pattern)


class AuthEnginesSchema(BaseModel, TaskGroup):
    model_config = ConfigDict(arbitrary_types_allowed=True, use_enum_values=True)

    kubernetes_auth_engine: Union[bool, KubernetesAuthEngineSchema] = False
    ad_auth_engine: bool = False
    github_oidc_auth: Union[bool, GithubOidcAuthSchema] = False
    
    @field_validator('kubernetes_auth_engine')
    def check_for_unwanted_attribute(cls, v):
        if isinstance(v, bool) and v:
            raise ValueError("kubernetes_auth_engine must be either False or an instance of KubernetesAuthEngine")
        return v
    
    @field_validator('github_oidc_auth')
    def check_for_unwanted_attribut(cls, v):
        if isinstance(v, bool) and v:
            raise ValueError("github_oidc_auth must be either False or an instance of GithubOidcAuth")
    
    def __init__(self, **data):
        super().__init__(**data)
        self.post_initialization()

    def post_initialization(self):
        if self.kubernetes_auth_engine:
            TaskGroup.add_on_services_task_list["k8s_authentication_task_group"]=k8s_authentication_methods
        if self.ad_auth_engine:
            TaskGroup.add_on_services_task_list["ad_auth_engine_task_group"]=ad_auth_engine_methods
        if self.github_oidc_auth:
            TaskGroup.add_on_services_task_list["github_oidc_auth_task_group"]:github_oidc_methods
         

class SecretsEnginesSchema(BaseModel, TaskGroup):
    ldap_secrets_engine: bool = False

    def __init__(self, **data):
        super().__init__(**data)
        self.post_initialization()

    def post_initialization(self):
        if self.ldap_secrets_engine:
            TaskGroup.add_on_services_task_list["ldap_secrets_engine_task_group"]=ldap_secrets_engine_methods


class AddOnServicesSchema(BaseModel):
    auth_methods: AuthEnginesSchema
    secrets_engines: SecretsEnginesSchema

class PrimaryRequirementsSchema(BaseModel):
    hashicorp_vault_namespace_name: str
    ad_group_admins: str
    ad_group_reader: str


class RequestBodySchema(BaseModel, TaskGroup):
    primary_requirements: PrimaryRequirementsSchema
    add_on_services: AddOnServicesSchema

    # def __init__(self, **data):
    #     super().__init__(**data)
    #     self.post_initialization()

    

       


# request_body = RequestBodySchema(**payload)
# print(request_body)
# print("######")
# print(request_body.primary_requirements)
# print("######")
# print(request_body.add_on_services)
# print("######")
# print(request_body.add_on_services.auth_methods)
# print("######")
# print(request_body.add_on_services.auth_methods.kubernetes_auth_engine)
# print("######")
# # print(request_body.add_on_services.auth_methods.kubernetes_auth_engine.cluster_names)
# print("######")
# # print(request_body.add_on_services.auth_methods.kubernetes_auth_engine.kubernetes_namespace)
# print("######")
# print(request_body.add_on_services.auth_methods.ad_auth_engine)
# print("######")
# print(request_body.add_on_services.secrets_engines)
# print("######")
# print(request_body.add_on_services.secrets_engines.ldap_secrets_engine)
# print("######")
# print(request_body.primary_requirements.hashicorp_vault_namespace_name)
# print("######")
# print(request_body.primary_requirements.ad_group_admins)
# print("######")
# print(request_body.primary_requirements.ad_group_reader)
# print(add_on_services)

