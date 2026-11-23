#!/usr/bin/env python3
"""One Word From Grandma -- make.fun bounty entry.

The task: send exactly one word, the single word a grandma would text
about AI. This program scores a table of candidate words against the
judge's five criteria (most important first) and writes the winning
word -- and nothing else -- to /output/entry.txt.

Criteria, in judge order:
  1. Grandma-texting-about-AI: reads as the word a grandma would text
     about AI itself.
  2. Grandma voice: warm, a little baffled, the way she types to a
     grandchild.
  3. Funny in one word: the joke lands with no caption.
  4. AI tie: feels tied to AI, robots or machines -- not a word that
     fits any subject.
  5. Fresh: not the obvious pick, but still instantly readable.

Scoring is 0-5 per criterion, weighted 5/4/3/2/1 so the judge's
priority order decides the winner. Standard library only, no network,
no randomness, fully deterministic.
"""

import os

OUTPUT_PATH = "/output/entry.txt"

# Each candidate: (word, (c1, c2, c3, c4, c5), reason)
#
# c1 grandma-texting-about-AI / c2 grandma voice / c3 funny /
# c4 AI tie / c5 fresh.
CANDIDATES = [
    # The word every grandma reaches for when a gadget she cannot name
    # does something she cannot explain. "This whatchamacallit keeps
    # talking to me." Warm, baffled, and it only really works for a
    # mysterious machine -- the AI tie is built into the confusion.
    ("Whatchamacallit", (5, 5, 5, 4, 4),
     "Grandma's default name for any device she can't name; AI is the "
     "ultimate unnamed gadget."),
    # Close cousin, same family of grandma gadget-words, but a touch
    # shorter on warmth and a touch more generic -- it names any small
    # thing, not specifically a baffling machine.
    ("Thingamajig", (4, 5, 4, 3, 4),
     "Same grandma gadget-word family, but fits any small object, not "
     "just a talking machine."),
    # The classic. Lovely and grandma, but it names any little widget --
    # a kitchen drawer item as easily as a robot -- so the AI tie is
    # weaker, and it is the more obvious pick of the three.
    ("Doohickey", (4, 5, 4, 2, 3),
     "Pure grandma, but just as likely to be a drawer handle as a "
     "robot, and the most expected choice."),
    # "This is witchcraft!" is exactly what a grandma says about a
    # machine that answers back. Funny and warm, but it fits any new
    # technology, not AI in particular.
    ("Witchcraft", (4, 4, 5, 2, 4),
     "What grandma calls any impossible tech; hilarious, but the AI tie "
     "is only by context."),
    # "That contraption" is peak grandma-suspicion of machinery, but it
    # sounds like something from the shed, not a text to a grandchild,
    # and it is a little stiff for a laugh.
    ("Contraption", (4, 4, 3, 3, 4),
     "Grandma-suspicious of machines, but reads more like a shed "
     "complaint than a text."),
    # Short, cute, very AI-flavoured -- but it is internet voice, not
    # grandma voice. A grandma would not type "beepboop" unprompted.
    ("Beepboop", (3, 2, 4, 5, 4),
     "Strong robot flavour, but no grandma has ever typed this; it is "
     "a meme word, not her word."),
    # Grandma's favourite nonsense exclamation. Delightful, but it could
    # follow any sentence about anything -- zero AI tie.
    ("Fiddlesticks", (2, 5, 4, 0, 3),
     "Wonderful grandma exclamation, but it fits a burnt roast as well "
     "as a robot -- no AI tie at all."),
    # "That's malarkey" is grandma dismissing nonsense. Warm and funny,
    # but it is a verdict on any claim, not a word about a machine.
    ("Malarkey", (2, 5, 3, 0, 3),
     "Grandma calling nonsense, but it judges any statement, not AI."),
    # The friendly little gadget word. Warm enough, but it sounds like a
    # gadget catalogue, not a grandma texting her grandchild.
    ("Gizmo", (3, 3, 3, 3, 2),
     "A gadget word, but more catalogue than grandma, and very common."),
    # Too clever by half: a grandma does not know Skynet, so it fails
    # the voice test outright, however funny the reference is.
    ("Skynet", (2, 1, 3, 5, 2),
     "Perfect AI reference, wrong speaker -- grandma has never heard "
     "of Skynet."),
]

# Judge-priority weights: criterion 1 matters most, 5 least.
WEIGHTS = (5, 4, 3, 2, 1)


def score(candidate):
    """Weighted total for one candidate: (word, scores, reason)."""
    _word, scores, _reason = candidate
    return sum(w * s for w, s in zip(WEIGHTS, scores))


def pick_winner():
    """Highest weighted score wins; ties break by earlier table order,
    so the table's ordering is the deliberate tie-break. Returns the
    winner, its score, and the margin over the runner-up, so the
    choice is auditable, not just asserted."""
    ranked = sorted(CANDIDATES, key=score, reverse=True)
    winner = ranked[0]
    runner_up = ranked[1]
    return winner, score(winner), score(winner) - score(runner_up), runner_up[0]


def main():
    winner, total, margin, runner_up = pick_winner()
    word = winner[0]
    assert 1 <= len(word) <= 30, "word must be 1-30 characters"
    assert word.strip() == word and " " not in word, "single word only"
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(word + "\n")
    print(f"Wrote {word!r} (score {total}, beats runner-up "
          f"{runner_up!r} by {margin}) to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
