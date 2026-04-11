from django import forms
from .models import MiniThesis, ThesisReviewHighlight


FIELD_CHOICES = [
    ('political', 'Political'),
    ('philosophic', 'Philosophic'),
    ('scientific', 'Scientific'),
    ('technical', 'Technical'),
]

LENS_CHOICES = [
    ('conservative', 'Conservative'),
    ('liberal', 'Liberal'),
    ('traditionalist', 'Traditionalist'),
    ('reform', 'Reform'),
    ('socialist', 'Socialist'),
    ('christian-democrat', 'Christian Democrat'),
    ('social-democrat', 'Social Democrat'),
    ('communist', 'Communist'),
    ('political-ecology', 'Political Ecology'),
    ('systems-outputs-optimizations', 'Systems Outputs Optimizations'),
    ('availability', 'Availability'),
    ('stewardship', 'Stewardship'),
    ('innovation', 'Innovation'),
    ('safety', 'Safety'),
    ('security', 'Security'),
]

FIELD_PRESETS = {
    'political': [
        'Political legitimacy requires transparent and accountable institutions.',
        'Public decisions should prioritize the common good over private gain.',
    ],
    'philosophic': [
        'Claims should be internally coherent and open to rational critique.',
        'Moral judgments require explicit principles, not implicit assumptions.',
    ],
    'scientific': [
        'Explanations should be grounded in reproducible evidence.',
        'Extraordinary claims require proportionally strong evidence.',
    ],
    'technical': [
        'Systems should be evaluated through reliability, safety, and maintainability.',
        'Trade-offs must be explicit when optimizing for performance or cost.',
    ],
}

LENS_PRESETS = {
    'conservative': [
        'Institutional stability is a public good that should not be disrupted lightly.',
    ],
    'liberal': [
        'Individual rights and civil liberties should be protected by default.',
    ],
    'traditionalist': [
        'Inherited social practices carry accumulated practical wisdom.',
    ],
    'reform': [
        'Institutions should evolve when evidence shows persistent harm or inefficiency.',
    ],
    'socialist': [
        'Economic arrangements should reduce structural inequality and exploitation.',
    ],
    'christian-democrat': [
        'Public policy should uphold human dignity, solidarity, and subsidiarity.',
    ],
    'social-democrat': [
        'Markets should be balanced by strong social protections and democratic oversight.',
    ],
    'communist': [
        'Collective ownership of key productive resources can be justified to prevent domination.',
    ],
    'political-ecology': [
        'Ecological limits should constrain economic and political decision-making.',
    ],
    'systems-outputs-optimizations': [
        'System design should optimize measurable outcomes under explicit constraints.',
    ],
    'availability': [
        'Critical services should prioritize continuity and graceful degradation.',
    ],
    'stewardship': [
        'Resources should be managed for long-term resilience, not short-term extraction.',
    ],
    'innovation': [
        'Experimentation is justified when paired with transparent evaluation and rollback paths.',
    ],
    'safety': [
        'Avoiding severe harm takes precedence over marginal efficiency gains.',
    ],
    'security': [
        'Threat modeling and least-privilege controls are baseline requirements for trust.',
    ],
}

COMBINED_PRESETS = {
    ('political', 'liberal'): [
        'Constitutional checks and minority rights are essential for legitimate governance.',
    ],
    ('political', 'conservative'): [
        'Policy change should preserve institutional continuity and social trust.',
    ],
    ('political', 'social-democrat'): [
        'Democratic legitimacy includes guaranteeing universal access to core public services.',
    ],
    ('scientific', 'political-ecology'): [
        'Policy should integrate scientific uncertainty with precaution against irreversible ecological harm.',
    ],
    ('technical', 'reform'): [
        'Legacy systems should be modernized incrementally with measurable safety and performance gains.',
    ],
    ('technical', 'availability'): [
        'Reliability budgets should be explicit and tied to user-facing service levels.',
    ],
    ('technical', 'security'): [
        'Security controls should be integrated by design, not added after deployment.',
    ],
    ('technical', 'safety'): [
        'Fail-safe behavior should be validated for high-impact failure modes.',
    ],
}


