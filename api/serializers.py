from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Client, Project, Task
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    # extra write-only inputs coming from the frontend form
    first_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    last_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    phone_number = serializers.CharField(write_only=True, required=False, allow_blank=True)
    company = serializers.CharField(write_only=True, required=False, allow_blank=True)

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirmation = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        # note: User model has no first_name/etc — these are accepted but not stored on the model
        fields = (
            'id',
            'email',
            'name',          # will auto-fill from first+last if not provided
            'role',
            'password',
            'password_confirmation',
            'first_name',
            'last_name',
            'phone_number',
            'company',
        )
        extra_kwargs = {
            'role': {'required': False},  # optional on register
            'name': {'required': False},
        }

    def validate(self, attrs):
        # optional confirmation check if frontend sends it
        pwd = attrs.get('password')
        pwd2 = attrs.get('password_confirmation')
        if pwd2 is not None and pwd != pwd2:
            raise serializers.ValidationError({"password_confirmation": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        # pull form-only fields (not in model)
        first = validated_data.pop('first_name', '').strip()
        last = validated_data.pop('last_name', '').strip()
        _phone = validated_data.pop('phone_number', '').strip()  # not stored (no field)
        _company = validated_data.pop('company', '').strip()     # not stored (no field)
        validated_data.pop('password_confirmation', None)

        # if name not provided, compose from first + last
        if not validated_data.get('name'):
            composed = f"{first} {last}".strip()
            if composed:
                validated_data['name'] = composed

        pwd = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(pwd)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'name',
            'role',
            'is_active',
            'is_staff',
            'created_at',
            'updated_at',
        )
class ClientSerializer(serializers.ModelSerializer):
    class Meta: model = Client; fields = '__all__'
class ProjectSerializer(serializers.ModelSerializer):
    class Meta: model = Project; fields = '__all__'
class TaskSerializer(serializers.ModelSerializer):
    class Meta: model = Task; fields = '__all__'