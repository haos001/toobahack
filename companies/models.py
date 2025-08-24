from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    
    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name="Название компании")
    description = models.TextField(verbose_name="Описание")
    address = models.CharField(max_length=300, verbose_name="Адрес")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    website = models.URLField(blank=True, verbose_name="Сайт")
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True, verbose_name="Логотип")
    
    # Благотворительная информация
    charity_description = models.TextField(verbose_name="Описание благотворительной деятельности")
    charity_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма пожертвований")
    charity_frequency = models.CharField(max_length=50, choices=[
        ('monthly', 'Ежемесячно'),
        ('yearly', 'Ежегодно'),
        ('weekly_friday', 'По пятницам'),
        ('percent_revenue', 'Процент от выручки'),
        ('tooba_collections', 'На сборы в Tooba'),
        ('once', 'Разово'),
    ], verbose_name="Периодичность")
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    is_verified = models.BooleanField(default=False, verbose_name="Проверено")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Координаты для карты
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('company_detail', kwargs={'pk': self.pk})


class CompanyApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]
    
    # Основная информация
    company_name = models.CharField(max_length=200, verbose_name="Название компании")
    contact_person = models.CharField(max_length=100, verbose_name="Контактное лицо")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    website = models.URLField(blank=True, verbose_name="Сайт компании")
    
    # Информация о компании
    description = models.TextField(verbose_name="Описание компании")
    address = models.CharField(max_length=300, verbose_name="Адрес")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    
    # Благотворительная деятельность
    charity_description = models.TextField(verbose_name="Описание благотворительной деятельности")
    charity_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма пожертвований")
    charity_frequency = models.CharField(max_length=50, choices=[
        ('monthly', 'Ежемесячно'),
        ('yearly', 'Ежегодно'),
        ('weekly_friday', 'По пятницам'),
        ('percent_revenue', 'Процент от выручки'),
        ('tooba_collections', 'На сборы в Tooba'),
        ('once', 'Разово'),
    ], verbose_name="Периодичность")
    
    # Дополнительная информация
    additional_info = models.TextField(blank=True, verbose_name="Дополнительная информация")
    
    # Статус заявки
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Заявка компании"
        verbose_name_plural = "Заявки компаний"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.company_name} - {self.get_status_display()}"
