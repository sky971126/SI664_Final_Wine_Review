import django_filters
from wine_review.models import Wine,Taster,WineReview,Country,WineVariety


class WineFilter(django_filters.FilterSet):
	wine_title = django_filters.CharFilter(
		field_name='wine_title',
		label='Wine Title',
		lookup_expr='icontains'
	)
	wine_variety = django_filters.ModelChoiceFilter(
		field_name='wine_variety',
		label='Grape Variety',
		queryset = WineVariety.objects.all().order_by('wine_variety_name'),
		lookup_expr='exact'
	)
	country = django_filters.ModelChoiceFilter(
		field_name='country',
		label='Country',
		queryset = Country.objects.all().order_by('country_name'),
		lookup_expr='exact'
	)

	class Meta:
		model = Wine
		# form = SearchForm
		# fields [] is required, even if empty.
		fields = []