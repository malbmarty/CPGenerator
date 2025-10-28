from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название компании")

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name="Проект")

    class Meta:
        verbose_name = "проект"
        verbose_name_plural = "проекты"

    def __str__(self):
        return self.name
    
class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name="Услуга", null=True, blank=True)
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        
    def __str__(self):
        return self.name

class CommercialProposal(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="proposals",
        verbose_name="Компания"
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name="Услуга"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name="Проект",
        null=True,
        blank=True
    )
    title = models.CharField(max_length=255, verbose_name="Название коммерческого предложения")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    date_created = models.DateField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Коммерческое предложение"
        verbose_name_plural = "Коммерческие предложения"

    def __str__(self):
        return f"{self.title} ({self.company.name})"
    


class ImplementationStage(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="stages",
        verbose_name="Услуга"
    )
    name = models.CharField(max_length=255, verbose_name="Этап реализации")
    order = models.PositiveIntegerField(default=1, verbose_name="Порядок этапа")

    class Meta:
        verbose_name = "Этап реализации"
        verbose_name_plural = "Этапы реализации"
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} ({self.service.name})"


class SubStage(models.Model):
    stage = models.ForeignKey(
        ImplementationStage,
        on_delete=models.CASCADE,
        related_name="sub_stages",
        verbose_name="Этап реализации"
    )
    name = models.CharField(max_length=255, verbose_name="Подэтап реализации")
    order = models.PositiveIntegerField(default=1, verbose_name="Порядок подэтапа")
    description = models.TextField(blank=True, null=True, verbose_name="Описание подэтапа")
    duration_days = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=0,
        verbose_name="Продолжительность (дней)",
    )
    cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Стоимость (₽)",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Подэтап реализации"
        verbose_name_plural = "Подэтапы реализации"
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} ({self.stage.name})"
