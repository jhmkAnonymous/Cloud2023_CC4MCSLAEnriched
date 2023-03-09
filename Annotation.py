"""
    Annotation of event logs 
"""
#### Ontology ####
from owlready2 import * 

##### Create new ontology #####
onto = get_ontology('http://test.org/onto.owl')

##### Ontology Definition #####
with onto: 
    class stateMachine(Thing):
        pass
    class State(stateMachine):
        pass
    class Start(State):
        pass
    class Execute(State):
        pass
    class Complete(State):
        pass
    class Transition(stateMachine):
        pass
    class eventType(Thing):
        pass
    class isRelatedTo(ObjectProperty, FunctionalProperty):
        domain = [eventType]
        range  = [stateMachine]

Service_Create = eventType('Service_Create', isRelatedTo=Start)
Service_Remove = eventType('Service_Remove', isRelatedTo=Start)
Service_Update = eventType('Service_Update', isRelatedTo=Start)
Container_Create = eventType('Container_Create', isRelatedTo=Execute)
Container_Destroy = eventType('Container_Destroy', isRelatedTo=Execute)
Container_Start = eventType('Container_Start', isRelatedTo=Complete)
Container_Stop = eventType('Container_Stop', isRelatedTo=Complete)
Ressource_Usage = eventType('Ressource_Usage', isRelatedTo=Transition)

##### Ancestors Calling #####
def search_ancestors(onto, ask):
    result = onto.search(iri = "*{}".format(ask))
    lcStep = str(result[0].isRelatedTo).split('.')[1]
    smElt = str(result[0].isRelatedTo.is_a[0]).split('.')[1]
    if lcStep == 'Transition':
        smElt = 'Transition'
        lcStep = 'N/A'
    return [smElt, lcStep]

#### Pre-processing based on ontology ####
import pandas as pd
import pm4py

#### Import event-logs from
dataframe = pd.read_csv('logs.csv', sep=',')
dataframe = pm4py.format_dataframe(dataframe, case_id='Resource Name', activity_key='Event-Type', timestamp_key='Timestamp')

#### Iterate through event logs ####
for idx, row in dataframe.iterrows():
    # Search event type in ontology and returns ancestors 
    smElt, lcStep = search_ancestors(onto, row['Event-Type'])
    dataframe.loc[[idx],'smElt'] = smElt
    dataframe.loc[[idx],'lcStep'] = lcStep

### Export as XES ###
event_log = pm4py.convert_to_event_log(dataframe)
xes = pm4py.write_xes(event_log, 'exported.xes')
