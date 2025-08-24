from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Company, Category, CompanyApplication


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'company_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    
    def company_count(self, obj):
        count = obj.company_set.count()
        return format_html('<span style="background: #007AFF; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{} компаний</span>', count)
    company_count.short_description = 'Количество компаний'


@admin.register(Company) 
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('logo_preview', 'name', 'category', 'charity_display', 'verification_status', 'is_verified', 'created_at')
    list_filter = ('category', 'charity_frequency', 'is_verified', 'created_at')
    search_fields = ('name', 'description', 'charity_description', 'address', 'phone', 'email')
    list_editable = ('is_verified', 'category')
    ordering = ('-created_at',)
    readonly_fields = ('logo_preview', 'view_on_site_link', 'created_at', 'updated_at')
    actions = ['verify_companies', 'unverify_companies']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'category', 'description', 'address', 'logo', 'logo_preview')
        }),
        ('Контакты', {
            'fields': ('phone', 'email', 'website')
        }),
        ('Благотворительность', {
            'fields': ('charity_description', 'charity_amount', 'charity_frequency')
        }),
        ('Местоположение', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Системные поля', {
            'fields': ('is_verified', 'created_at', 'updated_at', 'view_on_site_link')
        })
    )
    
    class Media:
        css = {
            'all': ('admin/css/admin_custom.css',)
        }
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 8px; object-fit: cover;" />', obj.logo.url)
        return format_html('<div style="width: 50px; height: 50px; background: #f0f0f0; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #999;"><i class="fas fa-building"></i></div>')
    logo_preview.short_description = 'Логотип'
    
    def charity_display(self, obj):
        return format_html(
            '<div style="color: #007AFF; font-weight: 600;">{:,.0f} ₽</div>'
            '<div style="color: #8E8E93; font-size: 12px;">{}</div>',
            obj.charity_amount,
            obj.get_charity_frequency_display()
        )
    charity_display.short_description = 'Благотворительность'
    
    def verification_status(self, obj):
        if obj.is_verified:
            return format_html('<span style="color: #34C759; font-weight: 600;">✓ Проверена</span>')
        return format_html('<span style="color: #FF9500; font-weight: 600;">⏳ На проверке</span>')
    verification_status.short_description = 'Статус'
    
    def view_on_site_link(self, obj):
        if obj.pk:
            url = obj.get_absolute_url()
            return format_html(
                '<a href="{}" target="_blank" style="background: #007AFF; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 12px;">👁️ Посмотреть на сайте</a>',
                url
            )
        return "Сохраните компанию, чтобы увидеть ссылку"
    view_on_site_link.short_description = 'Просмотр'
    
    def verify_companies(self, request, queryset):
        count = queryset.update(is_verified=True)
        self.message_user(request, f'Проверено {count} компаний.')
    verify_companies.short_description = 'Верифицировать выбранные компании'
    
    def unverify_companies(self, request, queryset):
        count = queryset.update(is_verified=False)
        self.message_user(request, f'Отменена верификация {count} компаний.')
    unverify_companies.short_description = 'Отменить верификацию'


@admin.register(CompanyApplication)
class CompanyApplicationAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'email', 'phone', 'category', 'status_display', 'status', 'created_at')
    list_filter = ('status', 'category', 'charity_frequency', 'created_at')
    search_fields = ('company_name', 'contact_person', 'email', 'phone', 'description')
    list_editable = ('status',)
    ordering = ('-created_at',)
    actions = ['approve_applications', 'reject_applications']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('company_name', 'contact_person', 'phone', 'email', 'website', 'category')
        }),
        ('О компании', {
            'fields': ('description', 'address')
        }),
        ('Благотворительность', {
            'fields': ('charity_description', 'charity_amount', 'charity_frequency')
        }),
        ('Дополнительно', {
            'fields': ('additional_info', 'status')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    class Media:
        css = {
            'all': ('admin/css/admin_custom.css',)
        }
    
    def status_display(self, obj):
        status_colors = {
            'pending': '#FF9500',
            'approved': '#34C759',
            'rejected': '#FF3B30'
        }
        color = status_colors.get(obj.status, '#8E8E93')
        return format_html(
            '<span style="color: {}; font-weight: 600;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Статус'
    
    def approve_applications(self, request, queryset):
        count = 0
        for application in queryset:
            if application.status == 'pending':
                # Создаем компанию из заявки
                company = Company.objects.create(
                    name=application.company_name,
                    description=application.description,
                    address=application.address,
                    phone=application.phone,
                    email=application.email,
                    website=application.website,
                    charity_description=application.charity_description,
                    charity_amount=application.charity_amount,
                    charity_frequency=application.charity_frequency,
                    category=application.category,
                    is_verified=True
                )
                application.status = 'approved'
                application.save()
                count += 1
        
        self.message_user(request, f'Одобрено {count} заявок и создано компаний.')
    approve_applications.short_description = 'Одобрить выбранные заявки'
    
    def reject_applications(self, request, queryset):
        count = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f'Отклонено {count} заявок.')
    reject_applications.short_description = 'Отклонить выбранные заявки'
