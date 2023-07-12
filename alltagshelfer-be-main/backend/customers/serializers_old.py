import logging
from rest_framework import serializers

from customers.models import Customer, CustomerFieldValue
from core.models import FieldMetadata


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer Class for customers
    """
    field_values = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        exclude = ('id', 'author', 'custom_fields')

    def validate(self, data):
        """
        If field_values were specified, add them
        """

        # Add fields dictionary to data
        data['field_values'] = self.context['request'].data.get(
            'field_values', None)

        return data

    def get_field_values(self, obj):
        """
        Display all fields to a given instance (if not specified, return null)
        """

        all_fields = FieldMetadata.objects.filter(kind=self.serializertype)
        values = []

        for field in all_fields:
            try:
                value = CustomerFieldValue.objects.get(
                    customer=obj.id, field=field).value
            except CustomerFieldValue.DoesNotExist:
                value = None

            values.append({
                'field_meta_data_id': field.id,
                'title': field.title,
                'value': value,
                'position': field.position,
                'enums': field.enums,
                'placeholder': field.placeholder,
                'field_type': str(field.field_type),
            })

        return values

    def get_queryset(self):
        return Customer.objects.filter(deleted=False)

    def create(self, validated_data):
        """
        Create new instance of customer
        """

        # Create Customer
        instance = Customer.objects.create(**validated_data)

        return instance

    def update(self, instance, validated_data):
        """
        Update instance of object. If Custom_fields were specified, create or add them
        """
        # Get additional fields and remove from validated data
        fields = validated_data.pop('field_values', [])
        # Get instance of Customer

        # Loop through all field values
        for field in fields:
            # Check if field value exists
            try:
                field_value = CustomerFieldValue.objects.get(
                    customer=instance, field=FieldMetadata.objects.get(id=field["field_meta_data_id"]))
                # If field value exists and is unequal update value
                if field_value.value != field["value"]:
                    field_value.value = field["value"]
                    field_value.save()
            # If field value does not exist, create it
            except CustomerFieldValue.DoesNotExist:
                if field["value"] is not None:
                    CustomerFieldValue.objects.create(customer=instance, field=FieldMetadata.objects.get(
                        id=field["field_meta_data_id"]), value=field["value"])

        # Update Customer instance
        instance.__dict__.update(validated_data)
        instance.save()
        return instance
