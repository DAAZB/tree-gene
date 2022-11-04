from copy import copy
import pandas as pd
from math import log
import operator

import visualize



'''
创建数据集
'''
def createDataSet():
    df = pd.read_excel('训练集.xlsx')
    labels = df.columns.to_list()[:-1] #特征标签
    data_set = df.to_numpy().tolist() #特征向量列表
    return data_set, labels


'''
计算经验熵
'''
def calcShannonEnt(data_set: list[list]) -> float:
    #训练数据集的行数
    n = len(data_set)
    #存放分类种类及其个数
    label_count = {}
    #统计各分类出现的频次
    for data in data_set:
        temp_label = data[-1]
        if temp_label not in label_count.keys():
            label_count[temp_label] = 0
        label_count[temp_label] += 1
    #计算经验熵
    shannon_ent = 0.0
    for key in label_count:
        prob = label_count[key] / n
        shannon_ent -= prob*log(prob, 2)
    return shannon_ent


'''
计算每个特征的增益，给出选择
'''
def chooseBestFeatureToSplit(data_set: list[list]) -> int:
    best_feature = -1 #最优特征索引
    base_entropy = calcShannonEnt(data_set) #数据集经验熵
    best_info_gain = 0.0 #信息增益
    feat_num = len(data_set[0])-1 #特征数量
    #遍历特征
    for i in range(feat_num):
        feat_list = [example[i] for example in data_set]
        unique_vals = set(feat_list)
        new_entropy = 0.0
        for value in unique_vals:
            sub_data_set = splitDataSet(data_set, i, value)
            prob = len(sub_data_set) / len(data_set)
            new_entropy += prob * calcShannonEnt(sub_data_set)
        info_gain = base_entropy - new_entropy
        # print('第{0}个特征的增益为{1}'.format(i , info_gain))
        if(info_gain > best_info_gain):
            best_info_gain = info_gain
            best_feature = i
    return best_feature


'''
按照给定特征划分数据集
'''
def splitDataSet(data_set: list[list], axis: int, value: int) -> list[list]:
    ret_data_set = []
    for feat_vec in data_set:
        if feat_vec[axis] ==value:
            reduced_feat_vec = feat_vec[:axis]
            reduced_feat_vec.extend(feat_vec[axis+1:]) #除去当前特征值
            ret_data_set.append(reduced_feat_vec)
    return ret_data_set #返回剩下的特征向量


'''
返回出现次数最多的元素
'''
def majorityCnt(class_list: list) -> any:
    class_count = {}
    for vote in class_list:
        if vote not in class_count.keys():
            class_count[vote] = 0
        class_count[vote] += 1
    sorted_class_count = sorted(class_count.items(), key = operator.itemgetter(1), reverse=True) #统计每个元素出现的次数并按降序排序
    return sorted_class_count[0][0] #返回出现次数最多的元素


'''
创建决策树
'''
def createTree(data_set:list[list], labels:list, feat_labels:list) ->dict:
    class_list = [example[-1] for example in data_set] #取分类标签
    # 退出条件
    if class_list.count(class_list[0]) == len(class_list): #只有一类，停止划分
        return class_list[0]
    if len(data_set[0]) == 1: #遍历完所有特征则返回出现次数最多的类标签
        return majorityCnt(class_list)

    best_feat = chooseBestFeatureToSplit(data_set) #选取最优特征（）
    best_feat_label = labels[best_feat] #最优特征的标签
    feat_labels.append(best_feat_label) #存储最优特征

    my_tree = {best_feat_label:{}} #根据最优特征生成树
    del(labels[best_feat]) #删除已使用的标签
    featValues = [example[best_feat] for example in data_set]
    unique_vals = set(featValues)
    for value in unique_vals: #遍历最优特征的属性值，生成子树
        labels2 = copy(labels) #复制标签，防止递归时删除标签对该层其他分支产生影响
        my_tree[best_feat_label][value] = createTree(splitDataSet(data_set, best_feat, value), labels2, feat_labels)
    return my_tree


'''
用决策树分类
'''
def classify(inputTree, feat_labels, test_vec):
    #获取决策树节点
    first_str = next(iter(inputTree))
    #下一个字典
    second_dict = inputTree[first_str]
    feat_index = feat_labels.index(first_str)
    class_label = ''

    for key in second_dict.keys():
        if test_vec[feat_index] == key:
            if type(second_dict[key]).__name__ == 'dict':
                class_label = classify(second_dict[key],feat_labels,test_vec)
            else: class_label=second_dict[key]
    return class_label


if __name__=='__main__':
    data_set,labels=createDataSet()
    # print(data_set)
    # print(labels)
    feat_labels = []
    my_tree = createTree(data_set, labels, feat_labels)
    # print(my_tree) #打印决策树
    # print(feat_labels)
    visualize.createPlot(my_tree) #可视化决策树


    # 测试数据
    tdf = pd.read_excel('测试集.xlsx', usecols = feat_labels) #只读决策树判断需要的特征值
    # print(tdf)
    tdf = tdf[feat_labels] #按决策树判断顺序重新排列特征向量
    # print(tdf)
    t_data_set = tdf.to_numpy().tolist() #转化为列表
    # print(t_data_set)
    for vec in t_data_set:
        result = classify(my_tree, feat_labels, vec)
        if result=='是':
            print('好瓜')
        if result=='否':
            print('坏瓜')