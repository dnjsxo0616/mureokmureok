from django.shortcuts import render, redirect
from .forms import PuzzleForm, SolvedPuzzleForm
from .models import Puzzle, SolvedPuzzle
from PIL import Image
import requests, random, base64, io
from io import BytesIO


def index(request):
    if request.method == 'POST':
        puzzle_form = PuzzleForm(request.POST)
        if puzzle_form.is_valid():
            puzzle = puzzle_form.save()
            return redirect('play_puzzle')
    else:
        puzzle_form = PuzzleForm()
    
    context = {
        'puzzle_form': puzzle_form,
    }
    return render(request, 'game/index.html', context)


def play_puzzle(request):
    image_url = 'https://source.unsplash.com/500x500/?plant'
    
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    
    pieces = split_image(image, 3)

    context = {
        'image_url': image_url,
        'pieces': pieces,
    }
    
    return render(request, 'game/play_puzzle.html', context)


def split_image(image, num_pieces):
    width, height = image.size
    piece_width = width // num_pieces
    piece_height = height // num_pieces
    
    pieces = []
    for row in range(num_pieces):
        for col in range(num_pieces):
            left = col * piece_width
            upper = row * piece_height
            right = left + piece_width
            lower = upper + piece_height
            
            piece = image.crop((left, upper, right, lower))
            piece_data = convert_image_to_base64(piece)  # 이미지를 Base64로 변환하여 데이터로 저장
            pieces.append(piece_data)
    
    random.shuffle(pieces)  # 조각들을 섞음
    
    return pieces


def convert_image_to_base64(image):
    image_data = io.BytesIO()
    image.save(image_data, format='PNG')
    image_base64 = base64.b64encode(image_data.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{image_base64}"



def solved_puzzles(request):
    # 맞춘 퍼즐 보기 로직
    return render(request, 'game/solved_puzzles.html')