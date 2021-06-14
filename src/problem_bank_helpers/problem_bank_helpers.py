# Author: Firas Moosvi, Jake Bobowski, others
# Date: 2021-05-26

from collections import defaultdict
import numpy as np
import sigfig

def roundp(*args,**kwargs):
    """ Wrapper function for the sigfig.round package.

    Args:
        num (number): Number to round or format.

    Returns:
        float/str: Rounded number output to correct significant figures.
    """
    
    return sigfig.round(*args,**kwargs)

def round_str(*args,**kwargs):
    
    if type(args[0]) is str:
        return args[0]
    
    if 'sigfigs' not in kwargs.keys():
        kwargs['sigfigs'] = 2
    
    if 'format' not in kwargs.keys():
        if np.abs(args[0]) < 1:
            return roundp(*args,**kwargs,format='std')
        elif np.abs(args[0]) < 1E6:
            return roundp(*args,**kwargs,format='English')
        else:
            return roundp(*args,**kwargs,format='sci')
    else:
        return roundp(*args,**kwargs)
    
def round_sig(x, sig_figs = 3):
    """A function that rounds to specific significant digits. Original from SO: https://stackoverflow.com/a/3413529/2217577; adapted by Jake Bobowski

    Args:
        x (float): Number to round to sig figs
        sig_figs (int): Number of significant figures to round to; default is 3 (if unspecified)

    Returns:
        float: Rounded number to specified significant figures.
    """
    return round(x, sig_figs-int(np.floor(np.log10(np.abs(x))))-1)

def num_as_str(num, digits_after_decimal = 2):
    """Rounds numbers properly to specified digits after decimal place

    Args:
        num (float): Number that is to be rounded
        digits_after_decimal (int, optional): Number of digits to round to. Defaults to 2.

    Returns:
        str: A string that is correctly rounded (you know why it's not a float!)
    """
    """
    This needs to be heavily tested!!
    WARNING: This does not do sig figs yet!
    """

    # Solution attributed to: https://stackoverflow.com/a/53329223

    if type(num) == str:
        return num
    elif type(num) == dict:
        return num
    else:
        from decimal import Decimal, getcontext, ROUND_HALF_UP

        round_context = getcontext()
        round_context.rounding = ROUND_HALF_UP

        tmp = Decimal(num).quantize(Decimal('1.'+'0'*digits_after_decimal))

        return str(tmp)
