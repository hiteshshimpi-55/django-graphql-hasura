import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from core.models import BaseUser, Category, Expense,Group,GroupMember
from django.db.models import Sum



class BaseUserType(DjangoObjectType):
    full_name = graphene.String()
    permissions = graphene.List(graphene.String)
    # allowed_roles = graphene.List(graphene.String)
    # documents = graphene.List(DocumentType)
    # external_reference_id = graphene.String()
    # agent = graphene.Field(AgentType)
    # payment_options = graphene.List("actions.schemas.PaymentDetailType")
    # language = graphene.String()

    class Meta:
        model = BaseUser
        exclude_fields = ("password", "is_superuser", "is_staff", "is_active")

    # @login_required
    # def resolve_documents(self, info):
    #     return self.documents.all()

    @login_required
    def resolve_permissions(self, info):
        return list(self.get_all_permissions())

    # @login_required
    # def resolve_allowed_roles(self, info):
    #     return get_allowed_roles(info.context.user)


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class ExpenseType(DjangoObjectType):
    class Meta:
        model = Expense

class GroupMemberType(DjangoObjectType):
    class Meta:
        model = GroupMember
        

class GroupType(DjangoObjectType):
    total_expense = graphene.Float()


    # total_expense = graphene.Float()
    total_members = graphene.Int()
     # Replace 'path.to.ExpenseType' with the actual path to your ExpenseType
    members = graphene.List(GroupMemberType)  # Replace 'path.to.GroupMemberType' with the actual path to your GroupMemberType

    class Meta:
        model = Group

    def resolve_members(self, info, **kwargs):
        return self.members.all() if hasattr(self, 'members') else []
    
   
    


    def resolve_total_members(self, info, **kwargs):
        # Calculate total members for the group
        return self.members.count()
    
class ExpenseFilterInput(graphene.InputObjectType):
    from_date = graphene.Date(required=False)
    to_date = graphene.Date(required=False)

