"""Component classes."""

# stdlib
from gettext import install
import logging

# external
import numpy as np

# project
from payload_designer.libs import physlib, utillib

LOG = logging.getLogger(__name__)

class Foreoptics:
    """Foreoptics component.

    Args:
        ds_i (float, optional): image distance. Defaults to None.
        ds_o (float, optional): object distance. Defaults to None.
        n (float, optional): f-number. Defaults to None.
        dm_a (float, optional): aperture diameter. Defaults to None.
        a_in_max (float, optional): maximum angle of incidence in degrees. Defaults to None.
        na (float, optional): numerical aperture. Defaults to None.
        b (float, optional): source radiance. Defaults to None.
        g (float, optional): geometric etendue. Defaults to None.
        s (float, optional): area of emitting source. Defaults to None.

    """

    def __init__(
        self,
        ds_i=None,
        ds_o=None,
        n=None,
        dm_a=None,
        a_in_max=None,
        na=None,
        b=None,
        g=None,
        s=None
    ):
        self.ds_i = ds_i
        self.ds_o = ds_o
        self.n = n
        self.dm_a = dm_a
        self.a_in_max = a_in_max
        self.na = na
        self.b = b
        self.g = g
        self.s = s

    def get_aperture_diameter(self):
        """Calculate the aperture diamter.

        Returns:
            float: aperture diameter (mm).
        """
        assert self.ds_i is not None, "ds_i is not set."

        if self.n is not None:
            dm_a = np.divide(self.ds_i, self.n)
        elif self.na is not None:
            dm_a = 2*np.multiply(self.ds_i, self.na)
        else:
            raise ValueError("n or na must be set.")

        return dm_a

    def get_magnification(self):
        """Calculate the magnification of the foreoptics.

        Returns:
            float: magnification (unitless).
        """
        assert self.ds_i is not None, "ds_i is not set."
        assert self.ds_o is not None, "ds_o is not set."

        m = np.divide(self.ds_i,self.ds_o)

        return m
    
    def get_f_number(self):
        """Calculate the f number (f/#).

        Returns:
            float: f/# (unitless).
        """
        if self.na is not None:
            n = np.divide(1, 2*self.na)
        elif self.ds_i is not None and self.dm_a is not None:
            n = np.divide(self.ds_i, self.dm_a)
        else:
            raise ValueError("ds_i and dm_a or na must be set.")

        return n
    
    def get_effective_focal_length(self):
        """Calculate the effective focal length.

        Returns:
            float: effective focal length (length).
        """
        assert self.ds_i is not None, "ds_i is not set."
        assert self.ds_o is not None, "ds_o is not set."

        efl = np.divide(self.ds_o + self.ds_i, np.multiply(self.ds_o, self.ds_i))

        return efl
    
    def get_numerical_aperture(self):
        """Calculate the numerical aperture.

        Returns:
            float: numerical aperture (unitless).
        """

        # region unit conversions
        a_in_max = np.radians(self.a_in_max)  # deg to rad
        # endregion        

        if a_in_max is not None:
            na = np.sin(a_in_max)
        elif self.n is not None:
            na = np.divide(1, 2*self.n)
        else:
            raise ValueError("a_in_max or n must be set.")       

        return na
    
    def get_geometric_etendue(self):
        """Calculate the geometric etendue.

        Returns:
            float: geometric etendue (length^2).
        """
        assert self.s is not None, "s is not set."
        assert self.a_in_max is not None, "a_in_max is not set."

        # region unit conversions
        a_in_max = np.radians(self.a_in_max)  # deg to rad
        # endregion

        g = np.multiply(np.pi, np.multiply(self.s, np.power(np.sin(a_in_max), 2)))

        return g

    def get_radiant_flux(self):
        """Calculate the flux.

        Returns:
            float: flux (watt).
        """
        assert self.b is not None, "b is not set."
        assert self.g is not None, "g is not set."

        f = np.multiply(self.b, self.g)

        return f


