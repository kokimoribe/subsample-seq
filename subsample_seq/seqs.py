"""Module for defining functions that handle sequencing data"""

from Bio.SeqIO.FastaIO import SimpleFastaParser
from Bio.SeqIO.QualityIO import FastqGeneralIterator

from subsample_seq.constants import FASTA, FASTQ


def parse(input_stream, file_format):
    """Parse sequence records from an input stream given its file format"""
    if file_format == FASTA:
        return parse_fasta(input_stream)

    elif file_format == FASTQ:
        return parse_fastq(input_stream)

    else:
        raise ValueError('Unexpected value for `file_format`: {}'.format(file_format))


def parse_fasta(input_stream):
    """
    Parse sequence records from a fasta formatted input stream"

    Returns a generator that yields tuples that contain name, sequence
    (e.g. ('example_1', 'ATCGATCG'))
    """
    return SimpleFastaParser(input_stream)


def parse_fastq(input_stream):
    """
    Parse sequence records from a fastq formatted input stream

    Returns a generator that yields tuples that contain name, sequence, and quality scores
    (e.g. ('example_1', 'ATCGATCG', 'W<N5.6Be')
    """
    return FastqGeneralIterator(input_stream)


def write(records, file_format, output_stream):
    """Write sequence records to an output stream given a file format"""
    if file_format == FASTA:
        return write_fasta(records=records, output_stream=output_stream)

    elif file_format == FASTQ:
        return write_fastq(records=records, output_stream=output_stream)

    else:
        raise ValueError('Unexpected value for `file_format`: {}'.format(file_format))


def write_fasta(records, output_stream):
    """Write sequence records to output stream in fasta format"""
    for record in records:
        name, sequence = record
        line = '>{name}\n{sequence}\n'.format(name=name, sequence=sequence)
        output_stream.write(line)


def write_fastq(records, output_stream):
    """Write sequence records to output stream in fastq format"""
    for record in records:
        name, sequence, quality_scores = record
        line = '@{name}\n{sequence}\n+\n{quality_scores}\n'.format(
            name=name,
            sequence=sequence,
            quality_scores=quality_scores
        )
        output_stream.write(line)
