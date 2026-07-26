import uuid

from django.db import models

class Activity(models.Model):
    """
    Activities that a company can be involved in.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(unique=True, help_text="Description of the activity")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "activity"


    def __str__(self) -> str:
        return f"{self.description}"