# Bachelor Thesis
This repository contains all the code (mostly LaTeX and Python) needed to reproduce my thesis with a single call to `make`.

## Requirements
For this thesis to be compiled correctly, the `cta-dev` environment for python is needed. Install it via the environment file found under:
```
configs/env.yml
```
With this, the whole document except one plot (`plots/quantiles_plot.py`, `build/quantiles_plot.pdf`) can be compiled. The latter plot needs data that is too large to store on GitHub and therefore cannot be created. I may add the plot manually at a later date, for now though, feel free to ask me for it.

## Building the Thesis
To build the thesis just call `make` in the root directory and lean back for a few minutes, depending on your CPU speed.
