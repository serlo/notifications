from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


@csrf_exempt
def set_state(request: HttpRequest) -> JsonResponse:
    return JsonResponse({})


@csrf_exempt
def execute_message(request: HttpRequest) -> JsonResponse:
    return JsonResponse({})
