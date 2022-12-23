# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 12:05:16 2022

@author: SCHWEINGRUBER.MISC
"""
from abc import ABC, abstractmethod
import numpy as np
from dataclasses import dataclass
import math
from scipy.spatial.transform import Rotation
from matplotlib import pyplot as plt
import matplotlib
import mplstereonet

@dataclass
class StressField(ABC):
    mu: float = None
    azim_SH: float = None #azimuth of SH. 0 wenn pointing to North, 90 when to east

    @property
    @abstractmethod
    def regime(self):
        '''
        stress regime after Andersson
        '''




    def get_abc(self):
        '''
        returns angles alpha, beta and gamma
        '''
        if self.regime == 'strike_slip':
            a = self.azim_SH
            b = 0
            c = math.radians(90)
        elif self.regime == 'normal':
            a = self.azim_SH + math.radians(90)
            b = math.radians(90)
            c = 0
        elif self.regime == 'thrust':
            a = self.azim_SH
            b = 0
            c = 0

        return a, b, c

    @property
    @abstractmethod
    def S1(self):
        ...

    @property
    @abstractmethod
    def S3(self):
        ...

    @property
    @abstractmethod
    def S2(self):
        ...
        
    @abstractmethod
    def get_ordered_s(self):
        '''
        returns ordered (ascending) list of Sh, SH and Sv
        '''
        ...


    @property
    def S1_S3_ratio(self):
        return factor_from_mu(self.mu)

    @property
    def critical_angle(self):
        return compute_critical_angle(self.mu)

    def compute_S1_from_S3(self):
        '''
        computes sigma_1 based on sigma_3 and the critically stressed crust
        theory
        '''
        return (self.S3 - self.Pp) * self.S1_S3_ratio + self.Pp

    def compute_sn_tau_on_plane(self, strike, dip):
        '''
        computes normal and shear stress on a plane defined by its strike and
        dip in the stress field.

        :param strike: strike direction (clockwise from north) (deg)
        :param dip: param dip: dip (clockwise from horizontal) (deg)
        '''
        tau, sn, _ = calc_tau_Sn_on_arbitrary_plane_3d(strike, dip,
                                            self.S1,
                                            self.S2,
                                            self.S3,
                                            self.azim_SH,
                                            self.regime)

        return tau, sn

    def compute_st_on_plane(self, strike, dip, normalize = True):
        '''
        computes the slip tendency of a fault defined by its strike and dip in
        the stress field.

        :param strike: strike direction (clockwise from north)
        :param dip: dip (clockwise from horizontal)
        :param normalize: If True, ST values are normalized using the stress
        fields mu attribute. Default is True.
        :returns: slip tendency
        '''
        tau, sn = self.compute_sn_tau_on_plane(strike, dip)

        if normalize:
            st = tau / (sn * self.mu)
        else:
            st = tau / sn

        return st

#    def plot_Mohr_3d(self, ax = None):
#        '''
#        plots a 3d Mohr circle
#        '''
#        if ax is None:
#            fig, ax = plt.subplots()
#
#        mc = Mohr3D(self)
#        mc.plot(ax)

@dataclass
class StressFieldAbs(StressField):
    '''
    Stress field defined by absolute S values
    '''
    Sh: float = None
    SH: float = None
    Sv: float = None
    Pp: float = None

    @property
    def regime(self):
        if self.Sv > self.SH > self.Sh:
            return 'normal'
        elif self.Sv < self.Sh < self.SH:
            return 'thrust'
        elif self.Sh < self.Sv < self.SH:
            return 'strike_slip'
        else:
            return 'something weird'

    @property
    def S1(self):
        return max([self.Sv - self.Pp, self.SH - self.Pp])

    @property
    def S3(self):
        return min([self.Sv - self.Pp, self.Sh - self.Pp])

    @property
    def S2(self):
        return np.sort([self.Sh - self.Pp,
                        self.SH  - self.Pp,
                        self.Sv - self.Pp])[1]
    
    def get_ordered_s(self):
        ordered_s_str = ['Sh', 'SH', 'Sv']
        
        ordered_s_num = [self.Sh, self.SH, self.Sv]
        
        ind = np.argsort(ordered_s_num)
        ordered_s_str = (np.take(ordered_s_str, ind))
        
        return ordered_s_str

@dataclass
class StressFieldGrad(StressField):
    '''
    Stress field defined by gradient

    :param Sh_grad: gradient in bar/m
    '''
    Sh_grad: float = None
    SH_grad: float = None
    Sv_grad: float = None
    Pp_grad: float = None

    @property
    def regime(self):
        if self.Sv_grad > self.SH_grad > self.Sh_grad:
            return 'normal'
        elif self.Sv_grad < self.Sh_grad < self.SH_grad:
            return 'thrust'
        elif self.Sh_grad < self.Sv_grad < self.SH_grad:
            return 'strike_slip'
        else:
            return 'something weird'

    @property
    def S1(self):
        return max([self.Sv_grad - self.Pp_grad, self.SH_grad - self.Pp_grad])

    @property
    def S3(self):
        return min([self.Sv_grad - self.Pp_grad, self.Sh_grad - self.Pp_grad])

    @property
    def S2(self):
        return np.sort([self.Sh_grad - self.Pp_grad, 
                        self.SH_grad - self.Pp_grad,
                        self.Sv_grad - self.Pp_grad])[1]

    #getters for dirfectional stresses at depth
    def get_Sh_at_z(self, z):
        '''
        z in m TVD
        '''
        return self.Sh_grad * z

    def get_SH_at_z(self, z):
        '''
        z in m TVD
        '''
        return self.SH_grad * z

    def get_Sv_at_z(self, z):
        '''
        z in m TVD
        '''
        return self.Sv_grad * z

    def get_Pp_at_z(self, z):
        '''
        z in m TVD
        '''
        return self.Pp_grad * z

    #getters for principal stresses at depth
    def get_S1_at_z(self, z):
        '''
        z in m TVD
        '''
        return self.S1 * z

    def get_S2_at_z(self, z):
        '''
        z in m TVD
        '''
        return self.S2 * z

    def get_S3_at_z(self, z):
        '''
        z in m TVD
        '''
        return self.S3 * z


    def compute_S1_from_S3(self):
        '''
        computes sigma_1 based on sigma_3 and the critically stressed crust
        theory
        '''
        return ((self.S3) * self.S1_S3_ratio + self.Pp_grad)
    
    def get_ordered_s(self):
        ordered_s_str = ['Sh', 'SH', 'Sv']
        
        ordered_s_num = [self.Sh_grad, self.SH_grad, self.Sv_grad]
        
        ind = np.argsort(ordered_s_num)
        ordered_s_str = np.take(ordered_s_str, ind)
        
        return ordered_s_str

class StressFieldSummarizer():
    def __init__(self, stress_field):
        self.stress_field = stress_field

    def summary(self):
        s = ''

        #TODO
        return s


class StressPolygon():
    def __init__(self, stress_field: StressField):
        self.stress_field = stress_field

    def plot(self, ax = None, consider_Pp = True):
        self.constructor = get_StressPolygon_constructor(self.stress_field)

        if ax is None:
            fig, ax = plt.subplots()

        ax = StressPolygonPlotter(self).plot(ax = ax)

class StressPolygonConstructor():
    def construct(self, stress_field):
        constructor = get_constructor(stress_field)
        
class StressPolygonConstructorABC(ABC):
    '''
    ABC for StressPolygonConstructor
    '''
    def __init__(self, stress_field: StressField):
        self.stress_field = stress_field
        
    def construct(self):
        '''
        constructs all coordinates needed to plot a StressPolygon. S1 ist taken 
        directly from the stress field, while Sv has been computed in the 
        appropriate StressPolygonConstructor
        '''
        #min Sh for NF
        self.min_Sh = self.stress_field.S1 / self.stress_field.S1_S3_ratio

        #max SH for RF
        self.max_SH = self.stress_field.S1 * self.stress_field.S1_S3_ratio

        #separator SS / NF
        self.SS_NF_x = [self.min_Sh, self.Sv]
        self.SS_NF_y = np.ones(2) * self.Sv

        #vertical connector to min_Sh
        self.vert_conn_Sh_x = np.ones(2) * self.min_Sh
        self.vert_conn_Sh_y = [self.min_Sh , self.Sv]

        #separator SS / RV
        self.SS_RV_x = np.ones(2) * self.Sv
        self.SS_RV_y = [self.Sv, self.max_SH]

        #horizontal connector to max_SH
        self.hor_conn_SH_x = [self.Sv, self.max_SH]
        self.hor_conn_SH_y = np.ones(2) * self.max_SH

        #slope
        self.slope_x = [self.min_Sh, self.Sv]
        self.slope_y = [self.Sv, self.max_SH]
        

class StressPolygonConstructorAbs(StressPolygonConstructorABC):
    '''
    constructor for absolute StressPolygon
    '''
    def __init__(self, stress_field: StressField):
        '''
        the only absolute value from the stress field used in the stress+
        polygon is the Sv. In a StressFieldGrad, Sv is Sv_grad
        '''
        super().__init__(stress_field)
        self.Sv = self.stress_field.Sv
        
        self.construct()
        
    
class StressPolygonConstructorGrad(StressPolygonConstructorABC):
    '''
    constructor for gradient StressPolygon
    '''

    def __init__(self, stress_field: StressField):
        super().__init__(stress_field)
        self.Sv = self.stress_field.Sv_grad

        self.construct()

class StressPolygonPlotter():
    def __init__(self, stress_polygon: StressPolygon):
        self.stress_polygon = stress_polygon

        self.stress_field = stress_polygon.stress_field

    def plot(self,  ax):
        Sh_ax = SH_ax = np.arange(0, self.stress_field.S1 *
                                  self.stress_field.S1_S3_ratio * 1.1)


        ax.plot(Sh_ax, SH_ax, '-', color = 'black')

        #Sv
        ax.scatter(self.stress_polygon.constructor.Sv,
                   self.stress_polygon.constructor.Sv, color = 'black')

        #separator SS / NF
        ax.plot(self.stress_polygon.constructor.SS_NF_x,
                     self.stress_polygon.constructor.SS_NF_y, color = 'black')

        #vertical connector to min_Sh
        ax.plot(self.stress_polygon.constructor.vert_conn_Sh_x,
                     self.stress_polygon.constructor.vert_conn_Sh_y, color = 'black')

        #separator SS / RV
        ax.plot(self.stress_polygon.constructor.SS_RV_x,
                     self.stress_polygon.constructor.SS_RV_y, color = 'black')

        #horizontal connector to max_SH
        ax.plot(self.stress_polygon.constructor.hor_conn_SH_x,
                     self.stress_polygon.constructor.hor_conn_SH_y, color = 'black')

        #delimiter of SS
        ax.plot(self.stress_polygon.constructor.slope_x,
                     self.stress_polygon.constructor.slope_y, color ='black')

        ax.set_xlabel('Sh ')
        ax.set_ylabel('SH')

        ax.grid()

        return ax

class circle():
    '''
    represents a circle with y of center equal to zero. Since intended for use
    in a Mohr circle, only the positive-y half of the circel is regarded.
    '''
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    #@property
    def trace(self, x = None):

        if x is None:
            step = (self.center + self.radius) / 500
            x = np.arange(self.center - self.radius, self.center + self.radius, step)
        y1 = np.sqrt(self.radius**2 - (x - self.center)**2)
        #y2 = -1 * y1

        return x, y1

    def plot(self, ax, color = 'black', xplot = None):
        if xplot is not None:
            x = xplot
            y = self.trace(x)[1]
        else:
            x = self.trace()[0]
            y = self.trace()[1]

        ax.plot(x, y, color = color, label = ' ')

class Mohr3D():
    def __init__(self, stress_field):
        self.sf = stress_field

    def plot(self, ax = None, color = 'black', plot_fc = True):
        if ax is None:
            fig, ax = plt.subplots()

        #mohr circles (3D)
        c1 = circle(self.sf.S3 + (self.sf.S2 - self.sf.S3)/2, (self.sf.S2 - self.sf.S3)/2)
        c2 = circle(self.sf.S2 + (self.sf.S1 - self.sf.S2)/2, (self.sf.S1 - self.sf.S2)/2)
        c3 = circle(self.sf.S3 + (self.sf.S1 - self.sf.S3)/2, (self.sf.S1 - self.sf.S3)/2)

        c1.plot(ax, color)
        c2.plot(ax, color)
        c3.plot(ax, color)

        if plot_fc: #plot failure criterion
            xs = [0, self.sf.S1]
            ys = [0, self.sf.S1 * self.sf.mu]
            ax.plot(xs, ys, color = color)
            
        #label sigmas
        x_positions = [self.sf.S3, self.sf.S2, self.sf.S1]
        x_labels = self.sf.get_ordered_s()
        y_ticks = ax.get_yticks()
        y =  -1.5* (y_ticks[1]- y_ticks[0])
        
        for i in zip(x_positions, x_labels):
            ax.text(i[0], y, i[1])
            
        ax.set_xlabel('Sigma n')
        ax.set_ylabel('Tau')
        ax.grid()

        #ax.axis('equal')
        
class StereonetPropertyPlotter():
    '''
    class to create a scatterplot of a property on a stereronet plot. the colorbar
    is normalized to min and max values of the property
    
    '''
    
    def __init__(self, strike: np.array,
                 dip: np.array, prop: np.array, title: str = ' '):
        '''
        :param strike: strike (from north, clockwise)
        :param dip: dip (from horizontal)
        :param prop: property to plot as scatter color
        '''
        self.strike = strike
        self.dip = dip
        self.prop = prop
        self.title = title
        
    def plot(self):
               
        fig = plt.figure()
        ax = fig.add_subplot(111, projection = 'stereonet')
        ax.grid()
        
        norm = matplotlib.colors.Normalize(vmin=min(self.prop),vmax = max(self.prop))
        cmap = matplotlib.cm.get_cmap('plasma')
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        
        for i in zip(self.strike, self.dip, self.prop):
            ax.pole(i[0], i[1], 'o', c = cmap(i[2]))
           # ax.plane(plane.strike, plane.dip, c = cmap(plane.st))
           
        fig.colorbar(sm, ax=ax)
        ax.set_title(self.title)
        
        plt.show()
# =============================================================================
#  General methods
# =============================================================================
def get_StressPolygon_constructor(stress_field):
    if isinstance(stress_field, StressFieldAbs):
        return StressPolygonConstructorAbs(stress_field)
    elif isinstance(stress_field, StressFieldGrad):
        return StressPolygonConstructorGrad(stress_field)

def factor_from_mu(mu):
    return (np.sqrt(mu**2 + 1) + mu)**2

def sigma_tn_at_angle(sigma1: float, sigma3: float, beta: float) -> float:
    '''
    computes tensile and normal stress on a plane inclined with beta
    relative to the maximum stress

    Parameters
    ----------
    sigma1: float
    Maximum stress
    sigma3: float
    Minimal stress
    beta: angle between the normal to the plane in question and the sigma1 direction (radian).
        i.e: when the plane lies orthogonal to tS1, then beta is 0.

    Returns
    ----------
    (sigma_n, sigma_t)
    '''
    sigma_n = 0.5 * (sigma1 + sigma3) + 0.5 * (sigma1 - sigma3) * np.cos(2 * beta)
    sigma_t = 0.5*(sigma1 - sigma3) * np.sin(2 * beta)

    return sigma_n, sigma_t

def compute_critical_angle(mu: float = 0.6):
    '''
    Computes the optimum angle for sliding in a stress field dependent on mu.
    (Eq. 4.42, page 132 in Zoback)

    Beta is defined as  the angle between a fault normal and the direction of Sigma 1.
    If the fault is parallel to S1, then beta is 90°.
    If the fault is normal to S1, then beta is 0°.

    Parameter
    --------
    mu: float, optional
    Coefficient of friction [rad]. Default is 0.6

    Returns
    --------
    critical angle (rad)
    '''

    return np.pi / 2 - np.arctan(mu)




# =============================================================================
# Alternative calculation of the shear and normal stress acting on arbitrarily oriented
# faults in three dimensions
# =============================================================================

def set_S(S1,S2,S3):
    S = np.array([[S1,0,0],
                   [0,S2,0],
                   [0,0,S3]])
    return S

# set_R1 assumes Sv is a principle stress
def set_R1(azimuth,faulting_regime='strike_slip'):

    '''
    set_R1 assumes Sv is a principle stress
    Rotation matrix to transform principle stress tensor into
    geographic coordinate system
    source: https://dnicolasespinoza.github.io/node38.html

    Parameter
    --------
    faulting_regime: must one of the following: 'strike_slip','normal','thrust' , string
    azimuth: must be projection angle on horizontal plane of Shmin(normal faulting) or Shmax(strike slip or thrust faulting) vector to geographic nord, float

    '''

    angles = dict(normal=[azimuth,90,0],
                  strike_slip=[azimuth,0,90],
                  thrust=[azimuth,0,0])

    a=math.radians(angles[faulting_regime][0])
    b=math.radians(angles[faulting_regime][1])
    c=math.radians(angles[faulting_regime][2])

    R1 = np.array([[np.cos(a)*np.cos(b),
                    np.sin(a)*np.cos(b),
                    -np.sin(b)],

                   [np.cos(a)*np.sin(b)*np.sin(c) - np.sin(a)*np.cos(c),
                    np.sin(a)*np.sin(b)*np.sin(c) + np.cos(a)*np.cos(c),
                    np.cos(b)*np.sin(c)],

                   [np.cos(a)*np.sin(b)*np.cos(c) + np.sin(a)*np.sin(c),
                    np.sin(a)*np.sin(b)*np.cos(c) - np.cos(a)*np.sin(c),
                    np.cos(b)*np.cos(c)]])


    return R1


def set_R1_abc(a,b,c):

    '''
    ATTENTION: angles must be provided in radiants!!!!!!!

    get rotation matrix based on director angles
    see fig. 5.22 https://dnicolasespinoza.github.io/node38.html
    for a graphic eplxaining a=alpha, b=beta, c=gamma
    '''

    R1 = np.array([[np.cos(a)*np.cos(b),
                    np.sin(a)*np.cos(b),
                    -np.sin(b)],

                   [np.cos(a)*np.sin(b)*np.sin(c) - np.sin(a)*np.cos(c),
                    np.sin(a)*np.sin(b)*np.sin(c) + np.cos(a)*np.cos(c),
                    np.cos(b)*np.sin(c)],

                   [np.cos(a)*np.sin(b)*np.cos(c) + np.sin(a)*np.sin(c),
                    np.sin(a)*np.sin(b)*np.cos(c) - np.cos(a)*np.sin(c),
                    np.cos(b)*np.cos(c)]])


    return R1


def get_Sg (S,R1):

    '''
    Zoback eq 5.10
    '''

    Sg = R1.T @ S @ R1

    return Sg


def calc_tau_Sn_on_arbitrary_plane_3d (str_fault,dip_fault,
                                       S1,S2,S3,
                                       azimuth,faulting_regime='strike_slip'):

    '''
    calculation of the shear and normal stress acting on arbitrarily oriented
    faults in three dimensions
    after https://dnicolasespinoza.github.io/node38.html

    Parameter
    --------
    S1,S2,S3: principle stresses, float, required
    azimuth: must be projection angle (in degrees) on horizontal plane of Shmin(normal faulting) or Shmax(strike slip or thrust faulting) vector to geographic nord, float, required
    faulting_regime: must one of the following: 'strike_slip','normal','thrust' , string, required
    str_fault: angle of strike vector of plane against North in degrees, float, required
    dip_fault: fault dip in degrees, float, required

    Returns
    ----------
    tau: absolute shear, τ , which acts in the direction of fault slip in the fault plane
    Sn: effective normal stress, Sn, in the fault plane
    rake: in degrees, The rake is the angle of the shear stress with respect to n_s (horizontal line) and quantifies the direction of expected fault movement in the fault plane

    '''

    S = set_S(S1,S2,S3)
    R1 = set_R1(azimuth,faulting_regime)
    Sg = get_Sg(S,R1)

    str_fault = math.radians(str_fault)
    dip_fault = math.radians(dip_fault)

    nn = np.array([-np.sin(str_fault)*np.sin(dip_fault),
                   np.cos(str_fault)*np.sin(dip_fault),
                   -np.cos(dip_fault)])

    ns = np.array([np.cos(str_fault),
                   np.sin(str_fault),
                   0])

    nd = np.array([-np.sin(str_fault)*np.cos(dip_fault),
                   np.cos(str_fault)*np.cos(dip_fault),
                   np.sin(dip_fault)])

    t = Sg @ nn

    Sn = t @ nn

    td = t @ nd
    ts = t @ ns

    tau = np.sqrt(td**2 + ts**2)

    rake = math.degrees(np.arctan(td/ts))

    return tau, Sn, rake



def calc_ST_reseng (str_fault,dip_fault,S1,S2,S3,a,b,c):

    '''
    calculation of the shear and normal stress acting on arbitrarily oriented
    faults in three dimensions
    after https://dnicolasespinoza.github.io/node38.html

    Parameter
    --------
    S1,S2,S3: principle stresses, float, required
    azimuth: must be projection angle (in degrees) on horizontal plane of Shmin(normal faulting) or Shmax(strike slip or thrust faulting) vector to geographic nord, float, required
    faulting_regime: must one of the following: 'strike_slip','normal','thrust' , string, required
    str_fault: angle of strike vector of plane against North in degrees, float, required
    dip_fault: fault dip in degrees, float, required

    Returns
    ----------
    tau: absolute shear, τ , which acts in the direction of fault slip in the fault plane
    Sn: effective normal stress, Sn, in the fault plane
    ST: Sliptendency not normalized
    ST_norm : Sliptendency to mu
    '''

    S = set_S(S1,S2,S3)
    R1 = set_R1_abc(a,b,c)
    Sg = get_Sg(S,R1)

    str_fault = math.radians(str_fault)
    dip_fault = math.radians(dip_fault)

    nn = np.array([-np.sin(str_fault)*np.sin(dip_fault),
                   np.cos(str_fault)*np.sin(dip_fault),
                   -np.cos(dip_fault)])

    ns = np.array([np.cos(str_fault),
                   np.sin(str_fault),
                   0])

    nd = np.array([-np.sin(str_fault)*np.cos(dip_fault),
                   np.cos(str_fault)*np.cos(dip_fault),
                   np.sin(dip_fault)])

    t = Sg @ nn

    Sn = t @ nn

    td = t @ nd
    ts = t @ ns

    tau = np.sqrt(td**2 + ts**2)




    ST = abs(tau/Sn)


    return tau, Sn, ST


def angle_in_range(alpha, lower, upper):
    return (alpha - lower) % 360 <= (upper - lower) % 360


def calc_ST_reseng_v2 (str_fault,dip_fault,S1,S2,S3,a,b,c,mu):

    '''
    calculation of the shear and normal stress acting on arbitrarily oriented
    faults in three dimensions
    after https://dnicolasespinoza.github.io/node38.html

    Parameter
    --------
    S1,S2,S3: principle stresses, float, required
    a,b,c: in radians, angles for rotation of principle stres tensor into geographic coordinate system
    faulting_regime: must one of the following: 'strike_slip','normal','thrust' , string, required
    str_fault: in radians, angle of strike vector of plane against North in degrees, float, required
    dip_fault: in radians fault dip in degrees, float, required
    mu: 0-1.0 kritischer Winkel aus Theorie der gespannten Kruste

    Returns
    ----------
    tau: absolute shear, τ , which acts in the direction of fault slip in the fault plane
    Sn: effective normal stress, Sn, in the fault plane
    ST: Sliptendency not normalized
    ST_norm : Sliptendency to mu
    '''
    
    #simple check if input angles are def not in radians:
    angles = [str_fault,dip_fault,a,b,c]
    for angle in angles:
        if angle_in_range(angle,6.29,360):
            print('WARNING: INPUT ANGLE NOT IN RADIANS!! {}'.format(angle))
    
    
    #set principle stress tensor
    S = set_S(S1,S2,S3)
    #generate rotation matrix for transformation into geogrpahic coordinate system
    R1 = set_R1_abc(a,b,c)
    #cauchy stress tensor in geographic coordinates system
    Sg = get_Sg(S,R1)


    #fault normal vector in geographic coordinates system
    nn = np.array([-np.sin(str_fault)*np.sin(dip_fault),
                   np.cos(str_fault)*np.sin(dip_fault),
                   -np.cos(dip_fault)])
    #fault strike vector in geographic coordinates system
    ns = np.array([np.cos(str_fault),
                   np.sin(str_fault),
                   0])
    #fault dip vector in geographic coordinates system
    nd = np.array([-np.sin(str_fault)*np.cos(dip_fault),
                   np.cos(str_fault)*np.cos(dip_fault),
                   np.sin(dip_fault)])
    
    
    t = Sg @ nn

    Sn = t @ nn


    td = t @ nd
    ts = t @ ns

    tau = np.sqrt(td**2 + ts**2)

    ST = abs(tau/Sn)
    ST_norm = ST/mu

    return tau, Sn, ST, ST_norm


def calc_ST_guido (planenormal,S1,S2,S3,a,b,c):
    # =============================================================================
    # =============================================================================
    # # Achtung GUIDO Function vernachlässigt Scherspannungen im Spannungsfeld und geht von einem N-S Spannungsfeld aus
    # =============================================================================
    # =============================================================================
    n_X = planenormal[0]
    n_Y = planenormal[1]
    n_Z = planenormal[2]
    # =============================================================================
    #       Umrechnen des Stressfeldes ins x,y,z Koordinatensystem
    # =============================================================================
    S = set_S(S1,S2,S3)
    R1 = set_R1_abc(a,b,c)
    Sg = get_Sg(S,R1)
    S_mag = np.sum(Sg,0) #summing vector components for x,y,z = summing up columns of matrix    
    
    # =============================================================================
    #    s_X=S_mag[0] #east = x = second column of Sg/S_mag
    #    s_Y=S_mag[1] #north = y = first column of Sg/S_mag
    #    s_Z=S_mag[2] #down = z = third column of Sg/S_mag
    # =============================================================================

    s_X=Sg[0,0] #east = x = second column of Sg/S_mag
    s_Y=Sg[1,1] #north = y = first column of Sg/S_mag
    s_Z=Sg[2,2] #down = z = third column of Sg/S_mag

    # =============================================================================
    #       Calculation of absolute shear stress on fault
    # =============================================================================
    t=(n_X**2*n_Y**2*(s_X-s_Y)**2 + n_Z**2*n_Y**2*(s_Z-s_Y)**2 + n_X**2*n_Z**2*(s_X-s_Z)**2)**0.5
    # =============================================================================
    #       Calculation of normal stress on fault
    # =============================================================================
    s=abs(n_X**2*s_X + n_Y**2*s_Y + n_Z**2*s_Z)
    # =============================================================================
    #       Calculation of Slip Tendecy
    # =============================================================================
    ST=abs(t/s)

    return t, s, ST






def unit_vector(vector):
    """ Returns the unit vector of a vector."""
    return vector / np.linalg.norm(vector)

def vector_magnitude(vector):
    """ Returns the magnitude of a vector."""
    return np.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

def angle_between(v1, v2):
    """Finds angle between two vectors"""
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))

def x_rotation(vector,theta):
    """Rotates 3-D vector around x-axis"""
    R = np.array([[1,0,0],[0,np.cos(theta),-np.sin(theta)],[0, np.sin(theta), np.cos(theta)]])
    return np.dot(R,vector)

def y_rotation(vector,theta):
    """Rotates 3-D vector around y-axis"""
    R = np.array([[np.cos(theta),0,np.sin(theta)],[0,1,0],[-np.sin(theta), 0, np.cos(theta)]])
    return np.dot(R,vector)

def z_rotation(vector,theta):
    """Rotates 3-D vector around z-axis"""
    R = np.array([[np.cos(theta), -np.sin(theta),0],[np.sin(theta), np.cos(theta),0],[0,0,1]])
    return np.dot(R,vector)

def rot_vector(vector, axis_v, angle):
    """Rotates 3-D vector around a given axis-vector"""
    angle_rad = np.radians(-angle)
    a1 = axis_v[0]
    a2 = axis_v[1]
    a3 = axis_v[2]

    ident = np.identity(3)
    out = np.outer(axis_v, axis_v)
    a_x = np.array([[0, -a3, a2], [a3, 0, -a1], [-a2, a1, 0]])
    rot_matrix = (np.cos(angle_rad) * ident) + (np.sin(angle_rad) * a_x) + (1 - np.cos(angle_rad)) * out

    return np.dot(rot_matrix,vector)

def rotate_via_scipy(inputvector,angle,rot_axis=np.array([0, 0, 1])):
    """Rotates 3-D vector around a given axis-vector"""
    rotation_degrees = -angle
    rotation_radians = np.radians(rotation_degrees)
    rotation_axis = rot_axis
    rotation_vector = rotation_radians * rotation_axis
    rotation = Rotation.from_rotvec(rotation_vector)
    rotated_vec = rotation.apply(inputvector)
    return rotated_vec

def get_strike_dip(plane_normal,hide_warnings=False):
    '''
    Retrieves strike and dip angles in geographic coordinate system (x,y,z = E,N,Down)
    from an input plane normal vector in x,y,z format 
    
    
    Parameters
    ----------
    plane_normal : 3D vector [x,y,z]

    Returns
    -------
    strike : strike angle in degrees of plane relative to North aka y of coordinate system
    dip : dip angle in degrees of plane relative to horizontal plane

    '''

    if vector_magnitude(plane_normal) > 0:

        plane_normal_projection_horizontal = unit_vector([plane_normal[0],plane_normal[1],0])
        north_v = np.array([0,1,0])

        dipdirection_angle = angle_between(plane_normal_projection_horizontal,north_v)

        if plane_normal[0] < 0:
            dipdirection_angle = 360 - dipdirection_angle

        strike = dipdirection_angle - 90
        
        if strike < 0:
            strike = strike + 360

        dipdirection_v = rot_vector([0,1,0], [0,0,1], dipdirection_angle) #rotate Northvector to dipdirection should be the same as plane_normal_projection_horizontal if normalized

        if np.allclose(dipdirection_v, plane_normal_projection_horizontal) == False:
            print('Warning ... something with dip angle is probably wrong!!')

        dip = 90 - angle_between(plane_normal,dipdirection_v)

    else:
        if hide_warnings == False:
            print('Warning ... planenormal has 0 maginitude --> strike,dip set to 0, calculation makes no sense!!')
        strike = 0
        dip = 0

    return strike,dip

def get_normal(strike,dip):
    '''

    Parameters
    ----------
    strike : strike angle in degrees of plane relative to North aka y of coordinate system
    dip : dip angle in degrees of plane relative to horizontal plane

    Returns
    -------
    plane_normal : 3D vector [x,y,z]

    '''

    #rotate Northvector by strikeangle
    strike_v = rot_vector([0,1,0], [0,0,1], strike)
    
    #rotate Northvector to dipdirection
    dipdirection_v = rot_vector([0,1,0], [0,0,1], strike+90)

    #rotate dipdirectionvector around strikevector by 90-dipangle
    plane_normal = rot_vector(dipdirection_v, strike_v, dip-90)


    return plane_normal

























# =============================================================================
#
# #exmaple of rotating vertical fault zone
# from matplotlib import pyplot as plt
# S1 = 310
# S2 = 150
# S3 = 100
# faulting_regime='strike_slip'
# azimuth=0 #in case of 'strike_slip' this is the azimuth of Shmax
# str_fault_list = np.arange(0,181)
# dip_fault = 90
#
# t_l = []
# n_l = []
# rake_l = []
# for str_fault in str_fault_list:
#
#     t, n, rake = calc_tau_Sn_on_arbitrary_plane_3d (str_fault,dip_fault,
#                                                     S1,S2,S3,
#                                                     azimuth=0,faulting_regime='strike_slip')
#     t_l.append(t)
#     n_l.append(n)
#     rake_l.append(rake)
#
# _, ax = plt.subplots()
# ax.plot(str_fault_list, n_l, label = 'normal')
# ax.plot(str_fault_list, t_l, label = 'shear')
# ax.plot(str_fault_list, rake_l, label = 'rake')
# ax.grid()
# ax.legend()
#
# plt.show()
# =============================================================================


# =============================================================================
# #benchmarks
# #5.9 https://dnicolasespinoza.github.io/node38.html
#
# S1 = 23
# S2 = 15
# S3 = 13.8
# faulting_regime='normal'
# azimuth=90
# str_fault = 0
# dip_fault = 60
#
# S = set_S(S1,S2,S3)
# R1 = set_R1(azimuth,faulting_regime)
# Sg = get_Sg(S,R1)
#
# str_fault = math.radians(str_fault)
# dip_fault = math.radians(dip_fault)
#
# nn = np.array([-np.sin(str_fault)*np.sin(dip_fault),
#                np.cos(str_fault)*np.sin(dip_fault),
#                -np.cos(dip_fault)])
#
# ns = np.array([np.cos(str_fault),
#                np.sin(str_fault),
#                0])
#
# nd = np.array([-np.sin(str_fault)*np.cos(dip_fault),
#                np.cos(str_fault)*np.cos(dip_fault),
#                np.sin(dip_fault)])
#
# t = Sg @ nn
#
# Sn = t @ nn
#
# td = t@nd
# ts = t@ns
#
# tau = np.sqrt(td**2+ts**2)
#
# rake = math.degrees(np.arctan(td/ts))
# =============================================================================