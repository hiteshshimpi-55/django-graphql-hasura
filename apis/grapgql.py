

import graphene
from graphql_jwt.decorators import login_required

from apis.schemas import BaseUserType
from .mutations import (
    auth,
    mutation
)  #
from .queries import (
    query
)


class MutationMain(graphene.ObjectType):
    login = auth.Login.Field()
    signup = auth.SignUp.Field()
    addExpense=mutation.CreateExpenseMutation.Field()
    createGroup=mutation.CreateGroupMutation.Field()
    inviteGroupMember=mutation.InviteUsersToGroupMutation.Field()


class QueryMain(graphene.ObjectType, query.AllCategoryQuery, query.UserExpenseQuery,query.UserGroupQuery):
    me = graphene.Field(BaseUserType)
    all_categories = graphene.List(query.CategoryType)
    # user_expenses = graphene.List(
    #     query.ExpenseType, date_lte=graphene.Date(), date_gte=graphene.Date())
    # myGroups = graphene.List(
    #     query.GroupType)
    # total_expenses_aggregate = graphene.Float(query.ExpenseType, date_lte=graphene.Date(), date_gte=graphene.Date())


    @login_required
    def resolve_me(self, info):
        return info.context.user
