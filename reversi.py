import sys

global dict, weights, inf, neg_inf, game_states, top, nodes, ind, node_list, win_pos, lines
dict={ 0:'a',1:'b', 2:'c', 3:'d', 4:'e',5:'f',6:'g',7:'h'}
weights = [[99,-8,8,6,6,8,-8,99],
           [-8,-24,-4,-3,-3,-4,-24,-8],
           [8,-4,7,4,4,7,-4,8],
           [6,-3,4,0,0,4,-3,6],
            [6,-3,4,0,0,4,-3,6],
           [8,-4,7,4,4,7,-4,8],
           [-8,-24,-4,-3,-3,-4,-24,-8],
           [99,-8,8,6,6,8,-8,99]
           ]
neg_inf = -999999
inf = 999999
game_states = []
top = -1
nodes = []
node_list = {}
ind = -1
win_pos = []
lines = []

class Node:

    def __init__(self, node, depth, val, alpha, beta, state):
        self.name = node
        self.depth = depth
        self.val = val
        self.alpha = alpha
        self.beta = beta
        self.state = state

def eval(state, player):
    if player == 'X':
        opponent = 'O'
    else:
        opponent = 'X'
    player_sum = 0
    opponent_sum = 0
    for i in range(8):
        for j in range(8):
             if state[i][j] == player:
                 player_sum += weights[i][j]
             elif state[i][j] == opponent:
                 opponent_sum += weights[i][j]

    value = player_sum - opponent_sum
    return value

def findValidMoves(state, player):
    pos = []
    if player == 'X':
        opponent = 'O'
    else:
        opponent = 'X'
    for i in range(8):
        for j in range(8):
            if state[i][j] == player:
                for xDir, yDir in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                    x = i + xDir
                    y = j + yDir

                    if x < 0 or x > 7 or y < 0 or y > 7:
                        continue

                    if state[x][y] == opponent:
                        while state[x][y] == opponent and state[x][y] != '*':
                            x += xDir
                            y += yDir
                            if x < 0 or x > 7 or y < 0 or y > 7:
                                break
                        if x < 0 or x > 7 or y < 0 or y > 7:
                            break
                        if state[x][y] == '*':
                            pos.append([x,y])
    return pos

def updateState(state, pos, player):
    new_state = []
    for i in range(0,8):
        new_state.append([])
        for j in range(0,8):
            new_state[i].append(state[i][j])
    i = pos[0]
    j = pos[1]
    if player == 'X':
        opponent = 'O'
    else:
        opponent = 'X'
    new_state[i][j] = player
    for xDir, yDir in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x = i + xDir
        y = j + yDir
        flips = []
        if x < 0 or x > 7 or y < 0 or y > 7:
            continue
        if new_state[x][y] == opponent:
            while new_state[x][y] == opponent and new_state[x][y] != '*':
                flips.append([x,y])
                x += xDir
                y += yDir
                if x < 0 or x > 7 or y < 0 or y > 7:
                    break
            if x < 0 or x > 7 or y < 0 or y > 7:
                break
            if new_state[x][y] == player and len(flips) != 0:
                for (a,b) in flips:
                    new_state[a][b] = player
    return new_state

def alpha_beta(state):
    global top, game_states, nodes, ind, op_file, lines
    count = 0
    node = Node("root",count,neg_inf,neg_inf, inf, state)
    nodes.append(node)
    node_list["root"] = node
    ind += 1
    #print >> op_file, "Node,Depth,Value,Alpha,Beta"
    lines.append("Node,Depth,Value,Alpha,Beta")
    value = max_value(state, neg_inf, inf, count)
    p = nodes[ind]
    a = node_list[p.name].alpha
    b = node_list[p.name].beta
    va = node_list[p.name].val
    if a == neg_inf:
        a = "-Infinity"
    if b == inf:
        b = "Infinity"
    if va == neg_inf:
        va = "-Infinity"
    if va == inf:
        va = "Infinity"
    #print >> op_file, "Max:",node_list[p.name].name+","+str(node_list[p.name].depth)+","+str(va)+","+str(a)+","+str(b)
    lines.append(node_list[p.name].name+","+str(node_list[p.name].depth)+","+str(va)+","+str(a)+","+str(b))
    return value

