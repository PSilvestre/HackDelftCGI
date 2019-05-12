from django.db import models


# Create your models here.
class SwitchModel(models.Model):
	switch_id = models.SmallIntegerField(null=False)
	timestamp = models.DateTimeField(auto_now=False, null=False)
	description = models.CharField(max_length=255, null=False)
	file_name = models.CharField(max_length=255, null=False)
	severity = models.CharField(max_length=255, null=True)

	def __str__(self):
		return f"{self.switch_id} {self.description}"
