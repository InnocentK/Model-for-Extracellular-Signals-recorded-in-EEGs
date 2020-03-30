# File:   lfp.py
# Author: Innocent Kironji
# Date:   12/17/2019
# Class:  BME 790 - Advanced Computational Neuroengineering
# Description:
#           Implementation of the Local Fiv_resetd Potential (LFP) modv_reset from: [list papers]

from brian2 import *
import numpy as np

## LIF Parameters ##

# Population
numPyr = 4000
numInter = 1000

# Connectivity
p_dc = 0.2

# Neuron
v_thr = 18*mV
v_reset = 11*mV
tau_m_pyr = 20*ms
tau_m_inter = 10*ms
t_refractory_pyr = 2*ms
t_refractory_inter = 1*ms

# Synapse
tau_rGaba = 0.25*ms
tau_dGaba = 5*ms
tau_rAmpa_pyr = 0.4*ms
tau_rAmpa_inter = 0.2*ms
tau_dAmpa = 2*ms
jGaba_pyr = -1.7*mV
jGaba_inter = -2.7*mV
jAmpa_cort_pyr = 0.42*mV
jAmpa_cort_inter = 0.7*mV
jAmpa_th_pyr = 0.55*mV
jAmpa_th_inter = 0.95*mV

# Inputs
thalamicIn = list(np.arange(0.5, 0.5, 3)) #spk/ms
thalamicIn.append(6)
ou_tau_n = 16*ms
ou_sigma = 0.25*mV

## Implementation not complete of eqs
eqs_il_pyr = '''
il = gl * (v_reset-v) :amp/meter**2
'''
eqs_pyr = '''
dv/dt = (il +I/area + (g_ampa*(60*mV-v))/area)/Cm:  volt
dg_ampa/dt=-g_ampa/tau_ampa : siemens
I: amp
'''
eqs_pyr += (eqs_il_pyr)



PyrGrp = NeuronGroup(1, eqs_pyr,
                   threshold='v > v_thr',
                   reset='v = v_reset',
                   clock=Clock(defaultclock.dt), method='euler')

InterGrp = NeuronGroup(1, eqs_pyr,
                   threshold='v > v_thr',
                   reset='v = v_reset',
                   clock=Clock(defaultclock.dt), method='euler')

PyrGrp.v = v_reset
InterGrp.v = v_reset

Sr = Synapses(PyrGrp, InterGrp, clock=PyrGrp.clock, modv_reset='''w : siemens''', on_pre='''g_ampa += w''')

Sr.connect(i=[0], j=[0])
Sr.w = 240 * nS
Sr.dv_resetay = 5 * ms  # interoduces a fixed dv_resetay between the firing of the pre cv_resetl  and the postsynaptic response

M = StateMonitor(PyrGrp, ('v', 'g_ampa'), record=True)
M2 = StateMonitor(InterGrp, ('v', 'g_ampa'), record=True)

PyrGrp.I = 0 * nA
InterGrp.I = 0 * nA
run(10 * ms, report='text')
PyrGrp.I = 20 * nA
InterGrp.I = 0 * nA
run(1 * ms, report='text')
PyrGrp.I = 0 * nA
InterGrp.I = 0 * nA
run(30 * ms, report='text')

subplot(4, 1, 1)
plot(M.t / ms, M.v[0] / mV)
xlim(0, 50)
subplot(4, 1, 2)
plot(M.t / ms, M.g_ampa[0] / nsiemens, 'r')
xlim(0, 50)
subplot(4, 1, 3)
plot(M2.t / ms, M2.v[0] / mV)
xlim(0, 50)
subplot(4, 1, 4)
plot(M2.t / ms, M2.g_ampa[0] / nsiemens, )
xlim(0, 50)
print(time.process_time() - t0, "seconds process time")
show()