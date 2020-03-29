import sys
import math
from tqdm import tqdm
from PIL import Image
import numpy as np
from hexgrid import calculate_polygons
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

if __name__ == '__main__':
    image_name = str(sys.argv[1])
    outfile_name = str(sys.argv[2])
    R = int(sys.argv[3])
    image = Image.open(image_name)
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
    pixelized_image.show()
    pixelized_image.save(outfile_name)
