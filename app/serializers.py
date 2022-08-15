from .models import Enrollment, Subscriber, Fund, Claim
from rest_framework import serializers

class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = ['uuid', 'name', 'year', 'chain_id', 'fy_premium', 'fy_allowable']

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ['uuid', 'subscriber', 'enrollment', 'claim_amount', 'status']

class EnrollmentSerializer(serializers.ModelSerializer):
    fund =  FundSerializer(read_only=True)
    claims  = ClaimSerializer(many=True, read_only=True)
    class Meta:
        model = Enrollment
        fields =  ['uuid', 'subscriber', 'fund', 'paid_in', 'date_paid_in', 'claims']

    def create(self, validated_data):
        fund = Fund.objects.get(name=validated_data.get('fund'))
        enrollment = Enrollment.objects.create(subscriber=validated_data.get('subscriber'), fund=fund, paid_in=validated_data.get('paid_in'))
        return enrollment

class SubscriberSerializer(serializers.ModelSerializer):
    enrollments = EnrollmentSerializer(many=True, read_only=True)

    class Meta:
        model = Subscriber
        fields = ['pub_key', 'first_name', 'last_name', 'email', 'enrollments']
        depth = 1

    def create(self, validated_data):
        sub = Subscriber.objects.get_or_create(pub_key = validated_data.get('pub_key'), first_name=validated_data.get('first_name'), last_name=validated_data.get('last_name'), email=validated_data.get('email'))
        return sub


