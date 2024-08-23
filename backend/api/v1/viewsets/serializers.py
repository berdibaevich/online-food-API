from rest_framework import serializers


class RecursiveSerializer(serializers.Serializer):
    """
        For Category Childreen
    """
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context = self.context)
        return serializer.data