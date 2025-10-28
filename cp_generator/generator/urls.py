from django.contrib import admin
from django.urls import path, include
from . import views 

urlpatterns = [
    path('', views.PdfPageView.as_view(), name="pdf"),
    path('api/proposals/<int:pk>/pdf/', views.GenerateProposalPDFView.as_view(), name='proposal_pdf'),
]