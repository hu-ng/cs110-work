# Professor, prior to running the code, you have to install the following packages: bitarray and mmh3.
# mmh3 requires Microsoft C++ Build Tools to install and run.

from bitarray import bitarray  # Makes it easier to implement setting up the bit array for the filter
import math  # Needed to implement the theoretical functions that the class constructor uses
import mmh3  # One of the main powerhouses of my implementation with the ability to create different hash results given different seeds
import random  # The random module is used to generate the seeds for MurmurHash and to help with creating plots
import matplotlib.pyplot as plt

class bloom(object):
    def __init__(self, capacity, fp_rate):
        """Create a bloom filter that is optimized for a specified capacity and desired false positive rate.
            The actual false positive rate will be around the imposed rate."""

        # Check capacity and fp_rate to see if the bloom object is created correctly or  not
        if not capacity > 0:
            raise ValueError("You must have something in the filter!")
        if not 0 < fp_rate < 1:
            raise ValueError("The desired false positive rate must be between 0 and 1")

        # The capacity of the filer
        self.capacity = capacity

        # The current number of items in the filter
        self.item_count = 0

        # The size of the bit array
        self.size = self.get_size(capacity, fp_rate)

        # The number of hash functions we are using
        self.hashfs = self.get_hash(fp_rate)

        # The seeds that murmurhash will use
        self.seeds = self.get_seeds(self.hashfs)

        # Initialize the bit array according to self.size
        self.array = bitarray(self.size)
        self.array.setall(0)

    @classmethod
    def get_size(cls, n, p):
        """Return the optimal size for the bit array based on capacity and false positive rate"""
        # m = bit array size is derived from the optimal theoretical relationship between m, n = capacity, and p = false positive rate
        m = -(n*math.log(p)) / ((math.log(2))**2)
        return int(m)  # int() is used to make sure that the bit array size does not have decimals

    @classmethod
    def get_hash(cls, p):
        """Return the optimal number of hash functions the filter should use based on the false positive rate input"""
        k = -math.log(p, 2)   # This is identical to k = (m/n)*math.log(2)
        if k < 1:
            # If p > 0.5, 0 < k < 1. ceil() is used to make sure the code always have at least 1 hash function.
            return math.ceil(k)
        else:
            # If k > 1, int makes sure k is an integer
            return int(k)

    @classmethod
    def get_seeds(cls, k):
        """Randomly generates seeds depending on the number of hash functions we are using"""
        # The call to random.sample() will generate k unique numbers in the range specified.
        # Unique numbers helps us generate unique murmur hash functions.
        seeds = random.sample(range(10**8), k)
        return seeds  # Returns a list

    def insert(self, item):
        """Add the item to the filter"""
        if self.item_count == self.capacity:
            # Check first to see if the filter is already at capacity.
            print("Filter is at capacity!")
            return

        # murmur hash only accepts strings, so this turns non-strings into strings
        if type(item) != str:
            item = str(item)

        for i in self.seeds:
            # For every seed in self.seeds, a new murmur hash is made.
            bit_index = mmh3.hash(item, i) % self.size  # Computes the index in the bit array
            self.array[bit_index] = True  # Turn the bit value at the index to True
        self.item_count += 1  # Increment the item counter

    def check(self, item):
        """Test for the membership of the item"""
        # Same operation as above to turn non-strings -> strings
        if type(item) != str:
            item = str(item)

        for i in self.seeds:
            bit_index = mmh3.hash(item, i) % self.size
            if self.array[bit_index] is False:
                # If only 1 index found is False, then the item is definitely not in the set
                return False
        return True  # After all the indices are checked and none are False, return True


def plot_mem_fp():
    """Creates a plot of memory usage with regards to the false positive rate.
        The false positive rate is divided into 1000 intervals and the capacity is held at 1000 items"""

    # These lists will hold the bit array sizes of three filters as the false positive rate changes
    memory1 = []
    memory2 = []
    memory3 = []

    # The imposed false positive rate is divided into 1000 intervals
    fp = [(1/1000)*i for i in range(1, 1000)]
    for i in fp:
        # At each interval, 3 filters are created with increasing capacities
        filter1 = bloom(1000, i)
        filter2 = bloom(3000, i)
        filter3 = bloom(6000, i)

        # The memory (bit array size) created based on the capacity and false positive rate of each filter is appended
        memory1.append(filter1.size)
        memory2.append(filter2.size)
        memory3.append(filter3.size)

    # The memory usage of three filters is graphed on the same plot as a function of false positive rate
    plt.plot(fp, memory1, color = 'red', label = 'Capacity = 1000')
    plt.plot(fp, memory2, color = 'blue', label = 'Capacity = 3000')
    plt.plot(fp, memory3, color = 'green', label = 'Capacity = 6000')
    plt.xlabel('False positive rate')
    plt.ylabel('Memory usage (in bits)')
    plt.legend()
    plt.show()


def plot_mem_cap():
    """Creates a plot of memory usage with regards to capacity. Values for capacity are in an increasing list from 1 to 10000.
        The false positive rate is held at 0.2"""
    memory1 = []
    memory2 = []
    memory3 = []

    capacity = [i for i in range(1, 10000)]
    for i in capacity:
        filter1 = bloom(i, 0.2)
        filter2 = bloom(i, 0.4)
        filter3 = bloom(i, 0.6)

        memory1.append(filter1.size)
        memory2.append(filter2.size)
        memory3.append(filter3.size)

    plt.plot(capacity, memory1, color = 'red', label = 'FP rate = 0.2')
    plt.plot(capacity, memory2, color = 'blue', label = 'FP rate = 0.4')
    plt.plot(capacity, memory3, color = 'green', label = 'FP rate = 0.6')
    plt.xlabel('Number of elements stored')
    plt.ylabel('Memory usage (in bits)')
    plt.legend()
    plt.show()


def plot_fp():
    """Plotting the actual false positive rate as a function of theoretical false positive rate"""
    # Holds the averaged actual false positive rate for each interval of theory_rate
    actual_rate = []

    # The input false positive rate is divided into 200 intervals
    theory_rate = [(1/200)*i for i in range(1, 200)]
    for i in theory_rate:

        # This holds values to be averaged
        result_trial = []

        for trial in range(20):  # Run the test 20 times at each i interval
            total_negative = 0  # Total number of negatives
            false_true = 0  # Total number of false positives
            filter = bloom(1000, i)   # Create a bloom filter for the specific i
            data = random.sample(range(100000), 1000)  # This is the data set we will put in the filter
            test = random.sample(range(100000), 1000)  # This is the data used to check the filter

            for x in data:
                filter.insert(x)  # Insert all the data from data
            for y in test:
                if filter.check(y) == False:  # Check every element of test with the bloom filter
                    total_negative += 1  # If False, increment total negatives
                else:
                    if y not in data:  # If True, check to see if the element of y exists in data
                        false_true += 1  # If not, increment total false positives and total negatives
                        total_negative += 1
            fp_rate = false_true/total_negative  # Calculate the false positive rate of THIS trial.
            result_trial.append(fp_rate)

        # Calculate the average result of all trials for THIS i interval
        avg_result = sum(result_trial)/len(result_trial)
        actual_rate.append(avg_result)  # Append the final result for THIS i interval to actual_rate.

        # Rinse and repeat for other intervals

    plt.plot(theory_rate, actual_rate)
    plt.xlabel('Theoretical false positive rate')
    plt.ylabel('Actual false positive rate')
    plt.show()