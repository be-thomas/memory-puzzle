import random, time
from timeit import default_timer as timer



class ScoreBoard:
    '''
    ScoreBoard class handles all input output operations related to storing and retrieving Top High Scores
    The data in file is saved in this format-
    Name
    score
    Name
    score
    ...
    
    If the scores are manually edited, this class will detect the format and delete it
    '''

    def __init__(self):
        self.path = "scores.txt"
 #scores get saved here
        self.limit = 10
   #only Top 10 scores are saved

    def create_new(self):
        open(self.path, "w").close()
  #deletes all existing data

    def check(self, score):
        '''this is a multipurpose function, the 2 purposes are listed here-
        1) update the self.scores array by reading from save file
        2) check whether passed score can fit in the list, i.e. check if it is higher than the lowest score in list
         for only updating the list, you can pass 0 or any other number, it doesn't matter
        '''
        self.scores = []
        try:
            sf = open(self.path, "r")
            #read all data from file as an array
            contents = sf.read().split("\n")[:-1]
            sf.close()
            #destroy the data if the array length is odd or array length is >20
            if (len(contents)%2 != 0) or len(contents)>20:
                self.create_new()
            else:
                i = 0
                while i < (len(contents)-1):
                # loop through the array to convert contents into an array of tuples, each tuple will have a name(string) and a score(integer)
                    try:
                        self.scores.append((contents[i], int(contents[i+1])))
                    except ValueError:
                    #if the score is not an integer destroy the data
                        scores = []
                        self.create_new()
                        break
                    i += 2
        except FileNotFoundError:
        #if file not found, create an empty file
            self.create_new()
        if len(self.scores) < self.limit:
            return True
        else:
            v = self.scores[0][1]
            for i in range(0, len(self.scores)):
#search for lowest score in the list
                if self.scores[i][1] < v:
                    v = self.scores[i][1]
            if score > v:
#if score is higher than the lower score, it can be added to the list
                return True
        return False
    def add(self, name, score):
        if len(self.scores) < self.limit: #if the list is smaller than 10 just add it
            self.scores.append((name, score))
        else:
        #if score > (lowest score in the list) then replace lowest score with the supplied score
            v = self.scores[0][1]
            for s in self.scores:
                if s[1] < v:
                    v = s[1]
            if score > v:
                for i in range(0, len(self.scores)):
                    if self.scores[i][1] == v:
                        self.scores[i] = (name, score)
                        break
        self.write()

    def cls(self):
        #prepare screen for new data
        print("\n"*25)

    def write(self):
    #safe self.scores list
        sf = open(self.path, "w")
        for x in self.scores:
            sf.write(x[0] + "\n" + str(x[1]) + "\n")
        sf.close()

    def draw(self):
        #draws the top 10 list
        l = sorted(self.scores,key=lambda x:x[1], reverse=True) #sort array in descending order
        x = 1
        print("Position | Score | Name")
        print("_________|_______|______________")
        for i in l:
            line = str(x)
            line += " "*(9-len(line))
            line += "| " + str(i[1])
            line += " "*(6-len(str(i[1]))) + "| " + i[0]
            print(line)
            x += 1


