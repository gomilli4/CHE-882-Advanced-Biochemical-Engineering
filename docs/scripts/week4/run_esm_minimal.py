import torch
import esm
import pickle
import gc

device = torch.device("cpu")

model, alphabet = esm.pretrained.esm2_t6_8M_UR50D()
model = model.to(device)
model.eval()

batch_converter = alphabet.get_batch_converter()

# load sequences (already working for you)
pdb_seqs = pickle.load(open("processed_file/pdb_seqs.pkl", "rb"))

embeddings = {}

for name, seq in pdb_seqs.items():
    print(f"Embedding {name} ({len(seq)} aa)")

    data = [(name, seq)]
    _, _, tokens = batch_converter(data)
    tokens = tokens.to(device)

    with torch.no_grad():
        out = model(tokens, repr_layers=[6], return_contacts=False)
        emb = out["representations"][6][0, 1:len(seq)+1].cpu().numpy()

    embeddings[name] = emb
    print("  → shape", emb.shape)

    # 🔥 THIS PART MATTERS
    del tokens, out, emb
    gc.collect()

# save once at the end
with open("processed_file/esm_emds/esm_part_0.pkl", "wb") as f:
    pickle.dump(embeddings, f)

print("Saved embeddings")