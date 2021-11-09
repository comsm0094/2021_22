import random
import matplotlib.pyplot as plt


class Neuron:

    def __init__(self,v_initial,v_t,v_r,e_l,e_s,tau):

        self.v=v_initial
        self.v_t=v_t
        self.v_r=v_r
        self.e_l=e_l
        self.e_s=e_s
        self.tau=tau

    def derivative(self,i_e,g_s):
        return ((self.e_l-self.v)+i_e+g_s*(self.e_s-self.v))/self.tau

    def update(self,delta_v):
        self.v+=delta_v
        if self.v>=self.v_t:
            self.v=self.v_r
            return True
        return False
    
class Synapse:

    def __init__(self,s_initial,tau,g_bar):
        self.s=s_initial
        self.tau=tau
        self.g_bar=g_bar

    def spike(self):
        self.s+=1.0

    def get_gs(self):
        return self.g_bar*self.s
        
    def derivative(self):
        return -self.s/self.tau

    def update(self,delta_s):
        self.s+=delta_s
    
def update_neuron(neuron,i_e,g_s,delta_t):
    delta_v=neuron.derivative(i_e,g_s)*delta_t
    return neuron.update(delta_v)

def update_synapse(synapse,delta_t):
    delta_s=synapse.derivative()*delta_t
    synapse.update(delta_s)

mV=0.001
ms=0.001

tau_m = 20.0*ms
e_l=-70.0*mV
v_r=-80.0*mV
v_t=-54.0*mV

#e_s=-80.0*mV
e_s=0.0*mV

r_mI_e=18*mV

r_mg_bar=0.075
tau_s=10*ms

neuron1=Neuron(random.uniform(v_r,v_t),v_t,v_r,e_l,e_s,tau_m)
neuron2=Neuron(random.uniform(v_r,v_t),v_t,v_r,e_l,e_s,tau_m)

synapse12=Synapse(random.uniform(0.0,1.0),tau_s,r_mg_bar)
synapse21=Synapse(random.uniform(0.0,1.0),tau_s,r_mg_bar)

t_initial=0.0*ms
t_final  =1000.0*ms
delta_t  =1.0*ms

t=t_initial

v1=[];v2=[]
# s12=[];s21=[]
ts=[]

while t<=t_final:
    g_s12=synapse12.get_gs()
    g_s21=synapse21.get_gs()

    spike1=update_neuron(neuron1,r_mI_e,g_s21,delta_t)
    spike2=update_neuron(neuron2,r_mI_e,g_s12,delta_t)

    update_synapse(synapse12,delta_t)
    update_synapse(synapse21,delta_t)
    
    if spike1:
        synapse12.spike()
    if spike2:
        synapse21.spike()

    v1.append(neuron1.v)
    v2.append(neuron2.v)

#    s12.append(synapse12.s)
#    s21.append(synapse21.s)
    
    ts.append(t)
    
    t+=delta_t

plt.plot(ts,v1)
plt.plot(ts,v2)

plt.show()

        
