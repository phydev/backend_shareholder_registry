import uuid

from django.db import models

class Status(models.Model):
    """
    Status entity, representing the status of a company.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bankruptcy = models.BooleanField(default=False, help_text="Bankruptcy status")
    under_liquidation = models.BooleanField(default=False, help_text="Under liquidation status")
    under_compulsory_liquidation_or_dissolution = models.BooleanField(default=False, help_text="Under compulsory "
                                                                                               "liquidation or"
                                                                                          "dissolution "
                                                                                   "status")
    registered_in_business_register = models.BooleanField(default=False, help_text="Registered in Business Register")
    registered_in_establishment_register = models.BooleanField(default=False, help_text="Registered in Establishment Register")
    registered_in_voluntary_register = models.BooleanField(default=False, help_text="Registered in Voluntary Register")
    last_annual_report_submitted = models.DateTimeField(help_text="Last annual report submitted", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "status"

    def __str__(self) -> str:
        return f"{self.id}"