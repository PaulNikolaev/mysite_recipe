from django import forms
from .models import Recipe, Ingredient, Step


class IngredientForm(forms.ModelForm):
    """
    Форма для добавления ингредиентов
    """

    class Meta:
        model = Ingredient
        fields = ('title', 'amount', 'quantity')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class StepForm(forms.ModelForm):
    """
    Форма для добавления этапов приготовления
    """

    class Meta:
        model = Step
        fields = ('step_number', 'description', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class RecipeCreateForm(forms.ModelForm):
    """
    Форма добавления статей на сайте
    """

    class Meta:
        model = Recipe
        fields = ('title', 'category', 'description', 'cooking_time', 'servings', 'thumbnail', 'status')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class RecipeUpdateForm(forms.ModelForm):
    """
    Форма обновления статьи на сайте
    """

    class Meta:
        model = Recipe
        fields = RecipeCreateForm.Meta.fields + ('fixed',)

        def __init__(self, *args, **kwargs):
            """
            Обновление стилей формы под Bootstrap
            """
            super().__init__(*args, **kwargs)
            self.fields['fixed'].widget.attrs.update({
                'class': 'form-check-input',
            })


class SearchForm(forms.Form):
    query = forms.CharField(label="Поиск рецептов")