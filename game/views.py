from django.shortcuts import render, redirect
from .forms import PuzzleForm, SolvedPuzzleForm
from .models import Puzzle, SolvedPuzzle
from PIL import Image, ExifTags
import requests
import random
import base64
import io
from io import BytesIO
from datetime import datetime
from pathlib import Path
from exif import Image as ExifImage


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
    
    pieces, original_image_data = split_image(image, 3)

    context = {
        'image_url': image_url,
        'pieces': pieces,
        'original_image_data': original_image_data,
    }
    
    # API_KEY = 'ZBtGYio5mhpsbQTxRmLHerj3tZAGxjvEi5E7mbNIrL7lAN3GB3'
    # result = identify_plant(image, API_KEY)
    # plant_name = result['suggestions'][0]['plant_name']
    # probability = result['suggestions'][0]['probability']
    # context['plant_name'] = plant_name
    # context['probability'] = probability
    
    return render(request, 'game/play_puzzle.html', context)


def split_image(image, num_pieces):
    width, height = image.size
    piece_width = width // num_pieces
    piece_height = height // num_pieces
    
    pieces = []
    original_image_data = convert_image_to_base64(image)
    
    for row in range(num_pieces):
        for col in range(num_pieces):
            left = col * piece_width
            upper = row * piece_height
            right = left + piece_width
            lower = upper + piece_height
            
            piece = image.crop((left, upper, right, lower))
            piece_data = convert_image_to_base64(piece)
            pieces.append(piece_data)
    
    random.shuffle(pieces)
    
    return pieces, original_image_data


def convert_image_to_base64(image):
    image_data = io.BytesIO()
    image.save(image_data, format='PNG')
    image_data.seek(0)
    image_base64 = base64.b64encode(image_data.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{image_base64}"


def solved_puzzles(request):
    # 맞춘 퍼즐 보기 로직
    return render(request, 'game/solved_puzzles.html')


# API_KEY = 'ZBtGYio5mhpsbQTxRmLHerj3tZAGxjvEi5E7mbNIrL7lAN3GB3'


def extract_exif(image):
    exif_data = None
    try:
        exif_data = image._getexif()
    except (AttributeError, IndexError, TypeError, ValueError):
        pass

    dt = None
    longitude = None
    latitude = None

    if exif_data is not None:
        for tag, value in exif_data.items():
            if tag in ExifTags.TAGS:
                tag_name = ExifTags.TAGS[tag]
                if tag_name == 'DateTimeOriginal':
                    dt = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                elif tag_name == 'GPSInfo':
                    if len(value) >= 2:
                        latitude = value[2]
                        longitude = value[4]

    return dt, longitude, latitude



def identify_plant(image, api_key: str) -> dict:
    dt, longitude, latitude = extract_exif(image)
    params = {
        'images': [convert_image_to_base64(image)],
        'datetime': int(dt.timestamp()) if dt else None,
        'longitude': longitude,
        'latitude': latitude,
    }

    headers = {
        'Content-Type': 'application/json',
        'Api-Key': api_key,
    }

    response = requests.post('https://api.plant.id/v2/identify', json=params, headers=headers)
    assert response.status_code < 300, response.text
    return response.json()
