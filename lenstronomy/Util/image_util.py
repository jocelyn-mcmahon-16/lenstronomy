__author__ = 'sibirrer'

import numpy as np
import astrofunc.util as util_astrofunc


def findOverlap(x_mins, y_mins, min_distance):
    """
    finds overlapping solutions, deletes multiples and deletes non-solutions and if it is not a solution, deleted as well
    """
    n = len(x_mins)
    idex = []
    for i in range(n):
        if i == 0:
            pass
        else:
            for j in range(0, i):
                if (abs(x_mins[i] - x_mins[j]) < min_distance and abs(y_mins[i] - y_mins[j]) < min_distance):
                    idex.append(i)
                    break
    x_mins = np.delete(x_mins, idex, axis=0)
    y_mins = np.delete(y_mins, idex, axis=0)
    return x_mins, y_mins


def coordInImage(x_coord, y_coord, numPix, deltapix):
    """
    checks whether image positions are within the pixel image in units of arcsec
    if not: remove it

    :param imcoord: image coordinate (in units of angels)  [[x,y,delta,magnification][...]]
    :type imcoord: (n,4) numpy array
    :returns: image positions within the pixel image
    """
    idex=[]
    min = -deltapix*numPix/2
    max = deltapix*numPix/2
    for i in range(len(x_coord)): #sum over image positions
        if (x_coord[i] < min or x_coord[i] > max or y_coord[i] < min or y_coord[i] > max):
            idex.append(i)
    x_coord = np.delete(x_coord, idex, axis=0)
    y_coord = np.delete(y_coord, idex, axis=0)
    return x_coord, y_coord


def rebin_image(bin_size, image, wht_map, sigma_bkg, ra_coords, dec_coords, idex_mask):
    """
    rebins pixels, updates cutout image, wht_map, sigma_bkg, coordinates, PSF
    :param bin_size: number of pixels (per axis) to merge
    :return:
    """
    numPix = int(len(image)/bin_size)
    if not numPix == len(image)/bin_size:
        raise ValueError("image with size %s can not be rebinned with factor %s" % (len(image), bin_size))
    image_resized = util_astrofunc.re_size_grid(grid=image, numPix=numPix)
    image_resized *= bin_size**2
    wht_map_resized = util_astrofunc.re_size_grid(grid=wht_map, numPix=numPix)
    sigma_bkg_resized = bin_size*sigma_bkg
    ra_coords_resized = util_astrofunc.re_size_grid(grid=ra_coords, numPix=numPix)
    dec_coords_resized = util_astrofunc.re_size_grid(grid=dec_coords, numPix=numPix)
    idex_mask_resized = util_astrofunc.re_size_grid(grid=idex_mask, numPix=numPix)
    idex_mask_resized[idex_mask_resized > 0] = 1
    return image_resized, wht_map_resized, sigma_bkg_resized, ra_coords_resized, dec_coords_resized, idex_mask_resized


def rebin_coord_transform(factor, ra_at_xy_0, dec_at_xy_0, x_at_radec_0, y_at_radec_0, Mpix2coord, Mcoord2pix):
    """
    adopt coordinate system and transformation between angular and pixel coordinates of a re-binned image
    :param bin_size:
    :param ra_0:
    :param dec_0:
    :param x_0:
    :param y_0:
    :param Matrix:
    :param Matrix_inv:
    :return:
    """
    factor = int(factor)
    Mcoord2pix_resized = Mcoord2pix / factor
    Mpix2coord_resized = Mpix2coord * factor
    x_at_radec_0_resized = (x_at_radec_0 + 0.5) / factor - 0.5
    y_at_radec_0_resized = (y_at_radec_0 + 0.5) / factor - 0.5
    ra_at_xy_0_resized, dec_at_xy_0_resized = util_astrofunc.map_coord2pix(-x_at_radec_0_resized, -y_at_radec_0_resized, 0, 0, Mpix2coord_resized)
    return ra_at_xy_0_resized, dec_at_xy_0_resized, x_at_radec_0_resized, y_at_radec_0_resized, Mpix2coord_resized, Mcoord2pix_resized


def stack_images(image_list, wht_list, sigma_list):
    """
    stacks images and saves new image as a fits file
    :param image_name_list: list of image_names to be stacked
    :return:
    """
    image_stacked = np.zeros_like(image_list[0])
    wht_stacked = np.zeros_like(image_stacked)
    sigma_stacked = 0.
    for i in range(len(image_list)):
        image_stacked += image_list[i]*wht_list[i]
        sigma_stacked += sigma_list[i]**2 * np.median(wht_list[i])
        wht_stacked += wht_list[i]
    image_stacked /= wht_stacked
    sigma_stacked /= np.median(wht_stacked)
    wht_stacked /= len(wht_list)
    return image_stacked, wht_stacked, np.sqrt(sigma_stacked)