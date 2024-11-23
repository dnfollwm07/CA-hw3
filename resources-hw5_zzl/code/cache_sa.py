
# Write team member names here:


'''
Base class file for building a set-associative cache
Credit: R. Martin (W&M), A. Jog (W&M), Ramulator (CMU)
'''

import numpy as np
from math import log
import random


class Cache:
    def __init__(self, cSize, ways=2, bSize=4):
        '''
        Keep ways > 1 to keep the cache set associative
        '''

        if(ways < 2):
            print("Emulating a Direct mapped Cache!")

        self.cacheSize = cSize  # Bytes
        self.ways = ways        # Default: 2 way (i.e., set associative)
        self.blockSize = bSize  # Default: 4 bytes (i.e., 1 word block)
        self.sets = cSize // bSize // ways

        self.blockBits = 0
        self.setBits = 0

        if (self.blockSize != 1):
            self.blockBits = int(log(self.blockSize, 2))

        if (self.sets != 1):
            self.setBits = int(log(self.sets, 2))

        self.cache = np.zeros((self.sets, self.ways, self.blockSize), dtype=np.int64)
        self.cache = self.cache - 1

        self.metaCache = np.zeros((self.sets, self.ways), dtype=np.int64)
        self.metaCache = self.metaCache - 1

        self.hit = 0
        self.miss = 0
        self.hitlatency = 5 # cycle

    def reset(self):
        self.cache = np.zeros((self.sets, self.ways, self.blockSize), dtype=np.int64)
        self.cache = self.cache - 1

        self.metaCache = np.zeros((self.sets, self.ways), dtype=np.int64)
        self.metaCache = self.metaCache - 1

        self.hit = 0
        self.miss = 0

    '''
    Warning: DO NOT EDIT ANYTHING ABOVE THIS LINE
    '''

    '''
    Returns the set number of an address based on the policy discussed in the class
    Do NOT change the function definition and arguments
    '''

    def find_set(self, address):
        set_mask = (1 << self.setBits) - 1
        return (address >> self.blockBits) & set_mask

    '''
    Returns the tag of an address based on the policy discussed in the class
    Do NOT change the function definition and arguments
    '''

    def find_tag(self, address):
        return address >> (self.blockBits + self.setBits)

    '''
    Search through cache for address
    return True if found
    otherwise False
    Do NOT change the function definition and arguments
    '''

    def find(self, address):
        set_number = self.find_set(address)
        tag = self.find_tag(address)

        for way in range(self.ways):
            if self.metaCache[set_number][way] == np.int64(tag):
                self.hit += 1
                # update lru
                self.move_element_to_head(self.metaCache[set_number], way)
                self.move_element_to_head(self.cache[set_number], way)
                return True

        self.miss += 1
        return False

    '''
    Load data into the cache. 
    Something might need to be evicted from the cache and send back to memory
    Do NOT change the function definition and arguments
    '''

    def load(self, address):
        set_number = self.find_set(address)
        tag = self.find_tag(address)

        use_way = -1
        # Check if there is an empty spot in the set
        for way in range(self.ways):
            if self.metaCache[set_number][way] == 0:
                use_way = way
                break

        # If no empty spot, use LRU replacement policy to evict one
        # The end of the array is the least recently used
        if use_way == -1:
            use_way = self.ways - 1
        self.metaCache[set_number][use_way] = np.int64(tag)
        # Load a dummy block of data (for simplicity, not simulating real data)
        self.cache[set_number][use_way] = np.zeros(self.blockSize, dtype=np.int64)

        # update lru
        self.move_element_to_head(self.metaCache[set_number], use_way)
        self.move_element_to_head(self.cache[set_number], use_way)

    def move_element_to_head(self, arr, index):
        """
           Moves the specified element in a NumPy array to the beginning of the array.
       """
        if index == 0:
            return arr
        target = arr[index]
        for i in range(index - 1, -1, -1):
            arr[i + 1] = arr[i]
        arr[0] = target
        return arr