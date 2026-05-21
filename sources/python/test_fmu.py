'''
FMI testing script.
Company: EAG
Author: FTM
This script has been made to test the main capabilities of any given FMI 3.0 or FMI 2.0 FMU. 
The script can do the following:
    Read all functionality flags of the fmu and plot them.
    Identify all of the output real variables and plot them with respect to the independent variable (to a maximum of 6 plots).
    Test setting and getting of integer, string and boolean variables.
    Test the getState, setState and serializeState functionalities if the model is set to enable those.
    Test the getrealOutputDerivatives call if the model is set to allow derivatives of order 2 or higher.
    Test the doStep new fmi 3.0 flags (earlyReturn, eventEncountered,terminateSim,lastSuccesfullTime)
    Test the entering and exiting of eventMode, initializationMode, configurationMode and reconfigurationMode 
    
Integer and Real variables are assumed to be 64 bit with sign.
All previously mentioned tests can be enabled or disabled with a flag.
To call the script use: python test_fmu.py <FMU_Name>.fmu
'''

from fmpy import read_model_description, extract
from fmpy.fmi3 import FMU3Slave
from fmpy.fmi2 import FMU2Slave
import matplotlib.pyplot as plt
import numpy as np
import shutil
import sys
import os
import base64
import ctypes

def intermediateUpdateFun(instanceEnvironment, intermediateUpdateTime , intermediateVariableSetRequested, intermediateVariableGetAllowed, intermediateStepFinished, canReturnEarly, earlyReturnRequested, earlyReturnTime):
    plt.plot(5,5)
    plt.show()
    earlyReturnRequested=True
    earlyReturnTime=intermediateUpdateTime
    print("This is the intermediate update function")

#testing flags
testOutputDerivatives=True
testSaveLoadState=False
testVariableGetSet=False
testDoStepOutputFlags=True
testConfigurationMode=False
plotSimResults=True
printStepTrace=False

realTypes=['Float64','Float32','Real']
integerTypes=['Int8','UInt8','Int16','UInt16','Int32','UInt32','Int64','UInt64','Integer']
stringTypes=['String']
boolTypes=['Boolean']
binaryTypes=['Binary']
clockTypes=['Clock']
enumType=['Enumeration']


# define the model name and simulation parameters
fmu_filename = sys.argv[1]

# time parameters, in seconds
start_time = 0.0
stop_time = 7
step_size = 0.1

# read the model description
model_description = read_model_description(fmu_filename)

#read functionality flags
isCoSimulation=model_description.coSimulation
canGetAndSetFMUState=False
canSerializeFMUState=False
needsExecutionTool=False
canBeInstantiatedOnlyOncePerProcess=False
providesDirectionalDerivatives=False
providesAdjointDerivatives=False
providesPerElementDependencies=False
providesEvaluateDiscreteStates=False

if(isCoSimulation):
    canGetAndSetFMUState = model_description.coSimulation.canGetAndSetFMUstate
    canSerializeFMUState = model_description.coSimulation.canSerializeFMUstate
    needsExecutionTool = model_description.coSimulation.needsExecutionTool
    providesDirectionalDerivatives = model_description.coSimulation.providesDirectionalDerivative
    providesAdjointDerivatives = model_description.coSimulation.providesAdjointDerivatives
    providesPerElementDependencies = model_description.coSimulation.providesPerElementDependencies
    providesEvaluateDiscreteStates = model_description.coSimulation.providesEvaluateDiscreteStates
    canBeInstantiatedOnlyOncePerProcess = model_description.coSimulation.canBeInstantiatedOnlyOncePerProcess
    canHandleVariableCommunicationStepSize = model_description.coSimulation.canHandleVariableCommunicationStepSize
    maxOutputDerivativeOrder = model_description.coSimulation.maxOutputDerivativeOrder
    providesIntermediateUpdate = model_description.coSimulation.providesIntermediateUpdate
    #mightReturnEarlyFromDoStep= model_description.coSimulation.mightReturnEarlyFromDoStep
    canReturnEarlyAfterIntermediateUpdate = model_description.coSimulation.canReturnEarlyAfterIntermediateUpdate
    hasEventMode = model_description.coSimulation.hasEventMode
    

print("\n*********************FUNCTIONALITY FLAGS*********************\n")

print("FMI version: " + model_description.fmiVersion)

if(isCoSimulation):
    print("CoSimulation model.\n")
else:
    print("Non CoSimulation model.")
    
if(canGetAndSetFMUState):
    print("Model accepts get and set state.")
testSaveLoadState= testSaveLoadState and canGetAndSetFMUState

if(canSerializeFMUState):
    print("Model can serialize its state.")
testSaveLoadState= testSaveLoadState and canSerializeFMUState

if(needsExecutionTool):
    print("Model needs execution tool.")
    
if(providesDirectionalDerivatives):
    print("Model provides directional derivatives.")
    
if(providesAdjointDerivatives):
    print("Model provides adjoint derivatives.")
    
if(providesPerElementDependencies):
    print("Model provides per element dependencies.")
    
