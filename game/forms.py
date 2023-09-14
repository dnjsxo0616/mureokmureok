from django import forms
from .models import Puzzle, SolvedPuzzle

class PuzzleForm(forms.ModelForm):
    class Meta:
        model = Puzzle
        fields = ['image', 'solved_image', 'width', 'height']

class SolvedPuzzleForm(forms.ModelForm):
    class Meta:
        model = SolvedPuzzle
        fields = ['puzzle_image']