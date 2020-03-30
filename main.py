import sys
import math
from tqdm import tqdm
from PIL import Image
import numpy as np
from hexgrid import calculate_polygons
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def hexagon(image, R, h):
    image = np.array(image)[:, :, :3]
    rows, cols, _ = image.shape
    hexagon_points = calculate_polygons(0, 0, rows, cols, R)
    polygons = [Polygon(points) for points in hexagon_points]
    polygon_to_i_j = [([], []) for _ in polygons]
    i_j_to_polygon = [[-1 for _ in range(cols)] for _ in range(rows)]
    for l, poly in tqdm(enumerate(polygons), total=len(polygons)):
        min_x, min_y, max_x, max_y = poly.bounds
        min_x = math.floor(min_x)
        min_y = math.floor(min_y)
        max_x = math.ceil(max_x)
        max_y = math.ceil(max_y)
        for i in range(max(0, min_x), min(max_x + 1, rows)):
            for j in range(max(0, min_y), min(max_y + 1, cols)):
                if i_j_to_polygon[i][j] != -1:
                    continue
                x, y = i, j
                if i == min_x or i == 0:
                    x = i + 0.1
                if j == min_y or j == 0:
                    y = j + 0.1

                point = Point(x, y)
                if poly.contains(point):
                    polygon_to_i_j[l][0].append(i)
                    polygon_to_i_j[l][1].append(j)
                    i_j_to_polygon[i][j] = l

    polygon_to_color = [255 for _ in polygons]
    for l in range(len(polygons)):
        indices = polygon_to_i_j[l]
        if len(indices[0]) > 0:
            color = np.mean(image[indices], axis=0)
            polygon_to_color[l] = color

    pixelized_image = np.ones_like(image) * 255.0
    for i in range(rows):
        for j in range(cols):
            polygon = i_j_to_polygon[i][j]
            pixelized_image[i, j] = polygon_to_color[polygon]

    pixelized_image = Image.fromarray(np.uint8(pixelized_image))
    return pixelized_image


def square(image, R, h):
    n = R
    pixel_size = R // 2 if h is None else h
    w, h = image.size

    def get_center(im, w, h, ps=pixel_size):
        w //= 2
        h //= 2
        box = (w - ps // 2, h - ps // 2, w + ps // 2, h + ps // 2)
        return im.crop(box)

    def get_center_mean(im, w, h, ps=pixel_size):
        center = get_center(im, w, h, ps)
        mean_val = np.mean(center, axis=(0, 1))
        center = np.array(center)
        center[:, :, :] = mean_val
        # center.show()
        return Image.fromarray(center)

    pixel_size -= (pixel_size % 2)
    box = (n * pixel_size, n * pixel_size)
    background = Image.new('RGB', box, (255, 255, 255))

    for i in range(n):
        for j in range(n):
            crop_box = (w // n * i, h // n * j, w // n * (i + 1), h // n * (j + 1))
            cropped = image.crop(crop_box)
            center = get_center_mean(cropped, w // n, h // n)
            paste_box = (i * pixel_size, j * pixel_size, (i + 1) * pixel_size, (j + 1) * pixel_size)
            background.paste(center, paste_box)

    return background


def split(image, R, h):
    width, height = image.size
    n_w = int(R * width / 100)
    n_h = int(R * height / 100)
    h = max(1, (n_w + n_h) // 20) if h is None else h

    def crop(im, w1, h1, n_w1, n_h1):
        box = (w1, h1, w1 + n_w1, h1 + n_h1)
        return im.crop(box)

    box = (width + (width // n_w - 1) * h, height + (height // n_h - 1) * h)
    background = Image.new('RGB', box, color=(255, 255, 255))

    i_c = 0
    j_c = 0
    for i in range(0, height, n_h):
        for j in range(0, width, n_w):
            foreground = crop(image, j, i, n_w, n_h)
            box = ((n_w + h) * (j_c), (n_h + h) * (i_c))
            background.paste(foreground, box)
            j_c += 1
        i_c += 1
        j_c = 0

    return background


switcher = {
    'hex': hexagon,
    'sq': square,
    'split': split,
}

if __name__ == '__main__':
    image_name = str(sys.argv[1])
    outfile_name = str(sys.argv[2])
    mode = str(sys.argv[3])
    R = int(sys.argv[4])
    try:
        h = int(sys.argv[5])
    except:
        h = None
    try:
        alpha = float(sys.argv[6])
    except:
        alpha = None

    image = Image.open(image_name)
    pixelized_image = switcher[mode](image, R, h)
    if mode != 'split' and alpha is not None:
        pixelized_image = Image.fromarray(
            (np.array(image) * alpha + (1 - alpha) * np.array(pixelized_image)).astype(np.uint8))

    # pixelized_image.show()
    pixelized_image.save(outfile_name)
