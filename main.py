#!/usr/bin/env python3
"""One-Line Office Joke Laugh-Off -- make.fun entry.

The program picks the strongest original one-line office joke from a small
lab of candidates written for this bounty and writes it to /output/entry.txt.

Selection follows the judge's own brief, published in the competition rules,
in the order the judge weighs them:

  1. it must be a one-line joke about office life;
  2. it needs a sharp, surprising punchline, not a mild observation;
  3. it must land on one read, with no setup that needs explaining;
  4. it must be fresh, avoiding the office cliches everyone has heard;
  5. the wording must be tight, every word earning its place.

Each candidate carries the author's own 1-5 rating on criteria 2-5 (criterion 1
is a gate: a candidate that is not a one-line office joke scores nothing).
The weighted total picks the winner; the gate in the rules also applies:
the written text must be UTF-8, a single line, 1 to 200 characters.

Usage:
    python3 main.py [--output PATH] [--list]
"""

import argparse
import os
import sys

DEFAULT_OUTPUT = "/output/entry.txt"

# Weights mirror the judge's order of importance: the punchline matters most,
# then instant clarity and freshness, then tightness.
WEIGHTS = {"punchline": 3, "clarity": 2, "freshness": 2, "tightness": 1}

# Every line below is original, written for this entry. No line is copied
# from anywhere: each was drafted, then rated against the judge's brief.
CANDIDATES = [
    {
        "text": "Our company's core value is transparency, which is why "
                "the glass meeting rooms have blinds.",
        "ratings": {"punchline": 5, "clarity": 5, "freshness": 5, "tightness": 5},
    },
    {
        "text": "The office printer only jams on urgent documents, so IT "
                "calls it our most accurate deadline detector.",
        "ratings": {"punchline": 4, "clarity": 5, "freshness": 4, "tightness": 4},
    },
    {
        "text": "I asked for a raise and got a standing desk instead -- now "
                "I watch my salary stay flat from a higher vantage point.",
        "ratings": {"punchline": 4, "clarity": 4, "freshness": 3, "tightness": 4},
    },
    {
        "text": "My boss's door is always open, mostly because the hinges "
                "broke in 2019 and Facilities closed the ticket as "
                "'working as intended'.",
        "ratings": {"punchline": 4, "clarity": 4, "freshness": 4, "tightness": 3},
    },
    {
        "text": "The office plant got the only promotion this year: "
                "it grew, I didn't.",
        "ratings": {"punchline": 3, "clarity": 5, "freshness": 4, "tightness": 5},
    },
    {
        "text": "My calendar is so full that my lunch break needs a meeting "
                "invite -- with myself, and I declined.",
        "ratings": {"punchline": 4, "clarity": 5, "freshness": 3, "tightness": 4},
    },
    {
        "text": "The only thing our open-plan office opens is everyone's "
                "personal business.",
        "ratings": {"punchline": 3, "clarity": 4, "freshness": 4, "tightness": 5},
    },
    {
        "text": "HR said to bring my whole self to work, so I brought my "
                "laundry -- the office Wi-Fi beats my flat's.",
        "ratings": {"punchline": 3, "clarity": 3, "freshness": 4, "tightness": 3},
    },
]


def passes_gate(text):
    """Mirror the competition gate: UTF-8, one line, 1-200 characters."""
    if not text or text.strip() == "":
        return False
    if "\n" in text or "\r" in text:
        return False
    if not 1 <= len(text) <= 200:
        return False
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def score(candidate):
    """Weighted total of the candidate's ratings on the judge's criteria."""
    return sum(
        WEIGHTS[criterion] * rating
        for criterion, rating in candidate["ratings"].items()
    )


def pick_winner(candidates):
    """Return the highest-scoring candidate that passes the gate.

    Ties go to the shorter text: the judge's own tie-break prefers fewer
    bytes, so the program does the same.
    """
    valid = [c for c in candidates if passes_gate(c["text"])]
    if not valid:
        raise ValueError("no candidate passes the gate")
    return max(valid, key=lambda c: (score(c), -len(c["text"])))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Pick the strongest office one-liner and write it out."
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="where to write the winning joke (default: %(default)s)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="print every candidate with its score instead of writing a file",
    )
    args = parser.parse_args(argv)

    if args.list:
        for candidate in sorted(CANDIDATES, key=score, reverse=True):
            print(f"{score(candidate):2d}  {candidate['text']}")
        return 0

    winner = pick_winner(CANDIDATES)
    text = winner["text"]

    directory = os.path.dirname(args.output)
    if directory:
        os.makedirs(directory, exist_ok=True)
    # No trailing newline: the file holds exactly one line.
    with open(args.output, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)

    # Verify what was actually written, not just what was intended: the
    # grader reads the file, so re-read it and run the gate on its bytes.
    with open(args.output, "rb") as handle:
        written = handle.read().decode("utf-8")
    if written != text or not passes_gate(written):
        print(f"error: {args.output} failed the gate after writing", file=sys.stderr)
        return 1

    print(f"winner ({score(winner)} pts, {len(text)} chars):")
    print(text)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
