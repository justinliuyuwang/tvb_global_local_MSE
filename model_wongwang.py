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
        conn.weights = conn.weights / scaling_factor
        conn.tract_lengths = np.ones_like(conn.weights)
        conn.centers = np.zeros(np.shape(conn.weights)[0])
        conn.speed = np.r_[np.Inf]
        return conn

def process_sub(my_noise,my_G,Mi,Jn,Ji,Wi,We):
    
    my_magic=1  # TO EDIT
    my_dt=1.0  # TO EDIT

    #start_time = time.time()
    rww = models.DecoBalancedExcInh()
    if not Mi==0:
        print("Mi")
        rww = models.DecoBalancedExcInh(M_i=np.array([Mi]),G=np.array([1.0, ]))
    elif not Jn==0:
        print("Jn")
        rww = models.DecoBalancedExcInh(J_N=np.array([Jn]),J_i=np.array([Ji]),G=np.array([1.0, ]))
    elif not Wi==0:
        print("Wi")
        rww = models.DecoBalancedExcInh(W_i=np.array([Wi]),W_e=np.array([We]),G=np.array([1.0, ]))

    #my_G=0.01
    #my_noise=1e-5
    #my_dt=1

    rww = models.DecoBalancedExcInh()

    sim = simulator.Simulator(
        model=rww,
        connectivity=connectivity.Connectivity.from_file(),
        #coupling=coupling.Linear(a=numpy.array([0.5 / 50.0])),
        coupling=coupling.Linear(a=np.array([my_G])),
        integrator=integrators.EulerStochastic(dt=my_dt, noise=noise.Additive(nsig=np.array([my_noise]))), #1e-5
        monitors=(monitors.TemporalAverage(period=1.),),
        simulation_length=5e3
    ).configure()

    #TODO MAY NEED TO CHANGE HOW get_connectivity gets from file


    (time, data), = sim.run()
    return(time,data)


