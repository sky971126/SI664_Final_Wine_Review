from wine_review.models import Wine,WineReview,Winery,WineVariety,Country,Province,Region,Taster
from rest_framework import response, serializers, status

class WinerySerializer(serializers.ModelSerializer):

	class Meta:
		model = Winery
		fields = ('winery_id', 'winery_name')

class WineVarietySerializer(serializers.ModelSerializer):

	class Meta:
		model = WineVariety
		fields = ('wine_variety_id', 'wine_variety_name')


class CountrySerializer(serializers.ModelSerializer):

	class Meta:
		model = Country
		fields = ('country_id', 'country_name')


class ProvinceSerializer(serializers.ModelSerializer):
    #country = CountrySerializer(many=False, read_only=True)
    class Meta:
        model = Province
        fields = ('province_id', 'province_name')#, 'country')


class RegionSerializer(serializers.ModelSerializer):
    #province = ProvinceSerializer(many=False, read_only=True)
    class Meta:
        model = Region
        fields = ('region_id', 'region_name')#, 'province')



class TasterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Taster
		fields = ('taster_id', 'taster_name',"taster_twitter")



class WineReviewSerializer(serializers.ModelSerializer):
	wine = serializers.ReadOnlyField(source='wine.wine_id')
	taster = serializers.ReadOnlyField(source='taster.taster_id')

	class Meta:
		model = WineReview
		fields = ('wine_id', 'taster_id', 'rating', 'description')


class WineSerializer(serializers.ModelSerializer):
    wine_title = serializers.CharField(
        allow_blank=False,
        max_length=100
    )

    wine_variety = WineVarietySerializer(
        many=False,
        read_only=True
    )
    wine_variety_id = serializers.PrimaryKeyRelatedField(
        allow_null=False,
        many=False,
        write_only=True,
        queryset=WineVariety.objects.all(),
        source='wine_variety'
    )
    winery = WinerySerializer(
        many=False,
        read_only=True
    )
    winery_id = serializers.PrimaryKeyRelatedField(
        allow_null=False,
        many=False,
        write_only=True,
        queryset=Winery.objects.all(),
        source='winery'
    )
    country = CountrySerializer(
        many=False,
        read_only=True
    )
    country_id = serializers.PrimaryKeyRelatedField(
        allow_null=True,
        many=False,
        write_only=True,
        queryset=Country.objects.all(),
        source='country'
    )
    province = ProvinceSerializer(
        many=False,
        read_only=True
    )
    province_id = serializers.PrimaryKeyRelatedField(
        allow_null=True,
        many=False,
        write_only=True,
        queryset=Province.objects.all(),
        source='province'
    )
    region = RegionSerializer(
        many=False,
        read_only=True
    )
    region_id = serializers.PrimaryKeyRelatedField(
        allow_null=True,
        many=False,
        write_only=True,
        queryset=Region.objects.all(),
        source='region'
    )
    taster_wine = WineReviewSerializer(
        source='taster_wine_set', # Note use of _set
        many=True,
        read_only=True
    )
    taster_wine_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Taster.objects.all(),
        source='taster_wine'
    )
    class Meta:
        model = Wine
        fields = (
            'wine_id',
            'wine_title',
            'wine_variety',
            'wine_variety_id',
            'winery',
            'winery_id',
            'region',
            'region_id',
            'province',
            'province_id',
            'country',
            'country_id',
            'taster_wine',
            'taster_wine_ids'
        )

    def create(self, validated_data):


        # print(validated_data)

        tasters = validated_data.pop('taster_wine')
        wine = Wine.objects.create(**validated_data)

        if tasters is not None:
            for taster in tasters:
                WineReview.objects.create(
                    wine_id=wine.wine_id,
                    taster_id=taster.taster_id,
                    rating=-1,
                    description='Not Given'
                )
        return wine

    def update(self, instance, validated_data):
        wine_id = instance.wine_id
        new_tasters = validated_data.pop('taster_wine')

        instance.wine_title = validated_data.get(
            'wine_title',
            instance.wine_title
        )
        instance.wine_variety = validated_data.get(
            'wine_variety',
            instance.wine_variety
        )
        instance.winery = validated_data.get(
            'winery',
            instance.winery
        )
        instance.region = validated_data.get(
            'region',
            instance.region
        )
        instance.province = validated_data.get(
            'province',
            instance.province
        )
        instance.country = validated_data.get(
            'country',
            instance.country
        )
        instance.save()

        # If any existing country/areas are not in updated list, delete them
        new_ids = []
        old_ids = WineReview.objects \
            .values_list('taster_id', flat=True) \
            .filter(wine_id__exact=wine_id)

        # TODO Insert may not be required (Just return instance)

        # Insert new unmatched country entries
        for taster in new_tasters:
            new_id = taster.taster_id
            new_ids.append(new_id)
            if new_id in old_ids:
                continue
            else:
                WineReview.objects.create(
                    wine_id=wine_id,
                    taster_id=new_id,
                    rating=-1,
                    description='Not Given'
                )
        # Delete old unmatched country entries
        for old_id in old_ids:
            if old_id in new_ids:
                continue
            else:
                WineReview.objects \
                    .filter(wine_id=wine_id, taster_id=old_id) \
                    .delete()

        return instance