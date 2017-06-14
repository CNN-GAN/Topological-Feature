from copy import deepcopy

class AttributeDict(dict):
    def __getattr__(self, attr):
        return self[attr]
    def __setattr__(self, attr, value):
        self[attr] = value
    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result
    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.items():
            setattr(result, k, deepcopy(v, memo))
        return result
    
def getANN(data, test, k=10):

    flann = FLANN()
    result, dists = flann.nn(data, test, k, algorithm="kmeans", branching=32, iterations=10, checks=16)
    return result, dists
