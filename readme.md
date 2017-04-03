TODO: Make this prettier.

Usage (for a thin, glass mug):

```python wtemp.py glass timeto 79.0```

This will print the time (in seconds) it takes for the mug of water to cool
until it reaches 79 degrees celsius. The defaults assume a mug of 2mm thickness
(very thin for a mug -- the defaults are based on my personal mug which is
pretty thin)

You can do this for a ceramic mug with:

```python wtemp.py ceramic timeto 79.0```

You can customize almost anything to fit a mug of your size. Just read the
source, it's extremely well documented. In fact, if you don't your results will
be innacurate since some setup details are specified (like putting a lid on the
mug and raising the mug off the counter with something which doesn't make a lot
of surface contact with the bottom).

Values are currently slightly off from what seems right, but I'm not sure. My
intuition for this could just be off. Will try to test this later tonight...

The CLI is done with google's python fire, so you can customize everything from
the command line:

```python wtemp.py --thickness=0.005 --t_ambient=74.6 --specific_heat=2.3 --surface_area=50 ceramic timeto 78```
