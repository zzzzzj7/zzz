class Edge:
    def __init__(self,u,v,w):
        self.u = u
        self.v = v
        self.w = w

def zhuliusf(edges,n,m,root):
    while True:
        pre = [-1] * n
        inin = [float('inf')] * n

    #找出最小入弧,对每一条弧的头
        inin[root] = 0
        for i in range(m):
            if edges[i].u != edges[i].v and edges[i].w < inin[edges[i].v]:
                pre[edges[i].v] = edges[i].u  #例如点2从点1来
                inin[edges[i].v] = edges[i].w  #将弧的权重记录在一个列表中它的头位置

    #不存在最小树形图的情况
        for i in range(n):
            if i != root and inin[i] == float('inf'):
                return None

    #找其中的圈
        quan = 0
        circle = [-1] * n
        visited = [-1] * n
        #遍历找圈，从第一个点开始向前遍历
        for i in range(n):
            v = i
            while visited[v] != i and circle[v] == -1 and visited[v] != root:  #形成一个圈，碰到一个圈，或是到达根节点
                visited[v] = i
                v = pre[v]      #不断前推，直到到达根节点，或者是走到已经标记过的点，退出while循环
            if circle[v] == -1 and v != root:    #如果最前面的节点不是根节点，并且也没有被标记过，也就是新形成了一个环，则将其标记
                while circle[v] != quan:
                    circle[v] = quan
                    #v = pre[v]
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


def msa(V, E, r, w):
    """
    Recursive Edmond's algorithm as per Wikipedia's explanation
    Returns a set of all the edges of the minimum spanning arborescence.
    V := set( Vertex(v) )
    E := set( Edge(u,v) )
    r := Root(v)
    w := dict( Edge(u,v) : cost)
    """

    """
    Step 1 : Removing all edges that lead back to the root
    """
    for (u, v) in E.copy():
        if v == r:
            E.remove((u, v))
            w.pop((u, v))

    """
    Step 2 : Finding the minimum incoming edge for every vertex. O(n**2) but okay since it is
    a small sized list
    """
    pi = dict()
    for v in V:
        edges = [edge[0] for edge in E if edge[1] == v]
        if not len(edges):
            continue
        costs = [w[(u, v)] for u in edges]
        pi[v] = edges[costs.index(min(costs))]

    """
    Step 3 : Finding cycles in the graph
    """
    cycle_vertex = None
    for v in V:
        if cycle_vertex is not None:
            break
        visited = set()
        next_v = pi.get(v)
        while next_v:
            if next_v in visited:
                cycle_vertex = next_v
                break
            visited.add(next_v)
            next_v = pi.get(next_v)

    """
    Step 4 : If there is no cycle, return all the minimum edges pi(v)
    """
    if cycle_vertex is None:
        return set([(pi[v], v) for v in pi.keys()])

    """
    Step 5 : Otherwise, all the vertices in the cycle must be identified
    """
    C = set()
    C.add(cycle_vertex)
    next_v = pi.get(cycle_vertex)
    while next_v != cycle_vertex:
        C.add(next_v)
        next_v = pi.get(next_v)

    """
    Step 6 : Contracting the cycle C into a new node v_c
    v_c is negative and squared to avoid having the same number
    """
    v_c = -cycle_vertex ** 2
    V_prime = set([v for v in V if v not in C] + [v_c])
    E_prime = set()
    w_prime = dict()
    correspondance = dict()
    for (u, v) in E:
        if u not in C and v in C:
            e = (u, v_c)
            if e in E_prime:
                if w_prime[e] < w[(u, v)] - w[(pi[v], v)]:
                    continue
            w_prime[e] = w[(u, v)] - w[(pi[v], v)]
            correspondance[e] = (u, v)
            E_prime.add(e)
        elif u in C and v not in C:
            e = (v_c, v)
            if e in E_prime:
                old_u = correspondance[e][0]
                if w[(old_u, v)] < w[(u, v)]:
                    continue
            E_prime.add(e)
            w_prime[e] = w[(u, v)]
            correspondance[e] = (u, v)
        elif u not in C and v not in C:
            e = (u, v)
            E_prime.add(e)
            w_prime[e] = w[(u, v)]
            correspondance[e] = (u, v)

    """
    Step 7 : Recursively calling the algorithm again until no cycles are found
    """
    tree = msa(V_prime, E_prime, r, w_prime)

    """
    Step 8 : 
    """
    cycle_edge = None
    for (u, v) in tree:
        if v == v_c:
            old_v = correspondance[(u, v_c)][1]
            cycle_edge = (pi[old_v], old_v)
            break

    ret = set([correspondance[(u, v)] for (u, v) in tree])
    for v in C:
        u = pi[v]
        ret.add((u, v))

    ret.remove(cycle_edge)

    return ret