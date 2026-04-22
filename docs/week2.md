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
