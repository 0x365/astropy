import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from tqdm import tqdm
import pandas as pd
from matplotlib.gridspec import GridSpec

class HybridSwarmOptimization2D:
    def __init__(self, array, num_particles=50, max_iter=100):
        """
        Initialize the hybrid swarm optimization with gradient descent.

        :param array: 2D NumPy array to find local minima.
        :param num_particles: Number of particles in the swarm.
        :param max_iter: Maximum number of iterations.
        :param gradient_weight: Weight for the gradient descent component.
        """
        self.array = array
        self.num_particles_start = num_particles
        self.num_particles = num_particles
        self.max_iter = max_iter
        self.rows, self.cols = array.shape
        
        # Initialize particles (row, col)
        self.particles = np.column_stack((
            np.clip(np.random.normal(self.rows/2, self.rows/6, size=num_particles), 0, self.rows-1),
            np.clip(np.random.normal(self.cols/2, self.cols/6, size=num_particles), 0, self.cols-1)
        )).astype(float)  # Ensure positions are floats for calculations
        self.velocities = np.random.uniform(-1, 1, (num_particles, 2))
        self.best_positions = self.particles.copy()
        self.best_scores = self.evaluate_particles(self.particles)
        
        # Initialize global best
        self.global_best_position = self.best_positions[np.argmin(self.best_scores)]
        self.global_best_score = np.min(self.best_scores)

    def evaluate_particles(self, particles):
        """
        Evaluate particle fitness based on the array values.

        :param particles: Array of particle positions.
        :return: Fitness scores for each particle.
        """
        return np.array([self.array[int(p[0]), int(p[1])] for p in particles])

    def compute_gradient(self, position):
        """
        Compute the gradient at a given position using finite differences.

        :param position: A particle's position as [row, col].
        :return: Approximate gradient as [grad_row, grad_col].
        """
        row, col = int(position[0]), int(position[1])

        # away = 7

        # grid_up = self.array[row+1:row+1+away,col-(away-1)//2:col+1+(away-1)//2].flatten()
        # grid_down = self.array[row-away:row,col-(away-1)//2:col+1+(away-1)//2].flatten()
        # grid_left = self.array[row-(away-1)//2:row+1+(away-1)//2,col-away:col].flatten()
        # grid_right = self.array[row-(away-1)//2:row+1+(away-1)//2,col+1:col+1+away].flatten()
        
        # order = np.array([[0,0], [1,0], [-1,0], [0,-1], [0,1]])
        
        # sorter = [grid_up, grid_down, grid_left, grid_right]
        # for x in range(len(sorter)):
        #     if len(sorter[x]) == 0:
        #         sorter[x] = np.inf
        #     else:
        #         sorter[x] = np.amin(sorter[x])
        # return order[np.argsort([self.array[row,col], *sorter])][0]

        around_ind = np.array([
            [0,0], [1,0], [0,1], [-1, 0], [0,-1], [1,1], [1,-1], [-1, 1], [-1,-1],
            [2,0], [0,2], [-2, 0], [0,-2], [2,1], [2,-1], [-1, 2], [1,2], 
            [-2,1], [-2,-1], [-1, -2], [1,-2],
                               ])
        around_vals = []
        for ind in around_ind:
            try:
                around_vals.append(self.array[row+ind[0],col+ind[1]])
            except:
                pass
        around_vals = np.array(around_vals)

        min_ind = around_ind[np.argsort(around_vals)][0]
        return min_ind


    def optimize(self):
        """
        Perform the optimization.

        :return: Positions and values of local minima found.
        """
        minima = []
        for iteration in tqdm(range(self.max_iter), desc="Optimising"):
            # Update velocities and positions
            for i in range(self.num_particles):
                r1, r2 = np.random.rand(2)
                inertia = 0.5 * self.velocities[i]
                cognitive = 1.5 * r1 * (self.best_positions[i] - self.particles[i])
                social = 1.5 * r2 * (self.global_best_position - self.particles[i])
                
                # Add gradient descent influence
                gradient_term = self.compute_gradient(self.particles[i])
                # gradient_term = -self.gradient_weight * gradient
                
                # Update velocity
                self.velocities[i] = gradient_term + inertia + cognitive #+ social + 
                self.particles[i] = self.particles[i] + self.velocities[i]
                
                # Enforce boundary conditions and convert to integers for indexing
                self.particles[i, 0] = np.clip(self.particles[i, 0], 0, self.rows - 1)
                self.particles[i, 1] = np.clip(self.particles[i, 1], 0, self.cols - 1)
            

            # Remove particles that overlap
            self.particles = np.round(self.particles)
            unique_particles = [self.particles[0]]
            ids = [0]
            for i in range(1,self.num_particles):
                inside = False
                for uni in unique_particles:
                    if self.particles[i][0] == uni[0] and self.particles[i][1] == uni[1]:
                        inside = True
                if not inside:        
                    unique_particles.append(self.particles[i])
                    ids.append(i)

            self.particles = self.particles[np.array(ids)]
            self.velocities = self.velocities[np.array(ids)]
            self.num_particles = len(self.particles)
            self.best_positions = self.best_positions[np.array(ids)]
            self.best_scores = self.best_scores[np.array(ids)]

            # Evaluate fitness
            scores = self.evaluate_particles(self.particles)
            
            # Update personal best
            for i in range(self.num_particles):
                if scores[i] < self.best_scores[i]:
                    self.best_scores[i] = scores[i]
                    self.best_positions[i] = self.particles[i]
            
            # Update global best
            min_idx = np.argmin(self.best_scores)
            if self.best_scores[min_idx] < self.global_best_score:
                self.global_best_score = self.best_scores[min_idx]
                self.global_best_position = self.best_positions[min_idx]

            minima.append(self._cluster_minima(self.best_positions, self.best_scores))

        # Cluster results for local minima
        # minima = self._cluster_minima(self.best_positions, self.best_scores)
        return minima

    def _cluster_minima(self, positions, values, threshold=1):
        """
        Cluster particles to identify local minima.

        :param positions: Particle positions.
        :param values: Array values at positions.
        :param threshold: Threshold for clustering minima.
        :return: Unique local minima positions and values.
        """
        sorted_indices = np.argsort(values)
        sorted_positions = positions[sorted_indices]
        sorted_values = values[sorted_indices]
        
        unique_minima = []
        for pos, val in zip(sorted_positions, sorted_values):
            if not unique_minima or np.linalg.norm(unique_minima[-1][0] - pos) > threshold:
                unique_minima.append((pos, val))
        return unique_minima

