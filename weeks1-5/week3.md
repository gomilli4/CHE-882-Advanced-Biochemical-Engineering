# Third week of class

This week we were tasked with running BioEmu and aSAMT/aSAM. I handled aSAMT/aSAM and Aaron handled BioEmu.

Instead of using a virtual environment like with Boltz2, this week I used a conda environment. I use conda environments in my work with Dr. Anstine, so I'm more familiar with them. They are much heavier than the venvs though, so I repeatedly ran into issues where I ran out of space on my home drive on the HPCC. I'll use scratch space one day.

To create the conda environment,

```
conda create -n sam2 python=3.10
conda activate sam2
```

While attempting to install aSAM2, I kept having bad version issues. My conda environments had the wrong python versions, PyTorch was the wrong version to work with the python version, etc. I created, experimented with, and eventually deleted many environments trying to get things correct.

After making sure I had the proper libraries installed, I followed the aSAM tutorial on their github page https://github.com/giacomo-janson/sam2 with these commands:

```
git clone https://github.com/giacomo-janson/sam2.git
```

then, cd'd into the new repo and ran

```
pip install -e .
```

When everything was installed, I created a directory for the sam2 weights, exported a variable instructing the shell to direct programs looking for SAM_WEIGHTS_PATH to my new directory, then ran the test script to see if it all worked, which it did.

```
mkdir -p ...sam2_weights
export SAM_WEIGHTS_PATH=...<real path goes here>/sam2_weights

python scripts/generate_ensemble.py \
  -c config/mdcath_model.yaml \
  -i examples/input/4qbuA03.320.pdb \
  -o sanity \
  -n 4 \
  -b 2 \
  -T 320 \
  -d cuda
```

The output of aSAM is a group of two types of files. The first is a pdb file. The second is a traj.dcd file, which contains the ensemble data. Both of these files can be loaded into PyMOL. Using

```
load protein.top.pdb
load protein.traj.dcd
```

in the PyMOL terminal, you're able to scrub through the ensemble or view it like an animation (even though it's not). After finishing the tutorial, I moved on to running the actual proteins for class.

Using pdb files for each of the class proteins, I collected them into a folder and used this script

```
for pdb in ~/sam2_inputs/*.pdb; do
  name=$(basename "$pdb" .pdb)
  echo "Running SAM2 on $name"
  python scripts/generate_ensemble.py \
    -c config/mdcath_model.yaml \
    -i "$pdb" \
    -o ~/sam2_runs/"$name" \
    -n 24 \
    -b 8 \
    -T 320 \
    -d cuda
done
```

hoping that it would run each pdb file nicely. Unfortunately, I kept getting

```
KeyError: 'NAG'
```

errors in the terminal. This was caused by issues with the pdb files containing non-amino acid information. I ended up having to clean each of the files by hand in PyMOL. There is probably a script that exists that would've done it for me, but chat gpt failed and I didn't want to worry about it.

To clean the files, in PyMOL I ran a combination of commands:


```
remove not polymer.protein
remove solvent
remove not chain A
create newObj, polymer.protein
save protein_name_clean.pdb, newObj
```

These remove everything in the file that isn't part of the protein, creates a new object from the cleaned protein, then saves it so I can use it elsewhere.

After cleaning, the jobs ran with no issue obvious issues, but they were taking a long time. I explored the sequences being run, and saw that they were all multiple times longer than the single sequence. During the crystallization procedure used to create the downstream pdb files, multiple proteins can be clumped together. I had to do another cleaning round to remove the redundant proteins. I'm not sure why the previous cleaning commands didn't remove them, but things ran fine after this.

After getting the sam2 outputs, I loaded the ensembles into PyMOL for rendering. I wanted the ensemble to be overlayed over the crystal structure, so these are the commands I ran to load and render them nicely:

```
load protein.top.pdb, rixi
load_traj protein.traj.dcd, rixi

intra_fit rixi

show cartoon, rixi
set cartoon_transparency, 0.7

load rixi_reference.pdb, rixi_ref

align rixi and state 1, rixi_ref
```

See the images in images/week3.