class Grid:
    '''
    Grid class handles the drawing, updating score and processing inputs for the game
    '''
    def __init__(self, sb):
        self.score, self.scoreboard = 0, sb
        self.revealed = []    #this array contains tuples of coordinates of the revealed places, in this format - (x, y)
        #create an array with all numbers from 0-9 occurring twice
        temp = [i for i in range(0, 10)]*2
        #shuffle the list
        random.shuffle(temp)
        x = 0
        self.board = []
        #board will be a 2d 4*5 array for the representation of the grid
        for i in range(0, 4):
            y = []
            for j in range(0, 5):
                y.append(temp[x])
                x += 1
            self.board.append(y)
        #note the time when the player started playing
        self.started = timer()
        self.interrupted = False
        self.mode = mode
        if self.mode == 'GUI':
            pygame.init()
            self.clock = pygame.time.Clock()
            self.screen = pygame.display.set_mode((500, 500))
            pygame.display.set_caption("Memory Puzzle")
            pygame.font.init()
            self.font = pygame.font.SysFont('Arial', 20)
            self.font1 = pygame.font.SysFont('Arial', 60)

    def draw(self):
        if self.mode == 'CLI':
            self.drawCLI()
        elif self.mode == 'GUI':
            self.drawGUI()

    def drawCLI(self):
        #draws/updates the board
        print("Score: " + str(self.score)+"\n\n")
        caption = "    " + " ".join([str(i) for i in range(1, 6)])
        caption += "\n" + "   ___________"
        caption += "\n" + "  |           |"
        print(caption)
        x, y = 0, 0
        for i in range(0, 4):
            line = ["A", "B", "C", "D"][i] + " | "
            x = 0
            while x<5:
                elem = -1
                if (x, y) in self.revealed:
                    elem = self.board[y][x]
                if elem == -1:
                    line += "*" + " "
                else:
                    line += str(elem) + " "
                x += 1
            y += 1
            line += "|"
            print(line)
        print("  |___________|\n\n\n")

    def drawGUI(self):
        ret = None
        # ---- Main Loop for GUI ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Game Interrupted!")
                self.interrupted = True
                ret = 0
        vw, vh = pygame.display.get_surface().get_size()
        mx, my = pygame.mouse.get_pos()
        left, middle, right = pygame.mouse.get_pressed()
        marginTop = 30
        padding = 3
        bw = vw / 5
        bh = (vh - marginTop) / 4
        self.screen.fill((255, 255, 255))
        # Display Score
        self.screen.blit(self.font.render('Score: ' + str(self.score), False, (0, 0, 0)), (10, 0))
        for y in range(4):
            for x in range(5):
                px = int(x * bw + padding)
                py = marginTop + int(y * bh + padding)
                pw = int(bw - padding*2)
                ph = int(bh - padding*2)
                if left and mx >= px and mx <= (px+pw) and my >= py and my <= (py+ph):
                    ret = (x, y)
                pygame.draw.rect(self.screen, (128, 128, 128), [px, py, pw, ph], 0)
                if (x, y) in self.revealed:
                    self.screen.blit(self.font1.render(str(self.board[y][x]), False, (0, 0, 0)), (px + padding, py + padding))


        pygame.display.flip()
        self.clock.tick(60)
        return ret

    def process_input(self):
        alphas = ["A", "B", "C", "D", "a", "b", "c", "d"]
        alpha_dict = {"A": 0, "B": 1, "C": 2, "D": 3, "a": 0, "b": 1, "c": 2, "d": 3}
        nums = ["1", "2", "3", "4", "5"]
        a, b = '', ''
        x, y = 0, 0
        while True:
            if self.mode == 'GUI':
                temp = self.drawGUI()
                if temp == 0:
                    return
                elif temp is None:
                    continue
                else:
                    x, y = temp
                    print("RET: ", temp, self.revealed)
                    if (x, y) not in self.revealed:
                        break
                continue
            a = input("1st set of coordinates: ").replace(" ", "")
#ignore spaces
            at = a.split(",") #ignore ","
            if len(a) < 2:
            #if incomplete data, try again
                print("____Invalid input, try again____"); continue
            elif a[0] in alphas and a[1] in nums:
            #if the format is - [A to D or a to d]<0 or more spaces>[1 to 5]
                y = alpha_dict[a[0]]
                x = int(a[1]) - 1
                if (x, y) in self.revealed:
                    print(a + "   <- already revealed\n____Try Again____"); continue
                break
            elif at[0] in alphas and at[1] in nums:
            #if the format is - [A to D or a to d]","<0 or more spaces>[1 to 5]
                y = alpha_dict[at[0]]
                x = int(at[1]) - 1
                if (x, y) in self.revealed:
                    print(a + "   <- already revealed\n____Try Again____"); continue
                break
            else:
                print("____Invalid input, try again____"); continue
        ax, ay = x, y
        self.revealed.append((ax, ay)) # reveal the coordinate
        self.cls(); self.draw()
