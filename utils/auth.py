from calendar import timegm
import jwt
import core.models
from datetime import datetime
from graphql_jwt.settings import jwt_settings
from django.conf import settings



def is_valid_role(permission):
    _, name = permission.split(".")
    return name.startswith(settings.PERMISSION_PREFIX) and name.endswith(settings.PERMISSION_SUFFIX)

def permission_to_role(permission):
    return "_".join(permission.split(".")[1].split("_")[1:-1])


def get_allowed_roles(user):
    return user.get_roles()

def get_allowed_roles(user):
    return user.get_roles()


def get_user_groups(user):
    return list(user.groups.values_list("name", flat=True))
    
## JWT payload for Hasura
def payload_handler(
    user, request=None, expiration_delta=jwt_settings.JWT_EXPIRATION_DELTA, context=None
):
    username = user.get_username()

    if hasattr(username, "pk"):
        username = username.pk

    payload = {
        user.USERNAME_FIELD: username,
        "exp": datetime.utcnow() + expiration_delta,
    }

    if jwt_settings.JWT_ALLOW_REFRESH:
        payload["origIat"] = timegm(datetime.utcnow().utctimetuple())

    if jwt_settings.JWT_AUDIENCE is not None:
        payload["aud"] = jwt_settings.JWT_AUDIENCE

    if jwt_settings.JWT_ISSUER is not None:
        payload["iss"] = jwt_settings.JWT_ISSUER

    allowed_roles = get_allowed_roles(user)
    user_groups = get_user_groups(user)
    payload["user_claims"] = {
        "x-hasura-allowed-roles": allowed_roles,
        "x-hasura-default-role": allowed_roles[0] if len(allowed_roles) > 0 else "",
        "x-hasura-user-id": str(user.id),
        "x-kite-auth-groups": user_groups,
    }
    return payload
