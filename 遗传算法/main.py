import random
import pandas as pd
import visualize

#全局变量定义
population_number = 40 #初始种群数量
iter_times = 1 #遗传代数
machine_number = 6 #机器数量
job_number = 8 #工件数量
process_number = 4 #工序数量
mutation_prob = 0.05 #变异概率


'''
初始化种群
'''
def initPopulation(data_set: list[list[int]]) -> list[list[int]]:
    init_pl = [] #初始种群
    for i in range(population_number):
        size = job_number * process_number #染色体长度
        chromosome = [-1 for _ in range(size)]
        index_list = list(range(size))
        for j in range(job_number):
            for k in range(machine_number):
                if k in data_set[j][::2]: #第j个工件在第k台机器上有待加工
                    k_t = data_set[j][::2].count(k) #第j个工件在第k台机器上的加工次数，该工件存在多道工序在同一台机器上
                    for _ in range(k_t):
                        index = random.randrange(len(index_list))
                        val = index_list.pop(index)
                        chromosome[val] = j
        # print(chromosome)
        init_pl.append(chromosome)
    return init_pl


'''
计算个体适应度
'''
def calculateFitness(chromosome: list[int], data_set: list[list[int]]):
    fit_ness = 1 #适应度=1/总时长
    gantt_data = {i:[] for i in range(job_number)} # {i:[[x,t1,t2], [..]..], ....}甘特图数据， 第i个工件从t1-t2时间段在第x台机器上加工
    sum_time = [0 for _ in range(machine_number)] #每台机器的总时长
    process_index = {} #染色体上每个工件的出现次数(到工件i的第几道工序了)
    start_time = [0 for _ in range(job_number)] #记录每个工件当前工序的开始时间和结束时间
    end_time = [0 for _ in range(job_number)]
    for i in chromosome:
        if i not in process_index.keys():
            process_index[i] = 0
        process_index[i] += 1
        t = data_set[i][2 * process_index[i]-1] #当前工序需要的时间
        cur_machine = data_set[i][::2][process_index[i]-1] #当前工作的机器序号
        start_time[i] = sum_time[cur_machine] if process_index[i] == 1 else max(end_time[i], sum_time[cur_machine])
        end_time[i] = start_time[i] + t
        gantt_data[i].append([cur_machine, start_time[i], end_time[i]]) #[机器序号，开始时间，结束时间]
        sum_time[cur_machine] = start_time[i] + t
    # print(process_index)
    # print(sum_time)
    fit_ness = 1 / max(sum_time) #适应度=1/最大时间
    return fit_ness, gantt_data


'''
交叉产生新个体
'''
def geneCross(chromosome1: list[int], chromosome2: list[int]) -> list: #返回一对孩子
    def geneGenetate(father: list[int], mother: list[int]):
        index_list = list(range(len(father)))
        p1 = index_list.pop(random.randrange(len(index_list)))
        p2 = index_list.pop(random.randrange(len(index_list)))
        start = min(p1, p2)
        end = max(p1, p2)
        # print(start, end)
        prototype = father[start:end+1] #随机选取父亲的一段染色体作为孩子的染色体原型
        mother1 = mother[:] #复制一份，后面pop会破坏源列表
        for v1 in prototype:
            for i in range(len(father)):
                if v1 == mother1[i]:
                    mother1.pop(i)
                    break
        child = mother1[:start] + prototype + mother1[start:]
        return child
    return [geneGenetate(chromosome1, chromosome2), geneGenetate(chromosome2, chromosome1)]


'''
染色体变异
'''
def geneMutation(chromosome: list[int]):
    index_list = [i for i in range(len(chromosome))]
    for i in range(2): # 产生两个交换突变
        a = index_list.pop(random.randrange(len(index_list)))
        b = index_list.pop(random.randrange(len(index_list)))
        chromosome[a], chromosome[b] = chromosome[b], chromosome[a]


'''
选择个体
'''
def selectIndividual(population: list[list[int]], data_set: list[list[int]]) -> list[int]:
    index_list = [i for i in range(len(population))]
    chosen = [] #抽取的个体下标
    for _ in range(int(population_number/10)): #随机抽取1/10个个体
        chosen.append(index_list.pop(random.randrange(len(index_list))))
    best_chomosome = population[chosen[0]]
    best_fitness, _ = calculateFitness(best_chomosome, data_set)
    for i in chosen[1:]: #选出1/10个当中适应度最好的
        fitness , _ = calculateFitness(population[i], data_set)
        if fitness > best_fitness:
            best_chomosome = population[i]
    population.pop(population.index(best_chomosome))
    return best_chomosome


'''
我的遗传算法
'''
def myGa(population, data_set, iter_times):
    for _ in range(iter_times): #迭代次数
        next_generation = [] #下一代种群
        for _ in range(int(population_number/2)):
            next_generation.append(selectIndividual(population, data_set)) #用竞争法选出较优的一半作为下一代种群的一部分以及父母
        for i in range(int(len(next_generation)/2)):
            children = geneCross(population[2*i], population[2*i+1]) #配对交叉产生新的一半个体
            next_generation += children
        population = next_generation
        prob = random.randrange(1, 101) / 100 #对所有个体进行概率变异
        if prob < mutation_prob:
            index = random.randrange(len(population))
            geneMutation(population[index])
    # print(len(population))
    bset_chromosome = population[0]
    best_fitness , _ = calculateFitness(bset_chromosome, data_set)
    for chomosome in population: #迭代结束后选出最终种群中适应度最好的个体作为最优解
        fitness, _ = calculateFitness(chomosome, data_set)
        if fitness > best_fitness:
            bset_chromosome = chomosome
    fitness, gantt_data = calculateFitness(bset_chromosome, data_set)
    print(bset_chromosome)
    print(fitness)
    # print(gantt_data)
    # {0: [[5, 0, 2], [5, 2, 9], [3, 13, 22], [3, 22, 31]],
    #  1: [[3, 6, 10], [3, 10, 11], [2, 11, 12], [4, 22, 25]],
    #  2: [[2, 2, 6], [5, 9, 10], [4, 18, 22], [3, 31, 33]],
    #  3: [[3, 0, 1], [1, 1, 2], [2, 7, 10], [4, 14, 18]],
    #  4: [[0, 0, 5], [3, 5, 6], [5, 10, 15], [0, 15, 19]],
    #  5: [[4, 0, 2], [4, 2, 4], [5, 15, 20], [2, 20, 25]],
    #  6: [[2, 0, 2], [2, 25, 28], [2, 28, 30], [5, 30, 34]],
    #  7: [[2, 6, 7], [0, 7, 10], [3, 11, 13], [4, 13, 14]]}
    visualize.plot_gantt(gantt_data) #画甘特图



if __name__ == '__main__':
    # 读文件数据
    df = pd.read_excel('作业调度案例2.xlsx', sheet_name='Sheet2')
    data_set = df.iloc[1:, 1:].to_numpy().tolist()
    # print(data_set)
    #[[5, 2, 5, 7, 3, 9, 3, 9],
    # [3, 4, 3, 1, 2, 1, 4, 3],
    # [2, 4, 5, 1, 4, 4, 3, 2],
    # [3, 1, 1, 1, 2, 3, 4, 4],
    # [0, 5, 3, 1, 5, 5, 0, 4],
    # [4, 2, 4, 2, 5, 5, 2, 5],
    # [2, 2, 2, 3, 2, 2, 5, 4],
    # [2, 1, 0, 3, 3, 2, 4, 1]]
    population = initPopulation(data_set) #初始化种群
    myGa(population, data_set, iter_times)
