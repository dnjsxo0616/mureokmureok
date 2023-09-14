from django.contrib.auth import get_user_model
from django.db import models


class Puzzle(models.Model):
    image = models.URLField()
    solved_image = models.URLField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

class PuzzlePiece(models.Model):
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE, related_name='pieces')
    position_x = models.PositiveIntegerField()
    position_y = models.PositiveIntegerField() 
    image = models.URLField() 
    is_solved = models.BooleanField(default=False)  

class SolvedPuzzle(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    puzzle_image = models.ImageField(upload_to='solved_puzzles')

    def __str__(self):
        return f"Solved Puzzle #{self.id}"