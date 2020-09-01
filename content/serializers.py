from rest_framework import serializers

from content.models import Content


class ContentSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField('get_category')

    def get_category(self, obj):
        return obj.category

    class Meta:
        model = Content
        fields = ['id', 'user', 'title', 'body', 'summary', 'document', 'category']
