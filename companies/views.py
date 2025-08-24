from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Company, Category, CompanyApplication
from .forms import CompanyApplicationForm


def company_list(request):
    companies = Company.objects.filter(is_verified=True).select_related('category')
    categories = Category.objects.all()
    
    # Поиск
    search = request.GET.get('search')
    if search:
        companies = companies.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search) |
            Q(charity_description__icontains=search)
        )
    
    # Фильтр по категории
    category = request.GET.get('category')
    if category:
        companies = companies.filter(category_id=category)
    
    # Фильтр по периодичности
    charity_frequency = request.GET.get('charity_frequency')
    if charity_frequency:
        companies = companies.filter(charity_frequency=charity_frequency)
    
    # Пагинация
    paginator = Paginator(companies, 12)  # 12 компаний на страницу
    companies = paginator.get_page(request.GET.get('page'))
    
    context = {
        'companies': companies,
        'categories': categories,
    }
    return render(request, 'companies/company_list.html', context)


def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk, is_verified=True)
    context = {
        'company': company,
    }
    return render(request, 'companies/company_detail.html', context)


def company_apply(request):
    try:
        if request.method == 'POST':
            form = CompanyApplicationForm(request.POST)
            if form.is_valid():
                application = form.save()
                messages.success(
                    request, 
                    'Ваша заявка успешно отправлена! Мы рассмотрим её в течение 2-3 рабочих дней и свяжемся с вами.'
                )
                return redirect('apply_success')
        else:
            form = CompanyApplicationForm()
        
        context = {
            'form': form,
            'categories': Category.objects.all(),
        }
        return render(request, 'companies/company_apply.html', context)
    except Exception as e:
        messages.error(request, 'Произошла ошибка при отправке заявки. Попробуйте еще раз.')
        return redirect('company_apply')


def apply_success(request):
    return render(request, 'companies/apply_success.html')
