import Maze_Gui
import datetime

from random import randint

class SearchEntry():  #节点类  保存节点的位置信息，计算得到的G值和F值，父节点
    def __init__(self, x, y, g_cost, f_cost=0, pre_entry=None):
        self.x = x
        self.y = y
        # 从起始节点到当前节点的开销
        self.g_cost = g_cost
        self.f_cost = f_cost
        self.pre_entry = pre_entry

    def getPos(self):
        return (self.x, self.y)



def AStarSearch(map, source, dest):  #A*搜索
    def getNewPosition(map, locatioin, offset):  #更新位置，上下左右
        x, y = (location.x + offset[0], location.y + offset[1])
        if x < 0 or x >= map.width or y < 0 or y >= map.height or map.map[y][x] == 1:
            return None
        return (x, y)

    def getPositions(map, location):
        # 四个移动方向
        #offsets = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        #八个移动方向
        offsets = [(-1,0), (0, -1), (1, 0), (0, 1), (-1,-1), (1, -1), (-1, 1), (1, 1)]
        poslist = []
        for offset in offsets:  #可以走的方向（遍历）
            pos = getNewPosition(map, location, offset)
            if pos is not None:  #不能走了
                poslist.append(pos)
        return poslist  #可以走的位置

    #启发式函数 h(x)曼哈顿距离  abs绝对值横纵坐标之差
    def calHeuristic(pos, dest):
        return abs(dest.x - pos[0]) + abs(dest.y - pos[1])
    #移动开销
    def getMoveCost(location, pos):
        if location.x != pos[0] and location.y != pos[1]:
            return 1.4
        else:
            return 1

    # 检查该元素是否在该列表
    def isInList(list, pos):
        if pos in list:
            return list[pos]
        return None

    # 添加可用的相邻位置
    def addAdjacentPositions(map, location, dest, openlist, closedlist):
        poslist = getPositions(map, location)
        for pos in poslist:
            #该位置不在closed表中时
            if isInList(closedlist, pos) is None:
                findEntry = isInList(openlist, pos)
                h_cost = calHeuristic(pos, dest)  #启发函数
                g_cost = location.g_cost + getMoveCost(location, pos)  #估值函数
                if findEntry is None:    # 如果不在open表
                    openlist[pos] = SearchEntry(pos[0], pos[1], g_cost, g_cost + h_cost, location)
                elif findEntry.g_cost > g_cost:  #如果新开销比较小，则更新
                    findEntry.g_cost = g_cost
                    findEntry.f_cost = g_cost + h_cost
                    findEntry.pre_entry = location

    # 从open中取出f值最小的节点
    def getFastPosition(openlist):
        fast = None
        for entry in openlist.values():
            if fast is None:
                fast = entry
            elif fast.f_cost > entry.f_cost:
                fast = entry
        return fast
    count = 0
    openlist = {} #open表
    closedlist = {}  #closed表
    location = SearchEntry(source[0], source[1], 0.0)  #入口坐标
    dest = SearchEntry(dest[0], dest[1], 0.0)  #出口坐标
    openlist[source] = location
    while True:
        location = getFastPosition(openlist)  #从open中取出f值最小的节点
        if location is None:
            # 如果open表为空
            print("找不到通路")
            break;
        if location.x == dest.x and location.y == dest.y:  #如果当前节点为目标节点
            break
        closedlist[location.getPos()] = location   #将该节点添加进closed表
        openlist.pop(location.getPos())   #在open表中删除该节点
        addAdjacentPositions(map, location, dest, openlist, closedlist)  #
    count = closedlist.__len__() + openlist.__len__()+2    #查询过的节点，加上起始节点和终止节点
    print("启发函数取哈夫曼距离   F(n):",count)
    # 将通路标记为2
    while location is not None:
        map.map[location.y][location.x] = 2
        location = location.pre_entry
    map.showMap()  # 2表示通路



def AStarSearch1(map, source, dest):  #A*搜索
    def getNewPosition(map, locatioin, offset):  #更新位置，上下左右
        x, y = (location.x + offset[0], location.y + offset[1])
        if x < 0 or x >= map.width or y < 0 or y >= map.height or map.map[y][x] == 1:
            return None
        return (x, y)

    def getPositions(map, location):
        # 四个移动方向
        #offsets = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        #八个移动方向
        offsets = [(-1,0), (0, -1), (1, 0), (0, 1), (-1,-1), (1, -1), (-1, 1), (1, 1)]
        poslist = []
        for offset in offsets:  #可以走的方向（遍历）
            pos = getNewPosition(map, location, offset)
            if pos is not None:  #不能走了
                poslist.append(pos)
        return poslist  #可以走的位置

    #对角线距离
    def calHeuristic(pos, dest):
        return ((dest.x - pos[0])**2 + (dest.y - pos[1])**2)**0.5
    #移动开销
    def getMoveCost(location, pos):
        if location.x != pos[0] and location.y != pos[1]:
            return 1.4
        else:
            return 1

    # 检查该元素是否在该列表
    def isInList(list, pos):
        if pos in list:
            return list[pos]
        return None

    # 添加可用的相邻位置
    def addAdjacentPositions(map, location, dest, openlist, closedlist):
        poslist = getPositions(map, location)
        for pos in poslist:
            #该位置不在closed表中时
            if isInList(closedlist, pos) is None:
                findEntry = isInList(openlist, pos)
                h_cost = calHeuristic(pos, dest)  #启发函数
                g_cost = location.g_cost + getMoveCost(location, pos)  #估值函数
                if findEntry is None:    # 如果不在open表
                    openlist[pos] = SearchEntry(pos[0], pos[1], g_cost, g_cost + h_cost, location)
                elif findEntry.g_cost > g_cost:  #如果新开销比较小，则更新
                    findEntry.g_cost = g_cost
                    findEntry.f_cost = g_cost + h_cost
                    findEntry.pre_entry = location

    # 从open中取出f值最小的节点
    def getFastPosition(openlist):
        fast = None
        for entry in openlist.values():
            if fast is None:
                fast = entry
            elif fast.f_cost > entry.f_cost:
                fast = entry
        return fast
    count = 0
    openlist = {} #open表
    closedlist = {}  #closed表
    location = SearchEntry(source[0], source[1], 0.0)  #入口坐标
    dest = SearchEntry(dest[0], dest[1], 0.0)  #出口坐标
    openlist[source] = location
    while True:
        location = getFastPosition(openlist)  #从open中取出f值最小的节点
        if location is None:
            # 如果open表为空
            print("找不到通路")
            break;
        if location.x == dest.x and location.y == dest.y:  #如果当前节点为目标节点
            break
        closedlist[location.getPos()] = location   #将该节点添加进closed表
        openlist.pop(location.getPos())   #在open表中删除该节点
        addAdjacentPositions(map, location, dest, openlist, closedlist)  #
    count = closedlist.__len__() + openlist.__len__()+2    #查询过的节点，加上起始节点和终止节点
    print("启发函数取对角线距离  F(n):",count)
    # 将通路标记为2
    while location is not None:
        map.map[location.y][location.x] = 2
        location = location.pre_entry
    map.showMap()  # 2表示通路

source = Maze_Gui.source
dest = Maze_Gui.dest
map = Maze_Gui.map

start = datetime.datetime.now()
AStarSearch(map, source, dest) #A*搜索哈夫曼
end = datetime.datetime.now()
print(end - start)

start = datetime.datetime.now()
AStarSearch1(map, source, dest) #A*搜索对角线
end = datetime.datetime.now()
print(end - start)

