from portal.models import ActionAcknowledgement


def acknowledge_action(user, action_type, object_id):
    ActionAcknowledgement.objects.get_or_create(
        user=user,
        action_type=action_type,
        object_id=object_id,
    )


def filter_unacknowledged(user, action_type, queryset):
    acked_ids = ActionAcknowledgement.objects.filter(
        user=user,
        action_type=action_type,
    ).values_list('object_id', flat=True)
    return queryset.exclude(pk__in=acked_ids)
