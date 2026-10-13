## 2026-10-12: commit: Completed sample_errors in noise.py with seedable RNG and wrote test suite

**Layout**
- Library code in `src/repcode/`, tests in `tests/`, plot scripts in `experiments/`. One file per job (`noise.py` for generating errors; `syndrome.py`, `decoders.py` and a metrics file later). Tests and experiments only call library functions and hold no logic. Alternative: one big script. Why: short files, easy to find things.

**Representation**
- Errors are a 2D NumPy array of shape `(shots, d)`: rows are shots, columns are physical bits, 1 means flipped. Alternative: qubit/ket objects with Python loops. Why: the array is the state, so there's nothing to initialise, and it's vectorised.

**Sampling**
- Goal: each cell is 1 (flipped) with probability p, and 0 otherwise, independently of every other cell.
- Chosen: `rng.binomial(1, p, size=(shots, d))`. A binomial with n=1 is a single Bernoulli trial per cell, and it returns 0/1 integers directly, in one step.
- Alternative that also works: draw a uniform random number in [0, 1) for each cell with `rng.random((shots, d))`, then set the cell to 1 if the number is below p (`< p`) and convert booleans to ints with `.astype(int)`. A uniform number is below p with probability exactly p, so this has the same distribution as binomial.
- Alternative that doesn't work: draw the uniform number and round it to the nearest integer. Numbers below 0.5 round to 0 and numbers above 0.5 round to 1, so every cell is 1 with probability 0.5, and p never appears in the calculation. The result would be wrong for every p except 0.5. The comparison against p is what builds p into the result.
- Why binomial: it's the simplest correct option and it's the Bernoulli trial from the maths. I'd switch to the compare version if I ever needed the raw uniform numbers for something else.
- Generator: `np.random.default_rng` (a Generator object). Alternative: legacy `np.random.seed`, which uses a hidden global state. Why: the random source is explicit, so it's easy to seed and test.

**Seed**
- `sample_errors(d, p, shots, seed=None)`. Alternatives: hardcoded 42 (every call returns the same grid, and "different seed" is untestable), or pass an `rng` object in. Why: tests need reproducibility, experiments need fresh randomness. I'd switch to passing in an `rng` if I need to share one stream across many calls.

**Tests**
- One test function per behaviour, so a failure names what broke and the others still run. Tests: p=0 all zeros, p=1 all ones, shape, values binary, mean close to p, same seed reproducible, different seeds differ.
- Shape test uses d ≠ shots (7 and 11) so a swapped order would fail.
- Mean test: d=5, shots=100,000, tolerance 0.01. The standard deviation of the mean is √(p(1−p)/N) ≈ 0.0006, so the tolerance is wide enough to never fail by luck and tight enough to catch a bug like using p². p=0 and p=1 can't catch that.
- Statistical tests use a fixed seed so a failure means the code changed. Tests with certain answers need no seed.
- Comparison tools: `np.array_equal` for exact grids (also checks shape), `np.isin(x, [0,1]).all()` for binary values, `abs(mean - p) < tol` for statistics.

**Open (not decided yet)**
- Decoder return type: correction grid (leaning this, closest to real decoders) vs yes/no per shot. All three decoders must match.
- Restrict to odd d (no ties in majority vote)?

## 2026-10-13: commit: <your commit message here>

**Decoder return type**
- Every decoder returns a 1D boolean array of length `shots`: True means the decoder failed on that shot. Alternatives: return a correction grid (`shots × d`), or return the logical error rate as a single number. Why: the plot only needs the failure rate, and a per-shot array lets the three decoders be compared shot by shot (the "all decoders agree" test). The mean happens later in `logical_error_rate`, not inside the decoder. I'd switch to a correction grid if I need to inspect what a decoder actually did. Caveat: the syndrome decoders only see the syndrome, so they'll need the original errors to judge failure. Revisit this when I build them.

**Majority vote**
- `majority_vote(errors)`: `errors.sum(axis=1) > d / 2`, where `d = errors.shape[1]`. Vectorised only for now. The plain-loop version is deferred to the Milestone 3 timing study. Cost: O(d × shots), which is the lower bound since every element must be read.
- It reads the data bits directly, so it's a baseline and not a real decoder (reading data would collapse a quantum state).
- Odd d only. Alternatives for even d: tie → 0 (flatters the error rate, since the stored bit is 0), tie → 1 (pessimistic), tie → random (needs its own rng and seed). Why: no ties exist for odd d, and the brief only uses odd d. With strict `>`, a tie would silently count as success, so even d should raise an error. <delete this line if you didn't add the check>
- The function takes the grid as a parameter and doesn't import `sample_errors`. Whoever calls it (a test, `logical_error_rate`) generates the grid and passes it in. `logical_error_rate` will take the decoder function as an argument so decoders can be swapped.

**Tests**
- Decoder tests use hand-built grids, not `sample_errors`, so the expected answer is known independently. A test that computes its answer with the same logic as the code would be circular.
- Cases: d=3 rows with 0, 1, 2, 3 ones; d=5 rows with 0, 2, 3, 5 ones (the 2-vs-3 boundary); all zeros never fails; all ones always fails.
- Expected output written as 0/1, which `np.array_equal` treats as equal to False/True.
- Mutation checks: flipping `>` to `<` and changing `/ 2` to `/ 3` should each fail a test. <tick when done>