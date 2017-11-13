"""
Module for testing CLI

See http://click.pocoo.org/6/testing/
"""

import pytest
from click.testing import CliRunner
from subsample_seq import cli
from subsample_seq.constants import FASTA, FASTQ


@pytest.fixture(name='runner')
def fixture_runner():
    """Fixture for CLI runner"""
    return CliRunner()


def test_subsample_fasta(runner):
    """Test subsampling fasta file"""
    sample_size = 3
    seed = 1

    args = [
        '--file-format', FASTA,
        '--sample-size', sample_size,
        '--seed', seed,
        '-',
        '-'
    ]

    stdin = """>test_record_0
ACCTGTACCCGGGATCGGCAGTGGTGCATGCCTTTGCGACGAATCGCTTCACTACGCAGTCATACTGCTCGCAGG
>test_record_1
TTAGCCAGGCTGCTTTTTCTTTGATAATACCCACGCGTCGTTCTTGCCAGTGATCGAGTGGAACGCCACTGGCAG
>test_record_2
AGGCATTCTATATCATCTGTGTCATATAATGTTTACCGCGAATCATTGACCCGCAAAAACGGATGCGGCTGAAGC
>test_record_3
AAGAACATCGATCAGTCAAATGCTACAATTCATTTGAACAGCGTTGGCCGACTGCTGCAAACCATAGTGGCTGAA
>test_record_4
CTAAGTCTCTCTTAGGGATAAAAGAACTGTGTCAATATGAGGTTTCACGAAAAGACAGGTCTTAACCCACGGTCC
"""

    result = runner.invoke(cli.main, args, input=stdin)

    expected_output = """>test_record_0
ACCTGTACCCGGGATCGGCAGTGGTGCATGCCTTTGCGACGAATCGCTTCACTACGCAGTCATACTGCTCGCAGG
>test_record_3
AAGAACATCGATCAGTCAAATGCTACAATTCATTTGAACAGCGTTGGCCGACTGCTGCAAACCATAGTGGCTGAA
>test_record_2
AGGCATTCTATATCATCTGTGTCATATAATGTTTACCGCGAATCATTGACCCGCAAAAACGGATGCGGCTGAAGC
"""

    assert not result.exception
    assert result.exit_code == 0
    assert result.output == expected_output


def test_subsample_fastq(runner):
    """Test subsampling fastq file"""
    sample_size = 3
    seed = 1

    args = [
        '--file-format', FASTQ,
        '--sample-size', sample_size,
        '--seed', seed,
        '-',
        '-'
    ]

    stdin = r"""@test_record_0
ACCATTCCCCATAATCAGGGCTAGACCTCCACGGTAAACGGGAAATGCGCTTACGCTATTGTTCCATTACACAAC
+
VPz#iu16@J9f@Dx)J4f,}7Jt$;=+r7r^"}s6u950Hq+0'LX^C*%v9p8R/JY5N[2SA7XEe%mB`tm
@test_record_1
GTAGGGCCCGATTCGCGAAACCCTGTCACGAGAGCAAAACGTGTGTTCTCCTCCGCGACGTGCGCCGTCACGATA
+
3ZPv(#T+J+Gg=Yi7Z86Z,buk[T\z5ZyMc%?1?-Q/P_Q%jz>jWL1)w$PdeLuiscM_r:xj+S"*\l<
@test_record_2
ACGGGTCTAGCAGTTTCTTAAAGCCAGTCTTATACGAATTCCACGTTCTGGTAAGACGTAGCTGGTACAACAATA
+
1w67+i/Z]+b63<$TzQQ2Q?`Uu#3{z$*DI&F&&1{6V^sP(RT+j-ny`}p+D_vg*;xL:@>+1F"?qVD
@test_record_3
AGACACAGATCAGCCCAAAGATTGATACTACAGTGTGATAAGTGACATGTGATTCGTATAGAAGGTTAGCGAGGC
+
|{-^=-quQ\rfxJ_U!v#Ak:`joYT<\/gY]fE[n0tf.yzThW<N5.6BeK?4(3o0@~\y-O"p,Rdd5{c
@test_record_4
CTCTTCACGATTATAAGGACTACAGGGTGCGCGTCCCACTGCTTGTTGAAGTACTTCCTCAAAAGAATTAAATGG
+
Vgw,Eb/B*|tWy$Z-NKT%[3V&d``{F/JxMPE2sT3-HAi_bE+j/|,8|z<i7d%KbAx.#sf2Z`@93p)
"""

    result = runner.invoke(cli.main, args, input=stdin)

    expected_output = r"""@test_record_0
ACCATTCCCCATAATCAGGGCTAGACCTCCACGGTAAACGGGAAATGCGCTTACGCTATTGTTCCATTACACAAC
+
VPz#iu16@J9f@Dx)J4f,}7Jt$;=+r7r^"}s6u950Hq+0'LX^C*%v9p8R/JY5N[2SA7XEe%mB`tm
@test_record_3
AGACACAGATCAGCCCAAAGATTGATACTACAGTGTGATAAGTGACATGTGATTCGTATAGAAGGTTAGCGAGGC
+
|{-^=-quQ\rfxJ_U!v#Ak:`joYT<\/gY]fE[n0tf.yzThW<N5.6BeK?4(3o0@~\y-O"p,Rdd5{c
@test_record_2
ACGGGTCTAGCAGTTTCTTAAAGCCAGTCTTATACGAATTCCACGTTCTGGTAAGACGTAGCTGGTACAACAATA
+
1w67+i/Z]+b63<$TzQQ2Q?`Uu#3{z$*DI&F&&1{6V^sP(RT+j-ny`}p+D_vg*;xL:@>+1F"?qVD
"""

    assert not result.exception
    assert result.exit_code == 0
    assert result.output == expected_output
