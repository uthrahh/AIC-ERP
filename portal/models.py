from django.db import models


class ActionAcknowledgement(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50)
    object_id = models.PositiveIntegerField()
    acknowledged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'action_acknowledgements'
        unique_together = ('user', 'action_type', 'object_id')
