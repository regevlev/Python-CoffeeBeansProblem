
# This is the main starting point of the program

from turtle import done
from CoffeeBeanContainer import Container
from CoffeeBean import CoffeeBean

class Start_Prog:

    def __init__(self, listMaxCapacities, listInitCapacities):
        Container.resetContainers(self)
        self.ContainersArray = []
        self.MaxCapacities = listMaxCapacities
        self.InitCapacities = listInitCapacities
        self.CoffeeMachine = Container(0)
        self.NumberOfContainers = len(listMaxCapacities)
        
        for i in range(self.NumberOfContainers):
            if i < len(listInitCapacities):
                self.ContainersArray.append(Container(listMaxCapacities[i], listInitCapacities[i]))


    # decide if need to shift beans from one container to another:
    # if yes, 
    #   Then one of the beans will be for the coffee machine and will be reduced from the pool
    # If not, 
    #   Then only reduce one bean from the container with the fewest amount

    def ShiftBeans(self, quantity, fromContainer ,ToContainer = None):
        if(ToContainer == None):
            if(quantity > 0):
                self.MakeCoffee(fromContainer)
            return
        
        beanShift = fromContainer.extractBeans(quantity)
        
        if(beanShift == None):
            return
        
        self.CoffeeMachine.addBeans(beanShift[:1])
        ToContainer.addBeans(beanShift[1:])
#        print(self.CoffeeMachine)
#        print (fromContainer)
#        print (ToContainer)

    def MakeCoffee(self, containerToUse):
        self.CoffeeMachine.addBeans(containerToUse.extractBeans(1))
          
          
    def UseAllCoffeeInContainer(self, ContainerToUse):
        beanQuntity = ContainerToUse.returnBeanQuantity()
        for x in range(beanQuntity):
            self.MakeCoffee(ContainerToUse)
            
    
    def UseBalansedLessFilledContainer(self):
        
        # get all empty containers
        List_EmptyContainers  = self.returnAllEmptyContainers()
        biggestEmptyContainer = None
        
        
        while len(List_EmptyContainers) < self.NumberOfContainers:
            print(self.ContainersArray)
            nextContainerToUse = self.returnContainerHoldsMinimumAmount(self.ContainersArray)

            # need to shift beans
            nextContainerBeanQuantity = nextContainerToUse.returnBeanQuantity()
            
            #if more then 2 beans left, and have empty container: shifting beans
            if nextContainerBeanQuantity > 2 and len(List_EmptyContainers) > 0:       
            
                # if avilable empth container, find the biggest
                biggestEmptyContainer = self.returnContainersWithMaxCapacity(List_EmptyContainers)
                emptyCapacity = biggestEmptyContainer.returnMaxCapacity()
                beansToShift = int((nextContainerBeanQuantity + 1) / 2)

                if (beansToShift - 1) > emptyCapacity:
                    beansToShift = (emptyCapacity + 1)
                    
                self.ShiftBeans(beansToShift, nextContainerToUse, biggestEmptyContainer)        
                           
            else:
                self.UseAllCoffeeInContainer(nextContainerToUse)

            #update empty containers list
            List_EmptyContainers  = self.returnAllEmptyContainers()
            
    def returnAllEmptyContainers(self):
        new_list = []
        for x in self.ContainersArray:
            if x.returnBeanQuantity() == 0:
                new_list.append(x)
                
        return new_list
    
    
    def returnContainerHoldsMinimumAmount(self, list):
        min_container = None
        for x in list:
            if x.returnBeanQuantity() > 0 :
                min_container = x
                break
            
        if min_container == None:
            return min_container
        
        for x in list:
            temp = x.returnBeanQuantity()
            if (temp > 0) and (temp < min_container.returnBeanQuantity()):
                min_container = x
        return min_container

    
    def returnContainersWithMaxCapacity(self, List_Containers = None):
        if List_Containers == None:
            return None
        biggestContainer = max(List_Containers, key=lambda x: x.returnMaxCapacity())
        return biggestContainer
    
    
    def returnSortedContainersByBeanQuantity(self):
        new_list = []
        new_list = sorted(self.ContainersArray , key=lambda x: x.returnBeanQuantity(), reverse=False)
        print(f"Sorted list: {new_list}")
        return new_list
    
    def returnSortedContainersByContainerMaxQuantity(self):
        new_list = []
        new_list = sorted(self.ContainersArray , key=lambda x: x.returnMaxQuantity(), reverse=False)
        print(f"Sorted list (by container size): {new_list}")
        return new_list
    
    def test(self, testCase):
        match testCase:
            # this will iterate on each container and use it antil it will be empty
            case 1:
                print(f"\n === Run Test Case {testCase} ===")
                self.returnSortedContainersByBeanQuantity()
                self.returnSortedContainersByContainerMaxQuantity()
                
            case 2:
                print(f"\n === Run Test Case {testCase} ===")
                self.MakeCoffee(self.ContainersArray[2])
            
            case 3:
                print(f"\n === Run Test Case {testCase} ===")
                '''
                if have empty container and the liss full have more then 2 
                take from the liss and move half + 1 to the empty container (with the largest capacity)
                else empty the liss full container
                '''
                self.UseBalansedLessFilledContainer()
                
            case _:
                print(f"\n === Run Test CasDefaulte Default ===")
                for x in self.ContainersArray:
                    self.UseAllCoffeeInContainer(x)
        
        print(self.ContainersArray)
        print(self.CoffeeMachine)

        
def main():
    print("The Program Started ...")

    listMaxCapacities =  [10, 20, 30, 40, 60, 50, 100, 50]
    listInitCapacities = [10,  0,  2,  0, 30, 40,   0, 35]
    start1 = Start_Prog(listMaxCapacities, listInitCapacities)
    print (f"Number of empty containers = {len(start1.returnAllEmptyContainers())}")
    start1.test(3)
    print (f"Number of empty containers = {len(start1.returnAllEmptyContainers())}")
    start1.test(0)
    print (f"Number of empty containers = {len(start1.returnAllEmptyContainers())}")
    exit()
    start1.printArray(True)
    start1.test(2)

    start1.test(1)

    start1.test(0)

    
    containersData.reverse()
    start2 = Start_Prog(containersSize, containersData)
    start2.test(0)
    #print(start2.CoffeeMachine)


    #start2.printArray(True)
    print("Program endded ")

if __name__ =="__main__":
    main()



