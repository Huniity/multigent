import threading
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from agents_ai.crew import SecurityCrew
from agents_ai.github.context_builder import build_context_from_pasted_code

from .models import Review, ReviewResult
from .serializers import ReviewSerializer, UserSerializer


class RegisterView(APIView):
    """
    API view for user registration, allowing new users to create accounts.
    """
    permission_classes = [AllowAny]
    

    def post(self, request):
        """
        Handle POST requests to create a new user account. Validates the input data and saves the user if valid.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    """
    API view to retrieve the authenticated user's information. Requires authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handle GET requests to return the authenticated user's details, including id, username, and email.
        """
        user = request.user
        return Response({'id': user.id, 'username': user.username, 'email': user.email})


class ReviewCreateView(APIView):
    """
    API view for creating a new review based on pasted code. Requires authentication.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handle POST requests to create a new review based on pasted code. Validates the input data and initiates the review process.
        """
        code = request.data.get('code', '').strip()
        if not code:
            return Response({'detail': 'No code provided.'}, status=status.HTTP_400_BAD_REQUEST)

        bundle = build_context_from_pasted_code(code)

        review = Review.objects.create(
            user=request.user,
            source='pasted_code',
            label='snippet',
        )

        thread = threading.Thread(target=_run_crew_sync, args=(review.id, bundle), daemon=True)
        thread.start()

        return Response({'id': review.id}, status=status.HTTP_202_ACCEPTED)


class ReviewListView(APIView):
    """
    API view to list all reviews for the authenticated user. Requires authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handle GET requests to return a list of reviews for the authenticated user.
        """
        reviews = Review.objects.filter(user=request.user).select_related('result')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class ReviewDetailView(APIView):
    """
    API view to retrieve details of a specific review. Requires authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            review = Review.objects.select_related('result').get(pk=pk, user=request.user)
        except Review.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ReviewSerializer(review).data)


class ReviewDeleteView(APIView):
    """
    API view to delete a specific review. Requires authentication and ownership of the review.
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        """
        Handle DELETE requests to remove a specific review. Validates that the review exists and belongs to the authenticated user before deletion.
        """
        try:
            review = Review.objects.get(pk=pk, user=request.user)
        except Review.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def _run_crew_sync(review_id: int, bundle: dict):
    """
    Internal function to run the security crew analysis asynchronously.
    """
    try:
        reports = SecurityCrew().run(bundle)
        ReviewResult.objects.create(
            review_id=review_id,
            **reports,
        )
        Review.objects.filter(pk=review_id).update(completed_at=timezone.now())
    except Exception:
        pass
