import graphene

from apis.grapgql import MutationMain,QueryMain



class QueryRoot(
    QueryMain,
    graphene.ObjectType,
):
    pass

class MutationRoot(
    MutationMain,
    graphene.ObjectType,
):
    pass




schema = graphene.Schema(query=QueryRoot, mutation=MutationRoot, auto_camelcase=False)
