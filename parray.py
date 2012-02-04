###############################################################################
#    PARRAY - Script to simulate phased arrays in numpy
#    Copyright (C) 2012 - Gokul Das B
#
#                   GNU General Public License - V3
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

"""Module for simulating phased arrays in numpy"""

import numpy as np
import matplotlib.pyplot as plt

def common_PA_elements(self):
    """Generate array elements for a common array"""
    el_n = \
    np.linspace(-(self.el_num - 1.0)/2, (self.el_num - 1.0)/2, self.el_num)

    print el_n
    self.el_x = 2 * np.pi * self.el_sep * el_n
    self.el_y = el_n * 0
    self.el_amp = np.ones(el_n.shape)
    self.el_phi = el_n * self.el_phs

#############################################

class PhasedArray:
    """Phased Array simulation"""
    def __init__(self, res, rng, el_sep, el_num, el_phs):
        """Initialize array parameters

        res     : Display Resolution
        rng     : Field range in terms of wavelength
        el_sep  : Array element separation in terms of wavelength
        el_num  : No of elements
        el_phs  : Phase separation between elements"""

        self.res = res
        self.rng = rng
        self.el_sep = el_sep
        self.el_num = el_num
        self.el_phs = el_phs

    # Define a replacable implementation of array element generator
    gen_elements = common_PA_elements
    
    def calc_field(self):
        """Calculate field"""

        x0 = y0 = \
        np.linspace(-2 * np.pi * self.rng, 2 * np.pi * self.rng, self.res)

        self._z = np.zeros((self.res, self.res))
        # self._mask = self._z != 0
        self._x, self._y = np.meshgrid(x0, y0)

        for xz, yz, az, pz in \
        zip(self.el_x, self.el_y, self.el_amp, self.el_phi):
            # print 'x y amp ph: ', xz, yz, az, pz
            xt, yt = x0 - xz, y0 - yz
            xi, yi = np.meshgrid(xt, yt)
            r = np.sqrt(xi ** 2 + yi ** 2)
            # self._mask = np.ma.mask_or(self._mask, r < 12)
            #val = (az / r ** 2) * np.sin(r + pz)    # Implement inverse square
            val = az * np.sin(r + pz)
            self._z = self._z + val
        
    def display(self):
        """Display field"""
        #zm = np.ma.masked_array(z, mask = self._mask)
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.contourf(self._x, self._y, self._z)
        ax.plot(self.el_x, self.el_y, 'o')
        fig.show()

    def simulate(self):
        """Run phased array simulation"""
        self.gen_elements()
        self.calc_field()
        self.display()

#############################################
########## COMMON PHASED ARRAYS #############
#############################################
params_generic = {    \
'res' : 200.0,  \
'rng' : 30.0,   \
'el_sep' : 0.5, \
'el_num' : 10,   \
'el_phs' : 2 * np.pi * 0.25 }

PAGeneric = PhasedArray(**params_generic)
#############################################
params_broadfire = {    \
'res' : 200.0,  \
'rng' : 30.0,   \
'el_sep' : 0.5, \
'el_num' : 10,   \
'el_phs' : 0 }

PABroadfire = PhasedArray(**params_broadfire)
#############################################
params_endfire = {    \
'res' : 200.0,  \
'rng' : 30.0,   \
'el_sep' : 0.5, \
'el_num' : 10,   \
'el_phs' : 2 * np.pi * 0.5}

PAEndfire = PhasedArray(**params_endfire)
############################################# 

