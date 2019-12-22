import numpy as np
import numpy.linalg as la

def regress(data, estimation_points, weighter, degree=1, kernel_window=1, iter=1):
    trend = np.zeros(estimation_points.shape[-1])

    for index, estimation_point in enumerate(estimation_points.T):
        total = 0.0
        weights = 0.0
        for row in data.itertuples(index=True):
            row_weight = weight(row, estimation_point)
            total += row_weight * row.percent
            weights += row_weight

        avg = total / weights
        trend[index] = avg

    return trend