def max_value(state, alpha, beta, count):
    global top, game_states, nodes, ind, node_list, depth, player, win_pos, lines
    if count == depth:
        return eval(state, player)

    state1 = []
    moves = findValidMoves(state, player)
    moves.sort(key=lambda k: [k[0], k[1]])
    num_moves = len(moves)

    if num_moves == 0:
        moves = ["pass"]
        num_moves = 1
        if "pass" in nodes[ind-1].name:
            return eval(state, player)

    v = neg_inf

    p = nodes[ind]
    node_list[p.name].val = v
    a = node_list[p.name].alpha
    b = node_list[p.name].beta
    va = node_list[p.name].val

    if a == neg_inf:
        a = "-Infinity"
    if b == inf:
        b = "Infinity"
    if va == neg_inf:
        va = "-Infinity"
    if va == inf:
        va = "Infinity"
    if "pass" in node_list[p.name].name:
        #print >> op_file, "Max:","pass,"+str(node_list[p.name].depth)+","+str(va)+","+str(a)+","+str(b)
        lines.append("pass,"+str(node_list[p.name].depth)+","+str(va)+","+str(a)+","+str(b))
    else:
        #print >> op_file, "Max:",node_list[p.name].name+","+str(node_list[p.name].depth)+","+str(va)+","+str(a)+","+str(b)
        lines.append(node_list[p.name].name+","+str(node_list[p.name].depth)+","+str(va)+","+str(a)+","+str(b))
    for i in range(0,8):
        state1.append([])
        for j in range(0,8):
            state1[i].append(state[i][j])
    game_states.append(state1)
    top += 1
    for pos in moves:
        if pos == "pass":

            if 'pass' in node_list:
                new = Node("pass"+str(count+1),count+1,v,alpha,beta, state)
                node_list["pass"+str(count+1)] = new
            else:
                new = Node("pass",count+1,v,alpha,beta, state)
                node_list["pass"] = new
            nodes.append(new)
            ind += 1
            new_v = min_value(state, alpha,beta, count+1)
        else:
            current = game_states[top]
            next_state = updateState(current, pos, player)
            new = Node(dict[pos[1]]+str((pos[0]+1)),count+1,v,alpha,beta, next_state)
            nodes.append(new)
            ind += 1
            node_list[dict[pos[1]]+str((pos[0]+1))] = new
            new_v = min_value(next_state, alpha,beta, count+1)
        curr = nodes[ind].name
        node_list[curr].val = new_v
        a = node_list[curr].alpha
        b = node_list[curr].beta
        va = node_list[curr].val

        temp = nodes[ind-1].name

        if a == neg_inf:
            a = "-Infinity"
        if b == inf:
            b = "Infinity"
        if va == neg_inf:
            va = "-Infinity"
        if va == inf:
            va = "Infinity"
        if "pass" in node_list[curr].name:
            #print >> op_file, "Max:","pass,"+str(node_list[curr].depth)+","+str(va)+","+str(a)+","+str(b)
            lines.append("pass,"+str(node_list[curr].depth)+","+str(va)+","+str(a)+","+str(b))
        else:
            #print >> op_file, "Max:",node_list[curr].name+","+str(node_list[curr].depth)+","+str(va)+","+str(a)+","+str(b)
            lines.append(node_list[curr].name+","+str(node_list[curr].depth)+","+str(va)+","+str(a)+","+str(b))
        v = max(v, new_v)
        node_list[temp].val = v
        node_list[curr].val = new_v
        if v >= beta:
            game_states.pop()
            top -= 1
            nodes.pop()
            ind -= 1
            return v
        if v > alpha:
            alpha = v
            node_list[temp].alpha = v
            node_list[curr].alpha = v
            win_pos.append(pos)
        nodes.pop()
        ind -=1
        num_moves -= 1
        if num_moves != 0:
            a = node_list[temp].alpha
            b = node_list[temp].beta
            va = node_list[temp].val
            if a == neg_inf:
                a = "-Infinity"
            if b == inf:
                b = "Infinity"
            if va == neg_inf:
                va = "-Infinity"
            if va == inf:
                va = "Infinity"
            if "pass" in node_list[temp].name:
                #print >> op_file, "Max:","pass,"+str(node_list[temp].depth)+","+str(va)+","+str(a)+","+str(b)
                lines.append("pass,"+str(node_list[temp].depth)+","+str(va)+","+str(a)+","+str(b))
            else:
                #print >> op_file, "Max:",node_list[temp].name+","+str(node_list[temp].depth)+","+str(va)+","+str(a)+","+str(b)
                lines.append(node_list[temp].name+","+str(node_list[temp].depth)+","+str(va)+","+str(a)+","+str(b))
    game_states.pop()
    top -= 1
    return v

