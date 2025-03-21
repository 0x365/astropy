import numpy as np
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import pdist, squareform
from scipy.stats import zscore

import pandas as pd

from tqdm import tqdm

import matplotlib.pyplot as plt

def calculate_spatial_autocorrelation(grid, radius=1):

    rows, cols = grid.shape
    spatial_auto = np.zeros_like(grid, dtype=float)
    
    # Pad the grid for boundary handling
    padded = np.pad(grid, radius, mode='constant', constant_values=np.nan)
    
    for i in range(rows):
        for j in range(cols):
            # Extract the neighborhood
            neighborhood = padded[i:i + 2 * radius + 1, j:j + 2 * radius + 1]
            neighborhood_flat = neighborhood.flatten()
            
            # Calculate Moran-like value (mean value excluding the center)
            center_value = grid[i, j]
            valid_neighbors = neighborhood_flat[~np.isnan(neighborhood_flat)]
            spatial_auto[i, j] = np.mean(valid_neighbors) - center_value
    
    return spatial_auto


def cluster_grid(grid, radius=1, eps=0.5, min_samples=5):

    # Step 1: Normalize the grid values
    normalized_grid = zscore(grid.flatten()).reshape(grid.shape)
    
    # Step 2: Calculate spatial autocorrelation
    spatial_auto = calculate_spatial_autocorrelation(normalized_grid, radius)
    
    # Step 3: Combine features for clustering
    combined_features = np.column_stack((
        normalized_grid.flatten(),  # Value at each point
        spatial_auto.flatten()      # Spatial autocorrelation
    ))
    # print("Here")
    # print(combined_features)
    # print(np.shape(combined_features))
    # return 7
    # return spatial_auto
    
    # Step 4: Run DBSCAN
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(combined_features)
    cluster_labels = clustering.labels_
    return cluster_labels.reshape(grid.shape)


# Example usage
if __name__ == "__main__":
    # Create a synthetic 2D grid
    grid = np.load("datasets/square_2ms_3000steps/grid_euc_distance.npy")
    grid = np.flip(grid,axis=0)
    # print(np.amin(grid))

    # grid = np.log10(grid+0.1)
    # grid = np.log10(grid)

    # grid[grid == 0] = np.nan
    ranks = pd.Series(grid.flatten()).rank(method="average")
    ranks_normalized = ranks / (len(grid.flatten()) + 1)
    grid = np.reshape(ranks_normalized, np.shape(grid))

    

    grid = (grid -np.nanmin(grid)) / (np.nanmax(grid)-np.nanmin(grid))

    grid = np.log1p(grid)

    # grid = grid[len(grid)//4:-len(grid)//4,len(grid)//4:-len(grid)//4]

    
    # print(grid)
    # Perform clustering
    fig, axs = plt.subplots(10, 10, figsize=(20,20), layout="constrained")
    axs = axs.flatten()
    axs[0].imshow(grid)

    # eps_try = np.linspace(0.0222,0.0768, 100)
    # eps_try = np.linspace(0.0257,0.0857, 100)
    # eps_try = np.linspace(0.0046,0.0275, 100)
    eps_try = np.linspace(0,0.0056, 100)
    for i in tqdm(range(1,100)):
        
        cluster_labels = cluster_grid(grid, radius=2, eps=eps_try[i], min_samples=20)
        # Print results
        # print("Grid:")
        # print(grid)
        # print("\nCluster Labels:")
        _, cou = np.unique(cluster_labels,return_counts=True)
        vals = np.mean(cou[1:])

        cluster_labels[cluster_labels > 20] = 0

        axs[i].axis("off")
        axs[i].set_title(str(round(eps_try[i],4)))
        
        axs[i].imshow(cluster_labels, cmap="tab20")
    plt.savefig("test.png", dpi=500)
