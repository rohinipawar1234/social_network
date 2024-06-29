from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import CustomUser, FriendRequest
from .serializers import UserSerializer, UserSearchSerializer, FriendRequestSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


class UserSignupView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """
        Create a new user with the provided email and password.

        Args:
            serializer (UserSerializer): Serializer instance containing validated data.
        """
        instance = serializer.save(username=self.request.data.get("email"))
        instance.set_password(instance.password)
        instance.save()


class UserLoginAPIView(APIView):
    """
    API endpoint for user login.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle user login request.

        Validates user credentials and logs in the user if valid.

        Args:
            request (Request): HTTP POST request object containing user credentials.

        Returns:
            Response: JSON response indicating success or failure of login attempt.
        """
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Please provide both email and password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return Response(
                {"message": "You have successfully logged in"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class UserSearchView(generics.ListAPIView):
    """
    API endpoint for searching users by email, first name, or last name.

    Allows authenticated users to search for other users based on specified query.
    """

    serializer_class = UserSearchSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["email", "first_name", "last_name"]
    permission_classes = [IsAuthenticated]  


    def get_queryset(self):
        """
        Get the queryset of users based on search parameters.

        Returns:
            queryset: Filtered queryset of users matching search criteria.
        """
        queryset = CustomUser.objects.all()
        search_query = self.request.query_params.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(email__iexact=search_query)
                | Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
            )
        return queryset


class SendFriendRequestView(generics.CreateAPIView):
    """
    API endpoint for sending a friend request.

    Allows authenticated users to send friend requests to other users.
    """

    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        """
        Override queryset method to return an empty queryset.

        Returns:
            queryset: Empty queryset.
        """
        return FriendRequest.objects.none()

    def perform_create(self, serializer):
        """
        Create a new friend request.

        Validates rate limit and existence of recipient user before creating the request.

        Args:
            serializer (FriendRequestSerializer): Serializer instance containing validated data.
        """
        from_user = self.request.user
        to_user_id = self.request.data.get("to_user")

        try:
            to_user = CustomUser.objects.get(id=to_user_id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"error": "User does not exist"})

        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests_count = FriendRequest.objects.filter(
            from_user=from_user, created_at__gte=one_minute_ago
        ).count()

        if recent_requests_count >= 3:
            raise serializers.ValidationError(
                {
                    "error": "You cannot send more than 3 friend requests within a minute."
                }
            )

        serializer.save(from_user=from_user, to_user=to_user)


class AcceptFriendRequestView(generics.UpdateAPIView):
    """
    API endpoint for accepting a friend request.

    Allows authenticated users to accept pending friend requests.
    """

    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]  

    def perform_update(self, serializer):
        """
        Update the status of a friend request to 'accepted'.

        Args:
            serializer (FriendRequestSerializer): Serializer instance containing updated data.
        """
        serializer.save(status="accepted")


class RejectFriendRequestView(generics.UpdateAPIView):
    """
    API endpoint for rejecting a friend request.

    Allows authenticated users to reject pending or accepted friend requests.
    """

    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]  

    def perform_update(self, serializer):
        """
        Update the status of a friend request to 'rejected'.

        Args:
            serializer (FriendRequestSerializer): Serializer instance containing updated data.

        Raises:
            ValidationError: If the friend request status is neither 'pending' nor 'accepted'.
        """
        if serializer.instance.status in ["pending", "accepted"]:
            serializer.save(status="rejected")
        else:
            raise ValidationError(
                "Only pending or accepted friend requests can be rejected."
            )


class ListAcceptFriendRequestView(generics.ListAPIView):
    """
    API endpoint for listing accepted friend requests.

    Allows authenticated users to view a list of friend requests that have been accepted.
    """

    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        """
        Get the queryset of accepted friend requests.

        Returns:
            queryset: Filtered queryset of friend requests with 'accepted' status.
        """
        return FriendRequest.objects.all().filter(status="accepted")


class ListPendingFriendRequestView(generics.ListAPIView):
    """
    API endpoint for listing pending friend requests.

    Allows authenticated users to view a list of pending friend requests.
    """

    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        """
        Get the queryset of pending friend requests.

        Returns:
            queryset: Filtered queryset of friend requests with 'pending' status.
        """
        return FriendRequest.objects.all().filter(status="pending")
