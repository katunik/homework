import numpy
import random
import math

# Вариант 14.
data=[]
weidhts=[]
volumes=[]
values=[]
file = open('14.txt')

for line in file:
    data.append(line.split())
maxWeight = float(data[0][0]) #грузоподъемность
maxVolume = float(data[0][1]) #вместимость

del data[0]
for item in data:
    weidhts.append(float(item[0])) #вес
    volumes.append(float(item[1])) #объем
    values.append(float(item[2]))  #ценность

indNum=200
population = []
# Начальная популяция (случайная генерация)
for i in range(indNum):
    individual=''
    for j in range(len(data)): # len(data) = 30
        individual+=str(random.randrange(2))
    population.append(individual)


 # Отбор особей для скрещивания(выбрать только 20% самых приспособленных особей)
def selection(population):
    sortedPop = sorted(population, key=  lambda i: fitness(i)[2], reverse=True)
    indForCross=[]
    for i in range(math.floor(len(sortedPop)*0.2)):
        indForCross.append(sortedPop[i])
    return indForCross

#Скрещивание (кроссинговер) между выбранными особями. 
#Каждая особь скрещивается 1 раз за 1 поколение, 1 пара дает 2 потомка:
#3.2 однородный (каждый бит от случайно выбранного родителя)
def crossingover(indForCross):
    children=[]
    for i in range(len(indForCross)):
        item1=''
        item2=''
        if i<len(indForCross)-i-1:
            for j in range(len(data)):
                if indForCross[i][j] == indForCross[len(indForCross)-i-1][j]:
                    bit=indForCross[i][j]
                    item1+=bit
                    item2+=bit
                else:
                    bit=random.randrange(2)
                    item1+=str(bit)
                    bit=random.randrange(2)
                    item2+=str(bit)
            children.append(item1)
            children.append(item2)
    return children

#Мутация (случайное изменение 3х битов у 5% особей) 
def mutation(children):
    for i in range(math.floor(len(children)*0.05)):
        index=random.randrange(len(children))
        for j in range(3):
            bit = random.randrange(len(children[index]))
            newValue=1-int(children[index][bit])
            children[index]=children[index][0:bit]+str(newValue)+children[index][bit+1:]
    return children

#Формирование новой популяции (замена своих родителей)
def createNewPopulation(population, children):
    newPopulation=population
    parents=selection(population)
    for parent in parents:
        newPopulation.remove(parent)
    for child in children:
        newPopulation.append(child)
    return newPopulation

#Оценка результата
def solver(population):
    lastIterRes=0
    for i in range(500):
        selectedInd=selection(population)
        children=crossingover(selectedInd)
        mutChildren=mutation(children)
        population=createNewPopulation(population,mutChildren)
        bestIndivid=sorted(population, key=  lambda i: fitness(i)[2], reverse=True)[0]
        bestIndividFit=fitness(bestIndivid)[2]
        if abs(bestIndividFit-lastIterRes) < math.floor(bestIndividFit*0.1):
            return bestIndivid
        if i>0 and i%15==0:
            lastIterRes=bestIndividFit
    return bestIndivid
    
def fitness(individual):
    weight = 0.0
    volume = 0.0
    value = 0.0
    
    for i in range(len(individual)):
        weight += int(individual[i])*weidhts[i]
        volume += int(individual[i])*volumes[i]
        value += int(individual[i])*values[i]
    if volume > maxVolume or weight > maxWeight:
        return maxWeight, maxVolume,  0           
    return weight, volume, value

 
best=solver(population)
print("packed items")
for i in range(len(best)):
    if(best[i]=='1'):
        print(i, data[i])
print("total weight, volume, value")
print(fitness(best))