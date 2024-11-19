from todo.models import Task
import django_filters


class TaskFilter(django_filters.FilterSet):
    """
    A Django FilterSet for Task model to filter tasks based on specific criteria.

    Attributes:
    -----------
    model : django.db.models.Model
        The model class to filter, in this case, Task.

    fields : dict
        A dictionary specifying the fields to filter and their filter types.
        The keys are the field names, and the values are lists of filter types.

    Methods:
    --------
    None

    """

    class Meta:
        """
        Meta class for TaskFilter.

        Attributes:
        -----------
        model : django.db.models.Model
            The model class to filter, in this case, Task.

        fields : dict
            A dictionary specifying the fields to filter and their filter types.
            The keys are the field names, and the values are lists of filter types.

        """

        model = Task
        fields = {
            "is_done": [
                "exact"
            ],  # Filter tasks based on their completion status
            "created_date": [
                "exact",
                "lte",
                "gte",
            ],  # Filter tasks based on their creation date
        }
