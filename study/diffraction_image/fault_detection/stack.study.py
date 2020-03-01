# coding: utf-8
#
# stack.study.py (Python)
# 
# Purpose: Study of the script 'stack.py' by copying and coment.
# 
# Site: http://www.dirackslounge.online
# 
# Version 1.0
# 
# Programer: Rodolfo Dirack 21/02/2020
# 
# Email: rodolfo_profissional@hotmail.com
# 
# License: GPL-3.0 <https://www.gnu.org/licenses/gpl-3.0.txt>.

from rsf.proj import *
import string, sys
import version

def stack(name, # filename
        v0, # Initial velocity
        nv, #number of velocities
        dv, # velocity sampling
        nx, # Number of cmp's
        padx, # pad data with zeros to avoid problems with filter boundaries
        nt, # Time samples
        tmin=0, # time window min
        tmax=10, # time window max
        rect1=10, # smooth radius time
        rect2=10, # smooth radius distance
        srect1=1, 
        srect2=3,
        vslope=None,
        units='Km',
        f1=1,
        j3=1,
        dx=1,
        x0=0,
        beg1=0,
        frect1=0,
        frect2=0,
        an=1,
        nout=2048,
        vx0=None):

    if version.old_version():
        return # think how to do it better

    scn = name+'-scn' # scaned velocity
    vel = name+'-vel' # velocity after picking

    # sfmutter aplies a muting in data, it uses
    # v0 to determine the slope and mute
    # sfvscan does the velocity analisys
    # if the parameter semblance=y compute
    # semblance function; v0, nv and dv define
    # the velocity window
    Flow(scn,name,
            'mutter v0=%g | vscan semblance=y v0=%g nv=%d dv=%g' % (v0,v0,nv,dv))

    # If 'vslope' is passed, mute the data
    # using that slope p0=1/v0
    if vslope:
        pick = 'mutter x0=%g v0=%g half=n | ' % (vx0,vslope)
    else:
        pick = ''

    # sfpick does the picking of semblance
    # like panels. rect's parameter define
    # the smooth radius
    pick = pick + 'pick rect1=%d rect2=%d | window' % (rect1,rect2)

    # ploting functions
    def grey(title):
        return '''
        window n1=%d |
        grey title="%s"
        label1=Time unit1=s label2=Distance unit2="%s"
        ''' % (nt,title,units)

    def velgrey(title):
        return grey(title)+'''
        color=j scalebar=y mean=y barlabel=Velocity barunit="%s/s"
        barreverse=y
        ''' % units

    # Do the velocity picking
    Flow(vel,scn,pick)    
    Result(vel,velgrey('RMS Velocity'))

    nmo = name+'-nmo' # After NMO data
    stk = name+'-stk' # Stacked section

    # Apply NMO in data to linearize reflection
    # events, after that stack the data
    Flow(nmo,[name,vel],'mutter v0=%g | nmo velocity=${SOURCES[1]}' % v0)
    Flow(stk,nmo,'stack')
    Result(stk,grey('NMO Stack'))

    # sflogstretch stretches along time axis
    # sffft1 is the fast fourier transform in time
    # sfinstack is a DMO stack by finite differences
    # and offset continuation
    stk2=stk+'2'
    Flow(stk2,nmo,
            '''
            window f1=%d | logstretch nout=%d |
            fft1 | transp plane=13 memsize=500 |
            finstack | transp memsize=500 |
            fft1 inv=y | window n1=%d |
            logstretch inv=y | pad beg1=%d |
            transp | bandpass fhi=%g | transp
            ''' % (f1,nout,nout,f1,0.75*0.5/dx))
    Result(stk2,grey('DMO Stack'))

    diffimg(name,stk2,v0,nv,dv,nx,padx,nt,tmin,tmax,
            rect1,
            rect2,
            srect1,
            srect2,
            vslope,
            units,
            f1,
            j3,
            dx,
            x0,
            beg1,
            frect1,
            frect2,
            an,
            nout,
            vx0)

