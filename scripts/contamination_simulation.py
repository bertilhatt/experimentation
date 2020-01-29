'''
If you run a dozen experiments at the same time, assuming each
splits the traffic in two, this means that you have
2^12 = 4,098 subsegments.You can split an audience of hundreds
of thousands in 4,000 segments and not risk significant contami-
nation. If you were to run 30 experiments, your traffic would have
to be split into more than a billion possible sub-segments. Those
can be uneven and still aggregate into non-contaminated, indepen-
dent segments but the likelihood of seeing a pair with more over-
lap than we‘d like increases.

The following sample simulation estimates that
* based on a sample of 10,000 individuals, for:
  - 10 simultaneous experiments, the worst overlap is around 2.24%
  - 20 experiments: 2.89%
  - 50 experiments: 3.27%
  - 100 experiments: 3.87%

* 30,000 individuals:
  - 10 experiments: 1.15%
  - 20 experiments: 1.58%
  - 50 experiments: 1.95%
  - 100 experiments: 2.06%

* 60,000 individuals :
  - 10 experiments: 0.86%
  - 20 experiments: 1.06%
  - 50 experiments: 1.38%
  - 100 experiments: 1.51%

* 100,000 individuals:
- 10 experiments: 0.711%
- 20 experiments: 0.915%
- 50 experiments: 1.044%
- 100 experiments: 1.119%

Therefore, if you run 20 experiments at the same time, you could
have two that slightly overlap, by 0.86%. If the most promising
increases conversion rate by, say around 2.5%, then we are over-
estimating the impact of the other experiment by 0.0215% or about
one order over the 5,000 or so orders, the order of magnitude of
orders that most of your experiments consider. This is an order of
magnitude less than a common minimum detectable effect (MDE). In 
that case, it is unlikely that this would have a material impact
on the other experiment. To prevent this from happening, you can
monitor  experiments for such an overlap. It makes sense to be
careful and prepare for running far more experiments at once.
'''

import numpy as np
import pandas as pd
import random

def simulate(n, k):
    df = pd.DataFrame(np.random.randn(n, k))
    df = (df > 0)
    c = pd.Series()
    for i in range(k):
        for j in range(i):
            c = c.append(pd.Series(
                df[i].corr(df[j])
            ))
    return max(c)

def multi_simulate(n, k, l, verbose=False):
    m = []
    for ll in range(l):
        if verbose:
            print(ll)
        np.random.seed(ll)
        m.append(simulate(n, k))
    return np.mean(m)

n = 10_000
k_list = [10, 20, 50, 100]
l = 10

def main(n=n, k_list=k_list, l=l, verbose=False):
    print("n = {}".format(str(n)))
    r = {}
    for k in k_list:
        if verbose:
            print(k)
        r[k] = multi_simulate(n, k, 10, verbose)
    print(r)
