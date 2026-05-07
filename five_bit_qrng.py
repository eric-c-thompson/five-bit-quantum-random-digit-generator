"""
Reference implementation for the five-bit quantum random digit protocol.

This file demonstrates the digitization logic only. The default bit source below
uses Python's standard pseudo-random generator to simulate fair input bits. It is
not a quantum random number generator and should not be used for cryptographic
randomness. In a physical QRNG implementation, replace simulated_fair_bits with
a validated hardware entropy source.
"""

import random
from collections import Counter


def simulated_fair_bits(n):
    """Simulate reading n ideal fair bits. This is not a QRNG."""
    return [random.choice([0, 1]) for _ in range(n)]


def bits_to_int(bits):
    """Convert a list of bits, such as [1, 0, 1, 0, 1], to an integer."""
    out = 0
    for bit in bits:
        if bit not in (0, 1):
            raise ValueError("Bits must be 0 or 1.")
        out = (out << 1) | bit
    return out


def basic_protocol(bit_source):
    """
    Yield uniform decimal digits using the basic five-bit
    extreme-sequence exclusion protocol.

    Assumes bit_source(n) returns n independent fair bits.
    """
    while True:
        block = bit_source(5)
        v = bits_to_int(block)

        if v == 0 or v == 31:
            continue

        yield v % 10


def carry_forward_protocol(bit_source):
    """
    Yield uniform decimal digits using the extreme-run
    carry-forward recycling protocol.

    Assumes bit_source(n) returns n independent fair bits.
    """
    carry_exists = False
    carry_bit = None

    while True:
        if carry_exists:
            block = [carry_bit] + bit_source(4)
            carry_exists = False
        else:
            block = bit_source(5)

        v = bits_to_int(block)

        if v == 0:
            carry_bit = 0
            carry_exists = True
            continue

        if v == 31:
            carry_bit = 1
            carry_exists = True
            continue

        yield v % 10


def sample_digits(generator, count):
    """Collect count digits from a digit generator."""
    return [next(generator) for _ in range(count)]


def demo_distribution(protocol, bit_source, count=100_000):
    """Quick simulation check of output digit frequencies."""
    gen = protocol(bit_source)
    digits = sample_digits(gen, count)
    counts = Counter(digits)

    for digit in range(10):
        print(f"{digit}: {counts[digit]} ({counts[digit] / count:.4f})")


if __name__ == "__main__":
    print("First 20 digits using the basic protocol:")
    basic_gen = basic_protocol(simulated_fair_bits)
    print(sample_digits(basic_gen, 20))

    print("\nFirst 20 digits using the carry-forward protocol:")
    carry_gen = carry_forward_protocol(simulated_fair_bits)
    print(sample_digits(carry_gen, 20))

    print("\nDistribution check: basic protocol")
    demo_distribution(basic_protocol, simulated_fair_bits)

    print("\nDistribution check: carry-forward protocol")
    demo_distribution(carry_forward_protocol, simulated_fair_bits)
