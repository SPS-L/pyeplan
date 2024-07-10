###########
 Input data
###########

.. role::  raw-html(raw)
    :format: html

CSV File Name: cbat_dist :raw-html:`&rarr;` characteristic of candidate battery units
*************************************************************************************

**Columns:**

+-----+-------+-------+-------+----+----+------+------+------+------+------+------+------+
| bus | icost | ocost | scost | ec | ed | emax | emin | eini | pmax | pmin | qmax | qmin |
+=====+=======+=======+=======+====+====+======+======+======+======+======+======+======+
+-----+-------+-------+-------+----+----+------+------+------+------+------+------+------+

bus: Bus number

icost: Annualised investment cost [$/year]

ocost: Operation cost [$/kWh] (default = 0)

scost: Start-up cost [$] (default = 0)

ec: Charging mode efficiency

ed: Discharging mode efficiency

emax: Maximum limit of stored energy for each battery unit [kWh]

emin: Minimum limit of stored energy for each battery unit [kWh]

pmax: Maximum limit of active power production for each battery unit
[kW]

pmin: Minimum limit of active power production for each battery unit
[kW]

qmax: Maximum limit of reactive power production for each battery unit
[kVAr]

qmin: Minimum limit of reactive power production for each battery unit
[kVAr]

CSV File Name: cblt_dist :raw-html:`&rarr;` Characteristic of different cables
******************************************************************************

**Columns:**

+-----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
| crs | r0 | i0 | r1 | x1 | z1 | i1 | r2 | x2 | z2 | i2 | r3 | x3 | z3 | i3 | r4 | x4 | z4 | i4 | r5 | x5 | z5 | i5 | r6 | x6 | z6 | i6 | r7 | x7 | z7 | i7 |
+=====+====+====+====+====+====+====+====+====+====+====+====+====+====+====+====+====+====+====+====+====+====+====+====+====+====+====+====+====+====+====+
+-----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+

csr: Cross-section [mm\ :sup:`2`]

r0: Resistance (2 cables, DC) [mΩ/m]

i0: Rated current (2 cables, DC) [A]

r1: Resistance (2 cables, single-phase DC, enclosed in conduit or
trunking) [mΩ/m]

x1: Reactance (2 cables, single-phase DC, enclosed in conduit or
trunking) [mΩ/m]

z1: Impedance (2 cables, single-phase DC, enclosed in conduit or
trunking) [mΩ/m]

i1: Rated current (2 cables, single-phase DC, enclosed in conduit or
trunking) [A]

r2: Resistance (2 cables, single-phase DC, cables touching) [mΩ/m]

x2: Reactance (2 cables, single-phase DC, cables touching) [mΩ/m]

z2: Impedance (2 cables, single-phase DC, cables touching) [mΩ/m]

i2: Rated current (2 cables, single-phase DC, cables touching) [A]

r3: Resistance (2 cables, single-phase AC, cables spaced) [mΩ/m]

x3: Reactance (2 cables, single-phase AC, cables spaced) [mΩ/m]

z3: Impedance (2 cables, single-phase AC, cables spaced) [mΩ/m]

i3: Rated current (2 cables, single-phase AC, cables spaced) [A]

r4: Resistance (3 or 4 cables, three-phase AC, enclosed in conduit or
trunking) [mΩ/m]

x4: Reactance (3 or 4 cables, three-phase AC, enclosed in conduit or
trunking) [mΩ/m]

z4: Impedance (3 or 4 cables, three-phase AC, enclosed in conduit or
trunking) [mΩ/m]

i4: Rated current (3 or 4 cables, three-phase AC, enclosed in conduit or
trunking) [A]

r5: Resistance (3 or 4 cables, three-phase AC, trefoil) [mΩ/m]

x5: Reactance (3 or 4 cables, three-phase AC, trefoil) [mΩ/m]

z5: Impedance (3 or 4 cables, three-phase AC, trefoil) [mΩ/m]

i5: Rated current (3 or 4 cables, three-phase AC, trefoil) [A]

r6: Resistance (3 or 4 cables, three-phase AC, cables touching, flat)
[mΩ/m]

x6: Reactance (3 or 4 cables, three-phase AC, cables touching, flat)
[mΩ/m]

z6: Impedance (3 or 4 cables, three-phase AC, cables touching, flat)
[mΩ/m]

i6: Rated current (3 or 4 cables, three-phase AC, cables touching, flat)
[A]

r7: Resistance (3 or 4 cables, three-phase AC, cables spaced, flat)
[mΩ/m]

x7: Reactance (3 or 4 cables, three-phase AC, cables spaced, flat)
[mΩ/m]

z7: Impedance (3 or 4 cables, three-phase AC, cables spaced, flat)
[mΩ/m]

i7: Rated current (3 or 4 cables, three-phase AC, cables spaced, flat)
[A]

CSV File Name\: cgen_dist :raw-html:`&rarr;` Characteristic of candidate dispatchable units
*******************************************************************************************

**Columns:**

+-----+-------+-------+-------+------+------+------+------+
| bus | icost | ocost | scost | pmin | pmax | qmin | qmax |
+=====+=======+=======+=======+======+======+======+======+
+-----+-------+-------+-------+------+------+------+------+

