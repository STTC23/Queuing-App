def first(element, queue, last): 
    last[0] += 1 #Last will be add up when one element is added
    queue[last[0]] = element #Every elemento goes to the queue list

queue = [""] * 100 # Size of list
last = [0] # List for the reference

print("-"*30)
amount_elements = int(input("Ingrese la cantidad de elementos que desea agregar a la lista:  ")) #User adds an amount of elements

for i in range(1, amount_elements + 1): 
    element = input(f"Ingrese el elemento #{i}:  ") #User adds an element
    first(element,queue,last) #Element is save in queue

if queue[1] != "": #if the list is "empty", we'll show us the "Cola vacia" message
    first_element = queue[1] #first element will be add to the variable 
    print("El primer elemento en cola es:  ", first_element)
else: 
    print("Lo sentimos, la cola está vacía")

print("-"*30)