def diffimg(name,
            stk,
            v0,
            nv,
            dv,
            nx,
            padx,
            nt,
            tmin=0,
            tmax=10,
            rect1=10,
            rect2=10,
            srect1=1,
            srect2=3,
            vslope=None,
            units='Km',
            f1=1,
            j3=1,
            dx=1,
            x0=0,
            beg1=0,
            frect1=0,
            frect2=0,
            an=1,
            nout=2048,
            vx0=None):

    if frect==0:
        frect1=2*rect1

    if frect==0:
        frect2=2*rect2/j3

    # ploting functions
    def grey(title):
        return '''
        window n1=%d |
        grey title="%s"
        label1=Time unit1=s label2=Distance unit2="%s"
        ''' % (nt,title,units)

    def velgrey(title):
        return grey(title)+ '''
        color=j scalebar=y bias=%g barlabel=Velocity barunit="%s/s"
        barreverse=y
        ''' % (v0+0.5*nv*dv,units)

    dip = name+'-dip' # dominant slope of stacked section

    # Calculate dominante slope, rect parameter
    # are the smooth radius
    Flow(dip,stk,'dip rect1=%d rect2=%d' % (rect1,rect2))
    Result(dip,grey('Dominant Slope') + \
            ' color=j scalebar=y barlabel=Slope barunit=samples ')

    pwk = name+'-pwk' # Stacked section after the plane wave construction filter

    # sfpwdsmooth2 is a 2-D smoothing 
    # by triangle plane-wave construction 
    # shaping
    Flow(pwk,dip,
            'noise rep=y seed=2007 | pwdsmooth2 dip=$SOURCE rect1=3 rect2=%d' % srect2)
    Result(pwk,grey('Pattern'))

    # Use plane wave destruction filter
    # to separate the diffractions
    pwd=name+'-pwd' # data after plane wave destruction filter Diffractions
    Flow(pwd,[stk,dip],'pwd dip=${SOURCES[1]}')
    Result(pwd,grey('Separated Diffractions'))

    # Use plane wave construction to separate
    # the reflections from diffractions
    ref=name+'-ref' # data after plane wave construction filter Reflections
    Flow(ref,[stk,dip],
            'pwdsmooth2 dip=${SOURCES[1]} rect1=%d rect2=%d' % (srect1,srect2))
    Result(ref,grey('Separated Reflections'))
    
    # Cut reflections from data
    # Keep diffractions
    # shp is the difference between then
    shp=name+'-shp'
    Flow(shp,[stk,ref],'add ${SOURCES[1]} scale=1,-1')
    Result(shp,grey('Diffractions'))

    # Velocity analisys by focusing
    # Stolt Migration. It needs the cosine
    # tranform of the data. sfvczo does
    # the velocity continuation process
    # migrate data multiple times with a
    # constant velocity
    velcon='''
    pad n2=%d beg1=%d | cosft sign2=1 | put o3=0 | 
    stolt vel=%g |
    vczo nv=%d dv=%g v0=%g |
    transp plane=23 |
    cosft sign2=-1 |
    window n2=%d f1=%d |
    put o2=%g |
    transp plane=23
    ''' % (padx,beg1,v0,nv,dv,v0,nx,beg1,x0)

    #
    vlf=name+'-vlf'
    Flow(vlf,pwd,velcon)

    Flow(vlf+'q',pwd,
            '''
            math output="input*input" | %s | clip2 lower=0
            ''' % velcon)

    # j#n is the jump parameter of sfwindow
    if j3 > 1:
        focus = 'window j3=%d | ' % j3
    else:
        focus = ''

    # Focusing analisys
    # local varimax is max when the velocity
    # collapses a diffraction
    focus = focus + '''
    focus rect1=%d rect3=%d |
    math output="1/abs(input)" |
    cut max1=%g | cut min1=%g
    ''' % (frect1,frect2,tmin,tmax)

    foc=name+'-foc' # focusing measure
    Flow(foc,vlf,focus)

    # semblance is the local varimax measure
    # sfmul multplies data
    # sfdivn does smooth data division
    sem=name+'-sem'
    Flow(sem,[vlf,vlf+'q'],
            '''
            mul $SOURCE |
            divn den=${SOURCES[1]} rect1=%d rect3=%d
            ''' % (rect1,rect2))

    pik=name+'-pik' # Data after picking

    # if vslope, use it to mute data
    if vslope:
        pick = 'mutter x0=%g v0=%g half=n | ' % (vx0,vslope)
    else:
        pick = ''

    pick = pick + 'scale axis=2 | pick an=%g rect1=%d rect2=%d | window' % (an.rect1,rect2)

    if j3 > 1:
        pick2 = pick + '''
        transp |
        spline n1=%d d1=%g o1=%g |
        transp
        ''' % (nx,dx,x0)
    else:
        pick2 = pick

    Flow(pik,sem,pick2)
    Result(pik,velgrey('Migration Velocity'))

    slc = name + '-slc' # slice of picking cube
    Flow(slc,[vlf,pik],'slice pick=${SOURCES[1]}')
    Result(slc,grey('Migrated Diffractions')

    Flow(vlf+'2',stk,velcon)
    Flow(slc+'2',[vlf+'2',pik],'slice pick=${SOURCES[1]}')

    Result(slc+'2',grey('Migrated Stack'))

    Flow(slc+'1',slc+'2','shapeagc rect1=200')
    Result(slc+'1',grey('Migrated Stacked'))

    Flow(vlf+'0',ref,velcon)
    Flow(slc+'0',[vlf+'0',pik],'slice pick=${SOURCES[1]}')

    Result(slc+'0',grey('Migrated Reflection'))




            


















