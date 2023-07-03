init:
    $ import game.minigames.pipes.pipes as pipes

label play_pipes_test:

    e "Welcome!"

    e "What do you want to Play??"

label pipes_retry_test:
    menu:
        "Pipes":
            $ pipes.main((1920, 1080), 4)

    menu:

        "Would you like to try again?"

        "Sure.":

            "Okay, get ready..."

            jump aliens_retry

        "No thanks.":

            "Okay, by"

            pass
    return
