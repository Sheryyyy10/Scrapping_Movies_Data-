from rest_framework import serializers
from .models import AppData, Language, Country


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class AppDataSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()
    country = CountrySerializer()

    class Meta:
        model = AppData
        fields = '__all__'
