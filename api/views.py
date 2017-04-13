from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .serializers import ProposalSerializer, UserCreateSerializer, UserLoginSerializer
from .models import Proposal

User = get_user_model()


# this class is not used yet
class ProposalCreate(CreateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProposalListAPIView(ListAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer


class ProposalDetailAPIView(RetrieveAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer


# --- Users ---
class UserCreate(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserLogin(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
