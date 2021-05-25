from random import random,choices

def Generate_Hexagon(a: int, p_node: float = 0.1, p_edge: float = 0.1):
    """
    a代表六边形的边长（一条边上的节点数）
    p_node代表一个节点被删除的概率
    p_edge代表一条边被删除的概率
    """
    result = Generate_Hexagon_Try(a,p_node,p_edge)
    while result==-1:
        result = Generate_Hexagon_Try(a,p_node,p_edge)
    return result

def Generate_Hexagon_Try(a: int, p_node: float = 0.1, p_edge: float = 0.1):
    """
    a代表六边形的边长（一条边上的节点数）
    p_node代表一个节点被删除的概率
    p_edge代表一条边被删除的概率
    """
    N_max = (3*a-2)*(a-1)+(2*a-1)
    l = 2/(a-1) # 可视化的边长
    #print("N_max ==",N_max)#
    design = {}
    xy = {}
    p_edge = p_edge**0.5 # 因为一条边连续两次被选中才会被删除

    cnt = 0
    N = 0 # 总节点数
    for i in range(a):
        for j in range(a+i):
            if (i,j) == (a-1,a):
                break
            if random()<p_node and cnt!=0:
                continue
            else:
                cnt += 1
                N += 2 if (i,j)!=(a-1,a-1) else 1
                design[cnt] = {}
                xy[cnt] = ( (-a+i+1) *l, ((a-1+i)/2-j) *l )
    
    #print("N ==",N)#
    #print("cnt ==",cnt)#
    
    for i in range(1,N//2+1): # 中心对称建节点
        design[N+1-i] = {}
        xy[N+1-i] = (-xy[i][0], -xy[i][1])
    
    #print(design)
    #print(xy)

    for i in range(1, (N+1)//2+1):
        for j in range(1, N+1):
            if i==j:
                continue
            if (xy[i][0]-xy[j][0])**2+(xy[i][1]-xy[j][1])**2 < 1*l: # 在图上是相邻节点
                if random()>=p_edge:
                    design[i][j] = 0 # 这里0是过路费，之后可以改，都可以改！
                    design[j][i] = 0
                    design[N+1-i][N+1-j] = 0 # 中心对称
                    design[N+1-j][N+1-i] = 0
            
    
    # dfs 判断连通性
    visited = [False for i in range(N+1)]
    def dfs(x: int):
        if visited[x]:
            return
        visited[x] = True
        for y in design[x]:
            dfs(y)
    dfs(1)
    for i in range(1,N+1):
        if visited[i]==False:
            #print("Oh shit. This map is not connected. \nRegenerating. ")
            return -1 # 生成失败
    for i in range(1,N+1):
        if len(design[i])<2: # 陈老师说，每个节点至少2度
            #print("Oh no, one of the nodes has only one edge. \nRegenerating. ")
            return -1 # 生成失败



    map_info = {"design": design, "xy": xy}
    #print(map_info)
    return map_info
