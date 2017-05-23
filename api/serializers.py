from django.contrib.auth import get_user_model
from django.db.models import Q, BooleanField
from rest_framework.exceptions import APIException
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer, EmailField, CharField
from rest_framework_jwt.settings import api_settings
from rest_framework.fields import CurrentUserDefault
from .models import Proposal, Profile, Category

User = get_user_model()


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

class ProposalSerializer(ModelSerializer):
    category_id = SlugRelatedField(source='category', slug_field='id', read_only=True)
    category_name = SlugRelatedField(source='category', slug_field='name', read_only=True)
    category_source = SlugRelatedField(source='category', slug_field='source', read_only=True)
    category_source_fill = SlugRelatedField(source='category', slug_field='source_fill', read_only=True)
    user = ProfileSerializer(read_only=True)

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
            'user'
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


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


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

    class Meta:
        model = User
        fields = [
            'username',
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
