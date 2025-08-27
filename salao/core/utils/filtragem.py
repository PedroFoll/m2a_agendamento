from django.contrib import admin

class PrecoRangeFilter(admin.SimpleListFilter):
    title='Faixa de preço'
    parameter_name = 'preço'

    def lookups(self, request, model_admin):
        return [
            ('0-50', 'Até R$50'),
            ('50-100', 'R$50 a R$100'),
            ('100-200', 'R$100 a R$200'),
            ('200+', 'Acima de R$200'),
        ]
    
    def queryset(self, request, queryset):
        if self.value()=='0-50':
            return queryset.filter(preco__lte=50)
        if self.value()=='50-100':
            return queryset.filter(preco__gte=50, preco__lte=100)
        if self.value()=='100-200':
            return queryset.filter(preco__gte=100, preco__lte=200)
        if self.value()=='200+':
            return queryset.filter(preco__gte=200)
        return queryset
