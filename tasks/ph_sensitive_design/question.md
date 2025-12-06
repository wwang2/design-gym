# pH-Sensitive Protein Design Task

## Problem Statement

Engineer a pH-sensitive "switch" into a stable protein scaffold. The goal is to introduce a buried Histidine-mediated hydrogen bond network that is stable at neutral pH (7.4) but becomes destabilizing at acidic pH (~6.0), triggering a conformational change or unfolding.

Using the provided scaffold `data/scaffold.pdb` (a de novo designed NTF2 fold, PDB ID 5L33), develop a computational workflow to:

1. **Identify Core Residues**: Find buried residues suitable for installing pH-sensing networks.
2. **Select Network Positions**: Identify residue pairs/triplets that can form His-mediated hydrogen bond networks.
3. **Sequence Design**: Install histidines and redesign surrounding sequence to stabilize the neutral-pH state.
4. **Validation**: Predict structures and verify the network is formed correctly.

## Deliverables

Save to output directory:
- `core.json`: Identified buried residues with properties
- `network.json`: Selected network positions with geometric data  
- `designs.json`: Designed sequences
- `predictions.json`: Validation metrics

## Background

- Histidine's pKa (~6.0) makes it ideal for physiological pH sensing
- Buried residues experience pKa shifts that enable pH sensing
- Structure prediction confidence indicates design quality
