from django.db import connection
from django.http import HttpResponse
from DataPower.models import Stall, Stake, Record, User

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0

def read_map(file_name):
    """
    # read_map usage 

    file_name = '../data/map.dat'
    matrix = read_map(file_name)


    # print map
    for row in matrix:
        print(row)

    """
    with open(file_name, 'r') as f:
        lines = f.readlines()
        park_map = []
        for line in lines:
            row = line.strip().split()
            park_map.append(row)

    return park_map 

class Grid:
    def __init__(self):
        self.map_mat = read_map('./data/map.dat') 
        self.height = len(self.map_mat)
        self.width = len(self.map_mat[0])

    def getSuccessors(self, pos, goal):
        dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        res = []
        for dx, dy in dir:
            new_pos = (pos[0]+dx, pos[1]+dy)
            # check index overflow
            if new_pos[0]<0 or new_pos[1]<0 or new_pos[0]>=self.height or new_pos[1]>=self.width :
                continue
            # check it is road or is goal
            if self.map_mat[new_pos[0]][new_pos[1]] != '0' and new_pos!=goal: 
                continue
            res += [new_pos]

        return res

    def search(self, start, end):
        visited = set()
        fringe = Queue()
        s_node = []
        # add start pos if start is road
        if self.map_mat[start[0]][start[1]] == '0':
            s_node += [start]
        fringe.push((start, s_node))

        while not fringe.isEmpty():
            state, path = fringe.pop()
            #print(state)

            if state == end:
                # pop end pos if end is not road
                if self.map_mat[end[0]][end[1]] != '0':
                    path = path[:-1]
                print(path)
                return path

            if state not in visited:
                visited.add(state)
                for succ in self.getSuccessors(state, end):
                    fringe.push((succ, path + [succ]))

        #print('path ?')
        return []

def reset_primary_key(model):
    table_name = model._meta.db_table
    with connection.cursor() as cursor:
        cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1;")

def get_road():
    map_mat = read_map('./data/map.dat')
    road_coord = []

    for i,_ in enumerate(map_mat): 
        for j,_ in enumerate(map_mat[i]):
            if map_mat[i][j] == '0':
                road_coord.append( (i,j) )

    return road_coord

def init_stall():
    map_mat = read_map('./data/map.dat')
    #print(type(map_mat))
    #print(type(map_mat[0]))
    Stall.objects.all().delete()
    reset_primary_key(Stall)

    sno = 0
    for i,_ in enumerate(map_mat): 
        for j,_ in enumerate(map_mat[i]):
            if map_mat[i][j] == 'P':
                sno += 1
                new_stall = Stall(stake_no=sno, p_row=i, p_col=j, status='free') 
                new_stall.save()

def init_stake():
    map_mat = read_map('./data/map.dat')
    Stake.objects.all().delete()
    reset_primary_key(Stake)

    for i in map_mat: 
        for j in i:
            if j == 'P':
                new_stake = Stake(status='off', start_time=None, finish_time=None) 
                new_stake.save()

def init_record():
    Record.objects.all().delete()
    reset_primary_key(Record)

def init_user():
    User.objects.all().delete()
    reset_primary_key(Record)

grid = Grid()
port = [(2, 0), (2, 23)]
