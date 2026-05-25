from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Review, ReviewResult


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, handling user creation with password hashing.
    The 'password' field is write-only to ensure it is not exposed in API responses.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ReviewResultSerializer(serializers.ModelSerializer):
    """
    Serializer for the ReviewResult model, including all relevant fields for review results.
    """
    class Meta:
        model = ReviewResult
        fields = [
            'bug_report', 'security_report', 'style_report',
            'performance_report', 'final_report', 'overall_score',
        ]


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model, including all relevant fields for reviews.
    """
    result = ReviewResultSerializer(read_only=True)

    class Meta:
        """
        Meta class for the ReviewSerializer, specifying the model and fields to include.
        """
        model = Review
        fields = [
            'id', 'source', 'label', 'score',
            'created_at', 'completed_at', 'result',
        ]
        read_only_fields = ['id', 'created_at', 'completed_at', 'score']