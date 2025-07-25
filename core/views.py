from django.http import JsonResponse

def handler404(request, exception):
    """
    Custom 404 handler to return a JSON response.
    """
    return JsonResponse({'detail': 'Not found.'}, status=404)