if(providesEvaluateDiscreteStates):
    print("Model allows to evaluate discrete states.")
  
if(canBeInstantiatedOnlyOncePerProcess):
    print("Model can be instantiated only once per process.")
    
if(canHandleVariableCommunicationStepSize):
    print("Model can handle variable communication step size.")
    
print("Maximun output derivative order: " + str(maxOutputDerivativeOrder))
if(maxOutputDerivativeOrder<2):
    testOutputDerivatives=False

if(providesIntermediateUpdate):
    print("Model allows to use intermediate update mode.")
    
# if(mightReturnEarlyFromDoStep):
    # print("Model might return early from step.")

if(canReturnEarlyAfterIntermediateUpdate):
    print("Model might return early from intermediate update.")
    
if(hasEventMode):
    print("Model has event mode.")
    
print("\n*************************************************************\n")


#read and handle variables
outputsNames = []
for element in model_description.outputs :
    outputsNames.append(element.variable.name)

vr_outputs = []
vr_inputs = []
vr_real = []
vr_string = []
vr_boolean = []
vr_integer = []
vr_independent = 0

vr_real_out = []
vr_real_out_name = []
vr_real_out_units = []
vr_string_in = []
vr_boolean_in = []
vr_integer_in = []

# collect the value references
types = {}
for tp in model_description.typeDefinitions:
    types[tp.name]=tp.unit

vrs = {}
for variable in model_description.modelVariables:
    vrs[variable.name] = variable.valueReference
    if(variable.causality == "independent"):
        vr_independent = vrs[variable.name] #We cannot actually access this variable for our FMUs, but is mandatory to have it on the modelDescription.xml
    elif(variable.type in realTypes):
        vr_real.append(vrs[variable.name])
        if(variable.causality=="output"):
            vr_real_out.append(vrs[variable.name])
            vr_real_out_name.append(variable.name)
            if(variable.declaredType):
                vr_real_out_units.append(types[variable.declaredType.name])
            else:
                vr_real_out_units.append(variable.unit)
    elif(variable.type in integerTypes):
        vr_integer.append(vrs[variable.name])
        if(variable.causality=="input"):
            vr_integer_in.append(vrs[variable.name])
    elif(variable.type in stringTypes):
        vr_string.append(vrs[variable.name])
        if(variable.causality=="input"):
            vr_string_in.append(vrs[variable.name])
    elif(variable.type in boolTypes):
        vr_boolean.append(vrs[variable.name])
        if(variable.causality=="input"):
            vr_boolean_in.append(vrs[variable.name])

for name in outputsNames:
    vr_outputs.append(vrs[name])


# extract the FMU
unzipdir = extract(fmu_filename)

if(model_description.fmiVersion=="3.0"):
    fmu = FMU3Slave(guid=model_description.guid, unzipDirectory=unzipdir,modelIdentifier=model_description.coSimulation.modelIdentifier)
    fmu.instantiate(visible=True, loggingOn=True, eventModeUsed=hasEventMode, earlyReturnAllowed=canReturnEarlyAfterIntermediateUpdate, logMessage=None, intermediateUpdate=intermediateUpdateFun)
    if(testConfigurationMode):
        fmu.fmi3EnterConfigurationMode(fmu.component)#does this really need to be called like this?
        fmu.fmi3ExitConfigurationMode(fmu.component)
        fmu.enterInitializationMode(startTime=start_time)
    fmu.enterInitializationMode(startTime=start_time)
else:
    fmu = FMU2Slave(guid=model_description.guid, unzipDirectory=unzipdir,modelIdentifier=model_description.coSimulation.modelIdentifier)
    # initialize
    fmu.instantiate( loggingOn=True)
    fmu.setupExperiment(startTime=start_time)
    fmu.enterInitializationMode()

fmu.exitInitializationMode()

times=[]
outputs=[]
outputDer=[]

if(testVariableGetSet):
    if(len(vr_string)>0):
        stringValues=fmu.getString(vr_string)
        print("Initial string values: " + str(stringValues))
        if(len(vr_string_in)>0):
            fmu.setString([vr_string_in[0]],["Hello"])
            stringValues=fmu.getString(vr_string)
            print("Changed string values: " + str(stringValues))
    if(len(vr_integer)>0):
        intValues = fmu.getInt64(vr_integer)
        print("Initial integer values: " + str(intValues))
        if(len(vr_integer_in)>0):
            fmu.setInt64([vr_integer_in[0]],[5])
            intValues = fmu.getInt64(vr_integer)
            print("Changed integer values: " + str(intValues))
    if(len(vr_boolean)>0):
        boolValues = fmu.getBoolean(vr_boolean)
        print("Initial boolean values: " + str(boolValues))
        if(len(vr_boolean_in)>0):
            fmu.setBoolean([vr_boolean_in[0]],[True])
            boolValues = fmu.getBoolean(vr_boolean)
            print("Changed boolean values: " + str(boolValues)) 
        
