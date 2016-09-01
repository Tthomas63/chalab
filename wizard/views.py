import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import UpdateView

from . import models, flow
from .flow import FlowOperationMixin
from .models import ChallengeModel, DatasetModel, TaskModel, MetricModel, ProtocolModel, \
    DocumentationModel

log = logging.getLogger('wizard.views')
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())


@login_required
def home(request):
    challenges = ChallengeModel.objects.filter(created_by=request.user)
    return render(request, 'wizard/home.html', context={'object_list': challenges})


class ChallengeDescriptionCreate(CreateView, LoginRequiredMixin):
    template_name = 'wizard/challenge/create.html'
    model = ChallengeModel
    fields = ['title', 'organization_name', 'description']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(ChallengeDescriptionCreate, self).form_valid(form)


class ChallengeDescriptionDetail(FlowOperationMixin, DetailView, LoginRequiredMixin):
    template_name = 'wizard/challenge/detail.html'
    model = ChallengeModel
    fields = ['title', 'organization_name', 'description']

    def get_context_data(self, challenge=None, **kwargs):
        context = super().get_context_data(challenge=self.object, **kwargs)
        return context


class ChallengeDataEdit(FlowOperationMixin, LoginRequiredMixin, UpdateView):
    template_name = 'wizard/data/editor.html'
    model = DatasetModel

    fields = ['name']
    current_flow = flow.DataFlowItem

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        c = ChallengeModel.objects.get(id=pk, created_by=self.request.user)

        context = super().get_context_data(challenge=c, **kwargs)
        context['challenge'] = c
        return context

    def get_object(self, **kwargs):
        pk = self.kwargs['pk']

        challenge = ChallengeModel.objects.get(id=pk, created_by=self.request.user)
        return challenge.dataset

    def dispatch(self, request, *args, **kwargs):
        if self.get_object(**kwargs) is None:
            return redirect('wizard:challenge:data.pick', pk=kwargs['pk'])
        else:
            return super().dispatch(request, *args, **kwargs)


class ChallengeTaskUpdate(FlowOperationMixin, LoginRequiredMixin, UpdateView):
    template_name = 'wizard/task.html'
    model = TaskModel
    context_object_name = 'task'

    fields = ['name']
    current_flow = flow.TaskFlowItem

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        c = ChallengeModel.objects.get(id=pk, created_by=self.request.user)

        context = super().get_context_data(challenge=c, **kwargs)
        context['challenge'] = c
        return context

    def get_object(self, **kwargs):
        pk = self.kwargs['pk']

        challenge = ChallengeModel.objects.get(id=pk, created_by=self.request.user)
        return challenge.task

    def dispatch(self, request, *args, **kwargs):
        if self.get_object(**kwargs) is None:
            return redirect('wizard:challenge:data.pick', pk=kwargs['pk'])
        else:
            return super().dispatch(request, *args, **kwargs)


def data_picker(request, pk):
    c = get_object_or_404(ChallengeModel, id=pk, created_by=request.user)

    if c.dataset is not None:
        return redirect('wizard:challenge:data', pk=pk)

    if request.method == 'POST':
        k = request.POST['kind']
        assert k == 'public'

        ds = request.POST['dataset']

        d = get_object_or_404(DatasetModel, is_public=True, id=ds)
        c.dataset = d

        t = get_object_or_404(TaskModel, dataset=d)
        c.task = t

        c.save()

        return redirect('wizard:challenge:data', pk=pk)
    else:
        pds = models.DatasetModel.objects.all().filter(is_public=True)
        context = {'public_datasets': pds,
                   'challenge': c,
                   'flow': flow.Flow(flow.DataFlowItem, c)}
        return render(request, 'wizard/data/picker.html', context=context)


def metric_picker(request, pk):
    c = get_object_or_404(ChallengeModel, id=pk, created_by=request.user)

    if c.metric is not None:
        return redirect('wizard:challenge:metric', pk=pk)

    if request.method == 'POST':
        k = request.POST['kind']
        assert k == 'public'

        mc = request.POST['metric']
        m = get_object_or_404(MetricModel, is_public=True, id=mc)
        c.metric = m
        c.save()
        return redirect('wizard:challenge:metric', pk=pk)
    else:
        public_metrics = MetricModel.objects.all().filter(is_public=True, is_ready=True)
        context = {'challenge': c, 'public_metrics': public_metrics}
        return render(request, 'wizard/metric/picker.html', context=context)


class ChallengeMetricUpdate(FlowOperationMixin, LoginRequiredMixin, UpdateView):
    template_name = 'wizard/metric/detail.html'
    model = MetricModel
    context_object_name = 'metric'

    fields = ['name']
    current_flow = flow.MetricFlowItem

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        c = ChallengeModel.objects.get(id=pk, created_by=self.request.user)

        context = super().get_context_data(challenge=c, **kwargs)
        context['challenge'] = c
        return context

    def get_object(self, **kwargs):
        pk = self.kwargs['pk']

        challenge = ChallengeModel.objects.get(id=pk, created_by=self.request.user)
        return challenge.metric

    def dispatch(self, request, *args, **kwargs):
        if self.get_object(**kwargs) is None:
            return redirect('wizard:challenge:metric.pick', pk=kwargs['pk'])
        else:
            return super().dispatch(request, *args, **kwargs)


class ChallengeProtocolUpdate(FlowOperationMixin, LoginRequiredMixin, UpdateView):
    template_name = 'wizard/protocol.html'
    model = ProtocolModel
    context_object_name = 'protocol'

    fields = ['end_date', 'allow_reuse', 'publicly_available',
              'max_submission_per_day', 'max_submissions']
    current_flow = flow.ProtocolFlowItem

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        c = ChallengeModel.objects.get(id=pk, created_by=self.request.user)

        context = super().get_context_data(challenge=c, **kwargs)
        context['challenge'] = c
        return context

    def get_object(self, **kwargs):
        pk = self.kwargs['pk']

        challenge = ChallengeModel.objects.get(id=pk, created_by=self.request.user)
        protocol = challenge.protocol

        if protocol is None:
            protocol = ProtocolModel.objects.create()
            challenge.protocol = protocol
            challenge.save()

        return protocol


def documentation(request, pk):
    c = get_object_or_404(ChallengeModel, id=pk, created_by=request.user)
    doc = c.documentation

    if doc is None:
        doc = DocumentationModel.create()
        c.documentation = doc
        c.save()

    context = {'challenge': c, 'doc': doc, 'pages': doc.pages}

    return render(request, "wizard/documentation.html", context=context)


def documentation_page(request, pk, page_id):
    return HttpResponse(status=200)
