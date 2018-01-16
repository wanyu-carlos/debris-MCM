import random
import math
import csv
import pickle

def generate():
    x = random.uniform(-1,1)
    y = random.uniform(-1,1)
    z = random.uniform(-1,1)
    radius = float(math.sqrt(math.pow(x,2)+math.pow(y,2)+math.pow(z,2)))
    new_x = x/radius
    new_y = y/radius
    new_z = z/radius
    point = [new_x, new_y, new_z]
    return point

class Node(object):
    def __init__(self,coor):
        self.coor = coor
        self.content = []

    def zerorize(self):
        self.content.clear()

    def check_collision(self): ##
        res = []
        if len(self.content) >= 2:
            children_number = len(self.content)*2 ## assumption 1
            for debris in self.content:
                res.append(debris)
            self.zerorize()
        return res

    def add(self,debris):
        self.content.append(debris)

class Grid(object):

    def __init__(self,decimal):
        self.grid = {}
        self.decimal = decimal

    def create_nodes(self):
        number = 10**self.decimal

        for i in range(-number,number+1):
            for k in range (-number,number+1):
                for q in range (-number,number+1):
                    new_point = [i/number,k/number,q/number]
                    new_node = Node(new_point)
                    self.grid[str(new_point)]= new_node
        return self.grid

    def check_collisions(self):
        final_res = [val for node in self.grid.values() for val in node.check_collision()]
        return final_res

class Simulation(object):
    # initialization
    def __init__ (self, velocity,grid,decimal):
        self.speed = velocity
        self.debris = {}
        self.grid = grid
        self.decimal =decimal
        self.counter = 0

    def begin(self,number):
        for i in range(0,number):
            point = generate()
            new_debris = Debris(self.speed,point,self.decimal,self.counter)
            self.debris[str(self.counter)] = new_debris
            self.counter+=1

    def move(self):
        for db in self.debris.values():
            db.move()
            self.match_to_grid(db)




    def match_to_grid(self,debris): ##
        coor = debris.get_coor()
        coor = [x+0 for x in coor]

        self.grid.grid[str(coor)].add(debris)

    def collide(self):
        removed = []
        removed = self.grid.check_collisions()
        for db in removed:
            print (db.id)
        for db in removed:
            coor= db.coor
            self.debris.pop(db.id)
            for i in range(0,2): #assumption 1
                new_debris = Debris(self.speed,coor,self.decimal,self.counter)
                self.debris[str(self.counter)]=new_debris
                self.counter+=1
                self.match_to_grid(new_debris)





    def getcount(self):
        return len(self.debris)

class Debris(object):
    def __init__ (self,velocity,coordinate,decimal,counter):
        self.decimal = decimal
        self.coor = coordinate
        x_0 = self.coor[0]
        y_0 = self.coor[1]
        z_0 = self.coor[2]
        self.id = str(counter)

        #velocity is unchanged until collision

        radius = math.sqrt(math.pow(x_0, 2)+math.pow(y_0, 2)+math.pow(z_0, 2))
        self.x = x_0/radius
        self.y = y_0/radius
        self.z = z_0/radius

        self.theta = math.atan(self.y/self.x)
        self.phi = math.acos(self.z)
        self.polar = [self.theta,self.phi]

        #speed is uniform
        self.vel = velocity

        #velocity is unchanged until collision
        self.local_delta1 = random.uniform(-1,1) #theta
        self.local_delta2 = random.uniform(-1,1)
        self.norm = math.sqrt(self.local_delta1**2+self.local_delta2**2)



    def move(self):
        self.theta += (self.vel/self.norm) * self.local_delta1/(math.sin(self.phi))
        self.phi += (self.vel/self.norm) * (self.local_delta2)

        #delta_x = (-1) *math.sin(self.theta) * math.sin(self.phi) * delta_theta + math.cos(self.theta) * math.cos(self.phi) * delta_phi
        #delta_y = math.cos(self.theta) * math.sin(self.phi) * delta_theta + math.sin(self.theta) * math.cos(self.phi) * delta_phi
        #delta_z = (-1) *math.sin(self.phi) * delta_phi


        #self.x += delta_x
        #self.y += delta_y
        #self.z += delta_z

        self.x = math.cos(self.theta)*math.sin(self.phi)
        self.y = math.cos(self.theta)*math.cos(self.phi)
        self.z = math.cos(self.phi)
        self.coor = [self.x, self.y,self.z]

    def get_coor(self):
        return [round(self.x,self.decimal),round(self.y,self.decimal),round(self.z,self.decimal)]




#Data input
decimal=1
iteration = 150
velocity= 0.4 # grid per time
SampleGrid = Grid(decimal)
SampleGrid.create_nodes()

Test = Simulation(velocity,SampleGrid,decimal)

#initialze

res=[]
Test.begin(10)

polar = []
    #start simulation
for t in range(0,iteration):
    Test.move()
    Test.collide()
    res.append(Test.getcount())

    snapshot = []
    for debris in Test.debris.values():
        snapshot.append(debris.polar)
    with open('polar{}.csv'.format(t), 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerows(snapshot)

    polar.append(snapshot)
print (polar)
print (res)



#
# #write data
# with open('polar{i}.csv'.format(t), 'w') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=',')
#     spamwriter.writerows(polar)
#     spamwriter.writecols()

