from django.contrib import admin
import nested_admin
from .models import Company, CommercialProposal, Service, ImplementationStage, SubStage, Project
from django.urls import reverse
from django.utils.html import format_html


class SubStageInline(nested_admin.NestedTabularInline):
    model = SubStage
    extra = 1
    verbose_name = "Подэтап"
    verbose_name_plural = "Подэтапы реализации"


class ImplementationStageInline(nested_admin.NestedTabularInline):
    model = ImplementationStage
    inlines = [SubStageInline]
    extra = 1
    verbose_name = "Этап"
    verbose_name_plural = "Этапы реализации"


@admin.register(Service)
class ServiceAdmin(nested_admin.NestedModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    inlines = [ImplementationStageInline]


@admin.register(CommercialProposal)
class CommercialProposalAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "service", "project", "date_created", "pdf_button")
    list_filter = ("company", "service",)
    search_fields = ("title", "company__name", "service__name")
    readonly_fields = ("date_created",)
    fieldsets = (
        (None, {
            "fields": ("company", "service", "project", "title", "description")
        }),
        ("Дополнительно", {
            "fields": ("date_created",),
            "classes": ("collapse",)
        }),
    )

    def pdf_button(self, obj):
        url = reverse("proposal_pdf", args=[obj.id])
        return format_html('<a class="button" href="{}" target="_blank">📄 Сформировать PDF</a>', url)

    pdf_button.short_description = "PDF"
    pdf_button.allow_tags = True


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
