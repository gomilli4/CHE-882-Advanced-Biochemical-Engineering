import os
import pickle
from Bio.PDB import PDBParser
from Bio.SeqUtils import seq1

PDB_DIR = "data/PDB/PDB_folder"
OUT_DIR = "processed_file"
os.makedirs(OUT_DIR, exist_ok=True)

parser = PDBParser(QUIET=True)

pdb_seqs = {}
pdb_points = {}

for fname in os.listdir(PDB_DIR):
    if not fname.endswith(".pdb"):
        continue

    pid = fname.replace(".pdb", "")
    structure = parser.get_structure(pid, os.path.join(PDB_DIR, fname))

    seq = ""
    coords = []

    for model in structure:
        for chain in model:
            for residue in chain:
                if residue.id[0] != " ":
                    continue
                try:
                    aa = seq1(residue.resname)
                except KeyError:
                    continue

                if "CA" not in residue:
                    continue

                ca = residue["CA"].get_coord()
                seq += aa
                coords.append((float(ca[0]), float(ca[1]), float(ca[2])))

            break
        break

    if len(seq) == 0 or len(coords) == 0:
        print(f"Skipping {pid} (empty)")
        continue

    pdb_seqs[pid] = seq
    pdb_points[pid] = coords
    print(f"Loaded {pid}: {len(seq)} residues")

with open(f"{OUT_DIR}/pdb_seqs.pkl", "wb") as f:
    pickle.dump(pdb_seqs, f)

with open(f"{OUT_DIR}/pdb_points.pkl", "wb") as f:
    pickle.dump(pdb_points, f)

print("Saved pdb_seqs.pkl and pdb_points.pkl")