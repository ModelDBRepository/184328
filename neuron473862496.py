'''
Defines a class, Neuron473862496, of neurons from Allen Brain Institute's model 473862496

A demo is available by running:

    python -i mosinit.py
'''
class Neuron473862496:
    def __init__(self, name="Neuron473862496", x=0, y=0, z=0):
        '''Instantiate Neuron473862496.
        
        Parameters:
            x, y, z -- position offset
            
        Note: if name is not specified, Neuron473862496_instance is used instead
        '''
        
        self._name = name
        # load the morphology
        from load_swc import load_swc
        load_swc('Nr5a1-Cre_Ai14_IVSCC_-177333.03.01.01_472477347_m.swc', self,
                 use_axon=False, xshift=x, yshift=y, zshift=z)

        # custom axon (works because dropping axon during import)
        from neuron import h
        self.axon = [h.Section(cell=self, name='axon[0]'),
                     h.Section(cell=self, name='axon[1]')]
        for sec in self.axon:
            sec.L = 30
            sec.diam = 1
            sec.nseg = 1
        self.axon[0].connect(self.soma[0](0.5))
        self.axon[1].connect(self.axon[0](1))
        self.all += self.axon
        
        self._insert_mechanisms()
        self._discretize_model()
        self._set_mechanism_parameters()
    
    def __str__(self):
        if self._name is not None:
            return self._name
        else:
            return "Neuron473862496_instance"
                
    def _insert_mechanisms(self):
        from neuron import h
        for sec in self.all:
            sec.insert("pas")
        for mech in [u'CaDynamics', u'Ca_HVA', u'Ca_LVA', u'Ih', u'Im', u'K_P', u'K_T', u'Kv3_1', u'NaTs', u'Nap', u'SK']:
            self.soma[0].insert(mech)
    
    def _set_mechanism_parameters(self):
        from neuron import h
        for sec in self.all:
            sec.Ra = 87.55
            sec.e_pas = -94.9662704468
        for sec in self.apic:
            sec.cm = 2.41
            sec.g_pas = 2.42523914136e-05
        for sec in self.axon:
            sec.cm = 1.0
            sec.g_pas = 0.000980017175089
        for sec in self.dend:
            sec.cm = 2.41
            sec.g_pas = 5.00705600632e-06
        for sec in self.soma:
            sec.cm = 1.0
            sec.ena = 53.0
            sec.ek = -107.0
            sec.gbar_Im = 0.00193143
            sec.gbar_Ih = 0.00465224
            sec.gbar_NaTs = 0.322147
            sec.gbar_Nap = 0.000806761
            sec.gbar_K_P = 0.00289639
            sec.gbar_K_T = 0.000170026
            sec.gbar_SK = 6.46305e-05
            sec.gbar_Kv3_1 = 0.0667562
            sec.gbar_Ca_HVA = 0.000151033
            sec.gbar_Ca_LVA = 0.00180911
            sec.gamma_CaDynamics = 0.00633033
            sec.decay_CaDynamics = 324.351
            sec.g_pas = 0.000716728
    
    def _discretize_model(self):
        for sec in self.all:
            sec.nseg = 1 + 2 * int(sec.L / 40)

