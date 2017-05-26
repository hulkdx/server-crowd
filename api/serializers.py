from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.exceptions import APIException
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer, EmailField, CharField, IntegerField, BooleanField
from rest_framework_jwt.settings import api_settings
from .models import Proposal, Profile, Category, ProposalVoteUser, Discussion

User = get_user_model()


# Profile
class ProfileSerializer(ModelSerializer):
    first_name = SlugRelatedField(source='user', slug_field='first_name', read_only=True)
    last_name = SlugRelatedField(source='user', slug_field='last_name', read_only=True)
    is_your_proposal = SerializerMethodField('check_users')

    def check_users(self, profile):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return profile.user == user

    class Meta:
        model = Profile
        fields = [
            'profile_pic_url',
            'first_name',
            'last_name',
            'is_your_proposal'
        ]


# Proposals
class ProposalSerializer(ModelSerializer):
    category_id = SlugRelatedField(source='category', slug_field='id', read_only=True)
    category_name = SlugRelatedField(source='category', slug_field='name', read_only=True)
    category_source = SlugRelatedField(source='category', slug_field='source', read_only=True)
    category_source_fill = SlugRelatedField(source='category', slug_field='source_fill', read_only=True)
    user = ProfileSerializer(read_only=True)
    are_you_voted = SerializerMethodField('check_voting')

    def check_voting(self, proposal):
        user = Profile.objects.get(user=self.context['request'].user)
        proposal_user = ProposalVoteUser.objects.filter(
            Q(user=user, proposal=proposal)
        ).distinct()
        if proposal_user.exists() and proposal_user.count() > 0:
            return True
        return False

    class Meta:
        model = Proposal
        fields = [
            'id',
            'title',
            'deadline',
            'description',
            'articles',
            'discussions',
            'category_id',
            'category_name',
            'category_source',
            'category_source_fill',
            'user',
            'are_you_voted'
        ]


class ProposalCreateSerializer(ModelSerializer):
    category_name = SlugRelatedField(source='category', slug_field='name', read_only=True)
    category_source = SlugRelatedField(source='category', slug_field='source', read_only=True)
    category_source_fill = SlugRelatedField(source='category', slug_field='source_fill', read_only=True)
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Proposal
        fields = [
            'title',
            'deadline',
            'description',
            'category',
            'articles',
            'discussions',
            'category_name',
            'category_source',
            'category_source_fill',
            'user'
        ]
        extra_kwargs = {"category":
                            {"write_only": True}
                        }


class ProposalVoteUpdateSerializer(ModelSerializer):
    id = IntegerField()
    vote_yes = BooleanField(default=False, write_only=True)
    vote_no = BooleanField(write_only=True)

    class Meta:
        model = Proposal
        fields = [
            'vote_yes',
            'vote_no',
            'id'
        ]

    def create(self, validated_data):
        id = validated_data['id']
        proposal = Proposal.objects.filter(
            Q(id=id)
        ).distinct()
        if proposal.exists() and proposal.count() == 1:
            proposal = proposal.first()
            user = Profile.objects.get(user=self.context['request'].user)
            # TODO: users can only vote one time
            proposal_user = ProposalVoteUser.objects.filter(
                Q(user=user, proposal=proposal)
            ).distinct()
            if proposal_user.exists() and proposal_user.count() > 0:
                raise APIException({'error': "the user already voted"})
            # if proposal_user_exist.count() > 0:
            #     Response(request.data, status=HTTP_400_BAD_REQUEST)
            # if request.data.get("vote_yes", None):
            #     ProposalVoteUser(
            #         user=user,
            #         proposal=proposal,
            #         vote=True
            #     ).save()
            # elif request.data.get("vote_no", None):
            #     ProposalVoteUser(
            #         user=user,
            #         proposal=proposal,
            #         vote=False
            #     ).save()
            #
            if validated_data.get('vote_yes', None):
                ProposalVoteUser(
                    user=user,
                    proposal=proposal,
                    vote=True
                ).save()
                proposal.votedYes = proposal.votedYes + 1
            elif validated_data.get('vote_no', None):
                ProposalVoteUser(
                    user=user,
                    proposal=proposal,
                    vote=False
                ).save()
                proposal.votedNo = proposal.votedNo + 1
            proposal.save()
        else:
            raise APIException({'error': "id is not valid!"})

        return validated_data


# Category
class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# Users
class UserCreateSerializer(ModelSerializer):
    email2 = EmailField(label='Confirm Email')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    def validate_email(self, value):
        data = self.get_initial()
        email2 = data.get("email2")
        email1 = value
        if email1 != email2:
            raise APIException({'error': "Emails must match."})
        user_qs = User.objects.filter(email=email1)
        if user_qs.exists():
            raise APIException({'error': "This user has already registered"})
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username=username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(allow_blank=True, required=False)
    profile_pic_url = CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'profile_pic_url',
            'password',
            'token',
        ]
        extra_kwargs = {"password":
                            {"write_only": True}}

    def validate(self, data):
        username = data.get("username", None)
        password = data["password"]
        if not username:
            raise APIException({'error': "Username is required to login"})

        user = User.objects.filter(
            Q(username=username)
        ).distinct()
        if user.exists() and user.count() == 1:
            user = user.first()
            data['first_name'] = user.first_name
            data['last_name'] = user.last_name
            data['email'] = user.email
            data['profile_pic_url'] = Profile.objects.get(user=user).profile_pic_url
            if not user.check_password(password):
                raise APIException({'error': "Incorrect username and password!"})
        else:
            raise APIException({'error': "username is not valid!"})
        # create jwt token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        # send the data back to the user.
        data['token'] = jwt_encode_handler(payload)

        return data


# Discussion
# Category
class DiscussionSerializer(ModelSerializer):
    class Meta:
        model = Discussion
        fields = '__all__'
