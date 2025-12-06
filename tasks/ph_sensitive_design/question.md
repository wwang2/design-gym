# pH-Sensitive Protein Design Task

## Problem Statement

Engineer a pH-sensitive "switch" into a stable protein scaffold. The goal is to introduce a buried Histidine-mediated hydrogen bond network that is stable at neutral pH (7.4) but becomes destabilizing at acidic pH (~6.0), triggering a conformational change or unfolding.

Using the provided scaffold `data/scaffold.pdb` (a de novo designed NTF2 fold, PDB ID 5L33), develop a computational workflow that:

1. **Identifies buried core residues** suitable for installing pH-sensing networks
2. **Discovers positions** where His-containing hydrogen bond networks can be installed
3. **Designs sequences** with the network installed and surrounding residues repacked
4. **Validates designs** through structure prediction, confirming the network forms correctly

## Success Criteria

A successful solution will:
- Produce designed sequences containing buried His networks
- Demonstrate high-confidence structure predictions (pLDDT > 70)
- Show geometric evidence that the His network is formed in predicted structures
- Explain why the design would function as a pH sensor

## Background

- Histidine's pKa (~6.0) makes it ideal for physiological pH sensing
- Buried residues experience pKa shifts that enable pH sensing
- At low pH, His protonation disrupts hydrogen bonds, destabilizing the core
