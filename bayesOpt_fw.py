from bayes_opt import BayesianOptimization
from bayes_opt.observer import JSONLogger
from bayes_opt.event import Events
from bayes_opt.util import load_logs
from bayes_opt import UtilityFunction
import sched, time
import subprocess

def tmdd_obj_discrete(k,n,s,m,c):
    """
    evaluation of tm-dd here,
    communicate with xix code
    using some polynomial function as reference
    """
    # write parameter
    paramFile = "C:/Users/taiseii/Documents/BEP/xPeriment/paramNresult/param.in"
    paramFileOpn = open(paramFile, "w")
    paramList = [str(k),str(m),str(n),str(s),str(c)]
    for p in paramList:
        paramFileOpn.write(p)
        paramFileOpn.write("\n")
    paramFileOpn.close()

    # start jar file tmDD call here
    subprocess.call(['java','-jar','tmDD_1.jar'])
    
    # read result
    resultFile = "C:/Users/taiseii/Documents/BEP/xPeriment/paramNresult/result.out"

    accuracy = None
    print(open(resultFile, "r").read())
    accuracy2 = float(open(resultFile, "r").read())

    # while not open(resultFile, "r").read():
    #     # print("No result yet")
    #     accuracy = open(resultFile, "r").read()
    # # open(resultFile, "w").close()
    # print(accuracy)
    # assert type(k) == int

    # returnVal = float(accuracy)
    # 4*k**3 + 3*m**2 -2*n + 10+s - c*s
    return float(accuracy2)

# k is a discrete value needed to be treated slighlt differently
def tmdd_obj(k, n, s, m, c):
    kd = int(k)
    return tmdd_obj_discrete(kd,n,s,m,c)

bounds = {'k':(1,100), 'n':(1,1000),'s':(1,1000),'m':(1,1000), 'c':(1,1000),}

optimizer = BayesianOptimization(
    f=None,
    pbounds=bounds,
    verbose=2,
    random_state=1,
)

# acquisition function(expected improvement)
utility = UtilityFunction(kind="ucb", kappa=2.5, xi=0.0)
# gaussian process tuning
optimizer.set_gp_params(alpha=1e-3)

logger = JSONLogger(path="./logs_1.json")

for _ in range(10):
    next_probing_point = optimizer.suggest(utility)
    print("Next point to probe is:", next_probing_point)
    target = tmdd_obj(**next_probing_point)
    print("Found the target value to be:", target)
    optimizer.register(
    params=next_probing_point,
    target=target,)
    optimizer.subscribe(Events.OPTMIZATION_STEP, logger)
print("optimum is: ",optimizer.max)