#### Study of the fault detection experiment

#### Study of the recipe in 'stack.py'
    
The original script, 'stack.py', is a Madagascar recipe for stacking and
diffraction imaging of the seimic data cube (Amplitude as a function of CMP x 
Offset x Time coordinates).
The file 'stack.study.py' is a study of this script with
coments and explanation of what each function does.

Firts it receives a seimic data cube in the function stack, do the
conventional NMO stacking and DMO stacking and pass the data for the
diffimg function to migrate the diffractions.

It separates reflections and diffractions using plane wave destruction
filters, do the velocity analisys by focusing measure and migrate them.

