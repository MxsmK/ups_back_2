import graphene
import my_app.schema

class Query(my_app.schema.Query, graphene.ObjectType):
    pass


class Mutation(my_app.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
