"""Tests the evaluation of the poten    al fer single and array-vauled arguments for the simple
harmonic oscillator, bump-down, and Kronig-Penney potentials.
"""
import pytest
from basis.potential import Potential
import numpy as np

def test_getattr():
    """Tests the attribute re-routing to Potential.params
    """
    pot = Potential("potentials/kronigPenney.cfg")
    assert 0==0

    pot = Potential("potentials/bumpdown.cfg")
    assert pot.a == pot.params["a"]

    pot = Potential("potentials/sho.cfg")
    with pytest.raises(AttributeError):
        pot.w 
        pot.dummy

def test_adjust():
    pot = Potential("potentials/bumpdown.cfg")
    pot.adjust(shift = 1)

    
def test_sho():
    """Tests the SHO potential."""
    pot = Potential("potentials/sho.cfg")

    assert pot(1.2) == 0.

def test_regions():
    """Tests for a missing regions section in the config file.
    """
    with pytest.raises(ValueError):
        pot = Potential("potentials/test_regions.cfg")      
    pot = Potential("potentials/test_numpy_import.cfg")
        
        
def test_kronigPenney():
    """Tests the Kronig-Penney potential
    """
    pot = Potential("potentials/kronigPenney.cfg")
    assert pot(0) == 10
    assert pot(1.5) == 0
    
def test_bumpdown():
    """Tests the bump down in the square well potential.
    """

    pot = Potential("potentials/bumpdown.cfg")
    params = [(2,1,15.,100),
              (1e5,5e4,1234.,1e5),
              (1./3,1./6,10,5),
              (np.pi,np.pi/2.,-np.sqrt(2),23)]
    
    for a, w, V0, N in params:
        pot.adjust(a=a, w=w, v0=V0)
        x = w+(a-w)/2.
        xa = np.linspace(-a, a, N)    
        assert pot(x) == V0
        assert pot(3./4*w) == 0.
        assert pot(5./4*w) == V0
        assert len(pot(xa)) == N
        assert pot(-.5*a) == 0.
        assert pot(-w) == 0
        assert pot(a) == 0.
        with pytest.raises(ValueError):
            pot("a")           
