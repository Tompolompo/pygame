from spacejet import spacejetRL

game = spacejetRL.Game()

for i in range(100):
    print(f"step = {i}")
    score = game.step_game([1,0,1,0])