import torch.nn.functional as F
import joblib

class KMeans:
    def __init__(self, n_clusters=3, max_iters=100):
        self.n_clusters = n_clusters
        self.max_iters = max_iters
        self.centroids = None

    def fit(self, X):
        indices = torch.randint(0, X.size(0), (self.n_clusters,))
        self.centroids = X[indices].clone().to(device)

        for _ in range(self.max_iters):
            distances = torch.cdist(X, self.centroids)

            labels = torch.argmin(distances, dim=1)

            new_centroids = torch.stack([X[labels == i].mean(dim=0) for i in range(self.n_clusters)])

            if torch.allclose(self.centroids, new_centroids, atol=1e-4):
                break
            
            self.centroids = new_centroids.clone()

        print("KMeans training completed.")
    
    def save_model(model, filename="kmeans_mcstat.pkl"):
        joblib.dump(model, filename)
        print(f"Model saved to {filename}")

kmeans = KMeans(n_clusters=3, max_iters=100)
kmeans.fit(mcstat_tensor)
kmeans.save_model("kmeans_mcstat.pkl")
