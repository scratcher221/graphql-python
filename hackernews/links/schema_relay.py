import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Link, Vote
from users.schema import UserType
from .schema import LinkType


class LinkFilter(django_filters.FilterSet):
    class Meta:
        model = Link
        fields = ['url', 'description']

class LinkNode(DjangoObjectType):
    class Meta:
        model = Link
        interfaces = (graphene.relay.Node,)

class RelayCreateLink(graphene.relay.ClientIDMutation):
    link = graphene.Field(LinkNode)

    class Input:
        url = graphene.String()
        description = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        user = info.context.user or None

        link = Link(
            url=input.get('url'),
            description=input.get('description'),
            posted_by=user,
        )
        link.save()

        return RelayCreateLink(link=link)

class VoteFilter(django_filters.FilterSet):
    class Meta:
        model = Vote
        fields = {
            'user': ['exact'],
            'link': ['exact'],
        }

class VoteNode(DjangoObjectType):
    class Meta:
        model = Vote
        interfaces = (graphene.relay.Node,)

class RelayCreateVote(graphene.relay.ClientIDMutation):
    vote = graphene.Field(VoteNode)

    class Input:
        link_id = graphene.Int()

    def mutate_and_get_payload(root, info, **input):
        user = info.context.user or None
        
        link_id = input.get('link_id')
        link = Link.objects.filter(pk=link_id).first()
        if not link:
            raise Exception('Invalid Link!')

        vote = Vote(
            user=user,
            link=link,
        )
        vote.save()

        return RelayCreateVote(vote=vote)

class RelayQuery(graphene.ObjectType):
    relay_link = graphene.relay.Node.Field(LinkNode)
    relay_links = DjangoFilterConnectionField(LinkNode, filterset_class=LinkFilter)

    relay_vote = graphene.relay.Node.Field(VoteNode)
    relay_votes = DjangoFilterConnectionField(VoteNode, filterset_class=VoteFilter)

class RelayMutation(graphene.AbstractType):
    relay_create_link = RelayCreateLink.Field()
    relay_create_vote = RelayCreateVote.Field()