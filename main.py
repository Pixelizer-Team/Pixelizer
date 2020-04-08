import sys
import math
from tqdm import tqdm
from PIL import Image
import numpy as np
from tile_generator import hexagon_tile, cubic_tile, the_wall_tile, double_cubic_tile, pyramid_tile
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from sklearn.metrics import pairwise_distances
from gifify import save_gif


# def intra_block_shuffle(image, R, h):
#     image = np.array(image)[:, :, :3]
#     rows, cols, _ = image.shape
#     pixelized_image = np.ones_like(image) * 255.0
#     for i in range(0, rows, R):
#         for j in range(0, cols, R):
#             image_segment = image[i: i + R, j: j + R, :]
#             image_segment_reshape = image_segment.reshape([-1, 3])


def voronoi_gif(image, R, h, x=100):
    n = R
    m = R if h is None else h

    margin = 0.1
    image = np.array(image)[:, :, :3]
    rows, cols, _ = image.shape
    rows *= 2
    centers = np.array((np.random.randint(-int(margin * rows), int(rows + rows * margin), n),
                        np.random.randint(-int(margin * cols), int(cols + margin * cols), m))).T

    pixels = np.stack(np.meshgrid(range(rows), range(cols)), axis=-1).reshape(-1, 2)
    distances = pairwise_distances(pixels, centers)
    centers_to_i_j = [([], []) for _ in centers]
    i_j_to_centers = [[-1 for _ in range(cols)] for _ in range(rows)]
    for l, p in tqdm(enumerate(pixels), total=len(pixels)):
        i, j = p
        c = np.argmin(distances[l])
        centers_to_i_j[c][0].append(i)
        centers_to_i_j[c][1].append(j)
        i_j_to_centers[i][j] = c

    frames = []
    offset = 0
    rows //= 2
    # print(rows, cols)
    for r in range(x):
        polygon_to_color = [255 for _ in centers]
        pixelized_image = np.ones_like(image) * 255.0
        for l in range(len(centers)):
            indices = [[], []]
            for a, b in zip(centers_to_i_j[l][0], centers_to_i_j[l][1]):
                if offset <= a < offset + rows:
                    indices[0].append(a-offset)
                    indices[1].append(b)
            # [centers_to_i_j[l]]
            # offs = [offset for _ in indices[0]]
            # tmp = [a - b for a, b in zip(indices[0], offs)]
            # indices = [tmp, indices[1]]
            if len(indices) > 0:
                color = np.mean(image[indices], axis=0)
                polygon_to_color[l] = color

            for i, j in zip(indices[0], indices[1]):
                polygon = i_j_to_centers[offset + i][j]
                pixelized_image[i, j] = polygon_to_color[polygon]

        offset += (rows // 2) // x
        pixelized_image = Image.fromarray(np.uint8(pixelized_image))
        frames.append(pixelized_image)

    return frames


def blob(image, R, h):
    image = np.array(image)[:, :, :3]
    rows, cols, _ = image.shape
    i_j_to_centers = np.ones([rows, cols], dtype=np.int32) * -1
    margin = 0.05
    R2 = R ** 2
    i_center = np.random.randint(-int(margin * rows), int(rows + rows * margin))
    j_center = np.random.randint(-int(margin * cols), int(cols + cols * margin))
    centers = []
    centers_to_i_j = []
    while True:
        centers.append((i_center, j_center))
        centers_to_i_j.append(([], []))
        for i in range(max(0, i_center - R), min(rows, i_center + R)):
            for j in range(max(0, j_center - R), min(cols, j_center + R)):
                if (i - i_center) ** 2 + (j - j_center) ** 2 <= R2:
                    if i_j_to_centers[i, j] == -1:
                        centers_to_i_j[-1][0].append(i)
                        centers_to_i_j[-1][1].append(j)
                        i_j_to_centers[i, j] = len(centers) - 1

        i_remaining, j_remaining = np.where(i_j_to_centers == -1)
        if len(centers) % 10 == 0:
            sys.stdout.write(f"\rProgress = {1 - len(i_remaining) / (rows * cols)}")
            sys.stdout.flush()
        if len(i_remaining) == 0:
            break
        index = np.random.randint(0, len(i_remaining))
        i_center, j_center = i_remaining[index], j_remaining[index]

    center_to_color = [255 for _ in centers]
    for l in range(len(centers)):
        indices = centers_to_i_j[l]
        if len(indices[0]) > 0:
            color = np.mean(image[indices], axis=0)
            center_to_color[l] = color

    pixelized_image = np.ones_like(image) * 255.0
    for i in range(rows):
        for j in range(cols):
            polygon = i_j_to_centers[i][j]
            pixelized_image[i, j] = center_to_color[polygon]

    pixelized_image = Image.fromarray(np.uint8(pixelized_image))
    return pixelized_image


def wall(image, R, h):
    image = np.array(image)[:, :, :3]
    rows, cols, _ = image.shape
    hexagon_points, _ = the_wall_tile(0, 0, rows, cols, R)
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


def voronoi(image, R, h):
    n = R
    m = R if h is None else h

    margin = 0.1
    image = np.array(image)[:, :, :3]
    rows, cols, _ = image.shape
    centers = np.array((np.random.randint(-int(margin * rows), int(rows + rows * margin), n),
                        np.random.randint(-int(margin * cols), int(cols + margin * cols), m))).T

    pixels = np.stack(np.meshgrid(range(rows), range(cols)), axis=-1).reshape(-1, 2)
    distances = pairwise_distances(pixels, centers)
    centers_to_i_j = [([], []) for _ in centers]
    i_j_to_centers = [[-1 for _ in range(cols)] for _ in range(rows)]
    for l, p in tqdm(enumerate(pixels), total=len(pixels)):
        i, j = p
        c = np.argmin(distances[l])
        centers_to_i_j[c][0].append(i)
        centers_to_i_j[c][1].append(j)
        i_j_to_centers[i][j] = c

    polygon_to_color = [255 for _ in centers]
    for l in range(len(centers)):
        indices = centers_to_i_j[l]
        if len(indices[0]) > 0:
            color = np.mean(image[indices], axis=0)
            polygon_to_color[l] = color

    pixelized_image = np.ones_like(image) * 255.0
    for i in range(rows):
        for j in range(cols):
            polygon = i_j_to_centers[i][j]
            pixelized_image[i, j] = polygon_to_color[polygon]

    pixelized_image = Image.fromarray(np.uint8(pixelized_image))
    return pixelized_image


def hexagon(image, R, h):
    image = np.array(image)[:, :, :3]
    rows, cols, _ = image.shape
    hexagon_points, _ = hexagon_tile(0, 0, rows, cols, R)
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


def cube(image, R, h):
    image = np.array(image)[:, :, :3]
    rows, cols, _ = image.shape
    hexagon_points, weights = cubic_tile(0, 0, rows, cols, R)
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
            pixelized_image[i, j] = polygon_to_color[polygon] * weights[polygon]

    pixelized_image = Image.fromarray(np.uint8(pixelized_image))
    return pixelized_image


def pyramid(image, R, h):
    image = np.array(image)[:, :, :3]
    rows, cols, _ = image.shape
    hexagon_points, weights = pyramid_tile(0, 0, rows, cols, R)
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
            pixelized_image[i, j] = polygon_to_color[polygon] * weights[polygon]

    pixelized_image[pixelized_image > 255.0] = 255.0
    pixelized_image = Image.fromarray(np.uint8(pixelized_image))
    return pixelized_image


def dcube(image, R, h):
    image = np.array(image)[:, :, :3]
    rows, cols, _ = image.shape
    hexagon_points, weights = double_cubic_tile(0, 0, rows, cols, R)
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
            pixelized_image[i, j] = polygon_to_color[polygon] * weights[polygon]

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
    'vor': voronoi,
    'hex': hexagon,
    'cube': cube,
    'dcube': dcube,
    'sq': square,
    'split': split,
    'wall': wall,
    'blob': blob,
    'pyramid': pyramid,
    'vor_gif': voronoi_gif,
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
    if mode != 'vor_gif':
        pixelized_image.save(outfile_name)
    else:
        save_gif(pixelized_image, outfile_name)
