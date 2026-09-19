
from Game.game import SnakeGame

if __name__ == "__main__":
    game = SnakeGame()
    while True:
        action = None
        reward,game_over,score = game.play_step(action)
        if game_over:
            game.reset()
