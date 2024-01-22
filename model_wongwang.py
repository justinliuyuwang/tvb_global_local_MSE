import sys, os, time
import numpy as np
import showcase1_ageing as utils
from tvb.simulator.lab import *
from tvb.simulator.backend.nb_mpr import NbMPRBackend
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import resource
import time
import fcntl




def get_connectivity(scaling_factor):


        conn = connectivity.Connectivity.from_file("connectivity_76.zip")
        #74, 75, 52, 53
        conn.weights = conn.weights / scaling_factor
        conn.tract_lengths = np.ones_like(conn.weights)
        conn.centers = np.zeros(np.shape(conn.weights)[0])
        indices = [73, 74, 51, 52]  # Adjusted for 0-indexing
        conn.weights = conn.weights[np.ix_(indices, indices)]
        conn.tract_lengths = conn.tract_lengths[np.ix_(indices, indices)]
        conn.centers = conn.centers[indices]

        conn.speed = np.r_[np.Inf]
        return conn

def process_sub(my_noise,my_G,Jn,Ji,Wp):
    
    my_magic=1  # TO EDIT
    my_dt=1.0  # TO EDIT

    #start_time = time.time()
    rww = models.DecoBalancedExcInh()
    if not Jn==0:
        print("Jn")
        rww = models.DecoBalancedExcInh(J_N=np.array([Jn]))
        my_noise=1e-5
    elif not Ji==0:
        print("Ji")
        rww = models.DecoBalancedExcInh(J_i=np.array([Ji]))
        my_noise=1e-5
    elif not Wp==0:
        print("Wp")
        rww = models.DecoBalancedExcInh(w_p=np.array([Wp]))
        my_noise=1e-5
    elif not my_G==0:
        print("G")
        rww = models.DecoBalancedExcInh(G=np.array([my_G, ]))
        my_noise=1e-5
    elif not my_noise==0:
        print("noise")
        rww = models.DecoBalancedExcInh()
        my_noise=my_noise
    else:
        print("default")
        rww = models.DecoBalancedExcInh()
        my_noise=1e-5

                        
    #my_G=0.01
    #my_noise=1e-5
    #my_dt=1

    rww = models.DecoBalancedExcInh()

    sim = simulator.Simulator(
        model=rww,
        #connectivity=connectivity.Connectivity.from_file(),
        connectivity=get_connectivity(1),
        #coupling=coupling.Linear(a=numpy.array([0.5 / 50.0])),
        coupling=coupling.Linear(a=np.array([0.00390625])),
        integrator=integrators.EulerStochastic(dt=my_dt, noise=noise.Additive(nsig=np.array([my_noise]))), #1e-5
        monitors=(monitors.TemporalAverage(period=1.),),
        simulation_length=9e3
    ).configure()

    #TODO MAY NEED TO CHANGE HOW get_connectivity gets from file


    (time, data), = sim.run()
    print(np.shape(time))
    return(time,data)


