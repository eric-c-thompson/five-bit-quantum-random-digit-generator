# A Simple Five-Bit Quantum Random Digit Generator

Reference implementation and companion materials for the white paper:

**A Simple Five-Bit Quantum Random Digit Generator:  
A Transparent Rejection-Sampling Protocol with Extreme-Run Recycling**

**Author:** Eric C. Thompson  
**ORCID:** [0009-0001-4127-1742](https://orcid.org/0009-0001-4127-1742)  
**Paper DOI:** [10.5281/zenodo.20076445](https://doi.org/10.5281/zenodo.20076445)  
**Software DOI:** [YOUR-SOFTWARE-DOI](YOUR-SOFTWARE-DOI-LINK)

## Overview

This repository contains a reference implementation of a simple five-bit digitization protocol for generating uniform decimal digits from an ideal two-outcome quantum random source.

The protocol groups five fair binary outcomes into a candidate block. Since five bits produce `2^5 = 32` possible sequences, the method rejects the two extreme runs, `00000` and `11111`, leaving exactly 30 accepted sequences. Those 30 sequences map evenly onto the ten decimal digits, with three accepted sequences per digit.

The white paper also introduces a small efficiency improvement called **extreme-run carry-forward recycling**. Instead of discarding a rejected all-zero or all-one block entirely, the protocol carries forward one bit from that rejected extreme run as the first bit of the next candidate block. Under ideal fair-bit assumptions, this preserves exact decimal uniformity while slightly reducing the expected raw-bit cost.

## Why This Matters

The purpose of this protocol is not maximum entropy efficiency. More advanced extractors and large-block methods can operate closer to the theoretical entropy limit.

The value of this protocol is **simplicity, transparency, and auditability**.

That makes it potentially useful in settings where a random-number process must be explained to nontechnical users, such as educational demonstrations, public lotteries, gaming systems, raffles, consumer-facing random selection tools, or other trust-critical applications where visible fairness matters.

The basic public explanation is compact:

> Five fair quantum bits produce 32 possible outcomes. Reject the two extreme runs. The remaining 30 outcomes divide evenly into ten decimal digits.

## Repository Contents

```text
five_bit_qrng.py     Reference Python implementation
paper/               White paper PDF
README.md            Project description
LICENSE              Repository license
.gitignore           Ignore rules for Python and LaTeX auxiliary files
```

## Important Note About the Code

The accompanying Python code is a reference implementation of the **digitization logic only**.

Its default bit source is a simulated fair-bit generator and is **not** a quantum random number generator. In a physical implementation, the function that supplies bits should be replaced by a validated quantum entropy source or hardware QRNG interface.

The code should not be used by itself for cryptographic randomness.

## Basic Protocol

1. Read five fair bits.
2. Convert the five-bit block to an integer from 0 to 31.
3. Reject `00000` and `11111`.
4. For all accepted values 1 through 30, output:

```text
digit = value mod 10
```

Because 30 is exactly divisible by 10, each decimal digit receives exactly three accepted five-bit sequences.

## Carry-Forward Protocol

The carry-forward version modifies only the rejection step:

- If `00000` occurs, carry forward one `0` as the first bit of the next block.
- If `11111` occurs, carry forward one `1` as the first bit of the next block.
- Draw only four new bits to complete the next five-bit candidate block.

Under independent fair-bit assumptions, the carried bit is itself fair, so the next candidate block remains uniformly distributed.

## Citation

If you use or discuss this protocol, please cite the Zenodo record:

```bibtex
@misc{thompson2026fivebitqrng,
  author       = {Thompson, Eric C.},
  title        = {A Simple Five-Bit Quantum Random Digit Generator: A Transparent Rejection-Sampling Protocol with Extreme-Run Recycling},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.20076445},
  url          = {https://doi.org/10.5281/zenodo.20076445}
}
```

## License

See the `LICENSE` file for reuse terms.
