from random import randint


class Map(): #初始化地图
    def __init__(self, width, height): #初始化地图
        self.width = width
        self.height = height
        self.map = [[0 for x in range(self.width)] for y in range(self.height)] #列表解析 0表示可通过的节点

    def createBlock(self, block_num): #创建不能通过的节点（用1表示）
        for i in range(block_num):
            x, y = (randint(0, self.width - 1), randint(0, self.height - 1))
            self.map[y][x] = 1

    def generatePos(self, rangeX, rangeY): #随机获取一个可移动的节点
        x, y = (randint(rangeX[0], rangeX[1]), randint(rangeY[0], rangeY[1]))
        while self.map[y][x] == 1:  #该节点不通时重新获取
            x, y = (randint(rangeX[0], rangeX[1]), randint(rangeY[0], rangeY[1]))
        return (x, y)

    def showMap(self):#显示地图函数
        print("#" * (3*self.width + 2)) #头

        for row in self.map:
            s = '#'
            for entry in row:          # \033[41m
                s += ' ' + str(entry) + ' '
            s += '#'
            print(s)
        print("#" * (3 * self.width + 2)) #尾


WIDTH = 11
HEIGHT = 11
BLOCK_NUM = 35
map = Map(WIDTH, HEIGHT)
map.createBlock(BLOCK_NUM)
map.showMap()   #创建的迷宫地图

source = map.generatePos((0, 2), (0, 2)) #在范围内随机获取入口与出口
dest = map.generatePos((9, 10), (9, 10))
print("迷宫入口坐标", source)
print("迷宫出口坐标", dest)
