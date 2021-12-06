from signalsimulator import signal_simulator
from name import NAME_correlator
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from random import random



#def correlator(signal_1,signal_2,tao) :
#    len_1 = len(signal_1)
#    R_tao_i = 0.0
#    for i in range(len_1-tao) :
#        R_tao_i += signal_2[i]*signal_1[i+tao]
#    return R_tao_i

def correlator(signal_1,signal_2) :
    len_1 = len(signal_1)
    R_tao_i = 0.0
    for i in range(len_1) :
        R_tao_i += signal_2[i]*signal_1[i]
    return R_tao_i

def time_delay_calculator(signal_1,signal_2) :
    len_1 = len(signal_1)
    len_2 = len(signal_2)
    points = len_1
    frequency = 1
    T = 1/frequency
    duration = 10.0
    T_in_duration = duration/T
    t_marked = duration/points # duration of single point [ s/point ]
    point_in_T = points/T_in_duration
    

    R_tao = []
    R_tao_i = 0.0
    #tao_try = len_1//10
    tao_try = int(point_in_T)
    for tao in range(tao_try) :
        R_tao_i = 0.0
    
        #s_1 = signal_1.tolist()
        #s_2 = signal_2.tolist()
        s_1 = signal_1.tolist()[tao:-tao_try+tao]
        s_2 = signal_2.tolist()[0:-tao_try]

        R_tao_i = correlator(s_1,s_2)
        R_tao.append(R_tao_i)


    print('--- Calculated ---')
    tao_max = max(R_tao)
    tao_max_i = R_tao.index(tao_max) # index delay
    #print('R(tao) : ',R_tao)
    #print('R_min : ',tao_max)

    corr_signal = signal_simulator()

    
    tao = tao_max_i*t_marked # time delay seconds
    phi_0_c = 2*np.pi*frequency*tao # phase delay rad
    print(' tried tao : ',len(R_tao))
    print()
    print('Calculated Phase shift : ',phi_0_c)
    print('Calculated Time delay : ',tao)
    print('  index : ',tao_max_i)


    plt.plot(range(tao_try), R_tao)
    plt.title('Rtao')
    #plt.savefig('aaa.jpg')
    plt.show()





if __name__ == '__main__' :
    NAME_correlator()

    add_noise = 'No'
    plot_yn = 'Yes'

    amplitude = 5.0
    frequency = 1
    duration = 10.0
    points = 1000
    phi_0_1 = 0.0


    time_delay = 0.2
    #bitsequence = [round(random()) for x in range(points)]
    mod_idx = np.pi/4.0
    bitsequence = [round(random()) for x in range(int(points/5))]
    bit_per_sample = 5



    phi_0_2 = 0.0
    t_marked = duration/points # duration of single point [ s/point ]
    imposed_tao = phi_0_2/(2*np.pi*frequency) + time_delay
    imposed_index = imposed_tao/t_marked

    print('--- Imposed ---')
    print('Imposed Phase shift : ',time_delay*(2*np.pi*frequency) + phi_0_2)
    print('Imposed Time delay : ',imposed_tao)
    print('  index : ',imposed_index)

    signal_1 = signal_simulator()
    signal_1.set_amplitude(amplitude)
    signal_1.set_frequency(frequency)
    signal_1.set_duration(duration)
    signal_1.set_initialphase(phi_0_1)
    signal_1.set_points_number(points)
    signal_1.set_mod_index(np.pi/4.0)
    signal_1.set_time_list()
    signal_1.set_modulation = 'BPSK'
    signal_1.set_mod_index(mod_idx)
    signal_1.set_bitsequence(bitsequence,bit_per_sample)
    signal_1.simulate_signal()


    signal_2 = signal_simulator()
    signal_2.set_amplitude(amplitude)
    signal_2.set_frequency(frequency)
    signal_2.set_duration(duration)
    signal_2.set_initialphase(phi_0_2)
    signal_2.set_time_delay(time_delay)
    signal_2.set_points_number(points)
    signal_2.set_mod_index(np.pi/4.0)
    signal_2.set_time_list()
    signal_2.set_modulation = 'BPSK'
    signal_2.set_mod_index(mod_idx)
    signal_2.set_bitsequence(bitsequence,bit_per_sample)
    signal_2.simulate_signal()

    if add_noise == 'Yes' :
        signal_2.add_noise(0.1)
        signal_1.add_noise(0.1)

    s_1 = signal_1.signal
    s_2 = signal_2.signal
    time_delay_calculator(s_1,s_2)

    if plot_yn == 'Yes' :
        timestep = signal_1.time_list
        plt.plot(timestep, s_1)
        plt.plot(timestep, s_2)
        plt.title('Signal')
        plt.ylabel('Signal (dB)')
        plt.xlabel('Time (s)')
        #plt.figure(num=figname)
        plt.show()

