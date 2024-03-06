import graphene
from apis.schemas import ExpenseType, GroupMemberType, GroupType
from core.models import BaseUser, Category, Expense, Group, GroupMember
from graphql import GraphQLError


class CreateExpenseMutation(graphene.Mutation):
    addExpense = graphene.Field(ExpenseType)

    class Arguments:
        expense_date = graphene.Date(required=True)
        category_id = graphene.ID(required=True)
        description = graphene.String(required=True)
        amount = graphene.Decimal(required=True)
        group_id = graphene.ID(default_value=None)

    def mutate(self, info, group_id, expense_date, category_id, description, amount):
        user = info.context.user
        addexpense = Expense(
            expense_date=expense_date,
            category_id=category_id,
            description=description,
            amount=amount,
            created_by=user
        )

        if group_id is not None:

            group = Group.objects.get(id=group_id)

            if group:
                addexpense.save()
                group.expenses.add(addexpense)
            else:
                raise graphene.GraphQLError(
                    f"Group with id {group_id} does not exist.")

        else:
            addexpense.save()

        return CreateExpenseMutation(addExpense=addexpense)


class CreateGroupMutation(graphene.Mutation):
    createGroup = graphene.Field(GroupType)

    class Arguments:
        name = graphene.String(required=True)

    def mutate(self, info, name):
        # Get the authenticated user
        user = info.context.user

        is_group_exists = Group.objects.filter(name=name, created_by=user)

        if is_group_exists:
            raise GraphQLError(
                f"You have created a group with name {name} already exsist in your group list.")
        else:

            addgroup = Group(
                name=name,
                created_by=user
            )
            addgroup.save()

            return CreateGroupMutation(createGroup=addgroup)


class InviteUsersToGroupMutation(graphene.Mutation):
    inviteGroupMember = graphene.Field(GroupMemberType)  # Change to List type

    class Arguments:
        group_id = graphene.ID(required=True)
        invited_user_id = graphene.ID(required=True)

    def mutate(self, info, group_id, invited_user_id):
        # Get the authenticated user
        invited_by_user = info.context.user

        # Get the group
        group = Group.objects.get(id=group_id)

        # Create GroupMember instances for each invited user
        invited_user = BaseUser.objects.get(id=invited_user_id)

        # Check if user is already invited
        user_already_invited = GroupMember.objects.filter(
            group=group, user=invited_user)

        if not user_already_invited:
            group_member = GroupMember.objects.create(
                group=group,
                invited_by=invited_by_user,
                user=invited_user,
                invitation_accepted=False
            )

            # Return the created group members
            return InviteUsersToGroupMutation(inviteGroupMember=group_member)
        else:

            group_member = GroupMember.objects.get(
                group=group, user=invited_user)
            if group_member.invitation_accepted:
                raise GraphQLError(
                    f"{invited_user} is already invited to this group.")
            else:
                raise GraphQLError(
                    f"{invited_user} is already invited to this group. but not accepted invitation.")
