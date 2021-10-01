import random
import time
#Libs to plot graphs
"""
import matplotlib
import matplotlib.pyplot as plt
"""
from CNF_Creator import *
 
#Initialize Population
def InitPopulation(popsize):
    population = []
    for x in range(popsize):
        Dict = [1]*50
        i = 0
        while i < 50:
            Dict[i] = -1 if random.choice(range(2)) == 0 else 1
            i += 1
        #print(Dict)
        population.append(Dict)
 
    return population
 
#Calculate Fitness Function Value for the sentence
def Calculatefitness(sentence,Dict):
    totalsentences = len(sentence)
    count = 0
    for clause in sentence:
        for l in clause:          
            if l*Dict[abs(l)-1] > 0:
                count += 1
                break
    ans = (count/totalsentences)*100

    return ans
 
#Reproduce child using 2 parents
def Reproduce(state1,state2):
    index = random.randint(0,49)
    child1 = state1[:index] + state2[index:]
    child2 = state2[:index] + state1[index:]
    return child1, child2
 
#Mutate child
def Mutate(state):
    pos = random.randint(0,49)
    state[pos] *= -1
    return state
 
# def compare(x, y):
#     if Calculatefitness(sentence, x) < Calculatefitness(sentence, y):
#         return -1
#     elif Calculatefitness(sentence, x) > Calculatefitness(sentence, y):
#         return 1
#     else:
#         return 0
 
#Genetic Algorithm
def Genetic_Algo(sentence, initPopSize):
    population = InitPopulation(initPopSize)
    ans = [0,[]]
    start_time = time.time()
    tmp_ans = ans[0]
    tmp_time = start_time
    while True:
        iterations = 0
        newpopulation = []
        weights = []
        curr = 0
        popsize = 0
        for x in population:
            cf = Calculatefitness(sentence,x)
            if cf == 100:
                return [100,x]
            if cf > ans[0]:
                ans = [cf,x]
            weights.append(cf)
        # print(ans[0])
        if (time.time() - start_time > 44.5) or (time.time() - tmp_time > 25 and ans[0] == tmp_ans): return ans
        if ans[0] > tmp_ans:
            tmp_ans = ans[0]
            tmp_time = time.time()
 
        while iterations < initPopSize:
            parent1,parent2 = random.choices(population,weights=weights,k=2) 
            child1, child2 = Reproduce(parent1,parent2)
 
            prob = random.uniform(0, 1)
            if(prob < 0.1):
                child1 = Mutate(child1)
                child2 = Mutate(child2)
 
            if Calculatefitness(sentence, child1) > Calculatefitness(sentence, child2):
                child = child1
            else:
                child = child2
 
            newpopulation.append(child)
            popsize += 1
            if popsize >= initPopSize: break

            newpopulation.append(population[curr])
            curr += 1
            popsize += 1
            if popsize >= initPopSize: break
 
            iterations += 1
        # sorted(newpopulation, key=cmp_to_key(lambda item1, item2: Calculatefitness(sentence, item1) - Calculatefitness(sentence, item2)), reverse=True)        
        population = newpopulation
    
    return ans
 
#Main Function  
def main():
    cnfC = CNF_Creator(n=50) # n is number of symbols in the 3-CNF sentence   
    sentence = cnfC.ReadCNFfromCSVfile()
    start_time = time.time()
    ans = Genetic_Algo(sentence, len(sentence))
 
    #Program to calculate average fitness function and average running time for 10 randomly generated 3-CNF sentences for each m value in range (100,120,....300)
    """
    clauses_size = [100,120,140,160,180,200,220,240,260,280,300]
    average_fitness = []
    average_time = []
    for x in clauses_size:
        cnfC = CNF_Creator(n=50)
        avg_f = []
        avg_rt = []
        for i in range(10):
            sentence = cnfC.CreateRandomSentence(x)
            start_time = time.time()
            ls = Genetic_Algo(sentence, x)
            end_time = time.time()
            avg_f.append(ls[0])
            avg_rt.append(end_time - start_time)
        average_fitness.append(sum(avg_f)/len(avg_f))
        average_time.append(sum(avg_rt)/len(avg_rt))
    """
 
    #Program to plot graphs using matplotlib for average fitness function and average running time calculated for 10 randomly generated 3-CNF sentences for each m value in range (100,120,....300)
    """
    plt.plot(clauses_size,average_fitness, color='c')
    plt.title("Average Fitness Value VS Number of Clauses")
    plt.xlabel('Number of Clauses (m Value)')
    plt.ylabel('Average Fitness Value (in %)')
    plt.xticks(clauses_size)
    plt.legend()
    plt.show()
 
    plt.plot(clauses_size,average_time, color='y')
    plt.title("Average Running Time VS Number of Clauses")
    plt.xlabel('Number of Clauses (m Value)')
    plt.ylabel('Average Running Time (in s)')
    plt.xticks(clauses_size)
    plt.legend()
    plt.show()
    """
    
    best_model = []
    for i in range(50):
        best_model.append((i+1)*ans[1][i])
 
    #Program Output
    print('\n\n')
    print('Roll No : 2018B2A70642G')
    print('Number of clauses in CSV file : ',len(sentence))
    print('Best model :',best_model)
    print('Fitness value of best model :',round(ans[0], 2),'%')
    print('Time taken :',round(time.time() - start_time, 4), 'seconds')
    print('\n\n')
    
if __name__=='__main__':
    main()