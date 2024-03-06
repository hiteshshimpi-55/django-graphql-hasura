from django.db import models
from django.contrib.auth.models import AbstractUser
from .abstract import AbstractTimestamp, AbstractAuthority
from utils.auth import is_valid_role, permission_to_role

active_roles = (
    ("user", "user"),
    ("manager", "manager")
)


class BaseUser(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = "base_user"

    def get_roles(self):
        return list(map(permission_to_role, filter(is_valid_role, self.get_all_permissions())))

    def get_groups(self):
        return self.groups.values_list("name", flat=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    kind = models.CharField(max_length=255)
    image = models.CharField(
        blank=True,
        null=True,
        default="https://www.google.com")

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.kind


class Expense(AbstractTimestamp, AbstractAuthority):
    expense_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "expense"

    def __str__(self):
        return f"{self.created_by}: {self.description} - {self.amount}"


class Group(AbstractTimestamp, AbstractAuthority):
    name = models.CharField(max_length=255)
    expenses = models.ManyToManyField(
        Expense, related_name="groups", blank=True)

    class Meta:
        db_table = "group"

    def __str__(self):
        return self.name



class GroupMember(models.Model):
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="members")
    invited_by = models.ForeignKey(
        BaseUser, on_delete=models.CASCADE, related_name="invited_by")
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    invitation_accepted = models.BooleanField(default=False)

    class Meta:
        db_table = "group_member"

    def __str__(self):
        return f"{self.user} - {self.invitation_accepted}"
