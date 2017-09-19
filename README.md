# About
Command line application to subsample sequences from a FASTA or FASTQ formatted text file.

# Usage

Subsample 3 sequences from a fasta file to a new file `out.fasta`.
```bash
subsample-seq --file-format fasta --sample-size 3 examples/example.fasta out.fasta
```

Subsample 3 sequences from a fastq file to stdout.
```bash
subsample-seq --file-format fastq --sample-size 3 examples/example.fastq -
```

Use `--seed` value for deterministic output.
```bash
subsample-seq --file-format fasta --sample-size 3 --seed 1 examples/example.fasta out.fasta
```

# Installation

```bash
git clone git@gitlab.com:koki.moribe/subsample-seq.git
cd subsample-seq
pip install .
```