class VPHGrism:
    """Volume-Phase Holographic grating grism component.

    Args:
        d (float, optional): DCG thickness. Defaults to None.
        t (float, optional): transmision ratio. Defaults to None.
        a_in (float, optional): incident ray angle in degrees. Defaults to None.
        a_out (float, optional): outgoing ray angle in degrees. Defaults to None.
        R (float, optional): resolvance. Defaults to None.
        l (array_like[float], optional): wavelength in nm. Defaults to None.
        l_g (float, optional): undeviated wavelength in nm. Defaults to None.
        a (float, optional): apex angle. Defaults to None.
        m (int, optional): diffraction order. Defaults to None.
        n_1 (float, optional): external index of refraction. Defaults to None.
        n_2 (float, optional): prism index of refraction. Defaults to None.
        n_3 (float, optional): grating substrate index of refraction.
            Defaults to None.
        v (float, optional): fringe frequency. Defaults to None.
        dl (float, optional): spectral resolution. Defaults to None.
        N (float, optional): Number of illumated fringes. Defaults to None.
    """

    def __init__(
        self,
        d=None,
        t=None,
        a_in=None,
        a_out=None,
        R=None,
        l=None,
        l_g=None,
        a=None,
        m=None,
        n_1=None,
        n_2=None,
        n_3=None,
        v=None,
        dl=None,
        N=None,
    ):
        self.d = d
        self.t = t
        self.a_in = a_in
        self.a_out = a_out
        self.R = R
        self.l = l
        self.l_g = l_g
        self.a = a
        self.m = m
        self.n_1 = n_1
        self.n_2 = n_2
        self.n_3 = n_3
        self.v = v
        self.dl = dl
        self.N = N

    def get_angle_out(self):
        """Calculates the outgoing angle from the grism.

        Returns:
            float: outgoing angle in degrees.
        """
        assert self.a_in is not None, "a_in is not set."
        assert self.n_1 is not None, "n_1 is not set."
        assert self.n_2 is not None, "n_2 is not set."
        assert self.n_3 is not None, "n_3 is not set."
        assert self.m is not None, "m is not set."
        assert self.a is not None, "a is not set."
        assert self.v is not None, "v is not set."
        assert self.l is not None, "l is not set."

        # region vectorization
        a_in = np.array(self.a_in).reshape(-1, 1)
        n_1 = np.array(self.n_1).reshape(-1, 1)
        n_2 = np.array(self.n_2).reshape(-1, 1)
        n_3 = np.array(self.n_3).reshape(-1, 1)
        m = np.array(self.m).reshape(-1, 1)
        a = np.array(self.a).reshape(-1, 1)
        v = np.array(self.v).reshape(-1, 1)
        l = np.array(self.l).reshape(-1, 1)
        # endregion

        # region unit conversions
        l = l * 10 ** -9  # m to nm
        a_in = np.radians(a_in)  # deg to rad
        a = np.radians(self.a)  # deg to rad
        # endregion

        angle_1 = a_in + a
        angle_2 = physlib.snell_angle_2(angle_1=angle_1, n_1=n_1, n_2=n_2)
        angle_3 = a - angle_2
        angle_4 = physlib.snell_angle_2(angle_1=angle_3, n_1=n_2, n_2=n_3)
        angle_5 = angle_4
        angle_6 = np.arcsin(np.sin(angle_5) - m * np.matmul(v, np.transpose(l)))
        angle_7 = angle_6
        angle_8 = physlib.snell_angle_2(angle_1=angle_7, n_1=n_3, n_2=n_2)
        angle_9 = angle_8 - a
        angle_10 = physlib.snell_angle_2(angle_1=angle_9, n_1=n_2, n_2=n_1)
        angle_out = angle_10 + a

        angle_out = np.degrees(angle_out)

        return angle_out

    def get_resolvance(self):
        """Caculates the grism resolvance.

        Raises:
            ValueError: if required parameters are not set.

        Returns:
            float: resolvance.
        """
        if self.l is not None and self.dl is not None:
            R = self.l / self.dl
        elif self.m is not None and self.N is not None:
            R = self.m * self.N
        else:
            raise ValueError("l and dl or m and N must be set.")

        return R

    def get_resolution(self):
        """Caclulates the grism optically-limited spectral resolution.

        Raises:
            ValueError: if required parameters are not set.

        Returns:
            float: resolution in nm.
        """
        if self.l is not None and self.R is not None:
            dl = self.l / self.R
        elif self.l is not None and self.m is not None and self.N is not None:
            dl = self.l / (self.m * self.N)
        else:
            raise ValueError("l and R or l and m and N must be set.")

        return dl


