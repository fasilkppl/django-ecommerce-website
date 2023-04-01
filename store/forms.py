from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = (
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    )

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)
    
    class Meta:
        model = Review
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 5}),
        }
