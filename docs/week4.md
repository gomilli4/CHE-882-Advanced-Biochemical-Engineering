# Fourth week of class

For this week we had to run DPFunc and it did not go well for me.

I started by creating a conda environment for DPFunc

```
conda create -n dpfunc python=3.8
conda activate dpfunc
```

My first bad idea was to not follow the tutorial in the ipython notebook. I installed the necessary version of PyTorch and other libraries with

```
pip install torch==1.12.0+cu113 torchvision -f https://download.pytorch.org/whl/torch_stable.html

pip install dgl-cu113==1.1.0
pip install numpy scipy scikit-learn pandas pyyaml tqdm biopython
```

and immediately had dependency errors caused by dgl 1.1.0. Chat gpt suggested I,

```
pip install packaging
pip install "setuptools<69"
```

which stopped the dependency error, but then I had a versioning problem with PyTorch. For some reason, despite the torch installation code above, I was still working with version 2.4.1, and DPFunc can't be run with PyTorch version >= 2.0.

I uninstalled the PyTorch related libraries

```
pip uninstall -y torch torchdata torchvision torchaudio
```

tried

```
pip install torch==1.12.0+cu113 torchvision==0.13.0+cu113 -f https://download.pytorch.org/whl/torch_stable.html
```

which installed PyTorch directly from the website instead of from PyPI.

Next I was presented with errors telling me I had installed the incorrect version of DGL somehow, so I uninstalled those libraries

```
pip uninstall -y dgl dgl-cu113 dgl-cu*
```

and installed the version I needed with

```
pip install dgl==1.1.0
```

which worked.

After apparently resolving the dependency issues and getting the correct version of the libraries, I tried to run DPFunc on the course proteins. At this point I was still not following the tutorial which would led to other complications.

I started by trying to use the existing data processing scripts in the DataProcess directory of the repo. The first script I attempted was

```
python DataProcess/old_generate_points.py -i eight_pids.txt -o data/pdb_points.pkl
```

which resulted in more problems
- The script expected a pkl file containing protein IDs, not a text file
- The script also wanted a specific file naming convention

After fixing those issues, I was met with more dependency problems like not having tqdm installed.

It was becoming increasingly clear that it wasn't efficient to keep trying to modify the old scripts to do what I needed them to, so I had chat gpt try and come up wit a python script that would extract the amino acid sequence and the 3D coordinates of the residues (see /scripts/week4 for the python files I used during this week), and save the newly produced pdb_seqs.pkl and pdb_points.pkl files in the "processed_file" directory.

I also had chat gpt try and make a script that generated the protein embeddings using the ESM model. This immediately failed because I didn't have the esm package installed, but that was quickly resolved with

```
pip install fair-esm
```

Initally, the script I made (process_esm.py) had issues with the memory on the HPC node I was using. To get around that, chat gpt suggested I use a smaller ESM model lik esm2_t6_8M which I did with the run_esm_minimal.py file. This file loaded the protein sequences, ran them through the smaller ESM model, generated the per-residue embeddings, and saved them in processed_file/esm_emds/. The embeddings had shape (sequence_length, 320) which would present a problem down the line.

The next step was to build the graph representations which I did with the build_graph_minimal.py script, and the produced graphs were saved in processed_file/graph_features/.

To actually run the model, I used the

```
python DPFunc_pred.py -d mf -n -1 -p class8
```

command. It looked like things were running correctly as far as the model architecture loading, the graph data being read, and the pipeline progressing without crashing. Unfortunately, the script failed at the prediction stage because the program couldn't find the pretrained model checkpoints.

At this point, I realized that the embeddings I generated were 320 dimensional, but DPFunc expected a 1280 dimensional embedding from the larger ESM model I was having memory issues with.

By the time I realized that, it was 3:45pm right before class, so I stopped trying. To get it to work, I think I need to have downloaded the pretrained model weights (which I probably would have if I followed the tutorial). However, Aaron also struggled to get it working and I think he did follow the tutorial, so maybe it was just bad luck.
