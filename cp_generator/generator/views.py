from django.http import HttpResponse, Http404
from django.views import View
from django.template.loader import render_to_string
from weasyprint import HTML
from django.views.generic.base import TemplateView
from .models import CommercialProposal,Service
from weasyprint import HTML, CSS
from django.conf import settings


class PdfPageView(TemplateView):
    template_name = "generator/pdf_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        proposal = CommercialProposal.objects.get(id=1)
        service = proposal.service

        context['subject'] = proposal.company.name if proposal.company.name else service.name
        context['label'] = "Для компании:" if proposal.company.name else "Услуга:"

        stages_with_totals = []
        total_days_all = 0
        total_cost_all = 0

        for stage in service.stages.prefetch_related('sub_stages').all():
            total_days = sum(sub.duration_days or 0 for sub in stage.sub_stages.all())
            total_cost = sum(sub.cost or 0 for sub in stage.sub_stages.all())

            total_days_all += total_days
            total_cost_all += total_cost
            
            stages_with_totals.append({
                'stage': stage,
                'sub_stages': stage.sub_stages.all(),
                'total_days': total_days,
                'total_cost': total_cost
            })

        context['stages'] = stages_with_totals
        context['total_days_all'] = total_days_all
        context['total_cost_all'] = total_cost_all

        return context
    
class GenerateProposalPDFView(View):

    def get(self, request, pk):
        try:
            proposal = CommercialProposal.objects.select_related('company', 'service').get(pk=pk)
        except CommercialProposal.DoesNotExist:
            raise Http404("Коммерческое предложение не найдено")

        service = proposal.service

        # Собираем данные об этапах и подэтапах
        stages_with_totals = []
        total_days_all = 0
        total_cost_all = 0

        for stage in service.stages.prefetch_related("sub_stages").all():
            total_days = sum(sub.duration_days or 0 for sub in stage.sub_stages.all())
            total_cost = sum(sub.cost or 0 for sub in stage.sub_stages.all())

            total_days_all += total_days
            total_cost_all += total_cost

            stages_with_totals.append({
                "stage": stage,
                "sub_stages": stage.sub_stages.all(),
                "total_days": total_days,
                "total_cost": total_cost,
            })

        context = {
            "proposal": proposal,
            "subject": proposal.company.name if proposal.company.name else service.name,
            "label": "Для компании:" if proposal.company.name else "Услуга:",
            "stages": stages_with_totals,
        }

        context['total_days_all'] = total_days_all
        context['total_cost_all'] = total_cost_all

        html_string = render_to_string("generator/pdf_template.html", context)
        pdf = HTML(string=html_string, base_url=settings.STATIC_ROOT).write_pdf(stylesheets=[CSS(string='@page { size: 1920px 1080px; margin: 0}')])

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="{proposal.title}.pdf"'
        return response
    
