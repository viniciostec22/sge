from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.template.loader import render_to_string

class BrandListView(ListView):
    model = models.Brand
    template_name = 'brand_list.html'
    context_object_name = 'brands'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        
        if name:
            queryset = queryset.filter(name__icontains=name)
            
        return queryset
    
class BrandCreateView( CreateView):
    model = models.Brand
    template_name = 'brand_create.html'
    form_class = forms.BrandForm
    success_url = reverse_lazy('brand_list')
    
class BrandDetailView(DetailView):
    model = models.Brand
    template_name = 'brand_detail.html'
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            brand = self.get_object()
            data = {
                'id': brand.id,
                'name': brand.name,
                'description': brand.description,
            }
            return JsonResponse(data)
        else:
            return super().render_to_response(context, **response_kwargs)
    
class BrandUpdateView(UpdateView):
    model = models.Brand
    template_name = 'brand_update.html'
    form_class = forms.BrandForm
    success_url = reverse_lazy('brand_list')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Marca atualizada com sucesso!')
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect_url': str(self.success_url)})
        else:
            return redirect(self.success_url)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form_html = render_to_string(self.template_name, {'form': form}, request=self.request)
            return JsonResponse({'success': False, 'form_html': form_html})
        else:
            return self.render_to_response(self.get_context_data(form=form))
    
class BrandDeleteView(SuccessMessageMixin,DeleteView):
    model = models.Brand
    template_name = 'brand_delete.html'
    success_url = reverse_lazy('brand_list')
    success_message = "Marca deletada com sucesso."
    
    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(self.request, self.success_message)
            return response
        except Exception as e:
            messages.error(self.request, "Erro ao deletar a marca: {}".format(str(e)))
            return self.render_to_response(self.get_context_data())
    
    