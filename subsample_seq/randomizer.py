"""Module for defining functions that use RNG"""


from random import Random


def subsample(records, sample_size, seed=None):
    """
    Return a random sample from an iterable collection of records.

    Reservoir Sampling is used to select the random sample.
    The specific implementation is known as Algorithm R.
    https://en.wikipedia.org/wiki/Reservoir_sampling
    """
    # Create an instance of `Random` to only set the seed within the scope of this function.
    # https://stackoverflow.com/questions/12368996/what-is-the-scope-of-a-random-seed-in-python
    random = Random(seed)

    reservoir = []
    for i, item in enumerate(records):
        if i < sample_size:
            reservoir.append(item)
        else:
            j = random.randint(1, i)
            if j < sample_size:
                reservoir[j] = item

    return reservoir