# Example usage
if __name__ == "__main__":
    # Create a sample 2D array (e.g., a topographic map)
    grid = np.load("datasets/line_1ms/grid_euc_distance.npy")[10:-10,10:-10]
    # grid = np.flip(grid,axis=0)

    

    ranks = pd.Series(grid.flatten()).rank(method="average")
    ranks_normalized = ranks / (len(grid.flatten()) + 1)
    grid = np.reshape(ranks_normalized, np.shape(grid))

    grid = (grid-np.amin(grid))/(np.amax(grid)-np.amin(grid))

    # grid = np.around(grid,1)

    array = grid.copy()

    
    # Perform optimization
    optimizer = HybridSwarmOptimization2D(array, num_particles=5000, max_iter=200)
    local_minima = optimizer.optimize()


    # Plot the array and minima
    plt.figure(figsize=(21,20), layout="constrained")
    plt.imshow(grid, cmap="viridis", origin="lower", interpolation=None)
    # plt.colorbar(label="Value")
    plt.scatter(
        [m[0][1] for m in local_minima[-1]],
        [m[0][0] for m in local_minima[-1]],
        color="red",
        label="Local Minima",
        s=10
    )
    # plt.legend()
    # plt.title("Local Minima Found by Hybrid PSO with Gradient Descent")
    plt.savefig("minima.png")
    plt.clf()

    # print(len(local_minima[-1]))
    # print(len(local_minima[-1][0]))
    # print(local_minima[-1])
    # # print(len(local_minima[-1][0][0]))
    

    np.save("datasets/minima.npy", np.array([m[0] for m in local_minima[-1]]))




    fig = plt.figure(figsize=(15,20))

    # fig = plt.figure(figsize=(8, 8))
    gs = GridSpec(2, 1, height_ratios=[4, 1], hspace=0.3)  # 3:1 height ratio

    # Big square graph
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])

    def update(frame):
        
        # Z_new = np.sin(X + frame * 0.1) + np.cos(Y + frame * 0.1)  # Animate the array
        ax1.clear()
        ax2.clear()

        c = ax1.imshow(grid, cmap="viridis", origin="lower")
        # plt.colorbar(label="Value")
        ax1.scatter(
            [m[0][1] for m in local_minima[frame]],
            [m[0][0] for m in local_minima[frame]],
            color="red",
            label="Local Minima",
            s=10
        )

        ax1.set_title(f"Iteration: {frame}")

        
        lengths_array = [optimizer.num_particles_start]
        for i in range(frame):
            lengths_array.append(len(local_minima[i]))
        ax2.plot(lengths_array)
        ax2.set_xlabel("Iteration")
        ax2.set_ylabel("Number of Minima")
        ax2.set_title(f"Number of Minima: {len(local_minima[frame])}")

        return [c]
    
    frames = len(local_minima)  # Number of frames
    anim = FuncAnimation(fig, update, frames=frames, blit=True)

    gif_path = "animated_wave.gif"
    writer = PillowWriter(fps=10)
    anim.save(gif_path, writer=writer, dpi=100)
    print(f"GIF saved to {gif_path}")

    # Close the plot
    plt.close()