# simulation loop
sim_time = start_time
loaded=False
while sim_time < stop_time:    
    # perform one step
    if(printStepTrace):
        print("New step: TIME = " + str(sim_time))
    if(model_description.fmiVersion=="3.0"):
        [eventEncountered,terminateSim,earlyReturn,lastSuccesfullTime]=fmu.doStep(currentCommunicationPoint=sim_time, communicationStepSize=step_size)
    else:
        fmu.doStep(currentCommunicationPoint=sim_time, communicationStepSize=step_size)  
        eventEncountered = False
        terminateSim = False
        earlyReturn = False
        lastSuccesfullTime = sim_time
    if(testDoStepOutputFlags):
        if(eventEncountered): #Our FMUs do not contemplate this usage.
            print("An event has been encountered.")
            print("Last succesfull time: " + str(lastSuccesfullTime))
            #Here we should change to event mode and handle the event. 
            fmu.enterEventMode()
            print("Handling events...")
            #Do event mode stuff
            fmu.enterStepMode()
        if(terminateSim):
            print("Slave has requested to terminate simulation.")
            print("Last succesfull time: " + str(lastSuccesfullTime))
            break
        if(earlyReturn): #Our FMUs do not contemplate this usage. 
            print("Slave has triggered an early return.")
            print("Last succesfull time: " + str(lastSuccesfullTime))
            #Here probably we should some sort of management. 
            fmu.fmi3EnterConfigurationMode(fmu.component)#does this really need to be called like this?
            #Change values to improve convergence? We don't really need to enter this mode with EcosimPro, but other FMUs might require ir for some parameters.
            fmu.fmi3ExitConfigurationMode(fmu.component)

    times.append(sim_time)
    if(model_description.fmiVersion=="3.0"):
        outputs.append(fmu.getFloat64(vr_real_out))
    else:
       outputs.append(fmu.getReal(vr_real_out))
    
    if(testOutputDerivatives):
        order=[1]*len(vr_real_out) + [2]*len(vr_real_out)
        vr=vr_real_out*2
        #outputDer.append(fmu.getOutputDerivatives(vr_outputs, order) #I'm quite convinced that this function has a bug on the fmpy side (it's calling fmi3GetOutputDerivatives with 5 arguments instead of 6)
        
        vr=(ctypes.c_ulong * len(vr))(*vr)
        order=(ctypes.c_long * len(order))(*order)
        values=(ctypes.c_double * len(order))()
        if(model_description.fmiVersion=="3.0"):
            fmu.fmi3GetOutputDerivatives(fmu.component,vr,len(vr),order,values,len(vr))
        else:
            fmu.fmi2GetRealOutputDerivatives(fmu.component,vr,len(vr),order,values)
        outputDer.append(values[:])
    
    # advance the time
    sim_time += step_size
    
    if(testSaveLoadState):
        if(abs(sim_time-3.0)<1e-5 and not loaded):
            print("Saving state")
            state = fmu.getFMUState()
            serializedState=fmu.serializeFMUState(state)
            with open( "state.bin", "wb" ) as fh:
                fh.write( serializedState)
            fmu.freeFMUState(state)
            
        if(abs(sim_time-5.0)<1e-5):
            if(not loaded):
                print("Loading state")
                with open( "state.bin", "rb" ) as fh:
                    serializedState = fh.read()
                    fmu.deserializeFMUState(serializedState,state)
                fmu.setFMUState(state)
                #sim_time=1.0
                loaded=True
            else:
                print("Done")
                break
    

fmu.terminate()
fmu.freeInstance()

# clean up
shutil.rmtree(unzipdir, ignore_errors=True)

t=np.array(times)
x=np.array(outputs)
xDer=np.array(outputDer)

max_plots=6
if(max_plots>len(vr_real_out)):
    max_plots=len(vr_real_out)
    
if(max_plots<3):
    numRows=1
else:
    numRows=2

print(max_plots)

if(plotSimResults):
    fig, axs = plt.subplots(nrows=numRows, ncols=int(max_plots/numRows) + max_plots%numRows)
    axs=axs.flat
    for i in range(max_plots):
        axs[i].plot(t, x[:,i])
        axs[i].set_title(vr_real_out_name[i])
        axs[i].set_xlabel("t(s)")
        axs[i].set_ylabel(vr_real_out_units[i])
    
if(testOutputDerivatives):
    fig1, axs1 = plt.subplots(nrows=numRows, ncols=int(2*max_plots/numRows))
    axs1=axs1.flat
    for i in range(2*max_plots):
        axs1[i].plot(t, xDer[:,i])
        axs1[i].set_xlabel("t(s)")
        if(i<max_plots):
            derString="der("
            unitString="/s"
            axs1[i].set_title(derString + vr_real_out_name[i] + ")") 
            if(vr_real_out_units[i]):            
                axs1[i].set_ylabel(str(vr_real_out_units[i]) + unitString)

        else:
            derString="der'("
            unitString="/s^2"
            axs1[i].set_title(derString + vr_real_out_name[int(i/2)] + ")")
            if(vr_real_out_units[int(i/2)]): 
                axs1[i].set_ylabel(str(vr_real_out_units[int(i/2)]) + unitString)
    
plt.show()

print( "FTM_END" )
