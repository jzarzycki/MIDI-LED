import animations

settings = {
    "snare": {
        "animation": animations.color_from_middle,
        "args": ((255, 255, 255), ),
        "multiplier": 1
    },
    "kick": {
        "animation": animations.flash
    },
    "tom1": {
        "animation": animations.color_from_middle,
        "args": ((0, 0, 255), ),
    },
    "tom2": {
        "animation": animations.color_from_middle,
        "args": ((0, 127, 127), ),
    },
    "tom3": {
        "animation": animations.color_from_middle,
        "args": ((0, 255, 0), ),
    },
    "ride head": {
        "animation": animations.color_from_rear,
        "args": ((0, 255, 0), ),
    },
}