init:
    $ import game.minigames.pipes.pipes as pipes

init:
    $ from game.minigames.pipes.pipes import PuzzleEnum

    define first_puzzle = [
        [
            PuzzleEnum.OneWayONE_EIGHTY,
            PuzzleEnum.ThreeWay,
            PuzzleEnum.TwoWay,
            PuzzleEnum.ThreeWay,
        ],
        [
            PuzzleEnum.TwoWay,
            PuzzleEnum.TwoWaySource,
            PuzzleEnum.TwoWay,
            PuzzleEnum.TwoWay,
        ],
        [
            PuzzleEnum.TwoWay,
            PuzzleEnum.TwoWay,
            PuzzleEnum.TwoWay,
            PuzzleEnum.OneWayZERO,
        ],
    ]

label play_pipes_test:

    e "Welcome!"

    e "What do you want to Play??"

label pipes_retry_test:
    menu:
        "Pipes":
            $ pipes.main((1920, 1080), first_puzzle, 4)

    menu:

        "Would you like to try again?"

        "Sure.":

            "Okay, get ready..."

            jump play_pipes_test

        "No thanks.":

            "Okay, by"

            pass
    return
