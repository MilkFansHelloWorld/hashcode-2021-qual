from dataparser import *
from queue import Queue
from collections import *

# inp: the input file as a single string
# out: the answer file produced by your solver, as a single string
# return the score of the output as an integer
def score(inp, out):
    ns = parse(inp)
    itr = (line for line in out.split('\n'))

    num_inter = ni(itr)
    graph = {}
    for _ in range(num_inter):
        inter_id = ni(itr)
        incoming_street_num = ni(itr)
        ls = []
        for _ in range(incoming_street_num):
            temp = next(itr).split()
            ls.append((temp[0], int(temp[1])))
        graph[inter_id] = ls

    queue_street = {}
    for street_name in ns.streets.keys():
        queue_street[street_name] = Queue()

    # initialize cars
    for car_id in ns.paths.keys():
        ls = ns.paths[car_id].st_names
        starting_street = ls[0]
        if len(ls) == 1:
            queue_street[starting_street].put((car_id, "end"))
        else:
            queue_street[starting_street].put((car_id, ls[1]))

    def green(street_name, t):
        inter_id = ns.streets[street_name].E
        cycle = 0
        if inter_id not in graph.keys():
            return False
        for (_, green_time) in graph[inter_id]:
            cycle += green_time
        remainder = t % cycle
        if remainder == 0:
            remainder = cycle
        temp_cnt = 0
        for (present_street, green_time) in graph[inter_id]:
            if temp_cnt < remainder and remainder <= temp_cnt + green_time:
                if present_street == street_name:
                    return True
                else:
                    return False
            else:
                temp_cnt += green_time

    in_move = {}

    score_counter = 0

    for t in range(1, ns.D):
        new_in_move = {}
        moved = set()
        for car_id in in_move.keys():
            (next_street, time_left) = in_move[car_id]
            if next_street == "end" and time_left == 1:
                score_counter += ns.F + (ns.D - (t + 1))
                # in_move.pop(car_id)
            elif next_street != "end" and time_left == 1:
                index = ns.paths[car_id].st_names.index(next_street)
                further_next_street = None
                if index == ns.paths[car_id].P - 1:
                    further_next_street = "end"
                else:
                    further_next_street = ns.paths[car_id].st_names[index + 1]
                queue_street[next_street].put((car_id, further_next_street))
                moved.add(car_id)
                #in_move.pop(car_id)
            else:
                new_in_move[car_id] = (next_street, time_left - 1)
                moved.add(car_id)
        in_move = new_in_move

        for street_name in queue_street.keys():
            queue = queue_street[street_name]
            if queue.qsize() == 0:
                continue
            if green(street_name, t):
                (head_car_id, next_street) = queue.queue[0]
                if head_car_id not in moved:
                    queue.get()
                    if next_street == "end":
                        score_counter += ns.F + (ns.D - (t + 1))
                    else:
                        if ns.streets[next_street].L == 1:
                            index = ns.paths[head_car_id].st_names.index(next_street)
                            further_next_street = None
                            if index == ns.paths[head_car_id].P - 1:
                                further_next_street = "end"
                            else:
                                further_next_street = ns.paths[head_car_id].st_names[index + 1]
                            queue_street[next_street].put((head_car_id, further_next_street))
                            moved.add(head_car_id)
                        else:
                            in_move[head_car_id] = (next_street, ns.streets[next_street].L - 1)
                            moved.add(head_car_id)

    return score_counter



inp = '''6 4 5 2 1000
2 0 rue-de-londres 1
0 1 rue-d-amsterdam 1
3 1 rue-d-athenes 1
2 3 rue-de-rome 2
1 2 rue-de-moscou 3
4 rue-de-londres rue-d-amsterdam rue-de-moscou rue-de-rome
3 rue-d-athenes rue-de-moscou rue-de-londres
'''

out = '''3
1
2
rue-d-athenes 2
rue-d-amsterdam 1
0
1
rue-de-londres 2
2
1
rue-de-moscou 1'''

score(inp, out)
