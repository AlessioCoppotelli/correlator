import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR)+'/utilities')
from name import NAME_signal_simulator
from randomator import randlist
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from random import random
matplotlib.use('TkAgg')


class signal_simulator :
    def __init__(self,*args,**kwargs) :
        self.signal         = None
        self.amplitude      = None #[ dB ]
        self.frequency      = None #[ Hz ]
        self.duration       = None #[ s ]
        self.initial_phase  = None #[ rad ]
        #------------
        self.modulation     = None # [ BPSK,QPSK,OQPSK ]
        self.bitsequence    = None # [ 0-1,00-01-10-11 ]
        self.carrier        = 'remnant' # [ suppressed, remnant ]
        self.mod_index      = None # [ 0,pi/2 ]
        self.bit_rate       = None # [ bit/sec ]
        #------------
        self.samplingrate   = None # [ point/sec ]
        #------------
        self.n_points       = None
        self.time_list      = None
        self.time_array     = None
        #-----------
        self.time_delay     = None #[ s ]

# --------- U T I L I T I E S
    def _error(self,string,value=None,Type=None) :
        out = 'ERROR in signal class : '+string
        if value is not None :
            try :
                out += ' (value : '+str(value)+')'
            except :
                pass
        if Type is not None :
            try :
                out += ' (type : '+str(Type)+')'
            except :
                pass
        print(out)

    def value_control(self,value,name,minval=0.0) :
        if type(value) not in [int,float] :
            out = None
            self._error(name+' not float or int. Set as None',Type=type(val))
        else :
            if minval is not None :
                if value <= minval :
                    out = None
                    self._error(name+' must be >= '+str(minval)+'. Set as None.',value=val)
                else :
                    out = value
            else :
                out = value
        return out
# --------- S E T   A T T R I B U T E S
    def set_amplitude(self,amplitude) :
        self.amplitude = self.value_control(amplitude,'Amplitude')
    def set_frequency(self,frequency) :
        self.frequency = self.value_control(frequency,'Frequency')
    def set_duration(self,duration) :
        self.duration = self.value_control(duration,'Duration')
    def set_initialphase(self,initial_phase) :
        self.initial_phase = self.value_control(initial_phase,'Initial Phase',minval=None)
    def set_points_number(self,points) :
        n_point = self.value_control(points,'Point number')
        self.n_points = int(n_point) if n_point is not None else n_point
    def set_time_list(self) :
        if self.duration is not None and self.n_points is not None :
            #time_list = np.arange(0,self.duration,self.n_points)
            time_list = np.linspace(0, self.duration,self.n_points , endpoint=True)
            self.time_array = time_list
            self.time_list = time_list.tolist()
        else :
            time_list = None
            self.time_array = None
            self.time_list = None
    def calculate_time_list(self) :
        if self.duration is not None and self.samplingrate is not None :
            self.n_points = self.duration/self.samplingrate
            time_list = np.linspace(0, self.duration,self.n_points , endpoint=True)
            self.time_array = time_list
            self.time_list = time_list.tolist()
        else :
            time_list = None
            self.time_array = None
            self.time_list = None


    def set_time_delay(self,time_delay) :
        self.time_delay = self.value_control(time_delay,'Time delay',minval=None)

    def set_modulation(self,modulation) :
        if type(modulation) == str :
            if modulation.upper() in [ 'BPSK','QPSK','OQPSK' ] :
                self.modulation = modulation
            else :
                _error('modulation not known',value=modulation.upper())
        else :
            _error('modulation must be a string')
            
    def set_samplingrate(self,samprate) :
        # set the rate of sampling
        self.samplingrate = samprate

    def set_bitrate(self,bit_rate) :
        self.bit_rate = bit_rate

    def set_bitsequence(self,bitsequence,data_per_sample) :
        bit_seq = []
        for i in bitsequence :
            bit_seq = bit_seq + [i for j in range(data_per_sample) ]
        delta_len = len(bit_seq) - len(self.time_array)
        if delta_len > 0 :
            # levare dati da bit_seq
            del bit_seq[-delta_len:-1]
        elif delta_len < 0 :
            # aggiungere 0 alla fine di bit_seq
            bit_seq = bit_seq + [0 for j in range(-delta_len)]
        
            

        self.bitsequence = bit_seq


    def set_mod_index(self,mod_idx) :
        self.mod_index = mod_idx

    def simulate_signal(self) :
        if self.amplitude is not None and self.frequency is not None and self.time_array is not None :
            A = self.amplitude
            freq = self.frequency
            t = self.time_array
            phi_0 = self.initial_phase
            delay = self.time_delay
            if delay is None :
                delay = 0.0

            if self.carrier is None :
                print('  carrier not defined. (remnant or suppressed)')
                s = A * np.sin( 2*np.pi*freq*(t+delay) + phi_0)
            elif self.carrier == 'remnant' :
                print('  remnant carrier signal')
                if self.mod_index is not None and self.bitsequence is not None:
                    print('  modulated signal')
                    mod_idx = self.mod_index
                    print('        with mod_idx : ',mod_idx)
                    m_t = np.array(self.bitsequence)
                    s = A * np.sin( 2*np.pi*freq*(t+delay) + phi_0 +mod_idx* m_t)
                else :
                    print('  not modulated signal')
                    s = A * np.sin( 2*np.pi*freq*(t+delay) + phi_0 )
            elif self.carrier == 'suppressed' :
                print('  suppressed carrier signal')
                s = A * m_t * np.sin( 2*np.pi*freq*(t+delay) + phi_0)
            else :
                s = None
        else :
            s = None
        self.signal = s
    
    def plot_signal(self,figname) :
        timestep = self.time_list
        signal = self.signal
        if timestep is not None and signal is not None :
            plt.plot(timestep, signal)
            plt.title('Signal')
            plt.ylabel('Signal (dB)')
            plt.xlabel('Time (s)')
            plt.show()
            #plt.savefig(figname+'.jpg')
        else :
            self._error('some None inputs in plot_signal')

    def add_noise(self,noise_amplitude) :
        rand_noise_component = randlist(length=len(self.signal),center=0,ssextension=noise_amplitude)
        noise_signal = np.ones(len(self.signal))*np.array(rand_noise_component)
        self.signal = self.signal + rand_noise_component





if __name__ == '__main__' :
    add_noise = 'no'

    NAME_signal_simulator()
    signal = signal_simulator()

    amplitude = 5.0
    frequency = 1
    duration = 10.0
    phi_0 = 0.0
    points = 1000
    mod_idx = np.pi/4.0
    bitsequence = [round(random()) for x in range(int(points/5))]
    bit_per_sample = 5

    signal.set_amplitude(amplitude)
    signal.set_frequency(frequency)
    signal.set_duration(duration)
    signal.set_initialphase(phi_0)
    signal.set_points_number(points)
    signal.set_time_list()
    signal.set_modulation = 'BPSK'
    signal.set_mod_index(mod_idx)
    signal.set_bitsequence(bitsequence,bit_per_sample)

    signal.simulate_signal()

    signal.plot_signal('test')

    if add_noise == 'yes' :
        signal.add_noise(0.5)
        signal.plot_signal('test')
