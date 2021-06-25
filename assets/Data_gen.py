from controls import pool_dict, possible_failures, RECIPES
import pandas as pd
import random as rd
import datetime

pool_temp = pd.DataFrame()
for pool in pool_dict[1:]:
    poolname = pool['label']
    t = rd.randint(20, 80)
    tlist = []
    for x in range(30):
        num = rd.gauss(t, 5)
        tlist.append(num)
    pool_temp[poolname] = tlist


poolname = []
units = []
surf = []
kg = []
time = []
nottime = []
for pool in pool_dict[1:]:
    poolname.append(pool['label'])
    unit = rd.randint(5, 30)
    units.append(unit)
    surf.append(unit*rd.gauss(80, 20))
    kg.append(unit*rd.gauss(400, 100))
    r = abs(19 - rd.gauss(10, 5))
    time.append(r if 0 < r < 24 else 24)
    nottime.append(24 - r)
pool_uses = pd.DataFrame({'Pool': poolname, 'Units': units, 'Surface': surf, 'Weight': kg,
                          'Time': time, 'Nottime': nottime})
pool_uses.set_index('Pool')


times = [rd.randint(1, 10) for fail in possible_failures]
failures = pd.DataFrame({'Failure': possible_failures, 'Times': times})


times = [rd.randint(1, 7) for recip in RECIPES]
recipes_used = pd.DataFrame({'Recipe': RECIPES, 'Times': times})


recipe = [rd.choice(RECIPES) for _ in range(76)]
day = [datetime.datetime(2021, 5, 1) + datetime.timedelta(rd.randint(1, 30)) for _ in range(76)]
shift = [rd.choice(['MS', 'AS', 'NS']) for _ in range(76)]
production = {'Recipe': recipe, 'Day': day, 'Shift': shift}
real_production = pd.DataFrame(production)
