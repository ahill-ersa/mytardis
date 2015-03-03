from django.contrib.auth.decorators import login_required, permission_required
from haystack.views import SearchView
from haystack.query import SearchQuerySet
from tardis.apps.acad.forms import RawSearchForm, AdvancedSearchForm
from tardis.tardis_portal.views import SearchQueryString
from tardis.tardis_portal.auth import decorators as authz
import logging
from django.shortcuts import render, get_object_or_404
from django.template import Context
from django.http import HttpResponseRedirect, HttpResponse,\
    HttpResponseForbidden, HttpResponseNotFound
from tardis.tardis_portal.models import Experiment, ExperimentParameter, \
    DatafileParameter, DatasetParameter, ObjectACL, DataFile, \
    DatafileParameterSet, ParameterName, GroupAdmin, Schema, \
    Dataset, ExperimentParameterSet, DatasetParameterSet, \
    License, UserProfile, UserAuthentication, Token
from tardis.tardis_portal.shortcuts import render_response_index, \
    return_response_error, return_response_not_found, \
    render_response_search, get_experiment_referer
from .models import Organism, Source, Sample, Extract, Library, Sequence,   Processing, Analysis

logger = logging.getLogger(__name__)

class AcadSearchView(SearchView):
    def __name__(self):
        return "AcadSearchView"

    def extra_context(self):
        extra = super(AcadSearchView, self).extra_context()
        # Results may contain Experiments, Datasets and DataFiles.
        # Group them into experiments, noting whether or not the search
        # hits were in the Dataset(s) or DataFile(s)
        logger.info("self.results %s"%self.results)
        exp_results=self.results.facet('experiment_id_stored')
        exp_facets = exp_results.facet_counts()
        if exp_facets:
            experiment_facets = exp_facets['fields']['experiment_id_stored']
            experiment_ids = [int(f[0])
                              for f in experiment_facets if int(f[1]) > 0]
        else:
            experiment_ids = []

        access_list = []

        if self.request.user.is_authenticated():
            access_list.extend(
                [e.pk for e in
                 authz.get_accessible_experiments(self.request)])

        access_list.extend(
            [e.pk for e in Experiment.objects.exclude(
                public_access=Experiment.PUBLIC_ACCESS_NONE)])

        ids = list(set(experiment_ids) & set(access_list))
        experiments = Experiment.objects.filter(pk__in=ids)\
                                        .order_by('-update_time')

        #results = []
        #for e in experiments:
        #    result = {}
        #    result['sr'] = e
        #    result['dataset_hit'] = False
        #    result['datafile_hit'] = False
        #    result['experiment_hit'] = False
        #    results.append(result)

        extra['experiments'] = experiments

        source_results=self.results.facet('source_id_stored')
        source_facets = source_results.facet_counts()
        if source_facets:
            source_facets = source_facets['fields']['source_id_stored']
            #logger.info(source_facets)
            source_ids = [f[0]
                              for f in source_facets if int(f[1]) > 0]
        else:
            source_ids = []
        sources=[]
        for id in list(set(source_ids)):
            sources.extend(Source.objects.extra(where=["id LIKE '"+id+"'"]))
        sources.sort(key=lambda source: source.date, reverse=False)

        extra['sources'] = sources

        return extra

    # override SearchView's method in order to
    # return a ResponseContext
    def create_response(self):
        (paginator, page) = self.build_page()

        # Remove unnecessary whitespace
        # TODO this should just be done in the form clean...
        query = SearchQueryString(self.query)
        context = {
            'search_query': query,
            'form': self.form,
            'page': page,
            'paginator': paginator,
        }
        context.update(self.extra_context())

        return render_response_index(self.request, self.template, context)


def single_search(request):
    #search_query = FacetFixedSearchQuery(backend=HighlightSearchBackend())
    sqs = SearchQuerySet() #query=search_query)
    sqs.highlight()

    return AcadSearchView(
        template='search/acad_search.html',
        searchqueryset=sqs,
        form_class=RawSearchForm,
    ).__call__(request)

def search_source(request):

    """Either show the search source form or the result of the search
    source query.

    """

    if len(request.GET) == 0:
        c = Context({'searchForm': AdvancedSearchForm()})
        url = 'search/advanced_search_form.html'
        return HttpResponse(render_response_search(request, url, c))

    #form = __getSearchExperimentForm(request)
    #experiments = __processExperimentParameters(request, form)

    # check if the submitted form is valid
    #if experiments is not None:
    #    bodyclass = 'list'
    #else:
    #    return __forwardToSearchExperimentFormPage(request)

    sqs = SearchQuerySet() #query=search_query)
    sqs.highlight()

    return AcadSearchView(
        template='search/acad_search.html',
        searchqueryset=sqs,
        form_class=AdvancedSearchForm,
    ).__call__(request)

def source_index(request):
    context = {'sources': Source.objects.all()}
    return render(request, 'source/index.html', context)

def source_detail(request, id):
    source = get_object_or_404(Source, pk=id)
    samples = source.sample_set.all()
    context = {'source': source, 'samples': samples}
    return render(request, 'source/detail.html', context)