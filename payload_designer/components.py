"""Component classes."""

# stdlib
import logging

# external
import numpy as np

# project
from payload_designer.libs import physlib

LOG = logging.getLogger(__name__)


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
        a_in (array_like[float], optional): incoming ray angle relative to optical axis.
            Defaults to None.
        a_out (array_like[float], optional): outgoing ray angle relative to optical
            axis. Defaults to None.
        d_i (array_like[float], optional): distance to image. Defaults to None.
        d_o (array_like[float], optional): distance from object. Defaults to None.
        f (array_like[float], optional): focal length in m. Defaults to None.
        h (array_like[float], optional): image height above optical axis.
            Defaults to None.
        trans_ratio (array_like[float], optional): transmission ratio of component.
            Defaults to None.
        trans_ratio_in (array_like[float], optional): incoming transmission ratio.
            Defaults to None.
        trans_ratio_out (array_like[float], optional): outgoing tranmission ratio.
            Defaults to None.
    """

    def __init__(
        self,
        a_in=None,
        a_out=None,
        d_i=None,
        d_o=None,
        f=None,
        h=None,
        trans_ratio=None,
        trans_ratio_in=None,
        trans_ratio_out=None,
    ):
        self.a_in = a_in
        self.a_out = a_out
        self.d_i = d_i
        self.d_o = d_o
        self.f = f
        self.h = h
        self.trans_ratio = trans_ratio
        self.trans_ratio_in = trans_ratio_in
        self.trans_ratio_out = trans_ratio_out

    def get_image_distance(self):
        """Calculate image distance for focuser.

        Returns:
            float: image distance in  m.
        """
        assert self.f is not None, "f is not set."

        d_i = self.f

        return d_i

    def get_source_distance(self):
        """Calculate source distance for collimator.

        Returns:
            float: source distance in m.
        """
        assert self.f is not None, "f is not set."

        d_o = self.f

        return d_o

    def get_focal_length(self):
        """Calculate focal length.

        Returns:
            float: focal length in m.
        """

        if self.d_i is not None:
            f = self.d_i
        elif self.d_o is not None:
            f = self.d_o
        elif self.h is not None and self.a_in is not None:
            a_in = np.radians(self.a_in)  # deg to rad
            f = self.h / np.tan(a_in)
        elif self.h is not None and self.a_out is not None:
            a_out = np.radians(self.a_out)  # deg to rad
            f = self.h / np.tan(a_out)
        else:
            raise ValueError("d_i or d_o or h and a_in or h and a_out must be set.")

        return f

    def get_image_height(self):
        """Calculate the image height along the focal plane.

        Returns:
            float: image height in m.
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

        h = np.matmul(f, np.transpose(np.tan(a_in)))

        return h

    def get_source_height(self):
        """[summary]"""

    def get_trans_ratio_out(self):
        """Calculates the outgoing transmittance ratio of the componenet.

        Returns:
            array_like[float]: Outgoing transmittance ratio.
        """
        assert self.trans_ratio_in is not None, "trans_ratio_in is not set."
        assert self.trans_ratio is not None, "trans_ratio is not set."

        trans_ratio_out = self.trans_ratio_in * self.trans_ratio

        return trans_ratio_out
