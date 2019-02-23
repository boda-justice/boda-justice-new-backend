from django.contrib.auth import get_user_model, authenticate
from rest_framework import status, response, permissions, generics, views, authtoken
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser
from . import serializers, models


User = get_user_model()

class UserCreate(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()


class LoginUser(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return response.Response({'error': 'Please provvide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return response.Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_401_UNAUTHORIZED)
        else:
            token, _ = authtoken.models.Token.objects.get_or_create(user=user)
            return response.Response({'token': token.key},
                    status=status.HTTP_200_OK)


class LawyersListCreate(generics.CreateAPIView):
    queryset = models.Lawyer.objects.all()
    serializer_class = serializers.LawyerSerializer
    permission_classes = (IsAdminUser,)


class LawyersListCreate(generics.ListAPIView):
    queryset = models.Lawyer.objects.all()
    serializer_class = serializers.LawyerSerializer


class LawyersDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Lawyer.objects.all()
    serializer_class = serializers.LawyerSerializer
    permission_classes = (IsAdminUser,)


class ComplainantListCreate(generics.CreateAPIView):
    queryset = models.Lawyer.objects.all()
    serializer_class = serializers.ComplainantSerializer
    permission_classes = (IsAdminUser,)


class OffenceList(generics.ListCreateAPIView):
    queryset = models.Offence.objects.all()
    serializer_class = serializers.OffenseSerializer
