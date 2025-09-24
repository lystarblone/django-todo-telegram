from rest_framework import serializers
from .models import Task, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, write_only=True)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        task = Task.objects.create(**validated_data)
        if category_ids:
            task.categories.set(category_ids)
        return task

    def update(self, instance, validated_data):
        category_ids = validated_data.pop('category_ids', None)
        instance = super().update(instance, validated_data)
        if category_ids is not None:
            instance.categories.set(category_ids)
        return instance