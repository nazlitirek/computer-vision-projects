import numpy as np
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pycaw.utils import AudioUtilities as AU
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

VOLUME_MIN_DIST = 17
VOLUME_MAX_DIST = 200

class VolumeController:
    def __init__(self):
        device = AU.GetSpeakers()
        interface = device._dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        vol_range = self.volume.GetVolumeRange()
        self.min_vol = vol_range[0]
        self.max_vol = vol_range[1]

    def set_volume(self, lm, w, h):
        x1 = int(lm[4].x * w)
        y1 = int(lm[4].y * h)
        x2 = int(lm[8].x * w)
        y2 = int(lm[8].y * h)

        distance = np.hypot(x2 - x1, y2 - y1)
        vol = np.interp(distance, [VOLUME_MIN_DIST, VOLUME_MAX_DIST], [self.min_vol, self.max_vol])
        self.volume.SetMasterVolumeLevel(vol, None)

        vol_percent = int(np.interp(distance, [VOLUME_MIN_DIST, VOLUME_MAX_DIST], [0, 100]))
        return vol_percent

    def set_brightness(self, lm, w, h):
        x1 = int(lm[4].x * w)
        y1 = int(lm[4].y * h)
        x2 = int(lm[12].x * w)
        y2 = int(lm[12].y * h)

        distance = np.hypot(x2 - x1, y2 - y1)
        brightness = int(np.interp(distance, [VOLUME_MIN_DIST, VOLUME_MAX_DIST], [0, 100]))
        sbc.set_brightness(brightness)
        return brightness