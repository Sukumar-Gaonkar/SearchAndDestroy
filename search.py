import random
import time
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

class GameMaster:

    def __init__(self, dimen, moving_target):

        self.target_marker = 20
        self.moving_target = moving_target

        self.game_map = self.genMap(dimen)
        self.target = self.create_random_target()
        self.dummy_player = None

    def genMap(self, dimen):
        gamemap = [[0 for i in range(dimen)] for i in range(dimen)]

        for i in range(dimen):
            for j in range(dimen):
                num = random.random()
                if num <= 0.2:
                    gamemap[i][j] = 0  # flat terrain less than 0.2
                elif num > 0.2 and num <= 0.5:
                    gamemap[i][j] = 1  # hilly terrain between 0.2 and 0.5
                elif num > 0.5 and num <= 0.8:
                    gamemap[i][j] = 2  # forested terrain betwwen 0.5 and 0.8
                elif num > 0.8 and num <= 1:
                    gamemap[i][j] = 3  # caves terrain graeter than 0.8
        return gamemap

    def create_random_target(self):
        while True:
            x = np.random.randint(0, len(self.game_map))
            y = np.random.randint(0, len(self.game_map))
            if self.game_map[x][y] == 3:
                break
        return (x, y)

    def search_cell(self, user_target):

        if tuple(self.target) == user_target:
            num1 = random.random()
            terrain_type = self.game_map[self.target[0]][self.target[1]]
            terrain_type = terrain_type - 5 if terrain_type >= 5 else terrain_type
            if terrain_type == 0:
                if num1 > 0.1:
                    return True
            elif terrain_type == 1:
                if num1 > 0.3:
                    return True
            elif terrain_type == 2:
                if num1 > 0.7:
                    return True
            elif terrain_type == 3:
                if num1 > 0.9:
                    return True

        # You got False

        if not self.moving_target:
            return False
        else:
            crossing = [0, 0]

            self.dummy_player.hit_freq[self.target[0]][self.target[1]] -= self.target_marker
            self.dummy_player.hit_freq_texts[self.target[0]][self.target[1]].set_text(str(self.dummy_player.hit_freq[self.target[0]][self.target[1]]))

            crossing[0] = self.game_map[self.target[0]][self.target[1]]

            temp_target = self.target
            moves = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
            move = moves[random.randint(0, 7)]
            temp_target = [move[0] + self.target[0], move[1] + self.target[1]]
            while not self.isvalid(temp_target):
                move = moves[random.randint(0, 7)]
                temp_target = [move[0] + self.target[0], move[1] + self.target[1]]

            self.target = temp_target
            crossing[1] = self.game_map[self.target[0]][self.target[1]]
            self.dummy_player.hit_freq[temp_target[0]][temp_target[1]] += self.target_marker
            self.dummy_player.hit_freq_texts[temp_target[0]][temp_target[1]].set_text(
                str(self.dummy_player.hit_freq[temp_target[0]][temp_target[1]]))

            return crossing

    def isvalid(self, target):
        if target[0] > -1 and target[0] < len(self.game_map) and target[1] > -1 and target[1] < len(self.game_map):
            return True
        else:
            return False

    def printMap(self):
        print(np.matrix(self.game_map))

    def set_player(self, player):
        self.dummy_player = player
        self.dummy_player.hit_freq[self.target[0]][self.target[1]] += self.target_marker


