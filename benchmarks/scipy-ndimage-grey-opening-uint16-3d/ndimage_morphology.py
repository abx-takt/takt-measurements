import numpy as np

from .common import Benchmark, safe_import

with safe_import():
    from scipy.ndimage import grey_opening


class GreyOpening3DUint16(Benchmark):
    param_names = ['side', 'mode']
    params = [[64, 128], ['reflect', 'constant']]

    def setup(self, side, mode):
        rng = np.random.default_rng(123)
        self.volume = rng.integers(0, 65536, size=(side,) * 3,
                                   dtype=np.uint16)
        z, y, x = np.ogrid[-4:5, -4:5, -4:5]
        self.footprint = x * x + y * y + z * z <= 16

    def time_grey_opening(self, side, mode):
        grey_opening(self.volume, footprint=self.footprint,
                     mode=mode, cval=0)
