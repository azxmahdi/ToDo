from rest_framework import serializers
from todo.models import Task
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.

    This serializer is used to convert Task instances into a format that can be easily
    transmitted and stored. It includes fields for 'id', 'url', 'user', 'title', 'is_done',
    'created_date', and 'updated_date'. The 'user' field is read-only, and the 'url' field
    is generated dynamically.
    """

    url = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "url",
            "user",
            "title",
            "is_done",
            "created_date",
            "updated_date",
        ]
        read_only_fields = ["user"]

    def create(self, validated_data):
        """
        Create a new Task instance.

        This method overrides the default create method to set the 'user' field of the
        validated_data to the current user making the request.

        Parameters:
        validated_data (dict): A dictionary containing the validated data for creating a new Task.

        Returns:
        Task: The newly created Task instance.
        """
        validated_data["user"] = User.objects.get(
            id=self.context["request"].user.id
        )
        return super().create(validated_data)

    def to_representation(self, instance):
        """
        Modify the representation of a Task instance.

        This method overrides the default to_representation method to remove the 'url' field
        from the representation if the request is for a specific Task instance (identified by
        the presence of a 'pk' in the kwargs).

        Parameters:
        instance (Task): The Task instance to be represented.

        Returns:
        dict: The modified representation of the Task instance.
        """
        rep = super().to_representation(instance)
        request = self.context.get("request")
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("url", None)
            return rep
        return rep

    def get_url(self, obj):
        """
        Generate the absolute URL for a Task instance.

        This method generates the absolute URL for a Task instance based on its get_absolute_url
        method.

        Parameters:
        obj (Task): The Task instance for which the URL is to be generated.

        Returns:
        str: The absolute URL for the Task instance.
        """
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_url())
