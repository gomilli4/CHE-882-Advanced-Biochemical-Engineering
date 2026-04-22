# Second week of class

This week, we ran AlphaFold3 and Boltz2. My partner ran AF3 and I focused on Boltz2 because we were struggling with the opposites.

## Boltz2
I started by creating a virtual environment in python with

```
python -m venv ~/venvs/boltz
source ~/venvs/boltz/bin/activate
```

After that, I followed the Boltz2 github page to install:

```
pip install boltz[cuda] -U
```

I ran into issues with versioning between torch, python, and Boltz that I used chat gpt to help me solve. I also needed to install a bunch of libraries to fix the dependency issues.

To run an actual prediction, I created a yaml file for eac of the 8 proteins we worked with this semester (see yamls/week2). For example, the FLS2 yaml contains this information:

```
sequences:
  - protein:
      id: A
      sequence: |
        QSFEPEIEALKSFKNGISNDPLGVLSDWTIIGSLRHCNWTGITCDSTGHVVSVSLLEKQLEGVLSPAIANLTYLQVLDLTSNSFTGKIPAEIGKLTELNQLILYLNYFSGSIPSGIWELKNIFYLDLRNNLLSGDVPEEICKTSSLVLIGFDYNNLTGKIPECLGDLVHLQMFVAAGNHLTGSIPVSIGTLANLTDLDLSGNQLTGKIPRDFGNLLNLQSLVLTENLLEGDIPAEIGNCSSLVQLELYDNQLTGKIPAELGNLVQLQALRIYKNKLTSSIPSSLFRLTQLTHLGLSENHLVGPISEEIGFLESLEVLTLHSNNFTGEFPQSITNLRNLTVLTVGFNNISGELPADLGLLTNLRNLSAHDNLLTGPIPSSISNCTGLKLLDLSHNQMTGEIPRGFGRMNLTFISIGRNHFTGEIPDDIFNCSNLETLSVADNNLTGTLKPLIGKLQKLRILQVSYNSLTGPIPREIGNLKDLNILYLHSNGFTGRIPREMSNLTLLQGLRMYSNDLEGPIPEEMFDMKLLSVLDLSNNKFSGQIPALFSKLESLTYLSLQGNKFNGSIPASLKSLSLLNTFDISDNLLTGTIPGELLASLKNMQLYLNFSNNLLTGTIPKELGKLEMVQEIDLSNNLFSGSIPRSLQACKNVFTLDFSQNNLSGHIPDEVFQGMDMIISLNLSRNSFSGEIPQSFGNMTHLVSLDLSSNNLTGEIPESLANLSTLKHLKLASNNLKGHVPESGVFKNINASDLMGNTDLCGSKKPLKPCTIKQK
```

I struggle back and forth with the right command to run a job, but eventually I got

```
boltz predict rixi.yaml --out_dir rixi_out --use_msa_server --no_kernels​
```

which did in fact run. After I was able to successfully test one protein, I ran the rest of the jobs with batch execution with commands like

```
boltz predict yamls --out_dir boltz_out --use_msa_server --no_kernels​
```

after moving all the yaml files to the yamls directory.

Please see images/week2 for the PyMOL renders.
