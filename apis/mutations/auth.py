import logging
import graphene
from graphql_jwt import JSONWebTokenMutation

from django.utils import timezone

from apis.schemas import BaseUserType
from core.models import BaseUser


class Login(JSONWebTokenMutation):
    me = graphene.Field(BaseUserType)
    # redirect_to = graphene.String()

    class Arguments:
        username = graphene.String()
        password = graphene.String()

    @classmethod
    def resolve(cls, root, info, **kwargs):
        user = info.context.user
        logging.info(f"User with username {user.username} attempted to log in at {timezone.now()}")
        user.last_login = timezone.now()
        user.save()
        logging.info(
            f"User with username {user.username} logged in successfully at {timezone.now()}"
        )
        return cls(me=info.context.user)
    
class SignUp(graphene.Mutation):
    me = graphene.Field(BaseUserType)

    class Arguments:
        username = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        phone_number = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, username, first_name, last_name, phone_number, email, password):
        # Perform user creation logic here
        user = BaseUser(
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email
        )
        user.set_password(password)
        user.save()

        # Return the created user in the response
        return SignUp(me=user)