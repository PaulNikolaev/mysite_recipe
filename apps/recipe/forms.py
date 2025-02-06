from django import forms
from .models import Recipe

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
