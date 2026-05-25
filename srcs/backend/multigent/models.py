from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
	"""
	Model representing a code review task.
	"""

	"""
	Source choices indicate whether the review is based on pasted code or uploaded files.
	"""
	SOURCE_CHOICES = [
		("pasted_code", "Pasted Code"),
		("uploaded_files", "Uploaded Files"),
	]
	"""
	Label choices indicate whether the review is focused on code snippets or filenames.
	"""
	LABEL_CHOICES = [
		("snippet", "Code Snippet"),
		("filename", "Filename"),
	]

	"""
	The Review model captures the user who requested the review, the source of the code (pasted or uploaded),
	"""
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
	source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
	label = models.CharField(max_length=20, choices=LABEL_CHOICES)
	score = models.IntegerField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	completed_at = models.DateTimeField(null=True, blank=True)


	class Meta:
		"""
		Orders reviews by creation date, with the most recent reviews appearing first.
		"""
		ordering = ["-created_at"]

	def __str__(self):
		"""
		Returns a string representation of the Review instance, including the review ID, username, source, label, and creation date.
		"""
		return f"Review {self.id} by {self.user.username} - {self.source} ({self.label}) - Created at: {self.created_at}"

class ReviewResult(models.Model):
	"""
	Model representing the results of a code review, linked to a specific Review instance.
	"""
	review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name="result")
	bug_report = models.TextField(null=True, blank=True)
	security_report = models.TextField(null=True, blank=True)
	style_report = models.TextField(null=True, blank=True)
	performance_report = models.TextField(null=True, blank=True)
	final_report = models.TextField(null=True, blank=True)
	overall_score = models.IntegerField(null=True, blank=True)

	def __str__(self):
		"""
		Returns a string representation of the ReviewResult instance, including the review ID, username, and overall score.
		"""
		return f"ReviewResult for Review {self.review.id} ({self.review.user.username}) - Overall Score: {self.overall_score}"