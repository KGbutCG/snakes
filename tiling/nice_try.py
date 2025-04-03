from PIL import Image, ImageDraw
import math
import numpy as np

# Цветовая палитра (R, G, B)
COLORS = {"green": (100, 160, 80), "yellow": (240, 210, 60), "blue": (70, 100, 180), "white": (255, 255, 255)}


def draw_hexagon_sector(draw, center, radius, angle_start, angle_end, color):
    """Рисует сектор шестиугольника с радиальными линиями"""
    points = [center]
    for angle in np.linspace(angle_start, angle_end, 4):  # 3 радиальные линии на сектор
        x = center[0] + radius * math.cos(math.radians(angle))
        y = center[1] + radius * math.sin(math.radians(angle))
        points.append((x, y))
        if len(points) > 2:
            draw.polygon(points, fill=color, outline="black")
            points = [center, (x, y)]


def generate_base_tile(size=300):
    """Создает базовый тайл с шестиугольным паттерном"""
    img = Image.new("RGB", (size, size), COLORS["white"])
    draw = ImageDraw.Draw(img)
    center = (size // 2, size // 2)
    max_radius = size // 2 - 10

    # Рисуем 6 секторов с радиальными линиями
    for i in range(6):
        angle_start = 60 * i
        angle_end = 60 * (i + 1)
        color = list(COLORS.values())[i % 3]  # Чередуем 3 цвета
        draw_hexagon_sector(draw, center, max_radius, angle_start, angle_end, color)

    # Добавляем центральный шестиугольник
    hex_points = [(center[0] + max_radius * 0.3 * math.cos(math.radians(60 * i + 30))),
        (center[1] + max_radius * 0.3 * math.sin(math.radians(60 * i + 30)))]
    for i in range(6):
        draw.polygon(hex_points, fill=COLORS["blue"], outline="black")
        return img


def create_pattern(tile_size=300, pattern_size=(3, 3)):
    """Генерирует бесшовный паттерн"""
    tile = generate_base_tile(tile_size)
    pattern_width = tile_size * pattern_size[0]
    pattern_height = tile_size * pattern_size[1]
    pattern = Image.new("RGB", (pattern_width, pattern_height))

    for x in range(0, pattern_width, tile_size):
        for y in range(0, pattern_height, tile_size):
            pattern.paste(tile, (x, y))

    return pattern


# Генерация и сохранение
pattern = create_pattern()
pattern.show()
pattern.save("hexagonal_pattern.png")
