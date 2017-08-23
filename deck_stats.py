# deck_stats.py

import matplotlib.pyplot as plt
%matplotlib inline
import numpy as np
import scipy.misc as sm
import collections

class deck_stats(object):
    '''This class is used to run simple probability statistics with a deck of created cards. The deck of cards
       can be made of any number of any type of card, and can be defined at each instance of the class.
       
       Initial publishing: August 23, 2017'''
    
    def __init__(self,names,distro='manual'):
        
        if type(names) is list:
            self.names = names # Distribution of card types, as a list.
        else:
            raise TypeError('names is not a list, cannot parse card types in deck.')
        
        # Set number of each (distribution of deck), either manually or as list.
        if type(distro) is list:
            self.distro = distro
        else:
            self.distro = []
            for i,name in enumerate(names):
                self.distro.append(int(input('How many %s?   '%name)))
        
        # Create dictionary of card names and identifying numeric keys:
        self.deck = [] # <--this will be the master namelist for the dexk; 3 'calico' will actually be 
                        # 3 'calico' instances.
        for i,name in enumerate(names):
            for x in range(self.distro[i]):
                self.deck.append(name) # <--this is the actual deck! List of strings.
    
    def subsetisin(self,subset,largeset):
        
        for i,check in enumerate(subset):
            if check in largeset:
                location = largeset.index(check)
                del largeset[location]
                isin = True
            else:
                isin = False
                break
                
        if isin == True:
            return True
        else:
            return False
    
    def draw(self,ndraw):
        '''Draws n cards from the deck, without replacement.'''
        
        drawn_cards = np.random.choice(len(self.deck),ndraw,replace=False) # <--indices of drawn cards.
        
        return [self.deck[i] for i in drawn_cards] # <--list of drawn cards.
    
    def specific_probability(self,ndraw,criteria,ntrials=10000):
        
        trials = []
        for i in range(ntrials):
            hand = self.draw(ndraw)
            #print(hand)
            trials.append(self.subsetisin(criteria,hand))
        trials = np.array(trials)
        
        if (np.count_nonzero(trials)/ntrials)==0.0:
            print(criteria)
        
        return (np.count_nonzero(trials)/ntrials)
    
    def uups(self,n,k):
        '''Unordered, unreplaced number of possible sets.'''

        num = sm.factorial(n)
        den = sm.factorial(k)*sm.factorial(n-k)

        return num/den
    
    def card_weights_frequentist(self,ndraw,ntrials=1000,nrep=1):
        
        weights = np.empty((nrep,len(self.names)))
        for rep in range(nrep):
            for i,name in enumerate(self.names):
                weights[rep,i] = self.specific_probability(ndraw,[name],ntrials)
        weights = np.around(np.mean(weights,axis=0),decimals=4)
            
        return dict(zip(self.names,weights))
    
    def card_weights_combinatoric(self,ndraw):
        
        weights = []
        decksize = sum(self.distro)
        for i,name in enumerate(self.names):
            weights.append(1.0-(self.uups(decksize-self.distro[i],ndraw)/self.uups(decksize,ndraw)))
            
        return collections.OrderedDict(zip(self.names,weights))
