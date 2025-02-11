
# This is the main starting point of the program

from tkinter.messagebox import NO
from turtle import done
from CoffeeBeanContainer import Container
from CoffeeBean import CoffeeBean

class CoffeeBeansProblem:

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

    def ShiftBeans(self, quantity, fromContainer, ToContainer = None, makeCoffee = True):
        if(ToContainer == None):
            if ( quantity > 0 and makeCoffee):
                self.MakeCoffeeFromContainer(fromContainer)
            return
        
        beanShift = fromContainer.extractBeans(quantity)
        
        if(beanShift == None):
            return
        
        if(makeCoffee):
            self.CoffeeMachine.addBeans(beanShift[:1])
            ToContainer.addBeans(beanShift[1:])
        
        else:
            ToContainer.addBeans(beanShift)
#        print(self.CoffeeMachine)
#        print (fromContainer)
#        print (ToContainer)

    def MakeCoffeeFromBean(self, coffeeBean):
        if isinstance(coffeeBean[0], CoffeeBean):
            self.CoffeeMachine.addBeans(coffeeBean)
        else:
            print(type(coffeeBean))
            print(type(CoffeeBean))
            print(f'Cant make good coffee from garbige')    
        
    def MakeCoffeeFromContainer(self, containerToUse):
        self.CoffeeMachine.addBeans(containerToUse.extractBeans(1))
          
          
    def UseAllCoffeeInContainer(self, ContainerToUse):
        beanQuntity = ContainerToUse.returnBeanQuantity()
        for x in range(beanQuntity):
            self.MakeCoffeeFromContainer(ContainerToUse)
            
    
    def UseBalansedLessFilledContainer(self):
        
        # get all empty containers
        List_EmptyContainers  = self.returnAllEmptyContainers()
        biggestEmptyContainer = None
        
        
        while len(List_EmptyContainers) < self.NumberOfContainers:
            nextContainerToUse = self.returnContainerHoldsMinimumAmount(self.ContainersArray)

            # need to shift beans
            nextContainerBeanQuantity = nextContainerToUse.returnBeanQuantity()
            
            # if more then 2 beans left, and have empty container: shifting beans
            if nextContainerBeanQuantity > 2 and len(List_EmptyContainers) > 0:       
            
                # if avilable empth container, find the biggest
                biggestEmptyContainer = self.returnContainersWithMaxCapacity(List_EmptyContainers)
                emptyCapacity = biggestEmptyContainer.returnMaxCapacity()
                beansToShift = int((nextContainerBeanQuantity + 1) / 2)

                if (beansToShift - 1) > emptyCapacity:
                    beansToShift = (emptyCapacity + 1)
                    
                self.ShiftBeans(beansToShift, nextContainerToUse, biggestEmptyContainer, True)        
                           
            else:
                self.UseAllCoffeeInContainer(nextContainerToUse)

            # update empty containers list
            List_EmptyContainers  = self.returnAllEmptyContainers()
            
            
            
    def FillLogBasedBalansedContainer(self):
        
        List_EmptyContainers  = self.returnAllEmptyContainers()
        
        while len(List_EmptyContainers) < self.NumberOfContainers:
            
            # use the container with the minimum anount of beans
            nextContainerToUse = self.returnContainerHoldsMinimumAmount(self.ContainersArray)
            
            SortedEmptyContainer = self.returnSortedContainersByContainerMaxCapacity(List_EmptyContainers, True)
            
            # if no empty containers or focus container holds less then 3 beans:
            #   us all beans in container
            if ((SortedEmptyContainer == None) or (nextContainerToUse.returnBeanQuantity() < 3)):
                self.UseAllCoffeeInContainer(nextContainerToUse)
                
            
            
            else:
                # Extract Beans to shift:
                #   if even number, extract half --> 8/2 = 4 
                #   if odd number, extract integer half + 1 --> 9/2 = 5
                TotalAvilableBeansToShift = int((nextContainerToUse.returnBeanQuantity()+1)/2)
                CurrentAvilableBeans = TotalAvilableBeansToShift
                BeanSpreadShift = []
            
                for x in SortedEmptyContainer:
                    
                    if CurrentAvilableBeans == 0:
                        continue
                    
                    # quantity beans to shift
                    beansToShift = int((CurrentAvilableBeans+1) / 2)
                                                
                    # current empty capacity
                    emptyCapacity = x.returnMaxCapacity()
                    
                    # abjust the shift amount to according to avilability
                    if beansToShift > emptyCapacity:
                        beansToShift = emptyCapacity
                    
                    BeanSpreadShift.append(beansToShift)
                    CurrentAvilableBeans -= beansToShift
                
                
                # calculate the amount of beans been used 
                # extract them and distribute based on the bean spread shift
                # rebuild the empty list
                
                ArrayBeansToShift = nextContainerToUse.extractBeans(TotalAvilableBeansToShift-CurrentAvilableBeans+1)
                self.MakeCoffeeFromBean(ArrayBeansToShift[:1])
                ArrayBeansToShift = ArrayBeansToShift[1:]

                for index in range (len(BeanSpreadShift)):
                    amount = BeanSpreadShift[index]
                    SortedEmptyContainer[index].addBeans(ArrayBeansToShift[:amount])
                    ArrayBeansToShift = ArrayBeansToShift[amount:]
                                       
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
    
    
    def returnSortedContainersByBeanQuantity(self, List_Containers = None, Reverse_List = False):
        new_list = []
        if List_Containers != None:
            new_list = sorted(List_Containers , key=lambda x: x.returnBeanQuantity(), reverse=Reverse_List)
            #print(f"Sorted list: {new_list}")
        return new_list
    
    def returnSortedContainersByContainerMaxCapacity(self, List_Containers = None, Reverse_List = False):
        new_list = []
        if List_Containers != None:
            new_list = sorted(List_Containers , key=lambda x: x.returnMaxCapacity(), reverse=Reverse_List)
            #print(f"Sorted list (by container size): {new_list}")
        return new_list
            
    
    def test(self, testCase):
        match testCase:
            # this will iterate on each container and use it antil it will be empty
            case 1:
                print(f"\n === Run Test Case {testCase} ===")
                self.returnSortedContainersByBeanQuantity(self.ContainersArray)
                self.returnSortedContainersByContainerMaxCapacity()
                testList = self.returnSortedContainersByBeanQuantity(self.ContainersArray)
                self.returnSortedContainersByContainerMaxCapacity(testList)
                self.returnSortedContainersByContainerMaxCapacity(testList, True)
                self.returnSortedContainersByBeanQuantity(self.ContainersArray, True)
                
            case 2:
                print(f"\n === Run Test Case {testCase} ===")
                self.MakeCoffeeFromContainer(self.ContainersArray[2])
            
            case 3:
                print(f"\n === Run Test Case {testCase} ===")
                '''
                if have empty container and the liss full have more then 2 
                take from the liss and move half + 1 to the empty container (with the largest capacity)
                else empty the liss full container
                '''
                self.UseBalansedLessFilledContainer()
            
            case 4:
                print(f"\n === Run Test Case {testCase} ===")
                '''
                if have empty container and the liss full have more then 2 
                take from the liss and move half to the empty container (with the largest capacity)
                    repeat the calculation for all the empty containers
                example:
                    5 containers: 
                        20/20   0/10    0/10    0/10    0/10
                    next step: 
                        9/20    5/10    3/10    2/10    0/10 --> 1 make coffee

                else empty the liss full container
                '''
                self.FillLogBasedBalansedContainer()
                
                  
            case _:
                print(f"\n === Run Test CasDefaulte Default ===")
                for x in self.ContainersArray:
                    self.UseAllCoffeeInContainer(x)
        
        print(self.ContainersArray)
        print(self.CoffeeMachine)

        
def main():
    print("The Program Started ...")

    listMaxCapacities =  [70,  6, 80,  3, 60, 50,  4, 50,  2]
    listInitCapacities = [45,  0, 80,  0, 50, 50,  0, 45,  0]
    start1 = CoffeeBeansProblem(listMaxCapacities, listInitCapacities)
    start1.test(3)
    
    start2 = CoffeeBeansProblem(listMaxCapacities, listInitCapacities)
    start2.test(4)
    
    '''
    print (f"Number of empty containers = {len(start1.returnAllEmptyContainers())}")
    start1.test(0)
    print (f"Number of empty containers = {len(start1.returnAllEmptyContainers())}")

    start1.printArray(True)
    start1.test(2)

    start1.test(1)

    start1.test(0)

    start2 = CoffeeBeansProblem(listMaxCapacities, listInitCapacities)
    start2.test(0)
    #print(start2.CoffeeMachine)
    #start2.printArray(True)
    '''
    
    print("Program endded ")

if __name__ =="__main__":
    main()



