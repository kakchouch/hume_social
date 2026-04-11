from django import forms
from .models import MiniThesis, Comment


class MiniThesisForm(forms.ModelForm):
    """Form for creating and editing mini-theses."""

    class Meta:
        model = MiniThesis
        fields = [
            'thesis',
            'facts',
            'normative_premises',
            'conclusion',
            'declared_limits',
        ]
        widgets = {
            'thesis': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'State your clear and contestable proposition...'
            }),
            'facts': forms.Textarea(attrs={
                'rows': 8,
                'placeholder': 'Present your sourced facts with references...'
            }),
            'normative_premises': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Declare your underlying moral values or postulates...'
            }),
            'conclusion': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'State your logically derived conclusion...'
            }),
            'declared_limits': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Acknowledge what you have not addressed...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True


class CommentForm(forms.ModelForm):
    """Form for adding comments."""

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Add your comment...'
            }),
        }
