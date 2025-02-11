
from CoffeeBean import CoffeeBean

# This is a Container definition which holdsd the coffee beans 
class Container:
    ObjectIndex = 0

    def __init__(self, MaxCapacity, InitQuantity = 0):
        
        self.ObjectIndex = Container.ObjectIndex
        self.MaxCapacity = MaxCapacity
        self.Openning = 0

        
        Container.ObjectIndex+=1
        
        self.__PrivateInit__(InitQuantity)
        
    def __PrivateInit__(self, InitQuantity = 0):
        self.InitQuantity = InitQuantity
        
        if(self.MaxCapacity < InitQuantity):
            print(f"Container {self.ObjectIndex} Init Quantity {self.InitQuantity} larger then {self.MaxCapacity}")
            print(f"Bean pool will be initiate to 0")
            self.InitQuantity = 0
        
        self.BeanPool = []
        self.__initBeanPool__()

    def __initBeanPool__(self):
        for i in range(self.InitQuantity):
            self.BeanPool.append(CoffeeBean())

    def __str__(self):
        if self.ObjectIndex == 0:
            return f"CoffeeMachine: Holds: {len(self.BeanPool)} Total quality = {self.returnTotalBeanQuality()}"
        else:
            return f"\nContainer: {self.ObjectIndex} Holds: {len(self.BeanPool)}/{self.returnInitQuantity()}/{self.returnMaxCapacity()} Total quality = {self.returnTotalBeanQuality()}"
    
    def __repr__(self):
        return str(self)
    
    
    def resetContainers(self):
        Container.ObjectIndex = 0

    def returnBeanQuantity(self):
        return len(self.BeanPool)

    def returnOpenning(self):
        return self.Openning

    def returnInitQuantity(self):
        return self.InitQuantity

    def __openContainer__(self):
        self.Openning+=1
        if self.ObjectIndex > 0:
            self.__incBeanPoolQuality__()

    def __incBeanPoolQuality__(self):
        for x in self.BeanPool:
            x.incQuality()

    def returnMaxCapacity(self):
        return self.MaxCapacity
    
    def extractBeans(self, amount):
        if amount > len(self.BeanPool):
            errMsg = f" Not Enough Beans in the container {self.ObjectIndex}"
            errMsg += f"\n Container holds {len(self.BeanPool)} which is less then {amount}"
            errMsg += f"\n No action will take place"
            print (errMsg)
            return None
        else:

            self.__openContainer__()
            extractedBeans = self.BeanPool[-amount:]
            self.BeanPool = self.BeanPool[:-amount]
            return extractedBeans


    def addBeans(self, Beans):
        
        if(self.ObjectIndex == 0):
            if(len(Beans) == 1):
                self.__openContainer__()
                self.BeanPool.extend(Beans)
            return
            
        if len(Beans) == 0:
            print("adding 0 is not legal [%d]" % (len(Beans)))
        elif (self.returnBeanQuantity() + len(Beans) > self.MaxCapacity):
            print("adding more then avilabl in the container is not legal")
            print(f"container {self.ObjectIndex} max quantity {self.MaxCapacity} currently contain {self.returnBeanQuantity()}")
            print(f"trying to add {len(Beans)} is over the limit")
        else:
            self.__openContainer__()
            self.BeanPool.extend(Beans)

    def returnObjectIndex(self):
        return self.ObjectIndex
    
    def returnBeanPoolInfo(self):
        self.poolDescription = ""
        for i , x in enumerate(self.BeanPool):
            self.poolDescription.join(f"{i}:{x} " )
        return self.poolDescription

    def returnTotalBeanQuality(self):
        sum = 0
        for x in self.BeanPool:
            sum+=x.returnQuality()
        return sum
