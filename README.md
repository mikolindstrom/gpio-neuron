# Gpio
Gpio neuron for kalliope
## Synopsis

Switch a gpios between high and low and get temperaturs or other data from the 1-wire bus.

## Installation
```bash
kalliope install --git-url https://github.com/corus87/gpio-neuron
```

## Options

| parameter    | required | choices  | comments          |
|--------------|----------|----------|-------------------|
| set_pin_high | no       | integer  | GPIO numbers (BCM)|
| set_pin_low  | no       | integer  |                   |
| sensor       | no       | string   | (GPIO_GCLK) GPIO 4|
| fahrenheit   | no       | boolean  | Default false     |

## Return values

<<<<<<< HEAD
| Name         | Description                | Type   | Sample |
|--------------|----------------------------|--------|--------|
| sensor       | Returns the temperature in | string | 24.6   |
|                celsius or fahrenheit                        |
=======
| Name         | Description                                      | Type   | Sample |
|--------------|--------------------------------------------------|--------|--------|
| sensor       | Returns the temperature in celsius or fahrenheit | string | 24.6   |

>>>>>>> 56e321f181d0a007670e304bd0d812efb91aa193


## Synapses example
```
  - name: "temp-out-living"
    signals:
      - order: "what are the temperaturs"
    neurons:
      - gpio:
          sensor: "28-0416b37f9bff"          
          say_template:
              - "outside {{ sensor }} degree,"   
      - gpio:        
          sensor: "28-0316b3bd7bff"
          say_template:
              - "and in the living room {{ sensor }} degree."  
  
  - name: "all-lights-on"
    signals:
      - order: "Turn all lights on"
    neurons:
      - gpio:
          set_pin_high:
            - 17
            - 18
            - 22
            - 27
 
 - name: "table-lamp-off"
    signals:
      - order: "Turn table lamp off"
    neurons:
      - gpio:
          set_pin_low: 17
```
## Notes
To get the sensor ID of each sensor use:
> cat /sys/devices/w1_bus_master1/w1_master_slaves



