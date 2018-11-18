import random
import time
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from collections import Counter

class GameMaster:

    def __init__(self, dimen):
        self.game_map = self.genMap(dimen)
        self.target = self.create_random_target()

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
            if self.game_map[x][y] == 0:
                break
        return (x, y)

    def search_cell(self, user_target):

        if self.target == user_target:
            num1 = random.random()
            terrain_type = self.game_map[self.target[0]][self.target[1]]
            if terrain_type == 0:
                if num1 <= 0.1:
                    return False
                else:
                    return True
            elif terrain_type == 1:
                if num1 <= 0.3:
                    return False
                else:
                    return True
            elif terrain_type == 2:
                if num1 <= 0.7:
                    return False
                else:
                    return True
            else:
                if num1 <= 0.9:
                    return False
                else:
                    return True
        else:
            return False

    def printMap(self):
        print(np.matrix(self.game_map))


class DummyPlayer:

    def __init__(self, map,rule,case):
        self.map = map
        self.dimen = len(map)
        self.rule=rule
        self.case=case
        self.hit_freq = [[0 for j in range(self.dimen)] for i in range(self.dimen)]
        self.belief = self.create_belief_matrix(self.dimen)
        self.belief_2=self.create_belief_matrix_2(self.dimen)
        self.plaincount=sum(x.count(0) for x in map)
        self.hillcount=sum(x.count(1) for x in map)
        self.forestcount=sum(x.count(2) for x in map)
        self.cavecount=sum(x.count(3) for x in map)
        self.arr1=[[0]*self.plaincount,[1]*self.hillcount,[2]*self.forestcount,[3]*self.cavecount]
        self.arr=[item for sublist in self.arr1 for item in sublist]
        self.k=0
        self.sort_arr=[item for items, c in Counter(self.arr).most_common() for item in [items] * c]
        self.marker = 5
        map[0][0] += self.marker
        self.prev_cell = (0, 0)

        plt.ion()
        self.fig = plt.figure(figsize=(10, 6))
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
        self.freq_plot = self.freq_ax.matshow(self.hit_freq)

        self.hit_freq_texts = [[None for i in range(self.dimen)] for i in range(self.dimen)]

        for (i, j), z in np.ndenumerate(self.hit_freq):
            self.hit_freq_texts[i][j] = self.freq_ax.text(j, i, '{}'.format(z), ha='center', va='center')

        plt.show()


    def update_belief_mat_animation(self,data):
        self.belief_plot.set_data(self.belief)

    def create_belief_matrix(self, dimen):
        belief = [[1 / (dimen * dimen) for j in range(dimen)] for i in range(dimen)]
        return belief
    def create_belief_matrix_2(self, dimen):
        belief_2 = [[1 / (dimen * dimen) for j in range(dimen)] for i in range(dimen)]
        return belief_2
    
    def printBelief(self):
        print(np.matrix(self.belief))
    def printBelief_2(self):
        print(np.matrix(self.belief_2))
        

    def update_belief_matrix(self, user_cell):

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
        # scaling_fac = (1 - fnr) * self.belief[user_cell[0]][user_cell[1]] / sum
        self.belief[user_cell[0]][user_cell[1]] *= fnr


        # Renormalize the Grid
        for i in range(self.dimen):
            for j in range(self.dimen):
                    self.belief[i][j] /= sum
                    self.belief_2[i][j] =(self.belief[i][j]/ sum)*(1-fnr)

                    

    def next_move(self):
        
        if(self.case==1):
            maxm=0
            if(self.k>=self.dimen*self.dimen) :
                self.k=0
            for i in range(self.dimen):
                for j in range(self.dimen):
                 #   print(self.k)
                    if self.map[i][j]==self.sort_arr[self.k]:
                        if(self.rule==1):
                            if self.belief[i][j]> maxm:
                    
                                maxm=self.belief[i][j]
                                user_cell = (i, j)
                        elif(self.rule==2):
                            if self.belief_2[i][j]> maxm:
                    
                                maxm=self.belief_2[i][j]
                                user_cell = (i, j)
            self.k=self.k+1
                                 
        if(self.case==2):
            if(self.rule==1):
                y = max(map(max, self.belief))
                for i in range(self.dimen):
                    for j in range(self.dimen):
                        if self.belief[i][j] == y:
                            user_cell = (i, j)
            elif(self.rule==2):
                y = max(map(max, self.belief_2))
                for i in range(self.dimen):
                    for j in range(self.dimen):
                        if self.belief_2[i][j] == y:
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
    dimen = 5
    fileName = "D:/results/profilerResults_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"
    f = open(fileName, "a", 1)
    f.write("Gridsize;IterationNo;Case;Rule;Searches\n")
     
    for case in range(1,3):
        for rule in range(1,3):
            game_master = GameMaster(dimen) 
            dummy_player = DummyPlayer(game_master.game_map,case,rule)    
            game_won = False
            game_master.printMap()
            dummy_player.printBelief()
            terrains = ["Plains", "Hilly", "Forest", "Caves"]
            print(dummy_player.map[game_master.target[0]][game_master.target[1]])
            print("Dimen: {}  Target: {},{} : {}".format(dimen, game_master.target[0], game_master.target[1], terrains[(dummy_player.map[game_master.target[0]][game_master.target[1]])%5]))
          #  input("Press 'Y' Key to continue")      # just to stop the execution before entering while loop
            i = 0
    
            while not game_won:
                i += 1
                user_cell = dummy_player.next_move()
                game_won = game_master.search_cell(user_cell)
                dummy_player.update_belief_matrix(user_cell)
                print("\nMove - {}: {},{}\n".format(i,user_cell[0],user_cell[1]))
                dummy_player.printBelief()
                dummy_player.terrain_plot.set_data(dummy_player.map)
                dummy_player.belief_plot.set_data(dummy_player.belief)
                dummy_player.freq_plot.set_data(dummy_player.hit_freq)
                dummy_player.fig.canvas.draw()
                #plt.pause(0.001)
                # time.sleep(0.01)

            print("Kudos you Won!!!\n{} cells Searched".format(i))
            f.write("{0};{1};{2};{3};{4}\n".format( dimen, 1,case,rule,i))
            #input()

