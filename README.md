temperature-monitor
===================

Indoor and outdoor temperature measurements on a 24h timeframe.

Silly project using thermistors for temperature sensing, arduino for data acquisition,
memcached for short term-storage and mathplotlib for plotting temperature variations.

The circuit
--
Every second, arduino measures voltage across a voltage divider made of a salvaged negative temperature
coefficient thermistor (NTC) from a salvaged indoor/outdoor thermometer and a 5k6 resistor.

 5v ----NTC---|-- analog input
 ref.         5
              k
              6
              |
             ___ ground
              _

This circuit can be repeated to have more temperature sensors if desired. I chose to use two.

The maths
--
NTCs have a non-linear temperature to resistance relationship, which can be modelized with a third order polynomial.

In order to figure out the coefficients, you have to measure the resistance of the ntc at different temperatures, using
an ohmmeter, a freezer, ice, water that you will heat and a reference thermometer. These are the readings I got.

T(c) Rntc(Ko)
-18	    48.8
-15	    42
  0	    24
 20	    12.4
 40	     5.4
 50	     4
 60	     2.8
 70	     2.15
 80	     1.65
 90	     1.34
100	     1.01

Now the resistance values are fine, but the arduino measures voltages, not resistances.
You must convert the resistance readings in voltage values as seen by the arduino, applying Ohm's Law to a voltage
divider network, where the output voltage measured across the series resistor is

    Vo = Vref * (Rntc /(Rntc+R))

where Vref is the reference voltage taken from the arduino (5 volts),
Rntc is the measured resistance,
and R is the series resistor.

Using this formula, you can determine Vo for all Rntc values.

T(c) Rntc(Ko)      Vo
-18	    48.8     0.51
-15	    42       0.59
  0	    24       0.95
 20	    12.4     1.56
 40	     5.4     2.55
 50	     4       2.92
 60	     2.8     3.33
 70	     2.15    3.61
 80	     1.65    3.86
 90	     1.34    4.03
100	     1.01    4.24

The resistor is chosen in order to have a voltage range that is roughly linear
in the target temperature range, and total resistance should be around 10k
for optimal results with the arduino.

In my case, 5k6 gave the best results.

Using Vo as the independant variable and T as the dependant variable, we can now
find a third order polynomial describing our system.

The polynomial that best fits this dataset is

    T = 3.296v^3 -22.378v^2 +70.951v -49.382

You can find online polynomial regression tools to determine these coefficients at
http://www.xuru.org/rt/pr.asp

Data acquisition
--
Every second, the arduino measures the voltages on one of the two analog inputs every,
and sends a temperature reading to the usb port, converting the voltage values in
temperature values using the polynomial equation, and indicating which input was read.

Data storage
--
Saving the data every second does seem like overkill, but the readings vary slightly
on every reading.

I chose to average the data sent on a one minute period, to get a less noisy measurement,
and then save the averaged value in memory. I chose memcache as the data storage because
the data does not require a long conservation time.

A one day period seems enough for reporting purposes. With two inputs and a measurement every
minute, it requires to store 2880 measurements per day.

A longer period would probably require a database to store the ever growing data.


Data structure
--
I chose to save the measurements in a stack-like structure.
Every measurement is saved sequentially, with a new key indicating the measurement
and a sequence number. Three infos have to be stored, the timestamp, the analog input
number, and the temperature measurement.

Using a global counter, whose value is saved under a constant key,
I can access to the last measurement, and all the ones before.
The values expire after one 24 hours.


Workflow
--
Using memcache as the storage allows to divide the work between distinct programs.

A single program is responsible to get the measurements from the arduino, compute the
average and store the value and timestamp in memcache.

A different program can then get the data from memcache and use it or display it.






