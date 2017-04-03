# wtemp
# =====
# This is a script to prepare a mug of water at a specific temperature without a
# thermometer. This bit of magic works by first setting the water at 100 degrees
# celsius (microwave until it is boiling) and then calculating the amount of
# time it would take for a mug of water to cool down to the desired temperature.
# WARNING: please read at least the first two items in the list of assumptions
# (below) to ensure you get accurate results. Also read up on how I calculated
# the variable MY_MUG_SURFACE_AREA below.
#
# If you have a thermometer, let me know how this program works compared to
# using your thermometer!
#
# Where did I get the math from?
# ==============================
# This page:
# http://www.physicsclassroom.com/class/thermalP/Lesson-1/Rates-of-Heat-Transfer
# I'm starting to question how accurate it is...
#
# List of assumptions (please read at lest the first two for accurate results)
# ============================================================================
# - The top of the mug is covered with a shield which has the same thickness and
# material as the rest of the mug. Sorry, I don't know how to model convection
# of water evaporating out of the cup. If you don't do this, the calculation
# will be way off.
# - The mug is not resting on a counter (I rest it on a ring of copper tube so
# that most of the mug surface area is in contact with air, and the parts which
# aren't are touching a hollow metal tube). Or if it is on a counter, that the
# counter does not heat up as the mug cools (infinite specific heat). This is
# because the atmosphere is kind of like a thermal ground -- even if the mug
# heats up the air around it, air currents will carry and air away and cold air
# will replace the warm air. The counter does not act like this at all and we do
# not model the counter.
# - That the liquid in the mug is water. If not, you can tweak the liquid
# specific heat to fit your liquid.
# - That the energy released from all the hot water in the mug does not
# seriously impact room temperature (it shouldn't, unless you have a really big
# mug or a really small room).
# - That the walls of the mug sticking up above the water level don't affect the
# heat transfer too much (admittedly, this is probably a big source of error).
# - No convection currents are induced in the water in the mug.

import fire
import math

# Constants
# =========
# This is approximate. Units are W/(mK) (watts/(meters*kelvin)). Data source:
# https://prezi.com/iwto6j4zvzni/heat-transfer-principles-of-coffee-cups/
GLASS_THERMAL_COEFFICIENT = 1.0
CERAMIC_THERMAL_COEFFICIENT = 0.9
# Units are Joules/(gram * degrees celsius)
WATER_SPECIFIC_HEAT = 4.186
# This is only valid for my personal mug. Units are meters. Includes the bottom
# and sides. Measured empirically. Be careful when you measure this, as you're
# actually measuring the surface area of the mug in contact with the water, so
# it depends on how high you fill the mug!! I fill mine up to a height of 5.5cm
# (marked off on my mug).
#
# Total SA = Wall SA + (bottom SA + top SA) = Wall SA + (bottom SA * 2) = PI * D
# * h + 2*(PI * r^2)
# h = 5.5cm = 0.055m
# d = 7.5cm = 0.075m
MY_MUG_SURFACE_AREA = math.pi * (0.075) * 0.055 + 2 * (math.pi * ((0.075/2) ** 2))
# Units are in meters. Measured with a pair of calipers (always gotta keep your
# calipers handy. never know when you're gonna need them). My glass is really
# skinny, a more normal value would be 0.005 (5mm). If your mug is thick, try
# 0.007 (7mm).
MY_MUG_THICKNESS = 0.002
# How much water you put in your cup. Units are in grams (for water, this is the
# same as milliliters).
MY_MUG_VOLUME = 250
# Units in celsius. Ambient temperature of the room the cup is in. 
MY_APARTMENT_AMBIENT_TEMPERATURE = 24.4444

class MugGenerator(object):
  def __init__(self, surface_area=MY_MUG_SURFACE_AREA, mass=MY_MUG_VOLUME,
      t_ambient=MY_APARTMENT_AMBIENT_TEMPERATURE, thickness=MY_MUG_THICKNESS,
      specific_heat=WATER_SPECIFIC_HEAT):
    self.surface_area = surface_area
    self.mass = mass
    self.t_ambient = t_ambient
    self.thickness = thickness
    self.specific_heat = specific_heat
  def glass(self):
    return Mug(GLASS_THERMAL_COEFFICIENT, self.surface_area, self.mass,
        self.t_ambient, self.thickness, self.specific_heat)
  def ceramic(self):
    return Mug(CERAMIC_THERMAL_COEFFICIENT, self.surface_area, self.mass,
        self.t_ambient, self.thickness, self.specific_heat)

class Mug(object):
    """A class which represents a mug of liquid."""
    def __init__(self, thermal_coefficient, surface_area, mass, t_ambient,
        thickness, specific_heat):
      self.thermal_coefficient = thermal_coefficient
      self.surface_area = surface_area
      self.mass = mass
      self.thickness = thickness
      self.specific_heat = specific_heat
      self.t_ambient = t_ambient
    def timeto(self, target_temp):
      # This is the differentiable equation:
      # dT/dt * s * m = -k * SA * (T - a) / d
      # T = temperature of water in degrees celsius
      # t = time seconds
      # s = specific heat
      # m = mass of water (grams or ml)
      # k = thermal conductivity
      # SA = surface area in square meters
      # a = temperature of air (ambient). degrees celsius.
      # d = thickness of mug in meters.
      # This is solved by wolfram alpha since I'm shit at diffeqs. Closed form
      # solution:
      # T(t) = a + const*e^(-k*SA*t/(d*m*s))
      # We can solve for the const since we know T(0) = 100 degrees celsius
      # const = 100 - a
      # Now we're trying to find the time t1 when T(t1) = target_temp.
      # target_temp = a + (100 - a)*e^(-k*SA*t1/(d*m*s))
      # ln(target_temp - a) = ln((100 - a)) - k*SA*t1/(d*m*s)
      # - ln((target_temp - a)/(100 - a)) * (d*m*s)/(k*SA) = t1
      # t1 = -(d*m*s)/(k*SA) * ln((target_temp - a)/(100 - a))
      return -1 * ((self.thickness * self.mass * self.specific_heat) /
          (self.thermal_coefficient * self.surface_area)) * math.log((target_temp - self.t_ambient)/(100 - self.t_ambient))

if __name__ == "__main__":
  fire.Fire(MugGenerator)
