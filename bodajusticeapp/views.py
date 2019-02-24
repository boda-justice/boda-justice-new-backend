from django.contrib.auth import get_user_model, authenticate
from rest_framework import status, response, permissions, generics, views, authtoken
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from . import serializers, models
from rest_framework.exceptions import PermissionDenied



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


class LawyersDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Lawyer.objects.all()
    serializer_class = serializers.LawyerSerializer
    permission_classes = (IsAdminUser,)


class ComplainantListCreate(generics.CreateAPIView):
    queryset = models.Complainants.objects.all()
    serializer_class = serializers.ComplainantSerializer


class OffenceList(generics.ListCreateAPIView):
    queryset = models.Offence.objects.all()
    serializer_class = serializers.OffenseSerializer

class CaseCreate(generics.ListCreateAPIView):
    queryset = models.Case.objects.all()
    serializer_class = serializers.CaseSerializer
    permission_classes = (IsAdminUser,)


class CloseCase(generics.UpdateAPIView):
    queryset = models.Case.objects.all()
    serializer_class = serializers.CaseSerializer
    permission_classes = (IsAdminUser,)


class ComplaintListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ComplaintSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(complainant=user.complainant_user)

    def get_queryset(self):
        user = self.request.user
        try:
            complainant_user = user.complainant_user
        except:
            raise PermissionDenied()            
        return models.Complaint.objects.filter(complainant=complainant_user)


class ComplaintRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ComplaintDetailsSerializer

    def get_queryset(self):
        user = self.request.user
        try:
            complainant_user = user.complainant_user
        except:
            raise PermissionDenied("The user trying to access this view is not a complainant")
        complaint = models.Complaint.objects.filter(complainant=complainant_user, id=self.kwargs["pk"])
        if not complaint:
            raise PermissionDenied("You are not allowed to view, edit, delete this complaint")           
        return complaint

