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

The output of Boltz2 looked like this:
```
.
└── boltz_results_yamls
    ├── lightning_logs
    │   └── version_0
    │       └── hparams.yaml
    ├── msa
    │   ├── FLS2_0.csv
    │   ├── FLS2_unpaired_tmp_env
    │   │   ├── bfd.mgnify30.metaeuk30.smag30.a3m
    │   │   ├── msa.sh
    │   │   ├── out.tar.gz
    │   │   ├── pdb70.m8
    │   │   └── uniref.a3m
    │   ├── OATP1B1_0.csv
    │   ├── OATP1B1_unpaired_tmp_env
    │   │   ├── bfd.mgnify30.metaeuk30.smag30.a3m
    │   │   ├── msa.sh
    │   │   ├── out.tar.gz
    │   │   ├── pdb70.m8
    │   │   └── uniref.a3m
    │   ├── PGIP2_0.csv
    │   ├── PGIP2_unpaired_tmp_env
    │   │   ├── bfd.mgnify30.metaeuk30.smag30.a3m
    │   │   ├── msa.sh
    │   │   ├── out.tar.gz
    │   │   ├── pdb70.m8
    │   │   └── uniref.a3m
    │   ├── rixi_0.csv
    │   ├── rixi_unpaired_tmp_env
    │   │   ├── bfd.mgnify30.metaeuk30.smag30.a3m
    │   │   ├── msa.sh
    │   │   ├── out.tar.gz
    │   │   ├── pdb70.m8
    │   │   └── uniref.a3m
    │   ├── scFab_L_0.csv
    │   ├── scFab_L_unpaired_tmp_env
    │   │   ├── bfd.mgnify30.metaeuk30.smag30.a3m
    │   │   ├── msa.sh
    │   │   ├── out.tar.gz
    │   │   ├── pdb70.m8
    │   │   └── uniref.a3m
    │   ├── scFab_P_0.csv
    │   ├── scFab_P_unpaired_tmp_env
    │   │   ├── bfd.mgnify30.metaeuk30.smag30.a3m
    │   │   ├── msa.sh
    │   │   ├── out.tar.gz
    │   │   ├── pdb70.m8
    │   │   └── uniref.a3m
    │   ├── scFv_L_0.csv
    │   ├── scFv_L_unpaired_tmp_env
    │   │   ├── bfd.mgnify30.metaeuk30.smag30.a3m
    │   │   ├── msa.sh
    │   │   ├── out.tar.gz
    │   │   ├── pdb70.m8
    │   │   └── uniref.a3m
    │   ├── scFv_P_0.csv
    │   └── scFv_P_unpaired_tmp_env
    │       ├── bfd.mgnify30.metaeuk30.smag30.a3m
    │       ├── msa.sh
    │       ├── out.tar.gz
    │       ├── pdb70.m8
    │       └── uniref.a3m
    ├── predictions
    │   ├── FLS2
    │   │   ├── confidence_FLS2_model_0.json
    │   │   ├── FLS2_model_0.cif
    │   │   ├── pae_FLS2_model_0.npz
    │   │   ├── pde_FLS2_model_0.npz
    │   │   └── plddt_FLS2_model_0.npz
    │   ├── OATP1B1
    │   │   ├── confidence_OATP1B1_model_0.json
    │   │   ├── OATP1B1_model_0.cif
    │   │   ├── pae_OATP1B1_model_0.npz
    │   │   ├── pde_OATP1B1_model_0.npz
    │   │   └── plddt_OATP1B1_model_0.npz
    │   ├── PGIP2
    │   │   ├── confidence_PGIP2_model_0.json
    │   │   ├── pae_PGIP2_model_0.npz
    │   │   ├── pde_PGIP2_model_0.npz
    │   │   ├── PGIP2_model_0.cif
    │   │   └── plddt_PGIP2_model_0.npz
    │   ├── rixi
    │   │   ├── confidence_rixi_model_0.json
    │   │   ├── pae_rixi_model_0.npz
    │   │   ├── pde_rixi_model_0.npz
    │   │   ├── plddt_rixi_model_0.npz
    │   │   └── rixi_model_0.cif
    │   ├── scFab_L
    │   │   ├── confidence_scFab_L_model_0.json
    │   │   ├── pae_scFab_L_model_0.npz
    │   │   ├── pde_scFab_L_model_0.npz
    │   │   ├── plddt_scFab_L_model_0.npz
    │   │   └── scFab_L_model_0.cif
    │   ├── scFab_P
    │   │   ├── confidence_scFab_P_model_0.json
    │   │   ├── pae_scFab_P_model_0.npz
    │   │   ├── pde_scFab_P_model_0.npz
    │   │   ├── plddt_scFab_P_model_0.npz
    │   │   └── scFab_P_model_0.cif
    │   ├── scFv_L
    │   │   ├── confidence_scFv_L_model_0.json
    │   │   ├── pae_scFv_L_model_0.npz
    │   │   ├── pde_scFv_L_model_0.npz
    │   │   ├── plddt_scFv_L_model_0.npz
    │   │   └── scFv_L_model_0.cif
    │   └── scFv_P
    │       ├── confidence_scFv_P_model_0.json
    │       ├── pae_scFv_P_model_0.npz
    │       ├── pde_scFv_P_model_0.npz
    │       ├── plddt_scFv_P_model_0.npz
    │       └── scFv_P_model_0.cif
    └── processed
        ├── constraints
        │   ├── FLS2.npz
        │   ├── OATP1B1.npz
        │   ├── PGIP2.npz
        │   ├── rixi.npz
        │   ├── scFab_L.npz
        │   ├── scFab_P.npz
        │   ├── scFv_L.npz
        │   └── scFv_P.npz
        ├── manifest.json
        ├── mols
        │   ├── FLS2.pkl
        │   ├── OATP1B1.pkl
        │   ├── PGIP2.pkl
        │   ├── rixi.pkl
        │   ├── scFab_L.pkl
        │   ├── scFab_P.pkl
        │   ├── scFv_L.pkl
        │   └── scFv_P.pkl
        ├── msa
        │   ├── FLS2_0.npz
        │   ├── OATP1B1_0.npz
        │   ├── PGIP2_0.npz
        │   ├── rixi_0.npz
        │   ├── scFab_L_0.npz
        │   ├── scFab_P_0.npz
        │   ├── scFv_L_0.npz
        │   └── scFv_P_0.npz
        ├── records
        │   ├── FLS2.json
        │   ├── OATP1B1.json
        │   ├── PGIP2.json
        │   ├── rixi.json
        │   ├── scFab_L.json
        │   ├── scFab_P.json
        │   ├── scFv_L.json
        │   └── scFv_P.json
        ├── structures
        │   ├── FLS2.npz
        │   ├── OATP1B1.npz
        │   ├── PGIP2.npz
        │   ├── rixi.npz
        │   ├── scFab_L.npz
        │   ├── scFab_P.npz
        │   ├── scFv_L.npz
        │   └── scFv_P.npz
        └── templates
```

Please see images/week2 for the PyMOL renders.
