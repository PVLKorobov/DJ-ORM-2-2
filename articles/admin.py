from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Article, Scope, Tag


class RelationshipFormset(BaseInlineFormSet):
    def clean(self) -> None:
        super().clean()

        mainCount = 0
        for form in self.forms:
            if form.cleaned_data['is_main']:
                mainCount += 1

        if mainCount == 0:
            raise ValidationError('Обязательно должен быть основной отдел')
        if mainCount > 1:
            raise ValidationError('Основной раздел может быть только один')


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = RelationshipFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']