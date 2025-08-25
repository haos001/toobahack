from django.apps import AppConfig


class CompaniesConfig(AppConfig):
    """
    Конфигурация приложения 'companies' для проекта Круг добра.
    Управляет компаниями-благотворителями и их каталогом.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'companies'
    verbose_name = 'Круг добра - Компании'
