import pickle
import torch
import dgl
import math
import os

# Load inputs
pdb_points = pickle.load(open("processed_file/pdb_points.pkl", "rb"))
esm_embs = pickle.load(open("processed_file/esm_emds/esm_part_0.pkl", "rb"))

graphs = {}

def dist(a, b):
    return math.sqrt(
        (a[0]-b[0])**2 +
        (a[1]-b[1])**2 +
        (a[2]-b[2])**2
    )

for pid, points in pdb_points.items():
    coords = [(p[0], p[1], p[2]) for p in points]
    n = len(coords)

    u, v, d = [], [], []
    for i in range(n):
        for j in range(n):
            if i != j:
                dd = dist(coords[i], coords[j])
                if dd <= 12.0:
                    u.append(i)
                    v.append(j)
                    d.append(dd)

    g = dgl.graph((torch.tensor(u), torch.tensor(v)), num_nodes=n)
    g.edata["dis"] = torch.tensor(d)

    # node features
    g.ndata["x"] = torch.tensor(esm_embs[pid])

    graphs[pid] = g
    print(f"Built graph for {pid}: {n} nodes")

os.makedirs("processed_file/graph_features", exist_ok=True)
pickle.dump(
    list(graphs.values()),
    open("processed_file/graph_features/mf_test_whole_pdb_part0.pkl", "wb")
)

print("Saved graph file")