class ThinLens:
    """Thin singlet lens component.

    Args:
        D (float, optional): diameter of the lens [mm]. Defaults to None.
        M (float, optional): mass of lens [g]. Defaults to None.
        T (path-like, optional): path to transmittace LUT data.
        a_in (array_like[float], optional): incoming ray angle relative to optical
            axis [°]. Defaults to None.
        a_out (array_like[float], optional): outgoing ray angle relative to optical
            axis [°]. Defaults to None.
        d_i (array_like[float], optional): distance to image plane [mm]. Defaults to
            None.
        d_o (array_like[float], optional): distance from object plane [mm]. Defaults to
            None.
        f (array_like[float], optional): focal length [mm]. Defaults to None.
        h_i (array_like[float], optional): image height above optical axis [mm].
            Defaults to None.
        h_o (array_like[float], optional): source height above optical axis [mm].
            Defaults to None.
    """

    def __init__(
        self,
        D=None,
        M=None,
        T=None,
        a_in=None,
        a_out=None,
        d_i=None,
        d_o=None,
        f=None,
        h_i=None,
        h_o=None,
    ):
        self.D = D
        self.M = M
        self.T = utillib.LUT(T)
        self.a_in = a_in
        self.a_out = a_out
        self.d_i = d_i
        self.d_o = d_o
        self.f = f
        self.h_i = h_i
        self.h_o = h_o

    def get_image_distance(self):
        """Calculate image distance for focuser.

        Returns:
            float: image distance [mm].
        """
        assert self.f is not None, "f is not set."

        d_i = self.f

        return d_i

    def get_source_distance(self):
        """Calculate source distance for collimator.

        Returns:
            float: source distance [mm].
        """
        assert self.f is not None, "f is not set."

        d_o = self.f

        return d_o

    def get_image_height(self):
        """Calculate the image height along the focal plane for focuser.

        Returns:
            float: image height [mm].
        """
        assert self.f is not None, "f is not set."
        assert self.a_in is not None, "a_in is not set."

        # region vectorization
        f = np.array(self.f).reshape(-1, 1)
        a_in = np.array(self.a_in).reshape(-1, 1)
        # endregion

        # region unit conversions
        a_in = np.radians(a_in)  # deg to rad
        # endregion

        h_i = np.matmul(f, np.transpose(np.tan(a_in)))

        return h_i

    def get_source_height(self):
        """Calculate the source height along the focal plane for collimator.

        Returns:
            float: source height [mm].
        """
        assert self.f is not None, "f is not set."
        assert self.a_out is not None, "a_out is not set."

        # region vectorization
        f = np.array(self.f).reshape(-1, 1)
        a_out = np.array(self.a_out).reshape(-1, 1)
        # endregion

        # region unit conversions
        a_out = np.radians(a_out)  # deg to rad
        # endregion

        h_o = np.matmul(f, np.transpose(np.tan(a_out)))

        return h_o

    def get_focal_length(self):
        """Calculate focal length.

        Returns:
            float: focal length [mm].
        """

        if self.d_i is not None:  # from image distance

            f = self.d_i

        elif self.d_o is not None:  # from source distance

            f = self.d_o

        elif self.h_i is not None and self.a_in is not None:  # from image height

            # region unit conversions
            a_in = np.radians(self.a_in)  # deg to rad
            # endregion

            f = self.h_i / np.tan(a_in)

        elif self.h_o is not None and self.a_out is not None:  # from source height

            # region unit conversions
            a_out = np.radians(self.a_out)  # deg to rad
            # endregion

            f = self.h_o / np.tan(a_out)

        else:
            raise ValueError("d_i or d_o or h_i and a_in or h_o and a_out must be set.")
            
        return f


class AchromDoublet:
    """Achromatic doublet component.

    Args:
        f_1 (float, optional): Focal length of first element (mm). Defaults to None.
        f_2 (float, optional): Focal length of second element (mm). Defaults to None.
        f_eq (float, optional): Effective focal length of system (mm). Defaults to None.
        V_1 (float, optional): Abbe number for first element. Defaults to None.
        V_2 (float, optional): Abbe number for second element. Defaults to None.
    """

    def __init__(
        self,
        f_1=None,
        f_2=None,
        f_eq=None,
        V_1=None,
        V_2=None,
    ):
        self.f_1 = f_1
        self.f_2 = f_2
        self.f_eq = f_eq
        self.V_1 = V_1
        self.V_2 = V_2

    def focal_length_1(self):
        assert self.V_1 is not None, "V_1 is not set."
        assert self.V_2 is not None, "V_2 is not set."
        assert self.f_eq is not None, "f_eq is not set."

        # region unit conversions
        f_eq = self.f_eq * 10 ** -3  # mm to m
        # endregion

        f_1 = f_eq * (self.V_1 - self.V_2) / self.V_1
        return f_1

    def focal_length_2(self):
        assert self.V_1 is not None, "V_1 is not set."
        assert self.V_2 is not None, "V_2 is not set."
        assert self.f_eq is not None, "f_eq is not set."

        # region unit conversions
        f_eq = self.f_eq * 10 ** -3  # mm to m
        # endregion

        f_2 = -f_eq * (self.V_1 - self.V_2) / self.V_2
        return f_2

    def effective_focal_length(self):

        # region unit conversions
        f_1 = self.f_1 * 10 ** -3  # mm to m
        f_2 = self.f_2 * 10 ** -3  # mm to m
        # endregion

        if f_1 is not None:
            f_eq = f_1 * self.V_1 / (self.V_1 - self.V_2)
        elif f_2 is not None:
            f_eq = -f_2 * self.V_2 / (self.V_1 - self.V_2)
        else:
            raise ValueError("f_1 or f_2 must be set.")

        return f_eq