bus: Bus number

icost: Annualised investment cost [$/year]

ocost: Operation cost [$/kWh]

scost: Start-up cost [$]

pmax: Maximum limit of active power production for each unit [kW]

pmin: Minimum limit of active power production for each unit [kW]

qmax: Maximum limit of reactive power production for each battery unit
[kVAr]

qmin: Minimum limit of reactive power production for each battery unit
[kVAr]

CSV File Name: clin_dist :raw-html:`&rarr;` Characteristic of candidate lines
*****************************************************************************

**Columns:**

+------+----+-----+-----+-----+-------+------+------+------+
| from | to | ini | res | rea | icost | smax | pmax | qmax |
+======+====+=====+=====+=====+=======+======+======+======+
+------+----+-----+-----+-----+-------+------+------+------+

from: Sending bus

to: Receiving bus

ini: Initial status

res: Resistance [pu]

rea: Reactance [pu]

icost: Annualised capital cost [$]

smax: Maximum limit of apparent power [kVA]

pmax: Inner approximation for maximum active power [kW]

qmax: Inner approximation for maximum active power [kVAr]

CSV File Name: csol_dist :raw-html:`&rarr;` Characteristic of candidate solar units
***********************************************************************************

**Columns:**

+------+-------+--------+--------+-------+--------+-------+--------+
| bus  | icost | ocost  | scost  | pmin  | pmax   | qmin  | qmax   |
+======+=======+========+========+=======+========+=======+========+
+------+-------+--------+--------+-------+--------+-------+--------+

bus: Bus number

icost: Annualised investment cost [$/year]

ocost: Operation cost [$/kWh]

scost: Start-up cost [$] (default: 0)

pmax: Maximum limit of active power production for each unit [kW]

pmin: Minimum limit of active power production for each unit [kW]

qmax: Maximum limit of reactive power production for each battery unit
[kVAr]

qmin: Minimum limit of reactive power production for each battery unit
[kVAr]

CSV File Name: csol_dist :raw-html:`&rarr;` Characteristic of candidate solar units
***********************************************************************************

**Columns:**

+------+-------+--------+--------+-------+--------+-------+--------+
| bus  | icost | ocost  | scost  | pmin  | pmax   | qmin  | qmax   |
+======+=======+========+========+=======+========+=======+========+
+------+-------+--------+--------+-------+--------+-------+--------+

bus: Bus number

icost: Annualised investment cost [$/year]

ocost: Operation cost [$/kWh]

scost: Start-up cost [$] (default: 0)

pmax: Maximum limit of active power production for each unit [kW]

pmin: Minimum limit of active power production for each unit [kW]

qmax: Maximum limit of reactive power production for each battery unit
[kW]

qmin: Minimum limit of reactive power production for each battery unit
[kW]

CSV File Name: cwin_dist :raw-html:`&rarr;` Characteristic of candidate wind units Columns
******************************************************************************************

+------+-------+--------+--------+-------+--------+-------+--------+
| bus  | icost | ocost  | scost  | pmin  | pmax   | qmin  | qmax   |
+======+=======+========+========+=======+========+=======+========+
+------+-------+--------+--------+-------+--------+-------+--------+

bus: Bus number

icost: Annualised investment cost [$/year]

ocost: Operation cost [$/kWh]

scost: Start-up cost [$] (default: 0)

pmax: Maximum limit of active power production for each unit [kW]

pmin: Minimum limit of active power production for each unit [kW]

qmax: Maximum limit of reactive power production for each battery unit
[kVAr]

qmin: Minimum limit of reactive power production for each battery unit
[kVAr]

CSV File Name: dtim_dist :raw-html:`&rarr;` Duration time of each representative day obtained by clustering techniques

**Columns:**

+-----------------------------------------------------------------------+
| dt                                                                    |
+=======================================================================+
+-----------------------------------------------------------------------+

dt: Duration time of each representative day obtained by clustering
techniques [h]

CSV File Name: egen_dist :raw-html:`&rarr;` Characteristic of existing dispatchable units
*****************************************************************************************

**Columns:**

+------+---------+---------+---------+----------+---------+----------+
| bus  | ocost   | scost   | pmin    | pmax     | qmin    | qmax     |
+======+=========+=========+=========+==========+=========+==========+
+------+---------+---------+---------+----------+---------+----------+

bus: Bus number

ocost: Operation cost [$/kWh]

scost: Start-up cost [$]

pmax: Maximum limit of active power production for each unit [kW]

pmin: Minimum limit of active power production for each unit [kW]

qmax: Maximum limit of reactive power production for each battery unit
[kVAr]

qmin: Minimum limit of reactive power production for each battery unit
[kVAr]

CSV File Name: elin_dist :raw-html:`&rarr;` Characteristic of existing lines
****************************************************************************

**Columns:**

+------+----+-----+-----+-----+-----+------+------+------+
| from | to | ini | res | rea | sus | smax | pmax | qmax |
+======+====+=====+=====+=====+=====+======+======+======+
+------+----+-----+-----+-----+-----+------+------+------+