def get_normative_presets(argument_field, viewing_lens):
    """Build a deduplicated list of presets from selected field and lens."""
    presets = []
    if argument_field in FIELD_PRESETS:
        presets.extend(FIELD_PRESETS[argument_field])
    if viewing_lens in LENS_PRESETS:
        presets.extend(LENS_PRESETS[viewing_lens])
    presets.extend(COMBINED_PRESETS.get((argument_field, viewing_lens), []))

    deduped = []
    seen = set()
    for premise in presets:
        if premise not in seen:
            deduped.append(premise)
            seen.add(premise)
    return deduped


def get_all_normative_presets():
    """Return every available preset for first-load form rendering."""
    presets = []
    for values in FIELD_PRESETS.values():
        presets.extend(values)
    for values in LENS_PRESETS.values():
        presets.extend(values)
    for values in COMBINED_PRESETS.values():
        presets.extend(values)

    deduped = []
    seen = set()
    for premise in presets:
        if premise not in seen:
            deduped.append(premise)
            seen.add(premise)
    return deduped


class MiniThesisForm(forms.ModelForm):
    """Form for creating and editing mini-theses."""

    argument_field = forms.ChoiceField(
        required=False,
        choices=[('', 'Select a field')] + FIELD_CHOICES,
        help_text='Choose the discourse field to load relevant normative presets.',
    )
    viewing_lens = forms.ChoiceField(
        required=False,
        choices=[('', 'Select a viewing lens')] + LENS_CHOICES,
        help_text='Choose the lens through which your thesis is framed.',
    )
    preset_normative_premises = forms.MultipleChoiceField(
        required=False,
        choices=[],
        widget=forms.CheckboxSelectMultiple,
        help_text='Select one or more preset normative premises.',
    )
    custom_normative_premises = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                'placeholder': 'Add your custom normative premises...',
            }
        ),
        help_text='You can add custom premises in your own words.',
        label='Custom normative premises',
    )

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

        argument_field = None
        viewing_lens = None
        if self.is_bound:
            argument_field = self.data.get('argument_field')
            viewing_lens = self.data.get('viewing_lens')

        if argument_field or viewing_lens:
            presets = get_normative_presets(argument_field, viewing_lens)
        else:
            presets = get_all_normative_presets()
        self.fields['preset_normative_premises'].choices = [
            (premise, premise) for premise in presets
        ]

        self.fields['normative_premises'].widget = forms.HiddenInput()
        if self.instance and self.instance.pk and self.instance.normative_premises:
            self.fields['custom_normative_premises'].initial = (
                self.instance.normative_premises
            )

        for field in self.fields.values():
            field.required = True

        self.fields['argument_field'].required = False
        self.fields['viewing_lens'].required = False
        self.fields['preset_normative_premises'].required = False
        self.fields['custom_normative_premises'].required = False
        self.fields['normative_premises'].required = False

    def clean(self):
        cleaned_data = super().clean()

        argument_field = cleaned_data.get('argument_field')
        viewing_lens = cleaned_data.get('viewing_lens')
        selected_presets = cleaned_data.get('preset_normative_premises') or []
        custom_premises = (cleaned_data.get('custom_normative_premises') or '').strip()

        if not selected_presets and not custom_premises:
            self.add_error(
                'custom_normative_premises',
                'Add at least one custom premise or select a preset premise.',
            )
            return cleaned_data

        lines = []
        if argument_field:
            lines.append(f"Field: {argument_field}")
        if viewing_lens:
            lines.append(f"Viewing lens: {viewing_lens}")
        if selected_presets:
            lines.append('Preset normative premises:')
            lines.extend([f"- {premise}" for premise in selected_presets])
        if custom_premises:
            lines.append('Custom normative premises:')
            lines.append(custom_premises)

        cleaned_data['normative_premises'] = '\n'.join(lines)
        return cleaned_data


class ThesisReviewHighlightForm(forms.ModelForm):
    """Create a highlight review by selecting exact text from one thesis section."""

    class Meta:
        model = ThesisReviewHighlight
        fields = ['section', 'selected_text', 'tag', 'comment']
        widgets = {
            'selected_text': forms.Textarea(attrs={'rows': 3, 'readonly': 'readonly'}),
            'comment': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Optional context for this highlighted segment...',
                }
            ),
        }

    def clean_selected_text(self):
        selected_text = (self.cleaned_data.get('selected_text') or '').strip()
        if not selected_text:
            raise forms.ValidationError('Select part of the thesis text before submitting a review highlight.')
        return selected_text
