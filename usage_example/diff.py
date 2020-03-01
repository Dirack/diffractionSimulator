# coding: utf-8
#
# diff.py (Python)
# 
# Purpose: Diffraction migration recipe using focusing measure.
# The input is a stacked section with only diffraction hiperbolas.
# 
# Site: http://www.dirackslounge.online
# 
# Version 1.0
# 
# Programer: Rodolfo Dirack 01/03/2020
# 
# Email: rodolfo_profissional@hotmail.com
# 
# License: GPL-3.0 <https://www.gnu.org/licenses/gpl-3.0.txt>.

from rsf.proj import *
import string, sys
import version

def diffmig(name,
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

    # Velocity continuation of diffraction
    vlf=name+'-vlf'
    Flow(vlf,stk,velcon)

    Flow(vlf+'q',stk,
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




            


















