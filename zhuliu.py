class Edge:
    def __init__(self,u,v,w):
        self.u = u
        self.v = v
        self.w = w

def zhuliusf(edges,n,m,root):
    while True:
        pre = [-1] * n
        inin = [float(inf)] * n

    #找出最小入弧,对每一条弧的头
        inin[root] = 0
        for i in range(m):
            if edges[i].u != edges[i].v and edges[i].w < inin[edges[i].v]:
                pre[edges[i].v] = edges[i].u  #例如点2从点1来
                inin[edges[i].v] = edges[i].w  #将弧的权重记录在一个列表中它的头位置

    #不存在最小树形图的情况
        for i in range(n):
            if i != root and inin[i] == float(inf):
                return None

    #找其中的圈
        quan = 0
        circle = [-1] * n
        visited = [-1] * n
        #遍历找圈，从第一个点开始向前遍历
        for i in range(n):
            v = i
            while visited[v] != i and circle[v] == -1 and visited[v] != root:
                visited[v] = i
                v = pre[v]      #不断前推，直到到达根节点，或者是走到已经标记过的点，退出while循环
            if circle[v] == -1 and v != root:    #如果最前面的节点不是根节点，并且也没有被标记过，则将其标记
                while circle[v] != quan:
                    circle[v] = quan
                quan += 1
        #没有圈
        if quan == 0:
            break
        # 给未编号的重新编号
        for i in range(n):
            if circle[i] == -1:
                circle[i] = quan
                quan += 1
        #把圈缩成点
        for i in range(m):
            v = edges[i].v
            edges[i].u = circle[edges[i].u]
            edges[i].v = circle[edges[i].v]
            # 如果边不属于同一个圈
            if edges[i].u != edges[i].v:
                edges[i].w -= inin[v]
        n = quan  #更新节点数量
        root = circle[root]   #更新根节点标号
    return
INF = 999999
if __name__ == '__main__':
    n, m, root = list(map(int, input().split()))
    edges = []
    for i in range(m):
        u, v, w = list(map(int, input().split()))
        edges.append(Edge(u-1, v-1, w))
    print(zhuliu(edges, n, m, root-1),end = "")

    import ts_datasets
