"""
Module for defining CLI commands.
"""
import click

from subsample_seq.constants import FASTA, FASTQ
from subsample_seq import randomizer
from subsample_seq import seqs


@click.command()
@click.option('--file-format', type=click.Choice([FASTA, FASTQ]))
@click.option('--sample-size', type=click.IntRange(1, None), default=100)
@click.option('--seed', type=float, default=None)
@click.argument('input_stream', type=click.File('r'))
@click.argument('output_stream', type=click.File('w'))
def main(file_format, sample_size, seed, input_stream, output_stream):
    """Subsample FASTA and FASTQ files."""
    records = seqs.parse(
        input_stream=input_stream,
        file_format=file_format
    )

    subsampled_records = randomizer.subsample(
        records=records,
        sample_size=sample_size,
        seed=seed
    )

    seqs.write(
        records=subsampled_records,
        output_stream=output_stream,
        file_format=file_format
    )

    return 0
