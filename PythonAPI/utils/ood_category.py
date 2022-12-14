import json 

def json_test():
    aDict = {"a":54, "b":87}
    jsonString = json.dumps(aDict)
    print(type(jsonString))
    print(jsonString)
    jsonFile = open("category.json", "w")
    print(type(jsonFile))

def save_category(cat):
    file = open("category.json", "w")
    file.write(json.dumps(cat))
    
def load_category(filename="category.json"):
    file = open(filename, "r")
    return json.loads(file.read())

if __name__ == "__main__":
    
    category = ["pizza", "apple", "cat", "dog", "horse",\
                "sheep", "cow", "elephant", "bear", "zebra",\
                "giraffe", "surfboard", "fork", "knife", "spoon",\
                "banana", "keyboard", "microwave", "oven", "cake"]
    
    save_category(category)