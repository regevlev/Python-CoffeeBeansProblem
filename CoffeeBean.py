# This is the basic class which holds the coffee bean for single portion
class CoffeeBean:
    
    def __init__(self):
        self.Quality = 0
        
    def incQuality(self):
        self.Quality +=1

    def returnQuality(self):
        return self.Quality
    
    def __str__(self):
        return f"{self.Quality}"
    
    def __repr__(self):
        return str(self)
    


'''
# Testing the Class
cb = CoffeeBean()
for x in range(5):
    cb.incQuality()
    print(cb)
'''