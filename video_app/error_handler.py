"""This module defines the function custom_404_view."""
from django.http import JsonResponse


# pylint: disable=unused-argument
def custom_404_view(request, exception):
    """Returns an error message if wrong url was searched by the user."""
    return JsonResponse({'error': 'Page not found.'}, status=404)
