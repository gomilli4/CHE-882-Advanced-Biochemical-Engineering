from Bio.PDB import MMCIFParser, PDBIO
import sys, pathlib

cif = sys.argv[1]
pdb = pathlib.Path(cif).with_suffix(".pdb")

parser = MMCIFParser(QUIET=True)
structure = parser.get_structure("complex", cif)

io = PDBIO()
io.set_structure(structure)
io.save(str(pdb))   # <-- critical fix

print(f"Wrote {pdb}")