# let the user see the revealed area
        while True:
            if self.mode == 'GUI':
                temp = self.drawGUI()
                if temp == 0:
                    return
                elif temp is None:
                    continue
                else:
                    x, y = temp
                    if (x, y) not in self.revealed:
                        break
                continue
            b = input("2nd set of coordinates: ").replace(" ", "")
            bt = a.split(",")
            if len(b) < 2:
                print("____Invalid input, try again____"); continue
            elif b[0] in alphas and b[1] in nums:
                y = alpha_dict[b[0]]
                x = int(b[1]) - 1
                if (x, y) in self.revealed:
                    print(a + "   <- already revealed\n____Try Again____"); continue
                break
            elif bt[0] in alphas and bt[1] in nums:
                y = alpha_dict[bt[0]]
                x = int(bt[1]) - 1
                if (x, y) in self.revealed:
                    print(a + "   <- already revealed\n____Try Again____"); continue
                break
            else:
                print("____Invalid input, try again____"); continue
        bx, by = x, y
        self.revealed.append((bx, by))
# reveal the coordinates
        #let the user see the revealed area for 2 seconds
        self.cls(); self.draw()
        time.sleep(2)
        if self.board[ay][ax] != self.board[by][bx]:
            #if the numbers do not match, remove the last 2 elements of the revealed list and score is decreased by 1
            self.revealed = self.revealed[:-2]
            self.score -= 1
        else:
            #if numbers match, score is increased by 5
            self.score += 5
        self.cls()

    def cls(self):
        print("\n"*25)

    def finish(self):
        if self.mode == 'GUI':
            pygame.quit()
        if self.interrupted:
            print('Game Interrupted!')
            self.cls()
            return
        #note the time when the player finished
        self.ended = timer()
        self.cls()
        print("Score: " + str(self.score))
        #calculate score as score / time elapsed since the player started playing by limiting decimal places
        elapsed = int((self.ended - self.started)/60)
        elapsed_s = (int(self.ended-self.started) % 60)/10
        elapsed += (elapsed_s)/10.0
        print("Time taken: " + str(elapsed) + "m")
        print("Final Score = " + str(self.score) + " / " + str(elapsed))
        self.score = int(self.score / elapsed)
        print("            = "+ str(self.score))
        print("\n\n\n        Score: "+str(self.score)+"        ")
        if self.scoreboard.check(self.score):
            #if this score is higher than the lowest score in top 10 list, add this to the list and remove the lowest one
            name = input("Your name: ")
            self.scoreboard.add(name, self.score)
            print("Your name has been added to the scoreboard!")
        else:
            print("Your score is too less to appear on the Score Board!")
            print("Play better next time!")
        time.sleep(2)
# wait 2 seconds
        self.cls()
    def finished(self):
        if self.interrupted:
            return True
        #if all the 10 pairs are revealed return true, otherwise false
        return len(self.revealed) == 20


sb = ScoreBoard()
while True:
    sb.cls()
    print("1. Start game")
    print("2. Display Top 10 Scores")
    print("3. Delete Top 10 Scores")
    print("4. Exit\n\n")
    a = input("Enter Choice: ")
    i = 0
    try:
        i = int(a)
    except ValueError:
        print("\n\n____Invalid input, try gain____"); continue
    if i not in (1, 2, 3, 4):
        print("\n\n____Invalid input, try again____"); continue
    if i == 1:
        grid = Grid(sb)
        while not grid.finished():
#loop until all 10 pairs are revealed
            grid.cls()
#clear the screen
            grid.draw()
#draw the board
            grid.process_input()
#take input
        grid.finish()
#show score when the 10 pairs are revealed
    elif i == 2:
        sb.check(0)
# retrieve data from file
        sb.draw()
# draw the data
        input("\n\nPress any key to Continue...")
#discard input
    elif i == 3:
        print("Deleting Top 10 scores...")
        sb.create_new()
#delete all existing data and create an empty one
        sb.check(0)
# retrieve the empty data from file
    elif i == 4:
        print("Thank you and see you next time")
        break
