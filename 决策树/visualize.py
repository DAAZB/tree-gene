from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties

'''
获取决策树叶子结点的数目
'''
def getleavesNum(myTree: dict) -> int:
    leavesNum = 0
    firstStr = next(iter(myTree))
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            leavesNum += getleavesNum(secondDict[key])
        else:
            leavesNum += 1
    return leavesNum


'''
获取决策树层数
'''
def getTreeDepth(myTree: dict) -> int:
    maxDepth = 0
    firstStr = next(iter(myTree))
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        thisDepth = 1
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth += 1
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    return maxDepth


'''
绘制决策树
'''
def plotTree(tree, parentPt, nodeTxt):
    decisionNode = dict(boxstyle = 'roundtooth', fc = 'white') #设置结点格式
    leafNode = dict(boxstyle = 'round4', fc = 'white') #设置叶子节点格式
    leavesNum = getleavesNum(tree)
    depth = getTreeDepth(tree)
    firstStr = next(iter(tree))
    centerPt = (plotTree.xOff + (1.0 + leavesNum) / 2 / plotTree.totalW, plotTree.yOff)
    plotMidText(centerPt, parentPt, nodeTxt) #标注有向边属性值
    plotNode(firstStr, centerPt, parentPt, decisionNode) #绘制结点
    secondDict = tree[firstStr] #下一个字典，也就是继续绘制子结点
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD #y偏移
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict': #测试该结点是否为字典，如果不是字典，代表此结点为叶子结点
            plotTree(secondDict[key],centerPt,str(key)) #不是叶结点，递归调用继续绘制
        else: #如果是叶结点，绘制叶结点，并标注有向边属性值
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), centerPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), centerPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD


'''
创建绘制面板
'''
def createPlot(tree):
    fig = plt.figure(1, facecolor= 'white')
    fig. clf()
    axprops = dict (xticks = [], yticks = [])
    createPlot.ax1 = plt.subplot(111, frameon = False, **axprops)
    plotTree.totalW = float(getleavesNum(tree)) #获取决策树叶结点数目
    plotTree.totalD = float(getTreeDepth(tree)) #获取决策树层数
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0 #x偏移
    plotTree(tree, (0.5,1.0), '') #绘制决策树
    plt.show() #显示绘制结果


'''
绘制结点
'''
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    arrow_args = dict(arrowstyle = '<-')
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
    createPlot.ax1.annotate(nodeTxt, xy=parentPt,  xycoords='axes fraction',    #绘制结点
        xytext=centerPt, textcoords='axes fraction',
        va="center", ha="center", bbox=nodeType, arrowprops=arrow_args, fontproperties=font)


'''
标注有向边属性的值
'''
def plotMidText(centerPt, parentPt, txtString):
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
    xMid = (parentPt[0]-centerPt[0])/2.0 + centerPt[0] #计算标注位置
    yMid = (parentPt[1]-centerPt[1])/2.0 + centerPt[1]
    createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30, fontproperties = font)