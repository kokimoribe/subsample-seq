##  About
Command line application to subsample sequences from a FASTA or FASTQ formatted text file.

## Usage

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

## Installation

```bash
git clone git@gitlab.com:koki.moribe/subsample-seq.git
cd subsample-seq
pip install .
```


## Algorithm
### Problem:
Randomly choose `k` sequences from a file containing multiple sequences. The total number of sequences in the file is not known up front.

### Solution (https://en.wikipedia.org/wiki/Reservoir_sampling#Algorithm_R):
Time complexity: O(*n*)
1. Initialize an array of size `k`. This array will be the `reservoir` that will eventually contain the randomly selected sequences.
1. Populate the array with the first *k* sequences from the file.
    ```python
    import itertools

    # Assume `sequences` is an iterable containing an unknown number of sequences
    reservoir = [seq for seq in itertools.islice(sequences, k)]
    ```
1. For any `i` th sequence that is past the `k` th sequence, generate a random position `j` that is between the start and current position `i` (inclusive). If the `j` th position sits within the reservoir, then replace sequence at the `j` th position in the reservoir with the `i` th sequence.
    ```python

    # In the code implementation, assume `i` and `j` use 0-based indexing and `k` is the size of the reservoir.

    if i >= k:
        j = random.randint(0, i)
        if j < k:
            reservoir[j] = sequence_i  # where `sequence_i` is the sequence found at index `i`
    ```
1. Iterate through all sequences using the above logic:
    ```python

    reservoir = []

    for i, sequence in enumerate(sequences):
        if i < k:
            reservoir.append(sequence)

        else:
            j = random.randint(0, i)
            if j < k:
                reservoir[j] = sequence

    return reservoir
    ```

### Explanation
This section explains why any given sequence in the collection has a probability `k/n` of being in the reservoir at the end.

For any `i`th sequence past the `k`th sequence, the probability of the sequence *entering* the reservoir is `k/i`. This is because the sequence will only enter the reservoir when `j` is a position that exists within the reservoir (recall that the reservoir only has `k` positions). In other words, out of all the possible positions that can be randomly selected (which is `i` positions), only `k` positions exist that will cause the `i`th sequence to enter the reservoir (i.e. `k/i`).

For any sequence that is in the reservoir, the chances of it getting replaced on each iteration is `1/i`. This is because a sequence will only get replaced if the randomly selected  `j`th position sits within the reservoir, which was just explained to have a probability of `k/i`. Thus, the probability for a sequence sitting in a *specific* position in the reservoir to get replaced is `k/i` multiplied by `1/k`, which equals to `1/i`.

We can use what we learned from above to prove that the probability of any given sequence will be included in the reservoir at the end is `k/n`, where `n` is the total number of sequences.

First, let's look at the scenario where `i` is the last sequence. If the `i`th sequence is the last one, then we know that `i` is equal to `n`. Since the probability of the `i`th sequence entering the reservoir is `k/i`, the probability of the *last* sequence entering the reservoir is `k/n`. We can ignore the probability of the sequence getting replaced in the reservoir since this is the last sequence.

Now, let's look at the *second to last sequence*, where `i` is equal to `n - 1`. Since we know the probability of the `i`th sequence entering the reservoir is `k/i`, we can say that the probability of the second to last sequence entering the reservoir is `k/(n - 1)`. If the second to last sequence ends up entering the reservoir, the probability of it getting replaced by the *next* sequence is `1/(i + 1)`, or `1/n`.

Thus, the probability of the second to last sequence entering the reservoir and *not getting replaced* by the last sequence is:

`k/(n - 1) * (1 - (1/n))` which simplifies to `k/(n - 1) * (n - 1)/n`, or `k/n`.

We can repeat this process to find the probability for any `i`th sequence to enter the reservoir and not get replaced by the remaining sequences.

```text
k/i * (1 - (1/(i + 1))) * (1 - (1/(i + 2))) * (1 - (1/(i + 3)) * ... * (1 - (1/(i + m)))

which simplifies to

k/i * i/(i + 1) * (i + 1)/(i + 2) * (i + 2)/(i + 3) * ... * (i + m - 1)/(i + m)
```

We can then see that the denominator of a given fraction is canceled out by the numerator of the following fraction. This continues until we reach the last denominator `i + m` where `i + m` equals to `n`, the total number of sequences. Thus, after we cancel out the possible denominators and numerators, we get the numerator of the first fraction over the denominator of the last fraction, i.e. `k/(i + m)`, or `k/n`.

Lastly, let's look at the first `k` sequences. We don't need to worry about the probability of the first `k` sequences entering the reservoir since the first `k` sequences are automatically included. However, we will need to calculate the probability of a given sequence that starts in the reservoir will *remain* in the reservoir (i.e. not get replaced) at the end. As explained earlier, we know that the probability of a given sequence in the reservoir at a specific position has a probability `1/i` of it getting replaced by the `i`th sequence. Thus, the probability of *not* getting replaced by the `i`th sequence is `1 - (1/i)`, or `(i - 1)/i`. We can then deduce that a sequence in the first `k` sequences will remain in the reservoir if it does not get replaced by the `k + 1`th sequence, the `k + 2`th sequence, and so on. Thus, the probability is equal to:
```
(k + 1 - 1)/(k + 1) * (k + 2 - 1)/(k + 2) * ... * (k + m - 1)/(k + m)

which simplifies to

k/(k + 1) * (k + 1)/(k + 2) * ... * (k + m - 1)/(k + m)
```

Similar to what we saw earlier, the denominator of a given fraction is canceled out by the numerator of the following fraction. This continues until we reach the last denominator `k + m` where `k + m` equals to `n`. Thus the equation can be simplified to `k/(k + m)`, or `k/n`