class DummyPlayer:

    def __init__(self, map, moving_target):
        self.map = map
        self.dimen = len(map)
        self.hit_freq = [[0 for j in range(self.dimen)] for i in range(self.dimen)]
        self.belief = self.create_belief_matrix(self.dimen)
        self.moving_target = moving_target

        self.marker = 5
        map[0][0] += self.marker
        self.prev_cell = (0, 0)

        plt.ion()
        self.fig = plt.figure(figsize=(12, 8))
        # self.ax = plt.subplot(1, 3, 1)
        self.belief_plot = plt.subplot(1, 3, 1).matshow(self.belief, cmap='Greys')
        plt.colorbar(self.belief_plot)

        cdict1 = {'red': ((0.0, 1.0, 1.0),
                          (0.2, 0.8, 0.8),
                          (0.4, 0.6, 0.6),
                          (0.6, 0.4, 0.4),
                          (0.8, 0.2, 0.2),
                          (1, 0, 0)),
                  'green': ((0.0, 1.0, 1.0),
                            (0.2, 0.8, 0.8),
                            (0.4, 0.6, 0.6),
                            (0.6, 0.4, 0.4),
                            (0.8, 0.2, 0.2),
                            (1, 0, 0)),
                  'blue': ((0.0, 1.0, 1.0),
                           (0.2, 0.8, 0.8),
                           (0.4, 0.6, 0.6),
                           (0.6, 0.4, 0.4),
                           (0.8, 0.2, 0.2),
                           (1, 0, 0))
                  }

        # terrain_colors = [[x/255.0 for x in l] for l in [[102, 51, 0], [0, 153, 0], [166, 166, 166], [255, 51, 0]]]
        # terrain_colors = [[x/255.0 for x in l] for l in [[199, 233, 192], [161, 217, 155], [116, 196, 118], [49, 163, 84], [0,0,0]]]
        # terrain_colors = plt.cm.Greens
        # terrain_colors = ['gray', 'green', 'brown', 'black', 'blue']
        # map[3][3] += 5
        cm = LinearSegmentedColormap('BlueRed1', cdict1)
        # cm = matplotlib.colors.ListedColormap(terrain_colors)
        self.terrain_plot = self.fig.add_subplot(1, 3, 2).matshow(map, cmap=cm)

        self.freq_ax = self.fig.add_subplot(1, 3, 3)
        self.freq_plot = self.freq_ax.matshow(self.hit_freq, cmap="Oranges")

        self.hit_freq_texts = [[None for i in range(self.dimen)] for i in range(self.dimen)]

        for (i, j), z in np.ndenumerate(self.hit_freq):
            self.hit_freq_texts[i][j] = self.freq_ax.text(j, i, '{}'.format(z), ha='center', va='center')

        plt.show()


    def isvalid(self, target):
        if target[0] > -1 and target[0] < len(self.map) and target[1] > -1 and target[1] < len(self.map):
            return True
        else:
            return False

    # def update_belief_mat_animation(self,data):
    #     self.belief_plot.set_data(self.belief)

    def create_belief_matrix(self, dimen):
        belief = [[1 / (dimen * dimen) for j in range(dimen)] for i in range(dimen)]
        return belief

    def printBelief(self):
        print(np.matrix(self.belief))

    def update_borders(self, i, j, dst, holder_mat):
        count = 0
        moves = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        valid_cells = []
        for move in moves:
            cell = [i + move[0], j + move[1]]
            if self.isvalid((cell[0],cell[1])) and self.map[cell[0]][cell[1]] % self.marker == dst:
                valid_cells.append(cell)
                count += 1

        for cell in valid_cells:
            holder_mat[cell[0]][cell[1]] = holder_mat[cell[0]][cell[1]] + self.belief[i][j] / count

        return count

    def border_cross_detected(self, user_cell, cross):
        # print(cross)

        cross[0] = cross[0] % self.marker
        cross[1] = cross[1] % self.marker

        if self.map[user_cell[0]][user_cell[1]] > 3:
            cell_val = self.map[user_cell[0]][user_cell[1]] - self.marker
        else:
            cell_val = self.map[user_cell[0]][user_cell[1]]

        if cell_val == 0:     # Plains
            fnr = 0.1
        elif cell_val == 1:   # Hilly
            fnr = 0.3
        elif cell_val == 2:   # Forest
            fnr = 0.7
        elif cell_val == 3:   # Caves
            fnr = 0.9

        sum = 1 - (1 - fnr) * self.belief[user_cell[0]][user_cell[1]]
        self.belief[user_cell[0]][user_cell[1]] *= fnr

        if self.moving_target:

            holder_mat = [[0 for j in range(dimen)] for i in range(dimen)]
            for i in range(dimen):
                for j in range(dimen):
                    if self.map[i][j] % self.marker == cross[0]:
                        self.update_borders(i, j, cross[1], holder_mat)
                    elif self.map[i][j] % self.marker == cross[1]:
                        self.update_borders(i, j, cross[0], holder_mat)
                    else:
                        sum -= self.belief[i][j]
                        holder_mat[i][j] = 0

            self.belief = holder_mat

        sum = 0
        for i in range(dimen):
            for j in range(dimen):
                sum += self.belief[i][j]

        # Renormalize the Grid
        for i in range(self.dimen):
            for j in range(self.dimen):
                    self.belief[i][j] /= sum

        yyy = 0

    def next_move(self):

        y = max(map(max, self.belief))

        for i in range(self.dimen):
            for j in range(self.dimen):
                if self.belief[i][j] == y:
                    user_cell = (i, j)

        if self.prev_cell is not None:
            self.map[self.prev_cell[0]][self.prev_cell[1]] -= self.marker

        self.prev_cell = user_cell
        self.map[user_cell[0]][user_cell[1]] += self.marker

        self.hit_freq[user_cell[0]][user_cell[1]] += 1
        hit_count = self.hit_freq[user_cell[0]][user_cell[1]]
        # self.freq_ax.text(user_cell[0], user_cell[1], '{}'.format(hit_count), ha='center', va='center')
        self.hit_freq_texts[user_cell[0]][user_cell[1]].set_text(str(hit_count))
        return user_cell


if __name__ == "__main__":
    dimen = 15

    moving_target = True
    game_master = GameMaster(dimen, moving_target)
    dummy_player = DummyPlayer(game_master.game_map, moving_target)
    game_master.set_player(dummy_player)

    game_won = False

    # dummy_player.hit_freq[game_master.target[0]][game_master.target[1]] += game_master.target_marker

    game_master.printMap()
    dummy_player.printBelief()

    terrains = ["Plains", "Hilly", "Forest", "Caves"]
    print("Dimen: {}  Target: {},{} : {}".format(dimen, game_master.target[0], game_master.target[1], terrains[dummy_player.map[game_master.target[0]][game_master.target[1]] % 5]))

    input("Press 'Y' Key to continue")      # just to stop the execution before entering while loop
    i = 0

    while True:
        i += 1
        user_cell = dummy_player.next_move()
        status = game_master.search_cell(user_cell)
        crossing = None
        if status == True:
            break
        else:
            crossing = status

        dummy_player.border_cross_detected(user_cell, crossing)
        # dummy_player.update_belief_matrix(user_cell)
        print("\nMove - {}: {},{}\n".format(i, user_cell[0], user_cell[1]))

        dummy_player.printBelief()
        dummy_player.terrain_plot.set_data(dummy_player.map)
        dummy_player.belief_plot.set_data(dummy_player.belief)
        dummy_player.freq_plot.set_data(dummy_player.hit_freq)
        dummy_player.freq_plot.set_clim(0, game_master.target_marker)
        dummy_player.fig.canvas.draw()
        plt.pause(0.0001)
        # time.sleep(0.01)

    print("Kudos you Won!!!\n{} cells Searched".format(i))
    input()
