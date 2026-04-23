import os

def read_fasta(path):
    sequences = {}
    name = None
    seq = []

    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if name:
                    sequences[name] = "".join(seq)
                name = line[1:]
                seq = []
            else:
                seq.append(line)
        if name:
            sequences[name] = "".join(seq)

    return sequences


enzymes = read_fasta("enzymes.fasta")
inhibitors = read_fasta("inhibitors.fasta")

os.makedirs("json_inputs", exist_ok=True)

job_list = []
idx = 0

for enz_name, enz_seq in enzymes.items():
    for inh_name, inh_seq in inhibitors.items():
        run_name = f"{enz_name}_{inh_name}"
        filename = f"{idx:03d}_{run_name}.json"

        json_text = f'''{{
  "name": "{run_name}",
  "dialect": "alphafold3",
  "version": 1,
  "modelSeeds": [1],
  "sequences": [
    {{
      "protein": {{
        "id": "A",
        "sequence": "{enz_seq}"
      }}
    }},
    {{
      "protein": {{
        "id": "B",
        "sequence": "{inh_seq}"
      }}
    }}
  ]
}}'''

        with open(f"json_inputs/{filename}", "w") as f:
            f.write(json_text)

        job_list.append(filename)
        idx += 1

# write job list
with open("job_list.txt", "w") as f:
    for j in job_list:
        f.write(j + "\n")

print(f"Generated {len(job_list)} jobs.")
