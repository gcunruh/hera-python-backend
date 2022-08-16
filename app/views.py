import io
import uuid
import json
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import ClaimSerializer, EnrollmentSerializer, SubscriberSerializer, FundSerializer
from .models import Subscriber, Fund, Enrollment
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser 
import boto3
from PIL import Image, ImageFont, ImageDraw
from django.conf import settings

@api_view(['GET'])
def fund_list(request):
    if request.method == 'GET':
        funds = Fund.objects.all()
        funds_serializer = FundSerializer(funds, many=True)
        return JsonResponse(funds_serializer.data, safe=False)
    
@api_view(['POST'])
def create_fund(request):
    if request.method == 'POST':
        fund_data = JSONParser().parse(request)
        fund_serializer = FundSerializer(data=fund_data)
        if fund_serializer.is_valid():
            fund_serializer.save()
            return JsonResponse(fund_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(fund_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def subscriber_detail(request, pub_key):
    if request.method == 'GET':
        try:
            subscriber = Subscriber.objects.filter(pub_key=pub_key)[0]
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
        enrollment = Enrollment.objects.get(uuid=claim_data.get('enrollment_id'))
        subscriber = Subscriber.objects.get(pub_key=claim_data.get('pub_key'))
        claim_serializer = ClaimSerializer(data=claim_data)
        if claim_serializer.is_valid():
            claim_serializer.save(enrollment=enrollment, subscriber=subscriber)
            return JsonResponse(claim_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(claim_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_image(request):
    if request.method == 'POST':
        card_data = JSONParser().parse(request)
        uuid_for_save = uuid.uuid4()

        sub = Subscriber.objects.filter(pub_key = card_data.get('pub_key'))[0]

        # Open card image
        card = Image.open("static/hera_card.png")
        # Choose font
        font = ImageFont.truetype('static/inter.ttf', 20)

        BUCKET_NAME = 'hera-health01'

        text = card_data.get('name')
        card_id = "00" + str(sub.pk)
        # pool = card_data.get('fund')
        coverage_period = str(card_data.get('year'))
        card_editable = ImageDraw.Draw(card)

        card_editable.text((198, 426), text, font=font, fill=(0, 0, 0))
        card_editable.text((198, 500), card_id, font=font, fill=(0, 0, 0))
        card_editable.text((198, 589), coverage_period, font=font, fill=(0, 0, 0))

        in_mem_file = io.BytesIO()
        card.save(in_mem_file, format=card.format)
        in_mem_file.seek(0)

        s3c = boto3.client(
            's3',
            region_name='us-west-2',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        response = s3c.put_object(
            Body=in_mem_file,
            Bucket=BUCKET_NAME,
            ContentType='image/jpeg',
            Key=f"card/{uuid_for_save}.png"
        )

        return JsonResponse({ "uri": f"https://{BUCKET_NAME}.s3.us-west-2.amazonaws.com/card/{uuid_for_save}.png" }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def create_metadata(request):
    
    if request.method == 'POST':
        nft_data = JSONParser().parse(request)
        uuid_for_save = uuid.uuid4()

        BUCKET_NAME = 'hera-health01'

        for_upload = bytes(json.dumps(nft_data).encode('utf-8'))

        s3c = boto3.client(
            's3',
            region_name='us-west-2',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        response = s3c.put_object(
            Body=for_upload,
            Bucket=BUCKET_NAME,
            ContentType='image/jpeg',
            Key=f"metadata/{uuid_for_save}.json"
        )

        return JsonResponse({ "uri": f"https://{BUCKET_NAME}.s3.us-west-2.amazonaws.com/metadata/{uuid_for_save}.json" }, status=status.HTTP_201_CREATED)

