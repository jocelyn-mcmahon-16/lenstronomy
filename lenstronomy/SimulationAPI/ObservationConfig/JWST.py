"""Provisional JWST instrument and observational settings.
ZP can be found here : https://jwst-docs.stsci.edu/files/182256933/182256934/1/1669487685625/NRC_ZPs_0995pmap.txt

Sky Brightness needs to be derived from the ETC
"""

import lenstronomy.Util.util as util

__all__ = ["JWST"]

# - keyword exposure_time: exposure time per image (in seconds)
# - keyword sky_brightness: sky brightness (in magnitude per square arcseconds in units of electrons)
# - keyword magnitude_zero_point: magnitude in which 1 count (e-) per second per arcsecond square is registered
# - keyword num_exposures: number of exposures that are combined (depends on coadd_years)
# - keyword seeing: Full-Width-at-Half-Maximum (FWHM) of PSF
# - keyword psf_type: string, type of PSF ('GAUSSIAN' and 'PIXEL' supported)


NIRCAM_F200W_band_obs = {
    "exposure_time": 3600.0,
    "sky_brightness": 29.52,  # this is derived using the ETC
    "magnitude_zero_point": 28.00,
    #'detector': 'NRCA1',
    "num_exposures": 1,
    "seeing": None,
    "psf_type": "PIXEL",
}

NIRCAM_F356W_band_obs = {
    "exposure_time": 3600.0,
    "sky_brightness": 28.39,  # this is derived using the ETC
    "magnitude_zero_point": 26.47,
    #'detector': 'NRCALONG',
    "num_exposures": 1,
    "seeing": None,
    "psf_type": "PIXEL",  # note kernel_point_source (the PSF map) must be provided separately
}

# for COSMOS-Web observations
NIRCAM_F115W_band_obs = {
    "exposure_time": 257,
    "sky_brightness": 30.96,
    "magnitude_zero_point": 28.02,
    "num_exposures": 8,
    "seeing": 0.04,  # PSF FWHM
    "psf_type": "PIXEL",
}

NIRCAM_F150W_band_obs = {
    "exposure_time": 257,
    "sky_brightness": 29.96,
    "magnitude_zero_point": 28.02,
    "num_exposures": 8,
    "seeing": 0.05,
    "psf_type": "PIXEL",
}

NIRCAM_F277W_band_obs = {
    "exposure_time": 257,
    "sky_brightness": 28.96,
    "magnitude_zero_point": 26.49,
    "num_exposures": 8,
    "seeing": 0.092,
    "psf_type": "PIXEL",
}

NIRCAM_F444W_band_obs = {
    "exposure_time": 257,
    "sky_brightness": 28.15,
    "magnitude_zero_point": 26.49,
    "num_exposures": 8,
    "seeing": 0.145,
    "psf_type": "PIXEL",
}


class JWST(object):
    """Class contains JWST instrument and observation configurations."""

    def __init__(self, band="F200W", psf_type="PIXEL", coadd_years=None):
        """

        :param band: string, 'F115W', 'F150W', 'F200W', 'F277W', 'F356W' or 'F444W' supported. Determines obs dictionary.
        :param psf_type: string, type of PSF ('GAUSSIAN', 'PIXEL' supported).
        :param coadd_years: int, number of years corresponding to num_exposures in obs dict. Currently supported: None.
        """

        if band == "F200W":
            self.obs = NIRCAM_F200W_band_obs
            self.arm = "short"
        elif band == "F356W":
            self.obs = NIRCAM_F356W_band_obs
            self.arm = "long"
        elif band == "F115W":
            self.obs = NIRCAM_F115W_band_obs
            self.arm = "short"
        elif band == "F150W":
            self.obs = NIRCAM_F150W_band_obs
            self.arm = "short"
        elif band == "F277W":
            self.obs = NIRCAM_F277W_band_obs
            self.arm = "long"
        elif band == "F444W":
            self.obs = NIRCAM_F444W_band_obs
            self.arm = "long"
        else:
            raise ValueError("band %s not supported!" % band)

        if psf_type == "GAUSSIAN":
            self.obs["psf_type"] = "GAUSSIAN"
        elif psf_type != "PIXEL":
            raise ValueError("psf_type %s not supported!" % psf_type)

        if coadd_years is not None:
            raise ValueError(
                " %s coadd_years not supported! "
                "You may manually adjust num_exposures in obs dict if required."
                % coadd_years
            )

        # NIRCAM camera settings
        if self.arm == "short":
            self.camera = {
                "read_noise": 15.77,
                "pixel_scale": 0.031,
                "ccd_gain": 2.05,
            }
        elif self.arm == "long":
            self.camera = {
                "read_noise": 13.25,
                "pixel_scale": 0.063,
                "ccd_gain": 1.82,
            }

        # - keyword read_noise: std of noise generated by read-out (in units of electrons)
        # - keyword pixel_scale: scale (in arcseconds) of pixels
        # - keyword ccd_gain: electrons/ADU (analog-to-digital unit).

    def kwargs_single_band(self):
        """

        :return: merged kwargs from camera and obs dicts
        """
        kwargs = util.merge_dicts(self.camera, self.obs)
        return kwargs
