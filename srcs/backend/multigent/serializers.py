from django.auth.models import User
from rest_framework import serializers
from .models import Review, ReviewResult


class ReviewSerializer(serializers.ModelSerializer):
	"""
	Serializer for the Review model, converting Review instances to and from JSON format.
	"""

	password = serializers.CharField(write_only=True)

	class Meta:
		"""
		Specifies the model and fields to be serialized. The password field is write-only for security reasons.
		""" 
		model = User
		fields = ['id', 'username', 'password']

	def create_user(self, data_valid):
		"""
		Creates a new user instance with the provided validated data.
		"""
		return User.objects.create_user(
			username=data_valid['username'],
			password=data_valid['password']
		)
