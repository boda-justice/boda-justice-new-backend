from django.contrib.auth import get_user_model, authenticate
from rest_framework import status, response, permissions, generics, views, authtoken
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from . import serializers, models
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token



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


class GetUser(views.APIView):
    def get(self, request, format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        user_token = token.split()[1]
        user = Token.objects.filter(key=user_token).first().user
        user_occupation = "Unassigned"
        try:
            user.lawyer_user
            user_occupation = "Lawyer"
        except:
            pass
        try:
            user.complainant_user
            user_occupation = "Complainant"
        except:
            pass

        return response.Response({'username': user.username,
        'occupation': user_occupation
        },
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
    serializer_class = serializers.CaseSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.Case.objects.all()


class CloseCase(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Case.objects.all()
    serializer_class = serializers.CaseSerializer
    permission_classes = (IsAuthenticated,)


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


class ComplaintList(generics.ListAPIView):
    serializer_class = serializers.ComplaintListSerializer

    def get_queryset(self):
        user = self.request.user
        try:
            complainant_user = user.lawyer_user
        except:
            raise PermissionDenied("The user trying to access this view is not a lawyer")
        complaints = models.Complaint.objects.filter(status=False)         
        return complaints

class ComplaintRetrieve(generics.RetrieveAPIView):
    serializer_class = serializers.ComplaintRetrieveSerializer


    def get_queryset(self):
        user = self.request.user
        try:
            complainant_user = user.lawyer_user
        except:
            raise PermissionDenied("The user trying to access this view is not a lawyer")
        complaints = models.Complaint.objects.filter(status=False)         
        return complaints


class CaseView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CaseSerializer

    def get_queryset(self):
        user = self.request.user
        try:
            lawyer = user.lawyer_user
        except:
            raise PermissionDenied("The user trying to access this view is not a lawyer")
        cases = models.Case.objects.filter(lawyer=lawyer)        
        return cases


class ReviewView(generics.ListCreateAPIView):
    serializer_class = serializers.ReviewsSerializers
    queryset = models.Reviews.objects.all()

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ReviewsSerializers
    queryset = models.Reviews.objects.all()