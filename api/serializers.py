from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.exceptions import APIException
from rest_framework.serializers import ModelSerializer, EmailField, CharField
from rest_framework_jwt.settings import api_settings

from .models import Proposal
User = get_user_model()


class ProposalSerializer(ModelSerializer):
    class Meta:
        model = Proposal
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
                            {"write_only": True} }

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
