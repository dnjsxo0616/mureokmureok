from rest_framework import serializers
from .models import Puzzle, PuzzlePiece, SolvedPuzzle

class PuzzlePieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuzzlePiece
        fields = ['id', 'position_x', 'position_y', 'image', 'is_solved']

class PuzzleSerializer(serializers.ModelSerializer):
    pieces = PuzzlePieceSerializer(many=True, read_only=True)

    class Meta:
        model = Puzzle
        fields = ['id', 'image', 'solved_image', 'width', 'height', 'pieces']

class SolvedPuzzleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolvedPuzzle
        fields = ['id', 'user', 'puzzle_image']