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

then, I ran

```
pip install -e .
```


