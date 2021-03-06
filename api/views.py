import sys
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .serializers import ProposalSerializer, UserCreateSerializer, UserLoginSerializer, ProposalCreateSerializer, \
    CategorySerializer, ProposalVoteUpdateSerializer, DiscussionSerializer
from .models import Proposal, Profile, Category, ProposalVoteUser, Discussion

User = get_user_model()


# --- Proposals ---
# this class is not used yet
class ProposalCreate(CreateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=Profile.objects.get(user=self.request.user))


class ProposalListAPIView(ListAPIView):
    queryset = Proposal.objects.all().order_by('-deadline')
    serializer_class = ProposalSerializer

    # This will filter base on user
    # def get_queryset(self):
    #     user = Profile.objects.get(user=self.request.user)
    #     return Proposal.objects.filter(user=user)


class ProposalDetailAPIView(RetrieveAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer


class ProposalVoteUpdate(APIView):
    serializer_class = ProposalVoteUpdateSerializer

    def put(self, request, *args, **kwargs):
        serializer = ProposalVoteUpdateSerializer(context={'request': request}, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=Profile.objects.get(user=self.request.user))
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


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


# --- Category ---
class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DiscussionListAPIView(ListAPIView):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer

    def get_queryset(self):
        proposal = Proposal.objects.filter(id=self.kwargs['pk'])
        return Discussion.objects.filter(proposal=proposal)