def min_value(state, alpha,beta, count):
    global top, game_states,nodes, ind, node_list, depth, player, lines
    if count == depth:
        return eval(state, player)
    v = inf

    state1 = []
    for i in range(0,8):
        state1.append([])
        for j in range(0,8):
            state1[i].append(state[i][j])
    moves = findValidMoves(state, opponent)
    moves.sort(key=lambda k: [k[0], k[1]])
    num_moves = len(moves)

    if num_moves == 0:
        moves = ["pass"]
        num_moves = 1
        if "pass" in nodes[ind-1].name:
            return eval(state, player)

    p = nodes[ind]
    node_list[p.name].val = v
    a = node_list[p.name].alpha
    b = node_list[p.name].beta
    va = node_list[p.name].val

    if a == neg_inf:
        a = "-Infinity"
    if b == inf:
        b = "Infinity"
    if va == neg_inf:
        va = "-Infinity"
    if va == inf:
        va = "Infinity"
    if "pass" in node_list[p.name].name:
        #print >> op_file, "Min:","pass,"+str(node_list[p.name].depth)+","+str(va)+","+str(a)+","+str(b)
        lines.append("pass,"+str(node_list[p.name].depth)+","+str(va)+","+str(a)+","+str(b))
    else:
        #print >> op_file, "Min:",node_list[p.name].name+","+str(node_list[p.name].depth)+","+str(va)+","+str(a)+","+str(b)
        lines.append(node_list[p.name].name+","+str(node_list[p.name].depth)+","+str(va)+","+str(a)+","+str(b))
    game_states.append(state1)
    top += 1

    for pos in moves:
        if pos == "pass":
            if 'pass' in node_list:
                new = Node("pass"+str(count+1),count+1,v,alpha,beta, state)
                node_list["pass"+str(count+1)] = new
            else:
                new = Node("pass",count+1,v,alpha,beta, state)
                node_list["pass"] = new
            nodes.append(new)
            ind += 1
            new_v = max_value(state, alpha,beta, count+1)
        else:
            current = game_states[top]
            next_state = updateState(current, pos, player)
            new = Node(dict[pos[1]]+str((pos[0]+1)),count+1,v,alpha,beta, next_state)
            nodes.append(new)
            ind += 1
            node_list[dict[pos[1]]+str((pos[0]+1))] = new
            next_state = updateState(current, pos, 'O')
            new_v = max_value(next_state, alpha,beta, count+1)
        v1 = v
        curr = nodes[ind].name
        node_list[curr].val = new_v
        a = node_list[curr].alpha
        b = node_list[curr].beta
        va = node_list[curr].val

        temp = nodes[ind-1].name

        if a == neg_inf:
            a = "-Infinity"
        if b == inf:
            b = "Infinity"
        if va == neg_inf:
            va = "-Infinity"
        if va == inf:
            va = "Infinity"
        if "pass" in node_list[curr].name:
            #print >> op_file, "Min:","pass,"+str(node_list[curr].depth)+","+str(va)+","+str(a)+","+str(b)
            lines.append("pass,"+str(node_list[curr].depth)+","+str(va)+","+str(a)+","+str(b))
        else:
            #print >> op_file, "Min:",node_list[curr].name+","+str(node_list[curr].depth)+","+str(va)+","+str(a)+","+str(b)
            lines.append(node_list[curr].name+","+str(node_list[curr].depth)+","+str(va)+","+str(a)+","+str(b))

        v = min(v, new_v)
        node_list[temp].val = v
        node_list[curr].val = new_v
        if v <= alpha:
            game_states.pop()
            top -= 1
            nodes.pop()
            ind -= 1
            return v
        if v < beta:
            beta = v
            node_list[temp].beta = v
            node_list[curr].beta = v
        nodes.pop()
        ind -= 1
        num_moves -= 1
        if num_moves != 0:
            a = node_list[temp].alpha
            b = node_list[temp].beta
            va = node_list[temp].val
            if a == neg_inf:
                a = "-Infinity"
            if b == inf:
                b = "Infinity"
            if va == neg_inf:
                va = "-Infinity"
            if va == inf:
                va = "Infinity"
            if "pass" in node_list[temp].name:
                #print >> op_file, "Min:","pass,"+str(node_list[temp].depth)+","+str(va)+","+str(a)+","+str(b)
                lines.append("pass,"+str(node_list[temp].depth)+","+str(va)+","+str(a)+","+str(b))
            else:
                #print >> op_file, "Min:",node_list[temp].name+","+str(node_list[temp].depth)+","+str(va)+","+str(a)+","+str(b)
                lines.append(node_list[temp].name+","+str(node_list[temp].depth)+","+str(va)+","+str(a)+","+str(b))
    game_states.pop()
    top -= 1
    return v

def main():
    global node_list,nodes,ind, win_pos, lines
    #ip_file = sys.argv[2]
    file = open("input4.txt", 'r')
    global op_file
    op_file = open("output.txt", 'a')
    global player
    global opponent
    input = file.read().splitlines()
    player = input[0]

    if player == 'X':
        opponent = 'O'
    else:
        opponent = 'X'
    global depth
    depth = input[1]
    depth = int(depth)
    state = []
    for i in range(2, 10):
        state.append(list(input[i]))
    result = alpha_beta(state)
    if win_pos[len(win_pos)-1] == "pass":
        result_state = state
    else:
        result_state = updateState(state, win_pos[len(win_pos)-1], player)
    for i in range(8):
        line = ''
        for j in range(8):
            line += result_state[i][j]
        print >> op_file, line
    for item in lines:
        print >> op_file, item
main()
