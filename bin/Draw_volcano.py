#!/usr/bin/env python3

"""
Usage:
  Draw_volcano.py --adata=<adata> [options]

Mandatory arguments:
  --adata=<adata>       adata

Optional arguments:
  --resDir=<resDir>     Output directory [default: ./]
"""

from docopt import docopt
import anndata as ad
import scanpy as sc
import decoupler as dc

# Only needed for processing and plotting
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

args = docopt(__doc__)
adata = args["--adata"]
resDir = args["--resDir"]

adata = sc.read_h5ad(adata)

# Get pseudo-bulk profile
padata = dc.get_pseudobulk(adata, sample_col='sample', groups_col='cell_type', layer='counts', min_prop=0.05, min_smpls=3, min_cells=10,)

# Normalize
sc.pp.normalize_total(padata, target_sum=1e4)
sc.pp.log1p(padata)

logFCs, pvals = dc.get_contrast(
  padata,
  group_col='cell_type',
  condition_col='group',
  condition='KO',
  reference='WT',
  method='t-test'
  )

for ct in logFCs.index.tolist():
  fig, ax = plt.subplots(1,1,figsize=(7,5))
  dc.plot_volcano(logFCs, pvals, ct, top=15, sign_thr=0.05, lFCs_thr=0.5, ax=ax)
  fig.savefig(f"{resDir}/{ct}_volcano.png", bbox_inches="tight") 
  