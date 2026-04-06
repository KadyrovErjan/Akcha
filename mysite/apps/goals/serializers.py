from rest_framework import serializers
from .models import Goal


class GoalSerializer(serializers.ModelSerializer):
    progress_percent = serializers.ReadOnlyField()

    class Meta:
        model = Goal
        fields = (
            'id', 'title', 'target_amount',
            'current_amount', 'progress_percent',
            'deadline', 'created_at'
        )
        read_only_fields = ('id', 'created_at', 'progress_percent')