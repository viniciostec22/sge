from django.urls import path
from . import views

urlpatterns = [
    path('outflow/list/', views.OutflowListView.as_view(), name='outflow_list'),
    path('outflow/create/', views.OutflowCreateView.as_view(), name='outflow_create'),
    path('outflow/<int:pk>/detail/', views.OutflowDetailView.as_view(), name='outflow_detail'),
    # path('outflows/<int:pk>/update', views.outflowUpdateView.as_view(), name='outflow_update'),
    # path('outflows/<int:pk>/delete', views.outflowDeleteView.as_view(), name='outflow_delete'),
]
