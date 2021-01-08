import mmh3


def hash_to_bucket(e, B):
    i = mmh3.hash128(str(e))
    p = i / float(2**128)
    for j in range(0, B):
        if j/float(B) <= p and (j+1)/float(B) > p:
            return j+1
    return B
