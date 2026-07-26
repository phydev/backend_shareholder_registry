import uuid

from django.db import models

class Industry(models.Model):
    """
    Industry entity, representing different sectors or industries a company can belong to.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True, help_text="Industry code", null=True)
    name = models.CharField(max_length=255, help_text="Industry name")
    description = models.TextField(blank=True, help_text="Description of the industry", null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "industry"
        unique_together = ("code", "name")

    def __str__(self) -> str:
        return f"{self.name} {self.code} {self.description}"
