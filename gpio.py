# -*- coding: iso-8859-1 -*-
import logging
import RPi.GPIO as GPIO
from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException, MissingParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")

class Gpio(NeuronModule):
    def __init__(self, **kwargs):
        super(Gpio, self).__init__(**kwargs)
        # the args from the neuron configuration
        self.set_pin_high = kwargs.get('set_pin_high', None)
        self.set_pin_low = kwargs.get('set_pin_low', None)       
        self.sensor = kwargs.get('sensor', None)
        self.fahrenheit = kwargs.get('fahrenheit', False)
        self.GPIO = GPIO

        # check if parameters have been provided
        if self._is_parameters_ok():

            # set gpio pins to high or low 
            self.GPIO.setwarnings(False)
            self.GPIO.setmode(GPIO.BCM)

            if self.set_pin_high:
                self.GPIO.setup(self.set_pin_high, GPIO.OUT)
                self.GPIO.output(self.set_pin_high, GPIO.HIGH)
                logger.debug('[GPIO] Set pin %s to high' % self.set_pin_high)
                
            if self.set_pin_low:
                self.GPIO.setup(self.set_pin_low, GPIO.OUT)                
                self.GPIO.output(self.set_pin_low, GPIO.LOW)              
                logger.debug('[GPIO] Set pin %s to low' % self.set_pin_low)
                
            # 1-Wire 
            if self.sensor:
                sensorpath = "/sys/bus/w1/devices/"			  
                sensorfile = "/w1_slave"				                          
                
                def callsensor():
                    with open(sensorpath + self.sensor + sensorfile, 'r') as f:	  
                        lines = f.read().splitlines()	
                        
                    temp_line = lines[1].find('t=')	
                    temp_output = lines[1].strip() [temp_line+2:] 
                    temp_celsius = float(temp_output) / 1000
                    
                    if self.fahrenheit:
                        temp_fahrenheit = temp_celsius * 9.0 / 5.0 + 32.0
                        logger.debug('[GPIO] Sensor %s returns %s° fahrenheit' % (self.sensor, '%.1f' % float(temp_fahrenheit)))
                        return temp_fahrenheit
                    else:
                        logger.debug('[GPIO] Sensor %s returns %s° celsius' % (self.sensor, '%.1f' % float(temp_celsius)))
                        return temp_celsius		
               
                message = {"sensor": str('%.1f' % float(callsensor())).rstrip('0').rstrip('.')}
                self.say(message)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise
        .. raises:: InvalidParameterException
        """
        if self.set_pin_low:
            try:
                self.set_pin_low = int(self.set_pin_low)    
            except ValueError:
                raise InvalidParameterException("[Gpio] %s is not a valid integer" % self.set_pin_low)
                
        if self.set_pin_high:
            try:
                self.set_pin_high = int(self.set_pin_high)    
            except ValueError:
                raise InvalidParameterException("[Gpio] %s is not a valid integer" % self.set_pin_high)
        
        if self.fahrenheit and not self.sensor:
            raise MissingParameterException("You must set a sensor")
        return True