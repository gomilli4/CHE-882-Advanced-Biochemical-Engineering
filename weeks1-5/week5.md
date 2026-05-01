# Fifth week of class

## Mid-Semester Project

For the mid-semester project (and the end of CHE 891), we were tasked with choosing a protein, then creating a panel of 50 small molecules or proteins, run binding simulations, then run a predictive ML model on the complexes to determined the binding affinites. Aaron and I chose scFV_P, which is a single-chain variable fragment antibody that binds to proteins. For this assignment, we used Boltz2, Prodigfy, MM/GBSA, and PPI-Graphomer.

Aaron and I chose 25 proteins each. He chose the first 25, which were different types of the ErB2/HER2 protein that the antibody should've been able to bind with. We had issues with the models though, so all of his predicted values were basically the same, hovering between -15 and -16 kcal/mol.

Given that Aaron had chosen versions of the proteins that scFV should have had a better chance at binding with, I decided to chose random proteins. At first I tried using BLASTP searches with the HER2 sequence, but all I could find were proteins that were too similar (which we already had). I had a similar experience using the RSCB database, which kept returning like 100% matches. Finally, I just started taking random proteins like receptors, intracellular proteins, and some other random ones I found. I figured this could be like the negative control.

Finally, I chose my list of proteins:

```
1BV8
1ZT3
2JTK
2QKQ
3FA7
5K38
7SZL
1L8K
2BT2
2MGS
2V0V
3H8M
6FNL
1M4K
2F9L
2NLS
3B2U
3TN2
7MN6
1SHU
2F9M
2NMS
3C09
4ET7
7RDB
```

For the structural prediction, I used the virtual python environment I had used for Boltz2 earlier in the semester. I ran into issues with the yaml files though, so I had to use BIO.PDB in a python script to convert my cif files to pdb files (see scripts/mid_semester_project/cif_to_pdb.py).

On the actual HPC, I ran into a common issue from this semester which was more versioning errors. After that, I had problems running Boltz, so I investigated the pdb files and found that they needed to be cleaned, because a number of them were full of "UNK" residues which Boltz couldn't handle. To fix this, chat gpt created a small bash script that looped through the pdb files and removed any residues that Boltz couldn't work with:

```
for f in *.pdb; do
  grep -v " UNK " "$f" > "${f%.pdb}.clean.pdb"
done
```

which worked nicely. Finally, I was able to run the yaml files I had collected using this regular Boltz command:

```
boltz predict yamls/ --use_msa_server --no_kernels --output_dir outputs
```

After the complexes had run through Boltz, I needed to use an affinity prediction model. I used both PPI-Graphomer and Prodigy, but I absolutely did not trust PPI-Graphomer's results (outputs/mid_semester_project). Like Aaron, all of the Graphomer results had basically no spread which seemed very unrealistic to me, which values hovering around 10-11. Prodigy gave me much more realistic (or maybe just believable?) results. From Prodigy, I got a larger spread of data, from -9.9 kcal/mol to amost -24 kcal/mol (see outputs/mid_semester_project/prodigy_results.tsv).

Unfortunately, I wasn't able to use this as a negative control, because Aaron's data was from Graphomer and so couldn't be trusted, so we couldn't compare. I did think my results were interesting because so many of the complexes were predicted to be quite stable (>-20 kcal/mol) even though I was using random proteins.

Regardless, after collecting the output files, I created my PyMOL renders using these commands to make them pretty:

```
reinitialize
load 1BV8_model_0.clean.pdb
hide everything
show cartoon
bg_color white
color marine, chain A
color orange, chain B
orient
png 1BV8.png, width=1600, height=1200, dpi=300
```

(see /images/mid_semester_project), then I used a python script to analyze my files and produce a nice sorted graph showing the values the models gave me (images/mid_semester_project/deltaD_data.png)
