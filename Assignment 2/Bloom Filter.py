from bitarray import bitarray
import math
import mmh3
import random
import time
import matplotlib.pyplot as plt

class bloom(object):
    def __init__(self, capacity, fp_rate): #bloom(1000, 0.03)
        """Create a bloom filter that is optimized for a specified capacity and false positive rate"""
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
        self.hashfs = self.get_hash(fp_rate)  # or fp_rate self.size, capacity

        # The seeds that murmurhash will use
        self.seeds = self.get_seeds(self.hashfs)

        # Initialize the array
        self.array = bitarray(self.size)
        self.array.setall(0)

    @classmethod
    def get_size(cls, n, p):
        """Return the optimal size for the bit array based on input"""
        m = -(n*math.log(p)) / ((math.log(2))**2)
        return int(m)  # math.ceil to it

    @classmethod
    def get_hash(cls, p):
        """Return the optimal number of hash functions the filter should use"""
        k = -math.log(p, 2)   # This is similar to k = (m/n)*math.log(2) -math.log(p, 2)
        return int(k)   # math.ceil to it

    @classmethod
    def get_seeds(cls, k):
        """Randomly generates seeds depending on the number of hash functions we are using"""
        seeds = []
        for i in range(k):
            seeds.append(random.randint(0, 1000000))  # might be a chance that seeds are the same
        return seeds

    def insert(self, item):
        """Add the item to the set in the filter"""
        if self.item_count == self.capacity:
            print("Filter is at capacity!")
            return

        if type(item) == int:
            item = str(item)

        for i in self.seeds:
            bit_index = mmh3.hash(item, i) % self.size
            self.array[bit_index] = True
        self.item_count += 1

    def check(self, item):
        """Test for the membership of the item"""
        if type(item) == int:
            item = str(item)

        for i in self.seeds:
            bit_index = mmh3.hash(item, i) % self.size
            if self.array[bit_index] is False:
                # If only 1 index is False, then the item is not in the set
                return False
        return True


def plot_mem_fp():
    """Creates a plot of memory usage with regards to the false positive rate.
        The false positive rate is divided into 1000 intervals and the capacity is held at 1000 items"""
    memory = []
    fp = [(1/1000)*i for i in range(1, 1000)]
    for i in fp:
        filter = bloom(1000, i)
        memory.append(filter.size)
    plt.plot(fp, memory)
    plt.xlabel('False positive rate')
    plt.ylabel('Memory usage (in bits)')
    plt.show()


def plot_mem_cap():
    """Creates a plot of memory usage with regards to capacity. Values for capacity are in an increasing list from 1 to 10000.
        The false positive rate is held at 0.2"""
    memory = []
    capacity = [i for i in range(1, 10000)]
    for i in capacity:
        filter = bloom(i, 0.2)
        memory.append(filter.size)
    plt.plot(capacity, memory)
    plt.xlabel('Number of elements stored')
    plt.ylabel('Memory usage (in bits)')
    plt.show()


def plot_time_fp():
    # Fp is the independent variable, capacity is held constant
    # Two cases: at capacity, not at capacity
    access_time = []
    fp = [(1 / 1000) * i for i in range(1, 1000)]
    for i in fp:
        time_list = []
        filter = bloom(2000, i)
        for x in range(2000):
            filter.insert(x)
        for x in range(2000):
            start = time.time()
            filter.check(x)
            duration = time.time() - start
            time_list.append(duration)
        access_time.append(sum(time_list)/len(time_list))
    plt.plot(fp, access_time)
    plt.xlabel('False positive rate')
    plt.ylabel('Access time (time to run the "check" operation)')
    plt.show()



def plot_time_cap():
    # Capacity is the independent variable, fp is held constant at 0.2
    # Two cases: at capacity, not at capacity
    access_time = []
    capacity = [i for i in range(1, 1000)]
    for i in capacity:
        filter = bloom(i, 0.2)
        time_list = []
        for x in range(i):
            filter.insert(x)
        for x in range(i):
            start = time.time()
            filter.check(x)
            duration = time.time() - start
            time_list.append(duration)
        access_time.append(sum(time_list) / len(time_list)) # the average time to search for an element in that filter

    plt.plot(capacity, access_time)
    plt.xlabel('Number of items stored (capacity)')
    plt.ylabel('Access time (time to run the "check" operation)')
    plt.show()


def plot_fp():
    """Plotting the actual false positive rate as a function of theoretical false positive rate"""
    actual_rate = []
    theory_rate = [(1 / 1000) * i for i in range(1, 1000)]
    for i in theory_rate:
        total_true = 0
        false_true = 0
        filter = bloom(1000, i)
        data = random.sample(range(100000), 1000)
        for x in data:
            filter.insert(x)
        test = random.sample(range(100000), 1000)
        for y in test:
            if filter.check(y) == True:
                total_true += 1
                if y not in data:
                    false_true += 1
        fp_rate = false_true/total_true
        actual_rate.append(fp_rate)
    plt.plot(theory_rate, actual_rate)
    plt.xlabel('Theoretical false positive rate')
    plt.ylabel('Actual false positive rate')
    plt.show()

def plot_fpv2():
    """Plotting the actual false positive rate as a function of theoretical false positive rate"""
    actual_rate = []
    theory_rate = [(1/100)*i for i in range(1, 50)]
    data = random.sample(range(100000), 1000)
    test = random.sample(range(100000), 1000)
    for i in theory_rate:
        total_negative = 0
        false_true = 0
        filter = bloom(1000, i)
        for x in data:
            filter.insert(x)
        for y in test:
            if filter.check(y) == False:
                total_negative += 1
            else:
                if y not in data:
                    false_true += 1
        fp_rate = false_true/total_negative
        actual_rate.append(fp_rate)
    plt.plot(theory_rate, actual_rate)
    plt.xlabel('Theoretical false positive rate')
    plt.ylabel('Actual false positive rate')
    plt.show()

def plot_fpv3():
    """Plotting the actual false positive rate as a function of theoretical false positive rate"""
    actual_rate = []
    theory_rate = [(1/100)*i for i in range(1, 50)]
    data = [i for i in range(0, 1000)]
    not_data = [i for i in range(1000, 1500)]
    random.shuffle(data)
    random.shuffle(not_data)
    test_words = data[:500] + not_data
    for i in theory_rate:
        total_negative = 0
        false_true = 0
        filter = bloom(1000, i)
        for x in data:
            filter.insert(x)
        for y in test_words:
            if filter.check(y) == False:
                total_negative += 1
            else:
                if y in not_data:
                    false_true += 1
                    total_negative += 1
        fp_rate = false_true/total_negative
        actual_rate.append(fp_rate)
    plt.plot(theory_rate, actual_rate)
    plt.xlabel('Theoretical false positive rate')
    plt.ylabel('Actual false positive rate')
    plt.show()


plot_fpv3()