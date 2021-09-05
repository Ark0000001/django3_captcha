from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,FormView,UpdateView,DeleteView
from django.views.generic.dates import ArchiveIndexView
from .models import Bb, Rubric

from .forms import BbForm, SearchForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory





# class BbCreateView(CreateView):
#     template_name = 'bboard/create.html'
#     form_class = BbForm
#     success_url = reverse_lazy('index')
#     def get_context_data(self, **kwargs):
#         context=super().get_context_data(**kwargs)
#         context['rubrics']=Rubric.objects.all()
#         return context

# def by_rubric(request,rubric_id):
#     bbs=Bb.objects.filter(rubric=rubric_id)
#     rubrics=Rubric.objects.all()
#     current_rubric=Rubric.objects.get(pk=rubric_id)
#     context={'bbs':bbs, 'rubrics':rubrics, 'current_rubric':current_rubric}
#     return render(request, 'bboard/by_rubric.html', context)

# class BbByRubricView(TemplateView):
#     template_name = 'bboard/by_rubric.html'
#
#     def get_context_data(self, **kwargs):
#         context=super().get_context_data(**kwargs)
#         context['bbs']=Bb.objects.filter(rubric=context['rubric_id'])
#         context['rubrics']=Rubric.objects.all()
#         context['current_rubric']=Rubric.objects.get(pk=context['rubric_id'])
#         return context

class BbByRubricView(ListView):
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        # context['bbs']=Bb.objects.filter(rubric=context['rubric_id'])
        context['rubrics']=Rubric.objects.all()
        context['current_rubric']=Rubric.objects.get(pk=self.kwargs['rubric_id'])
        return context



def index(request):
    bbs = Bb.objects.all()
    rubrics=Rubric.objects.all()
    paginator=Paginator(bbs,3)
    if 'page' in request.GET:
        page_num=request.GET['page']
    else:
        page_num=1
    page=paginator.get_page(page_num)
    context={'rubrics':rubrics, 'page':page,'bbs':page.object_list }

    return render(request, 'bboard/index.html', context)

def nologin(request):

    return render(request, 'bboard/nologin.html')

# def add(request):
#     bbf=BbForm()
#     context={'form':bbf}
#     return render(request,'bboard/create.html',context)
# def add_save(request):
#     bbf=BbForm(request.POST)
#     if bbf.is_valid():
#         bbf.save()
#         return HttpResponseRedirect(reverse('by_rubric',kwargs={'rubric_id':bbf.cleaned_data['rubric'].pk}))
#     else:
#         context={'form':bbf}
#         return render(request,'bboard/create.html',context)
# @login_required
# def add_and_save(request):
#     if request.method=='POST':
#         bbf = BbForm(request.POST)
#         if bbf.is_valid():
#             bbf.save()
#             return HttpResponseRedirect(reverse('bboard:by_rubric',kwargs={'rubric_id':bbf.cleaned_data['rubric'].pk}))
#         else:
#             context = {'form': bbf}
#             return render(request, 'bboard/create.html', context)
#     else:
#         bbf = BbForm()
#         context = {'form': bbf}
#         return render(request, 'bboard/create.html', context)

class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['rubrics']=Rubric.objects.all()
        return context

class BbAddView(LoginRequiredMixin,FormView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    initial = {'price':0.0}

    def get_context_data(self, *args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        context['rubrics']=Rubric.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object=super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('bboard:by_rubric', kwargs={'rubric_id':self.object.cleaned_data['rubric'].pk})


class BbEditView(LoginRequiredMixin,UpdateView):
    model = Bb
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        context['rubrics']=Rubric.objects.all()
        return context

class BbDeleteView(LoginRequiredMixin,DeleteView):
    model = Bb
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, *args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        context['rubrics']=Rubric.objects.all()
        return context

class BbIndexView(ArchiveIndexView):
    model = Bb
    date_field = 'published'
    date_list_period = 'day'
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(*args,**kwargs)
        context['rubrics']=Rubric.objects.all()
        return context

# def edit(request, pk):
    # bb=Bb.objects.get(pk=pk)
    # if request.mathod=='POST':
    #     bbf=BbForm(request.POST,instance=bb)
    #     if bbf.is_valid:
    #         if bbf.has_changed():
    #             bbf.save()
    #             return HttpResponseRedirect(reverse('bboard:by_rubric',kwargs={'rubric_id':bbf.cleaned_data['rubric'].pk}))
    #     else:
    #         context={'form':bbf}
    #         return render(request,'bboard/bb_form.html',context)
    # else:
    #     bbf=BbForm(instance=bb)
    #     context={'form':bbf}
    #     return render(request,'bboard/bb_form.html',context)


def search(request):
    if request.method=='POST':
        sf=SearchForm(request.POST)
        if sf.is_valid():
            keyword=sf.cleaned_data['keyword']
            rubric_id=sf.cleaned_data['rubric'].pk
            bbs=Bb.objects.filter(title__icontains=keyword,rubric=rubric_id)
            context={'bbs':bbs}
            return render(request,'bboard/search_results.html',context)
    else:
        sf=SearchForm()
    context={'form':sf}
    return render(request,'bboard/search.html',context)



# def search(request):
#     FS=formset_factory(SearchForm,extra=1,can_order=True,can_delete=True)
#
#     if request.method=='POST':
#         formset=FS(request.POST)
#         if formset.is_valid():
#             for form in formset:
#                 if form.cleaned_data and not form.cleaned_data['DELETE']:
#                     keyword=form.cleaned_data['keyword']
#                     rubric_id=form.cleaned_data['rubric'].pk
#                     order=form.cleaned_data['ORDER']
#                     bbs=Bb.objects.filter(title__icontains=keyword,rubric=rubric_id,order=order)
#                     context={'bbs':bbs}
#                     return render(request,'bboard/search_results.html',context)
#     else:
#         formset=FS()
#     context={'formset':formset}
#     return render(request,'bboard/search.html',context)