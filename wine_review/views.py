from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from .models import Wine
from .models import Taster
from .models import WineReview

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import WineForm
from django.urls import reverse_lazy

from django_filters.views import FilterView
from .filters import WineFilter

def index(request):
	return HttpResponse("Hello, world. You're at the Wine Review index page.")


class AboutPageView(generic.TemplateView):
	template_name = 'wine_review/about.html'


class HomePageView(generic.TemplateView):
	template_name = 'wine_review/home.html'

@method_decorator(login_required, name='dispatch')
class WineListView(generic.ListView):
    model = Wine
    context_object_name = 'wine_list'
    template_name = 'wine_review/wine.html'
    paginate_by = 200

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return Wine.objects.all().order_by('wine_title')


@method_decorator(login_required, name='dispatch')
class WineDetailView(generic.DetailView):
    template_name = 'wine_review/wine_detail.html'
    model = Wine
    context_object_name = 'wine'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@method_decorator(login_required, name='dispatch')
class ReviewListView(generic.ListView):
    model = WineReview
    context_object_name = 'review_list'
    template_name = 'wine_review/review.html'
    paginate_by = 200

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return WineReview.objects.all().order_by('-rating')


@method_decorator(login_required, name='dispatch')
class ReviewDetailView(generic.DetailView):
    template_name = 'wine_review/review_detail.html'
    model = WineReview
    context_object_name = 'review'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class WineCreateView(generic.View):
    model = Wine
    form_class = WineForm
    success_message = "Wine created successfully"
    template_name = 'wine_review/wine_new.html'
    # fields = '__all__' <-- superseded by form_class
    # success_url = reverse_lazy('heritagesites/site_list')

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        form = WineForm(request.POST)
        if form.is_valid():
            wine = form.save(commit=False)
            wine.save()
            taster = form.cleaned_data["taster"][0]
            WineReview.objects.create(wine=wine, taster=taster, rating=-1, description="Not Given")
            return redirect(wine) # shortcut to object's get_absolute_url()
            # return HttpResponseRedirect(wine.get_absolute_url())
        return render(request, 'wine_review/wine_new.html', {'form': form})

    def get(self, request):
        form = WineForm()
        return render(request, 'wine_review/wine_new.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class WineUpdateView(generic.UpdateView):
    model = Wine
    form_class = WineForm
    # fields = '__all__' <-- superseded by form_class
    context_object_name = 'wine'
    # pk_url_kwarg = 'wine_pk'
    success_message = "Wine updated successfully"
    template_name = 'wine_review/wine_update.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        wine = form.save(commit=False)
        # wine.updated_by = self.request.user
        # wine.date_updated = timezone.now()
        wine.save()
        # Current country_area_id values linked to wine
        
        old_ids = WineReview.objects\
            .values_list('taster_id', flat=True)\
            .filter(wine_id=wine.wine_id)
    
        # New countries list
    
        new_tasters = form.cleaned_data['taster']
    
        # TODO can these loops be refactored?

        # New ids
        new_ids = []
        #  Insert new unmatched country entries
        for taster in new_tasters:
            new_id = taster.taster_id
            new_ids.append(new_id)
            if new_id in old_ids:
                continue
            else:
                WineReview.objects \
                    .create(wine=wine, taster=taster, rating=-1, description="Not Given")
        
        # Delete old unmatched country entries
        for old_id in old_ids:
            if old_id in new_ids:
                continue
            else:
                WineReview.objects \
                    .filter(wine_id=wine.wine_id, taster_id=old_id) \
                    .delete()

        return HttpResponseRedirect(wine.get_absolute_url())
        #return redirect('wine_review/wine_detail', pk=wine.pk)

@method_decorator(login_required, name='dispatch')
class WineDeleteView(generic.DeleteView):
	model = Wine
	success_message = "Wine deleted successfully"
	success_url = reverse_lazy('wine')
	context_object_name = 'wine'
	template_name = 'wine_review/wine_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		# Delete WineJurisdiction entries
		WineReview.objects \
			.filter(wine_id=self.object.wine_id) \
			.delete()

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())

class PaginatedFilterView(generic.View):
	"""
	Creates a view mixin, which separates out default 'page' keyword and returns the
	remaining querystring as a new template context variable.
	https://stackoverflow.com/questions/51389848/how-can-i-use-pagination-with-django-filter
	"""
	def get_context_data(self, **kwargs):
		context = super(PaginatedFilterView, self).get_context_data(**kwargs)
		if self.request.GET:
			querystring = self.request.GET.copy()
			if self.request.GET.get('page'):
				del querystring['page']
			context['querystring'] = querystring.urlencode()
		return context


class WineFilterView(PaginatedFilterView, FilterView):
    model = Wine
    filterset_class = WineFilter
    context_object_name = 'wine_LIST'
    template_name = 'wine_review/wine_filter.html'
    paginate_by = 50