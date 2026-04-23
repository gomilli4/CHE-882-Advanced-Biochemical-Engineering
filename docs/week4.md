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
