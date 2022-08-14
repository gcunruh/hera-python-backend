from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import ClaimSerializer, EnrollmentSerializer, SubscriberSerializer, FundSerializer
from .models import Subscriber, Fund
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser 

@api_view(['GET'])
def fund_list(request):
    if request.method == 'GET':
        funds = Fund.objects.all()
        funds_serializer = FundSerializer(funds, many=True)
        return JsonResponse(funds_serializer.data, safe=False)

@api_view(['GET'])
def subscriber_detail(request, pub_key):
    if request.method == 'GET':
        try:
            subscriber = Subscriber.objects.get(pub_key=pub_key)
        except Subscriber.DoesNotExist:
            return JsonResponse({'message': 'Does not exist'}, status=status.HTTP_404_NOT_FOUND)
        subscriber_serializer = SubscriberSerializer(subscriber)
        return JsonResponse(subscriber_serializer.data)

def enrollment_detail(request, pk):
    enrollment = enrollment.objects.get(pk=pk)
    enrollment_serializer = EnrollmentSerializer(enrollment)
    return JsonResponse(enrollment_serializer.data)

@api_view(['POST'])
def enroll(request):
    if  request.method ==  'POST':
        enrollment_data = JSONParser().parse(request)
        subscriber_serializer = SubscriberSerializer(data=enrollment_data)
        fund = enrollment_data.get('fund')
        if subscriber_serializer.is_valid():
            subscriber = subscriber_serializer.save()
        enrollment_serializer = EnrollmentSerializer(data=enrollment_data)
        if enrollment_serializer.is_valid():
            enrollment_serializer.save(fund=fund, subscriber=subscriber[0])
            return JsonResponse(enrollment_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(enrollment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def claim(request):
    if request.method == 'POST':
        claim_data = JSONParser().parse(request)
        claim_serializer = ClaimSerializer(data=claim_data)
        if claim_serializer.is_valid():
            claim_serializer.save()
            return JsonResponse(claim_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(claim_serializer.errors, status=status.HTTP_400_BAD_REQUEST)