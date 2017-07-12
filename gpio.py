# -*- coding: iso-8859-1 -*-
import RPi.GPIO as GPIO
from kalliope.core.NeuronModule import NeuronModule, MissingParameterException

    
class Gpio(NeuronModule):
    def __init__(self, **kwargs):
        super(Gpio, self).__init__(**kwargs)
        # the args from the neuron configuration
        self.set_pin_high = kwargs.get('set_pin_high', None)
        self.set_pin_low = kwargs.get('set_pin_low', None)       
        self.sensor = kwargs.get('sensor', None)
        self.GPIO = GPIO

        # check if parameters have been provided
        if self._is_parameters_ok():
             # # # # # # # # # # # # # # # # # 
            #      set gpio pins to high or low    #
           # # ## # # # # # # # # # # # # #  
            self.GPIO.setwarnings(False)
            self.GPIO.setmode(GPIO.BCM)

        
            if self.set_pin_high:
                self.GPIO.setup(self.set_pin_high, GPIO.OUT)
                self.GPIO.output(self.set_pin_high, GPIO.HIGH)
                
            if self.set_pin_low:
                self.GPIO.setup(self.set_pin_low, GPIO.OUT)                
                self.GPIO.output(self.set_pin_low, GPIO.LOW)              
            
               # # # # # # # # 
              #      1-Wire     #
            # # ## # # # # 
            if self.sensor:
                sensorpath = "/sys/bus/w1/devices/"			  
                sensorfile = "/w1_slave"				                          
                
                def callsensor(self):
                    f = open(sensorpath + self.sensor + sensorfile, 'r')	  
                    lines = f.readlines()						                         
                    f.close()							                                    
                    temp_line = lines[1].find('t=')	
                    temp_output = lines[1].strip() [temp_line+2:]  
                    temp_celsius = float(temp_output) / 1000		  
                    return temp_celsius		
               
                message = {"sensor": str('%.1f' % float(callsensor(self))).rstrip('0').rstrip('.')}
                self.say(message)



    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: MissingParameterException
        """
        return True