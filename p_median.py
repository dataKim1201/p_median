import pulp
from pulp import LpVariable, LpInteger, lpSum, LpConstraint
import numpy as np
import argparse

def p_median(matrix, p):
    parts = [i for i in range(13)]
    prob = pulp.LpProblem('p-median', pulp.LpMinimize)

    route = [(i,j) for i in range(13) for j in range(13)]
    vars = LpVariable.dicts("Route", (parts, parts), 0, 1, LpInteger)
    prob += (
        lpSum([vars[w][b] * matrix[w][b] for (w, b) in route]),
        "Sum_of_Transporting_Costs",
        )
    prob += (lpSum([vars[b][b] for b in parts]) == p,f"group_constraint",)
    for i in parts:
        prob += (lpSum([vars[i][b] for b in parts]) == 1,f"Sum_of_Parts_allocated_{i}",)
        for b in parts:
            prob += vars[i][b] <= vars[b][b] 
    prob.solve()
    print(pulp.value(prob.objective))
    for i in prob.variables():
        tmp = i.to_dict()
        if tmp['varValue'] == 1:
            print(tmp['name'])
            # print(tmp['name'].split('_')[1:])
    prob.writeLP(f'result p : {p}.txt')

    # Create the PuLP problem
    # return facility_locations, demand_assignments, cost

def hamming_distance(distance):
    distance = np.array(distance)
    result = np.zeros((distance.shape[1],distance.shape[1]))
    for i in range(distance.shape[1]):
        for j in range(distance.shape[1]):
            p1 = distance[:,i]
            p2 = distance[:,j]
            score = sum((p1!=p2).astype(int))
            result[i,j] = score
    return result
if __name__=='__main__':
    machine1 = [0,1,1,0,0,0,1,1,1,0,0,1,1]
    machine2 = [0,1,0,0,0,0,1,1,0,0,1,1,0]
    machine3 = [1,0,0,0,0,1,0,0,0,0,0,0,0]
    machine4 = [0,0,1,0,1,0,0,0,0,1,0,0,0]
    machine5 = [0,0,1,0,0,0,1,1,1,0,0,1,1]
    machine6 = [0,0,0,0,1,0,0,0,0,0,0,0,0]
    machine7 = [0,0,0,1,0,0,0,0,0,1,0,0,0]
    machine8 = [0,0,0,1,0,0,0,0,0,1,0,0,0]
    machine9 = [0,0,0,0,0,1,0,0,0,0,0,0,0]
    distance_matrix =[machine1,machine2,machine3,machine4,machine5,machine6,machine7,machine8,machine9]
    distance_matrix = hamming_distance(distance_matrix)
    print(distance_matrix)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", default=3,dest="p", action="store",type=int)          # extra value
    args = parser.parse_args()


    # Solve the p-median problem for p=2
    p_median(distance_matrix, args.p)

    # Print the solution
    # print("Facility locations:", facility_locations)
    # print("Demand assignments:", demand_assignments)
    # print("Total cost:", cost)