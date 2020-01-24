## @package objects
#  Documentation for this module.
#
#  Contains all the Objects/Classes used in this program

from BlackHole import app
import random
import os

###########################################################################

class InvalidQuestion(Exception):
    """Base class for other exceptions"""
    # print("Invalid Question")
    pass

class NoLeafFound(InvalidQuestion):
    # print("Invalid Question | No Leaf Found")
    pass

class InvalidNumberBranches(InvalidQuestion):
    # print("Invalid Question | Not enough Branches")
    pass

###########################################################################
 
## User class representing each player with the following attributes:
#        Atributes: 
#            @var id           Player unique id.
#            @var q            Number of questions to be answered by this user.
#            @var points       Player current puntiantion.
#            @var currQuestion Identifier of the current question.
#            @var qindexs      Order of the questions to be answered by this user.
#            @var percentage   Player points percentage.
#            @var answers      Player list of answers to be compared to the corrent ones, generating a sheet for consulting.
class User(object):
    
    ## The Constructor
    #  @param self The object pointer.
    #  @param id   The player unique id.
    #  @param q    The number of questions to be answered.
    def __init__(self, id, q):
        self.id = id
        self.points = 0
        self.currQuestion = 0
        self.q = q
        self.qindexs = [i for i in range(self.q)]
        random.shuffle(self.qindexs)
        self.percentage = 0
        self.answers= list()

    ## Getters and Setters
    def getId(self):
        return self.id

    ## Getters and Setters
    def setId(self,id):
        self.id = id

    ## Getters and Setters
    def getCurrQuestion(self):
        return self.currQuestion

    ## Getters and Setters
    def setCurrQuestion(self,c):
        self.currQuestion = c

    ## Add points to the user current total points
    #  @param self The object pointer.
    #  @param p    Int number of points to be added.
    def addPoints(self,p):
        self.points += int(p)

    ## Deserialize a User Object
    #  @param obj User objet in Json format to be parsed to an object of class User
    #  @return user User object deserialized
    @staticmethod
    def dsobject(obj):
        user = User(obj['id'],obj['q'])
        user.points = obj['points']
        user.currQuestion = obj['currQuestion']
        user.qindexs = obj['qindexs']
        user.answers = obj['answers']
        return user

###########################################################################

## Game class representing a unique game with the following attributes:
#        Atributes: 
#            @var date             Game date.
#            @var users            Dict of Users playing the game.
#            @var path             Path for storing Users info.
#            @var questions        List of game questions.
#            @var complexityFactor Factor used in points calculation. 
class Game(object):
    
    fnames = ['Willard', 'Albert', 'Helene', 'Leopold', 'Cathy', 'Orpha', 'Helena', 'Lance', 'Miles', 'Lilian', 'Haley', 'Allen', 'Willa', 'Torey', 'Krista', 'Dorian', 'Carlie', 'Bernadine', 'Albin', 'Vernie', 'Zachery', 'Marcia', 'Savion', 'Augustine', 'Serena', 'Edwina', 'Monique', 'Adrien', 'Janie', 'Jolie', 'Melisa', 'Hillard', 'Cali', 'Herminia', 'Luella', 'Armand', 'Monty', 'Carson', 'Albertha', 'Maurice', 'Lazaro', 'Maye', 'Candice', 'Elwyn', 'Kelli', 'Garland', 'Clint', 'Freeda', 'Keyshawn', 'Jeramie', 'Noah', 'Gerhard', 'Christy', 'Danny', 'Santos', 'Callie', 'Adelbert', 'General', 'Kara', 'Brandi', 'Ellen', 'Jakayla', 'Adeline', 'Eduardo', 'Daron', 'Adah', 'Lysanne', 'Brayan', 'Kaitlin', 'Torrey']

    ## The Constructor
    #  @param self The object pointer.
    #  @param date Game date.
    #  @param path Path for storing Users info.
    #  @param cF   Factor added to punctuation calculation. 
    def __init__(self,date,path,cF):
        self.date = date
        self.users = {}
        self.path = path
        self.questions = []
        self.complexityFactor = cF
        try:
            folder = os.path.join(app.root_path,self.path)

            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
            
                if (os.path.isfile(file_path) or os.path.islink(file_path)) and "UsersData" in file_path:
                    os.unlink(file_path)
                else:
                    raise Exception("No such file or directory 'UsersData'")
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    
    ## Getters and Setters
    def setDate(self,date):
        self.date = date

    ## Getters and Setters
    def getDate(self):
        return self.date

    ## Getters and Setters
    def setUsers(self,users):
        self.users = users

    ## Getters and Setters
    def addUser(self,user):
        if user.getId() not in self.users:
            self.users[user.getId()] = user
            return True
        else:
            return False

    ## Getters and Setters
    def getUsers(self):
        return self.users

    ## Getters and Setters
    def getQuestions(self):
        return self.questions

    ## Getters and Setters
    def setQuestions(self,questions):
        self.questions = questions

    ## Shuffles the questions
    #  @param self The object pointer.
    def shuffleQuestions(self):
        qts = list(self.questions)
        random.shuffle(qts)
        self.questions = qts
        
    ## Loads the questions on a given file
    #  @important File format specification is the following
    #       1 question per line:
    #       Image$Trunk#branch1#branch2#branch3#branch4   [...]
    #       where Image is the name of the image file (Empty if none - $ needs to be there anyways) for this question, placed in the static/qres folder as the file, Trunk is the question text and the branches all the options - branch1 matches the correct answer
    #       Don't worry about the order of the branches/options cause they will be shuffled of every user
    #  @param self The object pointer.
    #  @param path The path where the game file is.
    def loadQuestions(self,path,filen):
        contents = []
        with app.open_resource(path + str(filen),'r') as f:
            contents = f.read()
        
        for l in str(contents).split('\n'):
            Objt = list(l.split('#'))
            branches = dict()
            for i in range(len(Objt[1:])):
                branches["branch"+str(i+1)] = Objt[i+1]     
            imtr =  str(Objt[0]).split('$')
            image = ''
            if imtr[0] is not '':
                image = "static/qres/" + imtr[0]               
            trunk = imtr[1]
            q = Question(trunk,Objt[1],**branches)
            q.image = image
            self.questions.append(q)

