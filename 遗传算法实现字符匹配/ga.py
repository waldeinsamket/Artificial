# coding=utf-8
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import random

best = [72, 111, 119, 32, 97, 114, 101, 32, 121, 111, 117, 44, 50, 48, 49, 55, 50, 49, 49, 50, 51, 48, 48, 53]
# 目标序列How are you，201721123005      --24

def get_ran(b=32, e=126):
   # 获取随机字符值，默认从可显示字符开始（33-126）
    return random.randint(b, e)

def get_pos(cou=23):
    #获取随机位置，默认到24
    return random.randint(0, cou)

class Chromosome:
    #染色体类
    def __init__(self, dna=None):
        #初始化，可指定DNA序列顺序，默认DNA为随机序列。
        if dna is not None:
            self.dna = dna[:]
        else:
            self.dna = []
            for i in range(24):#0-23
                self.dna.append(get_ran())

    def to_asc(self):
        #将DNA序列由int转为str
        str = ''
        for chrx in self.dna:
            str = str + chr(chrx)
        return str

    def __str__(self):
        #将DNA序列由int转为str
        str = ''
        for chrx in self.dna:
            str = str + chr(chrx)
        return str

    def mutation(self, which=-1):
        #变异操作，默认产生随机个变异位点，突变为随机值，可指定突变位置
        if which == -1:
            i = get_pos()
            for x in range(i):
                self.dna[get_pos()] = get_ran()
        else:
            self.dna[which] = get_pos()

    def comp(self, other):
        #计算与指定序列DNA的平方差
        l = []
        val = 0
        for x in range(24):
            d = self.dna[x] - other.dna[x]
            d = pow(d, 2)
            l.append(d)  #每位值的平方差
            val = val + d  #累计平方差
        return l, val

    def cross(self, other):
        #该染色体与其他染色体基因重组，产生新染色体，采用多点交叉
        new = []
        for i in range(24):
            if get_pos(1) == 0:  #随机取一个值，为零时i位上取self，不为零取other
                new.append(self.dna[i])
            else:
                new.append(other.dna[i])
        return Chromosome(new)


class Population:
    #种群类
    def __init__(self, much=1000,aim=[72, 111, 119, 32, 97, 114, 101, 32, 121, 111, 117, 44, 50, 48, 49, 55, 50, 49, 49, 50, 51, 48, 48, 53]):
        #初始化种群，默认种群数量   指定序列为How are you，201721123005
        self.group = []
        self.best = Chromosome(aim)
        i = 0
        while i < much:
            self.group.append(Chromosome()) #初始化种群，加入染色体
            i = i + 1

    def choice(self, p=0.05):
        #选择操作，采用锦标赛选择方法，默认保留0.05，与累计平方差最相近的
        group = []
        old = self.group
        count = int(self.group.__len__() * p) #1000*0.05=50
        once = int(self.group.__len__() / count) #1000/50=20
        t_b = old[0]
        t = 0
        for ch in old:
            if t == once: #每once倍取一个染色体作为样本t_b
                group.append(t_b) #每个once里面最佳样本收入
                t_b = ch
                t = 0
            v1 = t_b.comp(self.best)#当前样本，将其与目标比较
            v2 = ch.comp(self.best)#遍历染色体，将其与目标比较
            if v1 >= v2: #取累计平方差小的，再更新样本
                t_b = ch
            t = t + 1
        self.group.clear()
        self.group = group[:]

    def cross(self, p=0.7):
        #交叉操作，采用多点交叉
        count = int(self.group.__len__() * p) #20*0.7=14
        i = 0
        group = []
        while i < count:
            t = self.group.__len__()  #20
            group.append(self.group[get_pos(t - 1)].cross(self.group[get_pos(t - 1)])) #重组，选择group中任意一个染色体进行重组
            i = i + 1
        self.group = self.group + group

    def mutation(self, p=0.001):
        #种群突变
        count = int(self.group.__len__() * p)
        i = 0
        t = self.group.__len__()
        while i < count:
            self.group[get_pos(t - 1)].mutation() #基因突变
            i = i + 1

    def have_the_best(self):
        #判断是否存在目标序列
        for ch in self.group:
            v = ch.comp(self.best)#比较最佳序列中是否存在目标
            if v == 0:
                return True
        return False

    def value(self):
        #计算该种群的估值
        val = 0
        for ch in self.group:
            _, v = ch.comp(self.best)
            val = val + v
        return val / self.group.__len__()

    def get_best(self):
        """
        获取种群最优个体
        """
        best_one = self.group[0]
        _, val = best_one.comp(self.best)
        for ch in self.group:
            _, v = ch.comp(self.best)
            if val >= v:
                best_one = ch
                val = v
        return best_one

    def big_up(self):
        self.choice(0.9)
        self.cross(1.5)
        self.mutation(0.01)

    def big_down(self):
        self.choice()
        self.cross()
        self.mutation()


def main():
    """
    主函数
    """
    ch_b = Chromosome(best)
    po = Population(5000)
    i = 1
    vals = []
    popu = []
    while i <= 500:
        val = po.value()
        leng = po.group.__len__()
        str1 = '第 {:^4} 代: 数量为 {:^6},  估值 :{:^6}'.format(i, leng, int(val))
        str2 = ' -- 最佳 : {}'.format(po.get_best().to_asc())
        if po.group.__len__() < 500:
            # 种群个体少于500，需要补充大量新个体以免灭亡
            p1 = 0.8
            p2 = 1
            p3 = 0.12
        elif po.group.__len__() < 2500:
            p1 = 0.6
            p2 = 0.99
            p3 = 0.1
        elif po.group.__len__() < 5000:
            p1 = 0.5
            p2 = 0.9
            p3 = 0.09
        elif po.group.__len__() < 8000:
            p1 = 0.3
            p2 = 0.82
            p3 = 0.08
        elif po.group.__len__() < 10000:
            p1 = 0.2
            p2 = 0.78
            p3 = 0.05
        else:
            # 默认操作
            p1 = 0.05
            p2 = 0.7
            p3 = 0.001

        # #但估值趋于稳定时，刺激种群
        # if val < 1000 :
        #     p1 = p1 - 0.5
        #     if p1 <= 0 :
        #         p1 = 0.05
        #     p2 = p2 + 0.3
        #     p3 = p3 + 0.05

        # 模拟突增突降，可选
        # if get_pos(100) < 5 :
        #     po.big_down()
        #     print('big-down')
        # if get_pos(100) > 95 :
        #     po.big_up()
        #     print('big-up')

        print(str1 + str2)
        # print(str2)
        po.choice(p1)
        if po.have_the_best():
            print('找到目标！')
            print(ch_b.to_asc())
            break
        po.cross(p2)
        po.mutation(p3)
        vals.append(val)
        popu.append(leng)
        i = i + 1

    # 绘图
    plt.figure(1)
    plt.subplot(121)
    x = range(i - 1)
    y = vals[:]
    plt.plot(x, y)
    plt.subplot(122)
    y = popu[:]
    plt.plot(x, y)
    plt.show()


if __name__ == "__main__":
    """
    """
    main()
    input()