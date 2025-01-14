import numpy as np
from env import Env

class State(object):
    def __init__(self, index, reward, isTerminal = False):
        self._index = index
        self._reward = reward
        self._isTerminal = isTerminal

    def __str__(self):
        return str(self._index)

    def isTerminal(self):
        return self._isTerminal

    def getReward(self):
        return self._reward

    def getIndex(self):
        return self._index


class LongGrid(Env):

    def __init__(self, width, reward, noise):
        self.stateList = list()
        self.width = width
        self.noise = noise
        self.resultType = {'correct': (1 - self.noise), 'stay': self.noise / 2., 'reverse': self.noise / 2.}
        for i in range(width - 1):
            state = State(i, 0)
            self.stateList.append(state)
        # Terminal state
        self.stateList.append(State(width - 1, reward, True))

    def getAllStates(self):
        return self.stateList

    def getStartState(self):
        return self.stateList[0]

    def getNextStateListWithAction(self, state, action):
        index = state.getIndex()
        stateL = list()
        if state.isTerminal():
            return stateL
        if action == 'left':
            if index == 0:
                stateL.append((self.stateList[index], 1 - self.noise / 2.))
                stateL.append((self.stateList[index + 1], self.noise / 2.))
            elif index == (self.width - 1):
                stateL.append((self.stateList[index - 1], 1 - self.noise))
                stateL.append((self.stateList[index], self.noise))
            else:
                stateL.append((self.stateList[index - 1], 1 - self.noise))
                stateL.append((self.stateList[index], self.noise / 2.))
                stateL.append((self.stateList[index + 1], self.noise / 2.))
        else:
            if index == (self.width - 1):
                stateL.append((self.stateList[index], 1 - self.noise / 2.))
                stateL.append((self.stateList[index - 1], self.noise / 2.))
            elif index == 0:
                stateL.append((self.stateList[index], self.noise))
                stateL.append((self.stateList[index + 1], 1 - self.noise))
            else:
                stateL.append((self.stateList[index - 1], self.noise / 2.))
                stateL.append((self.stateList[index], self.noise / 2.))
                stateL.append((self.stateList[index + 1], 1 - self.noise))
        
        return stateL

    def getNextStateWithActionNoNoise(self, state, action):
        index = state.getIndex()
        if action == 'left':
            index = index - 1
        elif action == 'right':
            index = index + 1 
        if index < 0 or index >= self.width:
            index = state.getIndex()
        return self.stateList[index]

    def getNextStateWithAction(self, state, action):
        """
        Input current state and action
        Return next state
        """
        index = state.getIndex()
        invokeResult = np.random.choice(list(self.resultType.keys()), 1, p=list(self.resultType.values()))[0]
        if invokeResult == 'reverse':
            if action == 'left':
                action = 'right'
            else:
                action = 'left'
        elif invokeResult == 'stay':
            action = 'stay'
        return self.getNextStateWithActionNoNoise(state, action)

    def getPossibleActions(self, state):
        """
        Return a list of legal action
        """
        actions = list()
        if not state.isTerminal(): # not terminal state
            actions.append('left')
            actions.append('right')
        return actions

    def getRestartState(self):
        """
        Exclude terminal state
        """
        index = np.random.randint(self.width - 1)
        return self.stateList[index]

    def getReward(self, state, action, nextState):
        return nextState.getReward()

    def isTerminal(self, state):
        return state.isTerminal()

    def state2feature(self, state):
        feature = [1.0 if (i == state.getIndex()) else 0.0 for i in range(self.width)]
        return feature

    def action2feature(self, action):
        feature = list()
        if action == 'left':
            feature.append(-1)
        elif action == 'right':
            feature.append(1)
        return feature
