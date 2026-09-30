"""Linear algebra over GF(2) on bitmask rows. External analysis only: the
rule never uses any of this (spec, Forbidden structure)."""


class System:
    """A parity system A x = r over k local variables, rows as bitmasks."""

    def __init__(self, k, rows):
        self.k = k
        self.piv = {}          # pivot bit -> [mask, rhs]
        self.consistent = True
        self.independent = True
        for m, r in rows:
            if not self._insert(m, r):
                self.independent = False
        self._reduce()

    def _insert(self, m, r):
        while m:
            h = m.bit_length() - 1
            if h in self.piv:
                pm, pr = self.piv[h]
                m ^= pm
                r ^= pr
            else:
                self.piv[h] = [m, r]
                return True
        if r:
            self.consistent = False
        return False

    def _reduce(self):
        for h in sorted(self.piv):
            m, r = self.piv[h]
            for g in self.piv:
                if g != h and (self.piv[g][0] >> h) & 1:
                    self.piv[g][0] ^= m
                    self.piv[g][1] ^= r

    @property
    def rank(self):
        return len(self.piv)

    def in_rowspace(self, m):
        for h in sorted(self.piv, reverse=True):
            if (m >> h) & 1:
                m ^= self.piv[h][0]
        return m == 0

    def sample(self, rng):
        """A uniform solution, as a bitmask over the k variables."""
        x = 0
        for v in range(self.k):
            if v not in self.piv and rng.integers(2):
                x |= 1 << v
        for h, (m, r) in self.piv.items():
            rest = bin(m & ~(1 << h) & x).count("1") & 1
            if r ^ rest:
                x |= 1 << h
        return x


def parity(mask):
    return bin(mask).count("1") & 1