###########################################################################

## Question class representing each question with the following attributes:
#        Atributes: 
#            @var trunk    Question info text.
#            @var leaf     Correct Answer.
#            @var image    Path for image (option - under construction).
#            @var branches Dict containing all the options including the leaf.
class Question(object):

    ## The Constructor
    #  @param self     The object pointer.
    #  @param trunk    Question info text.
    #  @param leaf     Correct Answer.
    #  @param **kwargs Options container.
    def __init__(self,trunk,leaf,**kwargs):
        self.trunk = trunk
        self.leaf = leaf
        self.setBranches(**kwargs)
        self.image = ""

    ## Getters and Setters
    def getImage(self):
        return self.image
    
    ## Getters and Setters
    def getTrunk(self):
        return self.trunk
    
    ## Getters and Setters
    def setTrunk(self,trunk):
        self.trunk = trunk

    ## Getters and Setters
    def getLeaf(self):
        return self.leaf

    ## Getters and Setters
    def setLeaf(self,leaf):
        self.leaf = leaf
    
    ## Getters and Setters
    def getBranches(self):
        return self.branches

    ## Sets all the branches/options for this question
    #  @param self The object pointer.
    #  @param **kwargs Options container.
    def setBranches(self,**kwargs):
        self.branches = dict()
        found = False
        if len(kwargs) < 2 : raise(InvalidNumberBranches)
        for k,i in kwargs.items():
            if i == self.leaf:
                found = True
            self.branches[k] = i
        if found == False:
            raise(NoLeafFound)

    ## Evaluates an answer
    #  @param self   The object pointer.
    #  @param answer The answer to be evaluated
    #  @return True if correct, False if wrong 
    def evaluate(self,answer):
        return answer == self.leaf
    
    ## Shuffles the options
    #  @param self   The object pointer.
    #  @return opts Shuffled options for this question.
    def shuffleBranches(self):
        opts = list(self.branches.values())
        random.shuffle(opts)
        return opts
    
    ## Prints the Question fields on the console
    #  @param self   The object pointer.
    def print(self):
        print("Trunk: {}".format(self.trunk))
        opt = ""
        for k,i in self.branches.items():
            print(k + ": " + i)
            if i == self.leaf:
                opt = k
        print("Leaf: {} | {}".format(self.leaf,opt))
        print("Image: {}".format(self.image))
        print("###########################")