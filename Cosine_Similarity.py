import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm
import glob
import os
import pickle as pkl
import math
import random
import geopandas

DIR_P_PATH = os.getcwd() + '/Predict_Data/'
DIR_T_PATH = os.getcwd() + '/Test_Data/'

Test_Route = {}
Pred_Route = {}

min_lat = 33.120581  # Minimum latitude value
max_lat = 38.726809  # Maximum latitude value
min_lon = 124.896901  # Minimum longitude value
max_lon = 132.058734  # Maximum longitude value
cell_size = 0.001  # Cell size in degrees

# Data Loading

with open(DIR_T_PATH + 'Test_Route.pkl', "rb") as fd:
    Test_Route = pkl.load(fd)

with open(DIR_P_PATH + 'Predict_route.pkl', "rb") as fd:
    Pred_Route = pkl.load(fd)


# Grid function
class GridIndexer:
    def __init__(self, min_lat, max_lat, min_lon, max_lon, cell_size):
        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_lon = min_lon
        self.max_lon = max_lon
        self.cell_size = cell_size
        self.num_cols = int(math.ceil((max_lon - min_lon) / cell_size))  # col_size
        self.num_rows = int(math.ceil((max_lat - min_lat) / cell_size))  # row_size
        self.grid = [[None] * self.num_cols for _ in range(self.num_rows)]  # grid_size
        self.populate_grid()

    def populate_grid(self):
        index = 0
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.grid[row][col] = index
                index += 1

    # get_index(lat, lon) --> return grid_num (start index: 1)
    def get_index(self, lat, lon):
        col = int((lon - self.min_lon) / self.cell_size)
        row = int((lat - self.min_lat) / self.cell_size)
        return self.grid[row][col] + 1

    # get_M_coord(grid_num) --> return median_lat, median_lon (round: 4)
    def get_M_coord(self, index):
        row = (index - 1) // self.num_cols
        col = (index - 1) % self.num_cols
        median_lat = self.min_lat + (row + 0.5) * self.cell_size
        median_lon = self.min_lon + (col + 0.5) * self.cell_size
        return round(median_lat, 4), round(median_lon, 4)


class CosineSimilarityCalculator:
    def __init__(self, grid_route_num_list):
        self.grid_route_num_list = grid_route_num_list
        self.all_grid_nums = sorted(set(grid_route_num_list))
        self.vector = np.array([1 if num in grid_route_num_list else 0 for num in self.all_grid_nums])

    def calculate_similarity(self, other_grid_route_num_list):
        other_vector = np.array([1 if num in other_grid_route_num_list else 0 for num in self.all_grid_nums])
        dot_product = np.dot(self.vector, other_vector)
        norm_product = np.linalg.norm(self.vector) * np.linalg.norm(other_vector)
        similarity = dot_product / norm_product
        return similarity


class RouteSimilarityCalculator:
    def __init__(self, PR, TR):
        self.PR = PR
        self.TR = TR

    def get_route_indices(self, route):
        return sorted(list(set([indexer.get_index(num[0], num[1]) for num in route])))

    def find_matching_routes(self):
        predict_route = self.get_route_indices([(num[0], num[1]) for num in zip(self.PR.lat, self.PR.lon)])

        the_other_route = []
        for route in self.TR:
            for lat, lon in zip(route.lat, route.lon):
                the_other_route.append((lat, lon))

        data_route = self.get_route_indices(the_other_route)

        res_route = []
        for p_route in predict_route:
            for d_route in data_route:
                if p_route == d_route:
                    res_route.append(d_route)
                    data_route.pop(data_route.index(d_route))
        return predict_route, res_route

    def calculate_cosine_similarity(self):
        predict_route, res_route = self.find_matching_routes()
        cosine_calculator = CosineSimilarityCalculator(predict_route)
        similarity = cosine_calculator.calculate_similarity(res_route)
        return similarity


indexer = GridIndexer(min_lat, max_lat, min_lon, max_lon, cell_size)


def main(PR, TR):
    route_similarity_calculator = RouteSimilarityCalculator(PR, TR)
    similarity = route_similarity_calculator.calculate_cosine_similarity()
    return similarity


if __name__ == '__main__':
    res = main(Pred_Route, Test_Route)
    print(f'cos simiarity: {res}')
