# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

  


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        "*** YOUR CODE HERE ***"
        
        foodList = currentGameState.getFood().asList()
        maxDistance = -1000000

        for state in newGhostStates:
            if state.getPosition() == tuple(newPos):   #Daca pozitia fantomei este aceeasi cu pozitia curenta a Pacmanului atunci jocul e pierdut returnam 
                return -1000000                        #o valoare cat mai mica
 
        for x in foodList:
            currentDistance = -1 * (manhattanDistance(newPos, x)) 
            if (currentDistance > maxDistance):
                maxDistance = currentDistance

        return maxDistance

        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        return self.minimax(gameState, 0, 0)

    def minimax(self, gameState, agentIndex, depth):
        if depth == self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        if agentIndex == 0: 
            maxValue = -10000000
            action = Directions.STOP
            for state in gameState.getLegalActions(agentIndex):
                value = self.minimax(gameState.generateSuccessor(agentIndex, state), 1, depth)
                if value > maxValue:
                    maxValue = value
                    action = state
            if depth == 0:
                return action 
            else: 
                return maxValue
        else:
            next_agent = agentIndex + 1
            if agentIndex == gameState.getNumAgents() - 1:
                next_agent = 0
            minValue = 10000000
            for state in gameState.getLegalActions(agentIndex):
                if next_agent == 0:
                    value = self.minimax(gameState.generateSuccessor(agentIndex, state), 0, depth + 1)
                else: 
                    value = self.minimax(gameState.generateSuccessor(agentIndex, state), next_agent, depth)
                minValue = min(minValue, value)
            return minValue


        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.alphaBetaPruning(gameState, 0, 0, -1000000, 1000000)

    def alphaBetaPruning(self, gameState, agentIndex, depth, alpha, beta):
        if depth == self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        if agentIndex == 0: 
            maxValue = -10000000
            action = Directions.STOP
            for state in gameState.getLegalActions(agentIndex):
                value = self.alphaBetaPruning(gameState.generateSuccessor(agentIndex, state), 1, depth, alpha, beta)
                if value > maxValue:
                    maxValue = value
                    action = state
                alpha = max(alpha, value)
                if beta < alpha:
                    break
            if depth == 0:
                return action 
            else: 
                return maxValue
        else:
            next_ghost = agentIndex + 1
            if agentIndex == gameState.getNumAgents() - 1:
                next_ghost = 0
            minValue = 10000000
            for state in gameState.getLegalActions(agentIndex):
                if next_ghost == 0:
                    value = self.alphaBetaPruning(gameState.generateSuccessor(agentIndex, state), 0, depth + 1, alpha, beta)
                else: 
                    value = self.alphaBetaPruning(gameState.generateSuccessor(agentIndex, state), next_ghost, depth, alpha, beta)
                minValue = min(minValue, value)
                beta = min(beta, value)
                if beta < alpha:
                    break
            return minValue
        util.raiseNotDefined()

        
class RandomAgent ( Agent ) :

    def getAction ( self , gameState ) :
        legalMoves = gameState . getLegalActions ()
        # Pick randomly among the legal
        chosenIndex = random . choice ( range (0 , len ( legalMoves ) ) )
        return legalMoves [ chosenIndex ]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
