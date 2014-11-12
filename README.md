temperature-monitor
===================

Indoor and outdoor temperature measurements on a 24h time period.

A project using thermistors for temperature sensing, arduino for data acquisition,
memcached for short term-storage and mathplotlib for plotting temperature variations.

The circuit
--
Every second, arduino measures voltage across a voltage divider made of negative temperature
coefficient thermistor (NTC) taken from a salvaged indoor/outdoor thermometer and a 5k6 resistor. (See diagram temperature_monitor_diagram.png in *Samples* directory).

The NTC and the resistor are connected in series, between the Arduino 5v reference voltage and the ground.
A wire connected at the junction of the NTC and the resistor is also connected to an analog input of the arduino.

This circuit can be repeated to have more temperature sensors if desired. I chose to use two, one for indoor temperature, one for outdoor temperature.

The maths
--
NTCs have a non-linear temperature to resistance relationship, which can be modelized with a third order polynomial.

In order to figure out the coefficients of the polynomial, you have to measure the resistance of the NTC at different temperatures, using
an ohmmeter, a freezer, some ice, water that you will heat and a reference thermometer. These are the readings I got. Yours will probably be different.

<table>
<tr><th>T(c)</th><th>Rntc(Ko)</th></tr>
<tr><td>-18 </td><td> 48.8</dt></tr>
<tr><td>-15 </td><td> 42</dt></tr>
<tr><td>0 </td><td> 24</td></tr>
<tr><td>20 </td><td> 12.4</td></tr>
<tr><td>40 </td><td>  5.4</td></tr>
<tr><td>50 </td><td>  4</td></tr>
<tr><td>60 </td><td>  2.8</td></tr>
<tr><td>70 </td><td>  2.15</td></tr>
<tr><td>80 </td><td>  1.65</td></tr>
<tr><td>90 </td><td>  1.34</td></tr>
<tr><td>100 </td><td>  1.01</td></tr>
</table>

Now the resistance values are fine, but the arduino measures voltages, not resistances.
You must convert the resistance readings in voltage values as seen by the arduino,
applying Ohm's Law to a voltage divider network, where the output voltage measured across the series resistor is

    Vo = Vref * (R /(Rntc+R))

where Vref is the reference voltage taken from the arduino (5 volts),
Rntc is the measured resistance,
and R is the series resistor (5.6Ko).

Using this formula, you can determine Vo for all Rntc values.

<table>
<tr><th>T(c)</th><th>Rntc(Ko)</th><th>Vo</th></tr>
<tr><td>-18</td><td>48.8</td><td> 0.51</td></tr>
<tr><td>-15</td><td>42</td><td>0.59</td></tr>
<tr><td>  0</td><td>24</td><td>0.95</td></tr>
<tr><td> 20</td><td>12.4</td><td>1.56</td></tr>
<tr><td> 40</td><td>5.4</td><td>2.55</td></tr>
<tr><td> 50</td><td>4</td><td>2.92</td></tr>
<tr><td> 60</td><td>2.8</td><td>3.33</td></tr>
<tr><td> 70</td><td>2.15</td><td>3.61</td></tr>
<tr><td> 80</td><td>1.65</td><td>3.86</td></tr>
<tr><td> 90</td><td>1.34</td><td>4.03</td></tr>
<tr><td>100</td><td>1.01</td><td>4.24</td></tr>
</table>

The resistor is chosen in order to have a voltage range that is roughly linear
in the target temperature range, and total resistance should be around 10k
for optimal results with the arduino.

In my case, 5k6 gave the best results.

Using Vo as the independant variable and T as the dependant variable, we can now
find a third order polynomial describing our system.

The polynomial that best fits this dataset is

    T = 3.296v^3 -22.378v^2 +70.951v -49.382

(See diagram ntc_measurements_and_polynomial_regression.png in *Samples* directory).

You can find online polynomial regression tools to determine these coefficients at
http://www.xuru.org/rt/pr.asp

Data acquisition
--
Every second, the arduino measures the voltages at one of the two analog inputs,
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

A longer period would probably use a database to store the potentially ever growing data.


Data structure
--
I chose to save the measurements in a stack-like structure.
Every measurement is saved sequentially, with a new key indicating the measurement
and a sequence number. Three infos have to be stored, the timestamp, the analog input
number, and the temperature measurement.

Using a global counter, whose value is saved under a constant key,
I can access to the last measurement, and all the ones before.
The values expire after 24 hours.


Program workflow
--

Using memcache as the storage allows to divide the work between distinct programs, keeping them small and maintenable.

A single program is responsible to get the measurements from the arduino, compute the
average temperature and store the value and timestamp in memcache. Only one instance of the storage program should be running.

A different program can then get the data from memcache and display it or use it for other purposes. There is no limit to the number of simultaneous programs for reading.

### Commands available

- *tempstore*: reads temperature readings from arduino and stores them to memcache
- *tempread*: prints last readings on the console
- *templast*: prints readings for the last 24 hours on the console
- *tempgraphsaver*: saves last day readings as a graph in a png file
- *tempgraph*: displays last readings as a graph in an interactive display

Installing
--

Requires memcached, python_memcached, pyserial  and matplotlib.

tempgraph command requires matplotlib compiled with a tk backend.

`git clone https://github.com/pchartrand/temperature-monitor.git`

`cd temperature-monitor`

### System-wide installation


`sudo pip install .`


### Virtualenv installation


`pip install .`

### Uninstall

`pip uninstall temperature-monitor`


