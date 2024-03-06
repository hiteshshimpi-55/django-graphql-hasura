import graphene
from apis.schemas import CategoryType, ExpenseFilterInput, ExpenseType, GroupType
from core.models import Category, Expense, Group
from graphql_jwt.decorators import login_required
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


class AllCategoryQuery:
    AllCategories = graphene.List(CategoryType)

    @login_required
    def resolve_AllCategories(self, info, **kwargs):
        return Category.objects.all()


class UserExpenseQuery:

    myExpenses = graphene.List(
        ExpenseType,
        date_lte=graphene.Date(),
        date_gte=graphene.Date(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    myTotalExpensesAggregate = graphene.Float(
        date_lte=graphene.Date(),
        date_gte=graphene.Date(),


    )

    myGroupExpenses = graphene.List(
        ExpenseType, group_id=graphene.Int(), filter=ExpenseFilterInput())

    def resolve_myExpenses(self, info, date_lte=None, date_gte=None, offset=None, limit=None, **kwargs):
        user = info.context.user
        queryset = Expense.objects.filter(
            created_by_id=user.id, expense_date__lte=date_lte, expense_date__gte=date_gte)
        queryset = queryset.order_by('-expense_date')  # Descending order by ID

        paginator = Paginator(queryset, limit)

        try:
            expenses_page = paginator.page(offset)
        except PageNotAnInteger:
            expenses_page = paginator.page(1)
        except EmptyPage:
            expenses_page = paginator.page(paginator.num_pages)

        return expenses_page.object_list

    def resolve_myTotalExpensesAggregate(self, info, date_lte=None, date_gte=None, **kwargs):
        user = info.context.user
        total_expenses = Expense.objects.filter(
            created_by_id=user.id, expense_date__lte=date_lte, expense_date__gte=date_gte).aggregate(Sum('amount'))
        total_amount = total_expenses['amount__sum']
        return total_amount

    @login_required
    def resolve_myGroupExpenses(self, info, group_id=None, filter=None):
        user = info.context.user

        expenses = Expense.objects.filter(created_by=user)

        if group_id:
            expenses = expenses.filter(groups__id=group_id)

        if filter:
            from_date = filter.get('from_date')
            to_date = filter.get('to_date')

            if from_date:
                expenses = expenses.filter(expense_date__gte=from_date)

            if to_date:
                expenses = expenses.filter(expense_date__lte=to_date)

        return expenses


class UserGroupQuery:
    myGroups = graphene.List(GroupType, from_date=graphene.Date(
        required=False), to_date=graphene.Date(required=False))

    @login_required
    def resolve_myGroups(self, info, from_date=None, to_date=None):
        user = info.context.user
        groups = Group.objects.filter(expenses__created_by=user).distinct()

        for group in groups:
            expenses_query = Expense.objects.filter(groups=group)

            if from_date:
                expenses_query = expenses_query.filter(
                    expense_date__gte=from_date)

            if to_date:
                expenses_query = expenses_query.filter(
                    expense_date__lte=to_date)

            total_expense = expenses_query.aggregate(
                total=Sum('amount'))['total']
            group.total_expense = total_expense or 0

        return groups