from: Sending bus

to: Receiving bus

ini: Initial status

res: Resistance [pu]

rea: Reactance [pu]

sus: Susceptance [pu]

smax: Maximum limit of apparent power [kVA]

pmax: Inner approximation for maximum active power [kW]

qmax: Inner approximation for maximum active power [kVAr]

CSV File Name: esol_dist :raw-html:`&rarr;` Characteristic of existing solar units

**Columns:**

+------+---------+---------+---------+----------+---------+----------+
| bus  | ocost   | scost   | pmin    | pmax     | qmin    | qmax     |
+======+=========+=========+=========+==========+=========+==========+
+------+---------+---------+---------+----------+---------+----------+

bus: Bus number

icost: Annualised investment cost [$/year]

ocost: Operation cost [$/kWh]

scost: Start-up cost [$] (default: 0)

pmax: Maximum limit of active power production for each unit [kW]

pmin: Minimum limit of active power production for each unit [kW]

qmax: Maximum limit of reactive power production for each battery unit
[kVAr]

qmin: Minimum limit of reactive power production for each battery unit
[kVAr]

CSV File Name: cwin_dist :raw-html:`&rarr;` Characteristic of existing wind units

**Columns:**

+------+---------+---------+---------+----------+---------+----------+
| bus  | ocost   | scost   | pmin    | pmax     | qmin    | qmax     |
+======+=========+=========+=========+==========+=========+==========+
+------+---------+---------+---------+----------+---------+----------+

bus: Bus number

ocost: Operation cost [$/kWh]

scost: Start-up cost [$] (default: 0)

pmax: Maximum limit of active power production for each unit [kW]

pmin: Minimum limit of active power production for each unit [kW]

qmax: Maximum limit of reactive power production for each battery unit
[kVAr]

qmin: Minimum limit of reactive power production for each battery unit
[kVAr]

CSV File Name: geol_dist :raw-html:`&rarr;` Geographical location of load points for feeder routing
***************************************************************************************************

**Columns:**

+-----+-----------------------------------+----------------------------+
|     | Longtitude                        | Latitude                   |
+=====+===================================+============================+
+-----+-----------------------------------+----------------------------+

Longtitude: Longitude of a load point

Latitude: Latitude of a load point

Note: The first column represents the index of each load point and it
starts from 0

Worksheet File Name: mgpc_dist :raw-html:`&rarr;` Characteristic of load points
*******************************************************************************

**Sheets:**

Load Point: longitude, latitude, hourly participation factors of load
points

Load Level: Total load levels at each hour of the scheduling horizon

Note: To construct the load profile, the following tool from NREL can be
used:

Microgrid Load and LCOE Modelling Results, available online:
https://data.nrel.gov/submissions/79

CSV File Name: pdem_dist :raw-html:`&rarr;` Hourly participation factors of load points (active power)
******************************************************************************************************

Note: The **first row** represents the index of load points and **each
column** represents the hourly participation factors for 24 hours of a
single day.

CSV File Name: prep_dist :raw-html:`&rarr;` Hourly total active load levels of the microgrid
*********************************************************************************************

Note: The **first row** represents the index of all representative days
and **each column** represent the hourly total active load levels for 24
hours of each representative day in kW.

CSV File Name: psol_dist :raw-html:`&rarr;` Hourly total available solar active power of the microgrid
*******************************************************************************************************

Note: The **first row** represents the index of all representative days
and **each column** represent the hourly total available solar power for
24 hours of each representative day in kW.

CSV File Name: pwin_dist :raw-html:`&rarr;` Hourly total available wind active power of the microgrid
*****************************************************************************************************

Note: The **first row** represents the index of all representative days
and **each column** represent the hourly total available wind power for
24 hours of each representative day in kW.

CSV File Name: qdem_dist :raw-html:`&rarr;` Hourly participation factors of load points (reactive power)
********************************************************************************************************

Note: The **first row** represents the index of load points and **each
column** represents the hourly participation factors for 24 hours of a
single day.

CSV File Name: qrep_dist :raw-html:`&rarr;` Hourly total reactive load levels of the microgrid
**********************************************************************************************

Note: The **first row** represents the index of all representative days
and **each column** represent the hourly total reactive load levels for
24 hours of each representative day in kW.

CSV File Name: qsol_dist :raw-html:`&rarr;` Hourly total available solar reactive power of the microgrid
********************************************************************************************************

Note: The **first row** represents the index of all representative days
and **each column** represent the hourly total available solar power for
24 hours of each representative day in kW.

CSV File Name: qwin_dist :raw-html:`&rarr;` Hourly total available wind active power of the microgrid
*****************************************************************************************************

Note: The **first row** represents the index of all representative days
and **each column** represent the hourly total available wind power for
24 hours of each representative day in kW.

CSV File Name: rou_dist :raw-html:`&rarr;` Distance between pairs of connected buses
************************************************************************************

**Columns:**

+---------------------+------------+----------------------------------+
| from                | to         | distance                         |
+=====================+============+==================================+
+---------------------+------------+----------------------------------+

from: Sending bus

to: Receving bus

distance: Distance between a pair of connected buses


