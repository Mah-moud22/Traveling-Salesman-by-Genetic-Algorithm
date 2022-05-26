import random
from random import randint

number_of_cities = 5
cities = "ABCDE"

# size of population
N = 10 
# if no path between two cities 
inf_path = 1e12
#Hash Table for Cites index
dict_of_cities = dict()
# define crossover and mutation probability
crossover_probability = 0.7
mutation_probability = 0.01

population = []
new_population = []
length_of_each_path = [0] * N
fitness = [0] * N

#-----------------------------------------------------------------------------------------------

#Create Random Path for inital Population 
def create_Rand_Path():
    temp = random.sample(cities,number_of_cities)
    temp.append(temp[0])
    return temp

#-----------------------------------------------------------------------------------------------

#Create inital Population
def create_Population():
    for i in range(N):
        population.append(create_Rand_Path())


#-----------------------------------------------------------------------------------------------

#Determine Length of each Path in Population
def determine_Length_of_each_path(distances , dict_of_cities):
    for i in range(N):
        distance_temp = 0
        for j in range(1,number_of_cities+1):
            distance_temp += distances[dict_of_cities[population[i][j-1]]][dict_of_cities[population[i][j]]]
        length_of_each_path[i] = distance_temp


#-----------------------------------------------------------------------------------------------

       
#determine fitness for each path
def determine_Fitness():
    sum = 0
    for i in length_of_each_path:
        sum += i
    
    for i in range(N):
        fitness[i] = round((length_of_each_path[i] / sum) *100 , 2)



#-----------------------------------------------------------------------------------------------


#Random selection for Parent that will use for next population 
def selection():
    roulette_ratio = [0] * N
    roulette_ratio[0] = fitness[0]
    for i in range(1,N):
        roulette_ratio[i] += roulette_ratio[i-1] + fitness[i]
    
    for i in range(N // 2):
        rand_num1 = randint(0,100)
        rand_num2 = randint(0,100)
        if(rand_num1 == rand_num2):
            while(rand_num1 == rand_num2):
                rand_num2 = randint(0,100)
        index1 = 0
        index2 = 0
        for i in range(N):
            if(rand_num1 <= roulette_ratio[i]):
                index1 = i
                break
        

        for i in range(N):
            if(rand_num2 <= roulette_ratio[i]):
                index2 = i
                break
        
        crossover(population[index1] , population[index2])


    
#-----------------------------------------------------------------------------------------------


#Partially Mapped Crossover
def crossover(index1 , index2):
    p1, p2 = [0] * number_of_cities, [0] * number_of_cities

    # Initialize the position of each indices in the individuals
    for k in range(number_of_cities):
        p1[dict_of_cities[index1[k]]] = k
        p2[dict_of_cities[index2[k]]] = k
        
    # Choose crossover points
    cxpoint1 = random.randint(0, number_of_cities)
    cxpoint2 = random.randint(0, number_of_cities - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:  # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    for k in range(cxpoint1, cxpoint2):
        temp1 = index1[k]
        temp2 = index2[k]
    # Swap the matched value
        index1[k], index1[p1[dict_of_cities[temp2]]] = temp2, temp1
        index2[k], index2[p2[dict_of_cities[temp1]]] = temp1, temp2
    # Position bookkeeping
        p1[dict_of_cities[temp1]], p1[dict_of_cities[temp2]] = p1[dict_of_cities[temp2]], p1[dict_of_cities[temp1]]
        p2[dict_of_cities[temp1]], p2[dict_of_cities[temp2]] = p2[dict_of_cities[temp2]], p2[dict_of_cities[temp1]]
    
    index1[number_of_cities] = index1[0]
    index2[number_of_cities] = index2[0]
    new_population.append(index1)
    new_population.append(index2)


#-----------------------------------------------------------------------------------------------


def mutate():
    for i in range(N):
        x = randint(1,100);
        if(x == 74):
            # swaping two cities in this path
            rand_num1 = randint(1,number_of_cities)
            rand_num2 = randint(1,number_of_cities)
            temp = new_population[i][rand_num1]
            new_population[i][rand_num1] = new_population[i][rand_num2]
            new_population[i][rand_num2] = temp;
        



#-----------------------------------------------------------------------------------------------

   
def main():
    best_route = [0] * (number_of_cities+1)
    best_route_length = 1e12
    distances = [[0, 4, 4, 7, 3],
             [4, 0, 2, 3, 5],
             [4, 2, 0, 2, 3],
             [7, 3, 2, 0, 6],
             [3, 5, 3, 6, 0]];
    
    num_of_generation = 10
    
    for i in range(number_of_cities):
        dict_of_cities.update({cities[i] : i});
    
    # Generate initial Population 
    create_Population()
    
    print("intit_Population : \r\n")
    for i in population:
        print(i,'\r\n')
    
    for i in range(num_of_generation):
        determine_Length_of_each_path(distances,dict_of_cities);
        print("\r\nGeneration ",i+1)
        print("\r\nPath",' '*25,"Length\r\n");
        for j in range(N):
            print(population[j],''*10,length_of_each_path[j])
            if(length_of_each_path[j] < best_route_length):
                best_route_length = length_of_each_path[j]
                best_route = []
                best_route = population[j].copy()
        determine_Fitness()
        selection()
        mutate()
    print("\r\n\r\nBest Route :",best_route,"  Length = ",best_route_length)


#-----------------------------------------------------------------------------------------------

main()