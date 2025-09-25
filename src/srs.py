from dataclasses import dataclass

@dataclass
class Card:
    interval: int = 1
    ease: float = 2.5
    reps: int = 0

def review(card: Card, quality: int) -> Card:
    """quality: 0..5 (0=forgot, 5=easy)"""
    q = max(0, min(5, quality))
    if q < 3:
        card.reps = 0
        card.interval = 1
    else:
        card.reps += 1
        if card.reps == 1: card.interval = 1
        elif card.reps == 2: card.interval = 6
        else: card.interval = round(card.interval * card.ease)
        card.ease = max(1.3, card.ease + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)))
    return card
