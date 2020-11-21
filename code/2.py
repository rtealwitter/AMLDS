import math
import statistics
from scipy.stats import norm

# Most extreme distribution based on plot
extreme_threshold = [1,.75,.5,.25,-.25,-.5,-.75,-1]
extreme_proportion = [.01,1.99,14,34,34,14,1.99,.01]

# Variance of most extreme distribution
extreme_sample = []
for i in range(len(extreme_threshold)):
    reps = int(100*extreme_proportion[i])
    extreme_sample += reps*[extreme_threshold[i]]

extreme_var = statistics.variance(extreme_sample)

# Find CDF of near-duplicate with most extreme variance
prob_near = 1 - norm.cdf(x=.98, loc=0, scale=math.sqrt(extreme_var))

# Worst-case distribution for cosine similarity
worst_threshold = [.98,.98,.75,.5,.25,0,-.25,-.5,-.75]
worst_proportion = [prob_near,.01-prob_near,1.99,14,34,34,14,1.99,.01]

def hit_prob(v, r, t):
    ''' Probability q with v is found with r bands and t tables '''
    theta = math.acos(v)
    return 1 - (1 - (1 - theta/math.pi)**r)**t

def expected_candidate(i, r, t):
    ''' 
    Expected candidates with cosine similarity v
    found with r bands and t tables
    '''
    v = worst_threshold[i]
    # multiply by 10,000,000 since proportion
    # is already multipled by 100
    return hit_prob(v,r,t)*worst_proportion[i] * 10000000

def expected(r,t):
    ''' Expected total candidates found with r bands and t tables '''
    expected = 0
    for i in range(len(worst_threshold)):
        expected += expected_candidate(i,r,t)
    return expected

# Find minimum number of tables t such that no more
# than 1,000,000 near-duplicate candidates are checked
# on average subject to the probability of a near-duplicate
# hit staying above .99

def satisfy1():
    for t in range(1,100):
        for r in range(1,100):
            if hit_prob(.98, r,t) >= .99:
                if expected_candidate(0,r,t) <= 1000000:
                    print(r, t)
                    # Number of bands r=1, number of tables t=2
                    print(round(hit_prob(.98, 1,2), 3))
                    # 0.996 proportion of near duplicates checked
                    print(round(expected_candidate(0,1,2)))
                    # 38198 near duplicates checked on average
                    return

satisfy1()

# Find minimum number of tables t such that no more
# than 200,000 total candidates are checked
# on average subject to the probability of a near-duplicate
# hit staying above .99

def satisfy2():
    for t in range(1,100):
        for r in range(1,100):
            if hit_prob(.98, r,t) >= .99:
                if expected(r,t) <= 200000:
                    print(r, t)
                    # Number of bands r=35, number of tables t=44
                    print(round(hit_prob(.98, 35, 44),3))
                    # 0.990 proportion of near duplicates checked
                    print(round(expected(35,44)))
                    # 196100 candidates checked on average
                    return

satisfy2()