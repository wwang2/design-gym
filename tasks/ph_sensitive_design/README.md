# pH-Sensitive Binder Design Evaluation Task

## Overview
This task evaluates computational workflows for designing pH-sensitive protein binders, based on Ahn et al. 2025 "Computational Design of pH-Sensitive Binders".

## Paper Reference
- **Title**: Computational Design of pH-Sensitive Binders
- **Authors**: Green Ahn et al.
- **DOI**: 10.1101/2025.09.29.678932

## Two Design Strategies

### Strategy A: Interface Destabilization
- Place His adjacent to Arg/Lys at the binding interface
- At low pH (~5.5), His protonation causes electrostatic repulsion
- Weakens binder-target interaction

### Strategy B: Monomer Destabilization
- Install buried His-containing H-bond networks in protein core
- At low pH, His protonation disrupts these networks
- Destabilizes the binder fold itself

## Task Structure

```
ph_sensitive_design/
├── question.ipynb      # Evaluation notebook (Parts 0-3)
├── answer.txt          # Ground-truth answers
├── rubric.txt          # Scoring rubric (100 points)
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── data/
    ├── target_il6.pdb      # IL-6 structure (PDB 1ALU)
    ├── target_pcsk9.pdb    # PCSK9 structure (PDB 2P4E)
    └── scaffold.pdb        # 3-helix bundle (PDB 5L33)
```

## Parts

### Part 0: Conceptual Understanding (12 pts)
Multiple choice questions on pH-sensitivity fundamentals (Q0.1-Q0.4)

### Part 1: ProteinMPNN with Histidine Bias (23 pts)
- Task 1.1: Global bias argument syntax
- Task 1.2: Position-specific bias dictionary creation
- Task 1.3: Interface residue selection (distance-based)
- Task 1.4: Complete interface His-bias workflow

### Part 2: Interface Destabilization Scoring (35 pts)
- Task 2.1: His-Arg/Lys motif detection at interface
- Task 2.2: PyRosetta FastRelax and InterfaceAnalyzer
- Task 2.3: Filtering pipeline (His-cation pair + ddG_elec >= 0)

### Part 3: Monomer Destabilization with HBNet (30 pts)
- Task 3.1: Core residue identification (SASA < 25%)
- Task 3.2: HBNet configuration for His-His/His-Arg/His-Lys networks
- Task 3.3: Network scoring (His H-bond energy < -0.5 kcal/mol)
- Task 3.4: Complete monomer destabilization pipeline

## Implementation Notes

The notebook includes two types of implementations:

1. **TODO stubs**: Empty functions for candidates to implement
2. **Reference implementations**: Working `_reference` functions for validation

For heavy-duty tools (PyRosetta, ProteinMPNN, HBNet):
- Functions raise `NotImplementedError` with installation instructions
- `_stub` functions return mock data for pipeline testing

For lighter functions (BioPython-based):
- Full reference implementations are provided
- Can be tested with the provided PDB structures

## Required Tools
- **BioPython** (required): PDB parsing, SASA calculation, NeighborSearch
- **PyRosetta** (optional): FastRelax, InterfaceAnalyzer, HBNet
- **ProteinMPNN** (optional): Sequence design with amino acid bias

Install dependencies:
```bash
pip install biopython numpy
```

## Data Sources
- **PDB 1ALU**: Human IL-6 crystal structure
- **PDB 2P4E**: Human PCSK9 catalytic domain
- **PDB 5L33**: De novo designed 3-helix bundle

