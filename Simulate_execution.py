"""
    Execution simulation of state-machine
"""
#### Pre-processing based on ontology ####
import pandas as pd
import pm4py
import random

from datetime import timedelta, datetime

from random import choices

#### Import event-logs from
dataframe = pd.read_csv('logs.csv', sep=',')
dataframe = pm4py.format_dataframe(dataframe, case_id='Resource Name', activity_key='Event-Type', timestamp_key='Timestamp')
event_logs = pd.DataFrame(data=[],columns=["Timestamp","Source","Resource Name","Event-Type","Metric","Value"])

dataset_size = 1000
dataset_resources = 50

resources = []
for i in range(dataset_resources):
    resources.append(f'Service-{random.randint(0,256)}')

timestamp_start = datetime.strptime('09/03/23 00:00:00', '%d/%m/%y %H:%M:%S')
timestamp_step = timedelta(seconds=1)
timestamp = timestamp_start

def generate_state_initial(ts, res, rep):
    ts1 = ts + timestamp_step
    ts2 = ts1 + timestamp_step
    ts3 = ts2 + timestamp_step
    return ts3, pd.DataFrame([[ts1, 'Provider', res, 'Service_Create', 'replicas', rep],
                         [ts2, 'Provider', res, 'Container_Create', '/', '/'],
                         [ts3, 'Provider', res, 'Container_Start', '/', '/']], 
                        columns=["Timestamp","Source","Resource Name","Event-Type","Metric","Value"])

def generate_state_normal(ts, res, rep):
    ts1 = ts + timestamp_step
    ts2 = ts1 + timestamp_step
    ts3 = ts2 + timestamp_step
    evtType = [['Container_Create','Container_Start'],['Container_Destroy','Container_Stop']]
    evtType_value = random.randint(0,1)
    return ts3, pd.DataFrame([[ts1, 'Provider', res, 'Service_Update', 'replicas', rep],
                         [ts2, 'Provider', res, evtType[evtType_value][0], '/', '/'],
                         [ts3, 'Provider', res, evtType[evtType_value][1], '/', '/']], 
                        columns=["Timestamp","Source","Resource Name","Event-Type","Metric","Value"])

def generate_state_final(ts, res):
    ts1 = ts + timestamp_step
    ts2 = ts1 + timestamp_step
    ts3 = ts2 + timestamp_step
    return ts3, pd.DataFrame([[ts1, 'Provider', res, 'Service_Remove', 'replicas', 0],
                         [ts2, 'Provider', res, 'Container_Destroy', '/', '/'],
                         [ts3, 'Provider', res, 'Container_Stop', '/', '/']], 
                        columns=["Timestamp","Source","Resource Name","Event-Type","Metric","Value"])

def generate_resource_usage(ts, res):
    return pd.DataFrame([[ts, 'Ressource', res, 'Ressource_Usage', 'Cpu Usage', random.randint(0,100)]], 
                        columns=["Timestamp","Source","Resource Name","Event-Type","Metric","Value"])

population = [1, 2, 3]
weights = [0.05, 0.7, 0.01]

for r in resources:
    tk = 0
    rd_tk = 0
    for idx, data in enumerate(range(dataset_size)):
        #print(f'idx:{idx}, rd_tk:{rd_tk}, tk:{tk}')
        if idx==0 or tk == 3: 
            timestamp, current = generate_state_initial(timestamp, r, random.randint(1,25))
            tk = 1
        elif rd_tk == 1 and tk == 1:
            timestamp, current = generate_state_normal(timestamp, r, random.randint(1,25))
        elif rd_tk == 2 and tk == 1:
            current = generate_resource_usage(timestamp, r)
        elif rd_tk == 3 and tk == 1:
            timestamp, current = generate_state_final(timestamp, r)
            tk = 3
        else:
            print('Error')

        event_logs = pd.concat([event_logs, current], ignore_index=True)
        timestamp += timestamp_step + timedelta(seconds=random.randint(0,60))
        rd_tk = choices(population, weights)[0]

        if (idx == (dataset_size-2)):
            rd_tk = 3

event_logs.to_csv('Simulated_logs.csv')