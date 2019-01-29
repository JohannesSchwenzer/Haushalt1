# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 15:34:32 2019

@author: s0536
"""

from oemof.tools import logger
from oemof.tools import helpers

import oemof.solph as solph
import oemof.outputlib as outputlib

import logging
import os
import pandas as pd
import pprint as pp

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None
    
solver = 'cbc'  # 'glpk', 'gurobi',....
debug = False  # Set number_of_timesteps to 3 to get a readable lp-file.
number_of_time_steps = 24*7*52   #stündlich    entspricht mit 8760
solver_verbose = False  #eventuell raus

# initiate the logger (see the API docs for more information)
logger.define_logging(logfile='oemof_example.log',
                      screen_level=logging.INFO,
                      file_level=logging.DEBUG)

logging.info('Initialize the energy system')
date_time_index = pd.date_range('1/1/2018', periods=number_of_time_steps,
                                freq='H')

energysystem = solph.EnergySystem(timeindex=date_time_index)

# Read data file
filename = os.path.join(os.path.dirname(__file__), 'Haushalt1.csv')
data = pd.read_csv(filename)

logging.info('Create oemof objects')

bel = solph.Bus(label="electricity")


energysystem.add(bel)


###Solaranlage mit 20% Wirkungsgrad. nominal_value=1 entspricht 5m².###
###nominal_value=2 entspricht 10m² usw...  ###


energysystem.add(solph.Source(label='pv', outputs={bel: solph.Flow(
    actual_value=data['pv'], nominal_value=2.5, fixed=True)}))
    
# Überproduktion die nicht in einer Batterie gespeichert wird, wird ins Netz eingespeist #    
    
energysystem.add(solph.Sink(label='Netzeinspeisung', inputs={bel: solph.Flow()}))

# Wenn der Strombedarf die PV Produktion und die gespeicherte Energiemenge in der Batterie
# übersteigt, wird der Strom vom Stromanbieter aus dem Netz zu 26ct/kwh bezogen.

energysystem.add(solph.Source(label='Netzbezug',
                     outputs={bel: solph.Flow(variable_costs=26)}))

# Strombedarf stündlich aufgelistet mit dem LoadProfileGenerator erstellt

energysystem.add(solph.Sink(label='Stromverbrauch', inputs={bel: solph.Flow(
    actual_value=data['Last'], fixed=True, nominal_value=1)})) 

# Batterie mit nominal capacity in kWh. Nominal_capacity=10 entspricht 10kWh Kapazität.
# Wirkungsgrad 80%    
    
storage = solph.components.GenericStorage(
    nominal_capacity=10,
    label='storage',
    inputs={bel: solph.Flow(nominal_value=10)},
    outputs={bel: solph.Flow(nominal_value=10, variable_costs=0.001)},
    capacity_loss=0.00, initial_capacity=None,
    inflow_conversion_factor=1, outflow_conversion_factor=0.8,)

energysystem.add(storage)    
   

logging.info('Optimise the energy system')
model = solph.Model(energysystem)


# nur für debug. kann ignoriert werden
if debug:
    filename = os.path.join(
        helpers.extend_basic_path('lp_files'), 'basic_example.lp')
    logging.info('Store lp-file in {0}.'.format(filename))
    model.write(filename, io_options={'symbolic_solver_labels': True})
    
    

logging.info('Solve the optimization problem')
model.solve(solver=solver, solve_kwargs={'tee': solver_verbose})

logging.info('Store the energy system with the results.')



# add results to the energy system to make it possible to store them.
energysystem.results['main'] = outputlib.processing.results(model)
energysystem.results['meta'] = outputlib.processing.meta_results(model)

energysystem.dump(dpath=None, filename=None)

logging.info('Restore the energy system and the results.')
energysystem = solph.EnergySystem()
energysystem.restore(dpath=None, filename=None)


results = energysystem.results['main']
storage = energysystem.groups['storage']
electricity_bus = outputlib.views.node(results, 'electricity')
custom_storage = outputlib.views.node(results, 'storage')
demand = outputlib.views.node(results, 'Stromverbrauch')


if plt is not None:
    fig, ax = plt.subplots(figsize=(10,5))
    custom_storage['sequences'].plot(ax=ax, kind='line', drawstyle='steps-post')
    plt.legend(loc='upper center', prop={'size':8}, bbox_to_anchor=(0.5, 1.25), ncol=2)
    fig.subplots_adjust(top=0.8)
    plt.show()

    fig, ax = plt.subplots(figsize=(10,5))
    electricity_bus['sequences'].plot(ax=ax, kind='line', drawstyle='steps-post')
    plt.legend(loc='upper center', prop={'size':8}, bbox_to_anchor=(0.5, 1.3), ncol=2)
    fig.subplots_adjust(top=0.8)
    plt.show()

    fig, ax = plt.subplots(figsize=(10,5))
    demand['sequences'].plot(ax=ax, kind='line', drawstyle='steps-post')
    plt.legend(loc='upper center', prop={'size':8}, bbox_to_anchor=(0.5, 1.3), ncol=2)
    fig.subplots_adjust(top=0.8)
    plt.show()

# print the sums of the flows around the electricity bus
print('********* Main results *********')
print(electricity_bus['sequences'].sum(axis=0))

#om.write('path/my_model.lp', io_options={'symbolic_solver_labels': True})