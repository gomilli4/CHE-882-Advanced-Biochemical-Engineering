import re

def parse_clstr(file_path):
    clusters = []
    current_cluster = None

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()

            # New cluster
            if line.startswith(">Cluster"):
                if current_cluster:
                    clusters.append(current_cluster)
                current_cluster = {
                    "name": line,
                    "size": 0,
                    "rep": None
                }

            else:
                current_cluster["size"] += 1

                # Extract sequence ID
                match = re.search(r'>(.*?)\.\.\.', line)
                if match:
                    seq_id = match.group(1)

                    # Representative sequence marked with *
                    if line.endswith("*"):
                        current_cluster["rep"] = seq_id

        # Append last cluster
        if current_cluster:
            clusters.append(current_cluster)

    return clusters


def get_top_clusters(clusters, top_n=11):
    # Sort by cluster size (descending)
    sorted_clusters = sorted(clusters, key=lambda x: x["size"], reverse=True)
    return sorted_clusters[:top_n]


def main():
    clstr_file = "search_output.fasta.clstr"  # <-- change this
    clusters = parse_clstr(clstr_file)

    top_clusters = get_top_clusters(clusters, top_n=11)

    print("Top 11 clusters by size:\n")
    for i, cluster in enumerate(top_clusters, 1):
        print(f"{i}. {cluster['name']}")
        print(f"   Size: {cluster['size']}")
        print(f"   Representative: {cluster['rep']}\n")


if __name__ == "__main__":
    main()
