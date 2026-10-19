
from Import_CWD import *
from astropy import units
from astropy.visualization import ImageNormalize, AsinhStretch
from sunpy.visualization.colormaps import cm as sunpy_cm



############################################################
# SDO
############################################################


date_str  = "2026-04-18"

date_str2 = "20260418_051200"


aia_filename = "aia.lev1_euv_12s.2026-04-18T051210Z.171.image_lev1.fits"


path_aia = os.path.join(path_data, "sdo_aia", date_str.replace("-", ""))
file_aia = os.path.join(path_aia, aia_filename)

print("file_aia =", file_aia)


hmi_filename = "hmi.sharp_cea_720s.14594.20260418_051200_TAI.Br.fits"

path_hmi = os.path.join(path_data, "sdo_hmi", date_str.replace("-", ""))
file_hmi = os.path.join(path_hmi, hmi_filename)

print("file_hmi =", file_hmi)



# Amplified local area in helioprojective coordinates [arcsec].
HMI_COORDINATES_RANGE = [[-365.78, -46.56], [223.46,382.66]]


############################################################
# NLFFF magnetic fields
############################################################


# Reuse saved geometry for this date_str2 case. Prefer helioprojective files;
# if absent, use CEA files and convert their footprints for display through FITS WCS.
# Directory containing nlfff_vis_<HMI_TIME>; set this to your extraction output root.
NLFFF_VISUALIZATION_DIR: str = os.path.join(path_data, "nlfff_visualization")
NLFFF_SAVE_MODE: str = "h5"  # "h5" or "npz", matching the extraction scripts.

# Optional existing files; relative paths use this case's path_nlfff below.
# Select CEA or helioprojective geometry for the same case, with SRMT mode="default".
FIELDLINE_FILE: str | None = None
ISOSURFACE_FILE: str | None = None
COORDINATE_CONVERSION_BLOCK: int = 100000

if NLFFF_SAVE_MODE not in {"h5", "npz"}:
    raise ValueError('NLFFF_SAVE_MODE must be "h5" or "npz".')

nlfff_fieldline_filename  = f"data_fieldlines_helioprojective.{NLFFF_SAVE_MODE}"
nlfff_isosurface_filename = f"data_isosurfaces_helioprojective_srmt.{NLFFF_SAVE_MODE}"


path_nlfff      = os.path.join(os.path.expanduser(NLFFF_VISUALIZATION_DIR), "nlfff_vis_%s"%(date_str2))


def resolve_geometry_file(default_filename: str, override: str | None) -> str:
    """Prefer the requested file, then the same case's CEA file in the same format."""
    if override is not None:
        return os.path.join(path_nlfff, os.path.expanduser(override))
    requested = os.path.join(path_nlfff, default_filename)
    if os.path.isfile(requested):
        return requested
    cea_file = os.path.join(path_nlfff, default_filename.replace("_helioprojective", "_cea"))
    return cea_file if os.path.isfile(cea_file) else requested


file_fieldline  = resolve_geometry_file(nlfff_fieldline_filename, FIELDLINE_FILE)
file_isosurface = resolve_geometry_file(nlfff_isosurface_filename, ISOSURFACE_FILE)


print("file_fieldline  =", file_fieldline)
print("file_isosurface =", file_isosurface)



fontsize_label      = 8
fontsize_tick       = 6
fontsize_tick_zoom  = 6

# Extra long-label spacing beyond the outer edge of the tick labels.
xlabel_pad = 10
ylabel_pad = 10
zlabel_pad = 10

# Extra tick-label spacing away from the anchored axes.
xticklabel_pad = 5
yticklabel_pad = 12
zticklabel_pad = 10

# Legend and axis-box styling.
legend_fontsize       = 8
legend_location       = "upper right"
legend_bbox_to_anchor = (0.835, 0.94)

axis_linewidth        = 0.2


#ISOSURFACE_COLORS   = ["black","grey","silver"]

ISOSURFACE_COLORS    = ["black","grey","grey"]

ISOSURFACE_OPACITIES = [0.75,0.35,0.20]



print("ISOSURFACE_COLORS     =",ISOSURFACE_COLORS)
print("ISOSURFACE_OPACITIES  =",ISOSURFACE_OPACITIES )



VIEW_ELEVATION =  16.0
VIEW_AZIMUTH   = -80.0

BOX_ZOOM       =   1.00


FIELDLINE_COLOR_MIN   = -200
FIELDLINE_COLOR_MAX   =  200

FIELDLINE_COLOR_CMAP  = "coolwarm"
FIELDLINE_COLOR_ALPHA = 0.5
FIELD_LINEWIDTH       = 0.4


FIELDLINE_XMIN = HMI_COORDINATES_RANGE[0][0]
FIELDLINE_XMAX = HMI_COORDINATES_RANGE[0][1]

FIELDLINE_YMIN = HMI_COORDINATES_RANGE[1][0]
FIELDLINE_YMAX = HMI_COORDINATES_RANGE[1][1]

FIELDLINE_ZMIN = 0
FIELDLINE_ZMAX = 45


############################################################
# Parameters
############################################################

def to_helioprojective_geometry(points: numpy.ndarray, coordinates: str, hmi_wcs: Any, aia_wcs: Any) -> numpy.ndarray:
    """Convert saved CEA footprints to AIA Tx/Ty in arcsec; retain local z in Mm.

    The NLFFF writer stores native CEA u in radians and v=sin(native latitude),
    not Carrington longitude/latitude in degrees. Invert the complete CEA
    projection-plane mapping, including its pixel matrix, offsets and lambda.
    Then use the same HMI-to-AIA frame transformation as the HMI image panel.
    This preserves the existing footprint-plus-height display convention; it
    does not project elevated coronal points along their full lines of sight.
    Saved arrays and physical measurements are not modified.
    """
    from astropy import units
    from astropy.wcs import utils

    points = numpy.asarray(points, dtype=numpy.float64)
    if points.ndim < 2 or points.shape[-1] != 3 or not numpy.all(numpy.isfinite(points)):
        raise ValueError("Geometry must be a finite array with final dimension 3.")
    coordinates = str(coordinates).strip().lower()
    if coordinates == "helioprojective":
        return points
    if coordinates != "cea":
        raise ValueError("This figure accepts CEA or Helioprojective geometry.")
    if tuple(hmi_wcs.wcs.ctype) != ("CRLN-CEA", "CRLT-CEA") or hmi_wcs.has_distortion:
        raise ValueError("CEA geometry conversion requires the matching HMI Carrington CEA WCS without additional pixel distortions.")
    if not isinstance(COORDINATE_CONVERSION_BLOCK, (int, numpy.integer)) or COORDINATE_CONVERSION_BLOCK <= 0:
        raise ValueError("COORDINATE_CONVERSION_BLOCK must be a positive integer.")

    cea_lambda = float(next((value for axis, parameter, value in hmi_wcs.wcs.get_pv() if axis == 2 and parameter == 1), 1.0))
    if not numpy.isfinite(cea_lambda) or not 0.0 < cea_lambda <= 1.0:
        raise ValueError("The CEA projection parameter lambda must lie in (0,1].")
    inverse = numpy.linalg.inv(hmi_wcs.pixel_scale_matrix)
    if not numpy.all(numpy.isfinite(inverse)):
        raise ValueError("The HMI CEA pixel matrix must be finite and invertible.")
    hpc_frame = utils.wcs_to_celestial_frame(aia_wcs)
    flat = points.reshape(-1, 3)
    converted = numpy.empty_like(flat)
    for start in range(0, len(flat), COORDINATE_CONVERSION_BLOCK):
        block = flat[start:start+COORDINATE_CONVERSION_BLOCK]
        if numpy.any(numpy.abs(block[:, 0]) > numpy.pi + 1.0e-12) or numpy.any(numpy.abs(block[:, 1]) > 1.0):
            raise ValueError("Native CEA coordinates require u in [-pi,pi] radians and v in [-1,1].")
        xi = numpy.rad2deg(block[:, 0]) - hmi_wcs.wcs.cel.prj.x0
        eta = numpy.rad2deg(block[:, 1]) / cea_lambda - hmi_wcs.wcs.cel.prj.y0
        pixel_x = inverse[0, 0]*xi + inverse[0, 1]*eta + hmi_wcs.wcs.crpix[0] - 1.0
        pixel_y = inverse[1, 0]*xi + inverse[1, 1]*eta + hmi_wcs.wcs.crpix[1] - 1.0
        hmi_coordinates = utils.pixel_to_skycoord(pixel_x, pixel_y, hmi_wcs, origin=0)
        hpc_coordinates = hmi_coordinates.transform_to(hpc_frame)
        converted[start:start+len(block), 0] = hpc_coordinates.Tx.to_value(units.arcsec)
        converted[start:start+len(block), 1] = hpc_coordinates.Ty.to_value(units.arcsec)
        converted[start:start+len(block), 2] = block[:, 2]
    if not numpy.all(numpy.isfinite(converted)):
        raise ValueError("CEA-to-helioprojective conversion produced non-finite positions; check the case and FITS WCS.")
    return converted.reshape(points.shape)



def validate_required_files() -> None:
    """Fail early with clear paths when an input data product is unavailable."""
    required = (("AIA FITS", file_aia), ("HMI FITS", file_hmi), ("NLFFF field lines", file_fieldline), ("SRMT isosurfaces", file_isosurface))
    missing = [f"{label}: {path}" for label, path in required if not os.path.isfile(path)]

    if missing:
        instructions = ["Missing required input files:", "  " + "\n  ".join(missing)]
        if not os.path.isfile(file_fieldline) or not os.path.isfile(file_isosurface):
            instructions.extend([
                "", "Set the following in fieldlines_data.py and isosurfaces_data.py:",
                f"  HMI_TIME = {date_str2!r}",
                '  COORDINATES = "Helioprojective"',
                f"  SAVE_MODE = {NLFFF_SAVE_MODE!r}",
                f"  PATH_DIR_OUTPUT = {path_nlfff!r}",
                "Use the same NLFFF input case in both scripts. In isosurfaces_data.py use ISOSURFACE_METHOD='SRMT', ISOSURFACE_STEM='data_isosurfaces', and LYpy_SRMT mode='default'; in fieldlines_data.py use FIELDLINE_STEM='data_fieldlines'.",
                f"In fieldlines_data.py, choose seeds inside this case's NLFFF domain; the displayed region has Tx={HMI_COORDINATES_RANGE[0]!r} and Ty={HMI_COORDINATES_RANGE[1]!r} arcsec. Update any hard-coded seed bounds from another case.",
                "Run from the NLFFF script directory:",
            ])
            if not os.path.isfile(file_fieldline):
                instructions.append("  python fieldlines_data.py")
            if not os.path.isfile(file_isosurface):
                instructions.append("  python isosurfaces_data.py")
            instructions.extend([
                "Then rerun this figure script.",
                "If the files already exist elsewhere, set NLFFF_VISUALIZATION_DIR, FIELDLINE_FILE or ISOSURFACE_FILE in this script. Overrides must identify the same case and CEA or helioprojective geometry.",
                "Matching CEA files are selected automatically and converted for display. Keep their original filenames and coordinate metadata. Cartesian files require separate conversion.",
            ])
            if os.path.isdir(path_nlfff):
                available = sorted(entry for entry in os.listdir(path_nlfff) if entry.startswith(("data_fieldlines", "data_isosurface")) and entry.lower().endswith((".h5", ".hdf5", ".npz")))
                if available:
                    instructions.extend(["Existing geometry filenames in this case directory:", "  " + "\n  ".join(available)])
        if not os.path.isfile(file_aia) or not os.path.isfile(file_hmi):
            instructions.append("Check path_data, the observing date, and the AIA/HMI FITS filenames above; the geometry scripts do not create these observational inputs.")
        raise FileNotFoundError("\n".join(instructions))

    for label, path in (("Field-line", file_fieldline), ("Isosurface", file_isosurface)):
        if os.path.splitext(path)[1].lower() not in {".h5", ".hdf5", ".npz"}:
            raise ValueError(f"{label} input must be an HDF5 or NPZ file: {path}")

    roi = numpy.asarray(HMI_COORDINATES_RANGE, dtype=float)

    if roi.shape != (2, 2) or not numpy.all(numpy.isfinite(roi)) or numpy.any(roi[:, 1] <= roi[:, 0]):
        raise ValueError("HMI_COORDINATES_RANGE must contain two finite, increasing [min,max] intervals.")

    if len(ISOSURFACE_COLORS) != len(ISOSURFACE_OPACITIES):
        raise ValueError("ISOSURFACE_COLORS and ISOSURFACE_OPACITIES must have equal lengths.")

    if any(not numpy.isfinite(value) or value < 0.0 or value > 1.0 for value in ISOSURFACE_OPACITIES):
        raise ValueError("Every isosurface opacity must lie in [0,1].")



############################################################
# Main
############################################################

if __name__ == "__main__":

    validate_required_files()

    # Validate geometry before allocating the figure or processing the FITS images.
    isovalues, stored_isosurface_coordinates, stored_method = load_isosurfaces(file_isosurface)
    fieldlines, seeds, stored_fieldline_coordinates = load_fieldlines(file_fieldline)

    if not isovalues:
        raise ValueError("The SRMT isosurface file contains no isovalues.")

    if not fieldlines:
        raise ValueError("The NLFFF field-line file contains no field lines.")

    if len(ISOSURFACE_COLORS) < len(isovalues) or len(ISOSURFACE_OPACITIES) < len(isovalues):
        raise ValueError(f"The plot defines {len(ISOSURFACE_COLORS)} isosurface styles but the file contains {len(isovalues)} isovalues.")

    if str(stored_method).strip().upper() != "SRMT":
        raise ValueError(f"This figure requires SRMT isosurfaces; the file stores {stored_method!r}.")

    if str(stored_isosurface_coordinates).strip().lower() not in {"cea", "helioprojective"} or str(stored_fieldline_coordinates).strip().lower() not in {"cea", "helioprojective"}:
        raise ValueError(f"The AIA overlay supports CEA or Helioprojective geometry; isosurfaces={stored_isosurface_coordinates!r}, field lines={stored_fieldline_coordinates!r}.")
    print("display coordinate system = Helioprojective (Tx, Ty in arcsec; local z in Mm)")
    if "cea" in {str(stored_isosurface_coordinates).strip().lower(), str(stored_fieldline_coordinates).strip().lower()}:
        print("CEA geometry conversion = HMI CEA WCS to AIA helioprojective frame; existing local heights retained")

    # Print stored extraction diagnostics together with exact geometry statistics from the loaded mesh.
    # Missing extraction metadata are reported as "not stored" rather than reconstructed from the final surface.
    isosurface_diagnostics = load_isosurface_diagnostics(file_isosurface, isovalues)
    for isovalue, diagnostics in zip(isovalues, isosurface_diagnostics):
        if diagnostics.get("srmt_mode") != "default":
            raise ValueError(f"Isovalue {float(isovalue['level']):g} G has SRMT mode={diagnostics.get('srmt_mode')!r}; expected 'default'. Regenerate this case with LYpy_SRMT mode='default' and saved diagnostics; unknown legacy or uniform-mode data cannot be relabelled.")
    print_isosurface_diagnostics(isovalues, stored_method, stored_isosurface_coordinates, isosurface_diagnostics)


    fieldline_bz = srmt_load_fieldline_bz(file_fieldline)
    if len(fieldline_bz) != len(fieldlines):
       raise ValueError("Stored field-line coordinates and Bz diagnostics contain different numbers of lines.")


    ########################################################
    ########################################################

    hfig = plt.figure(figsize=(7.48, 4.2), dpi=figure_dpi)


    length_aia  = 0.24
    width_aia   = length_aia*1.8

    print("aia = (%.4f, %.4f)"%(length_aia,width_aia))
    print("aia = (%.4f, %.4f)"%(length_aia,(1.0-width_aia)*0.5))


    pos_full    = [0.08, 0.35, length_aia, width_aia]

    pos_zoom1   = [0.22, 0.61, 0.15, 0.15]
    pos_zoom2   = [0.22, 0.40, 0.15, 0.15]

    pos_bar_aia = [0.12, 0.22, 0.16, 0.015]
    pos_bar_hmi = [0.12, 0.12, 0.16, 0.015]


    pos_nlfff   = [0.25, 0.01, 0.75, 0.98]



    ########################################################
    # SDO AIA
    ########################################################

    aia_fits = aia_fits_read(file_aia)

    aia_data = numpy.abs(aia_fits["data"])
    aia_utc = aia_fits["utc"]
    aia_wavelength = aia_fits["wavelength"]
    aia_wcs = aia_fits["wcs"]

    hmi_fits = hmi_fits_read(file_hmi)
    hmi_data = hmi_fits["data"]
    hmi_wcs = hmi_fits["wcs"]

    ########################################################
    # Colormap and normalization
    ########################################################

    cmap = sunpy_cm.cmlist["sdoaia%d" % int(round(aia_wavelength))]

    positive = aia_data[numpy.isfinite(aia_data) & (aia_data > 0.0)]
    if positive.size == 0:
        raise ValueError("AIA image contains no finite positive intensities.")

    # Fixed AIA display range to match the requested colorbar ticks.
    vmin = 1.0
    vmax = 1600.0

    norm = ImageNormalize(vmin=vmin, vmax=vmax, stretch=AsinhStretch(a=0.15), clip=True)
    print("AIA display range =", vmin, vmax)

    imshow_args = {
        "origin": "lower",
        "interpolation": "nearest",
        "cmap": cmap,
        "norm": norm,
    }




    ########################################################
    # Full-disk panel in helioprojective coordinates
    ########################################################

    haxe = hfig.add_axes(pos_full, projection=aia_wcs)
    him = haxe.imshow(aia_data, **imshow_args, zorder=10)

    tx_coord = haxe.coords[0]
    ty_coord = haxe.coords[1]

    tx_coord.set_format_unit(units.arcsec)
    ty_coord.set_format_unit(units.arcsec)

    tx_coord.set_axislabel(r"$T_x\ \rm{[arcsec]}$", fontsize=fontsize_label)
    ty_coord.set_axislabel(r"$T_y\ \rm{[arcsec]}$", fontsize=fontsize_label)

    tx_coord.set_ticklabel(size=fontsize_tick)
    ty_coord.set_ticklabel(size=fontsize_tick)

    tx_coord.set_ticks(spacing=500 * units.arcsec, size=2)
    ty_coord.set_ticks(spacing=500 * units.arcsec, size=2)

    #haxe.coords.grid(True, color="white", alpha=0.35, linestyle="--", linewidth=0.4)

    full_xlim = (-1200.0, 1200.0)
    full_ylim = (-1200.0, 1200.0)
    set_helioprojective_limits(haxe, aia_wcs, full_xlim, full_ylim)
    haxe.set_aspect("equal", adjustable="datalim")
    haxe.set_position(pos_full, which="both")


    roi_xlim = (float(HMI_COORDINATES_RANGE[0][0]), float(HMI_COORDINATES_RANGE[0][1]))
    roi_ylim = (float(HMI_COORDINATES_RANGE[1][0]), float(HMI_COORDINATES_RANGE[1][1]))

    roi_rect, roi_xpix_lim, roi_ypix_lim = add_hpc_rectangle(haxe, aia_wcs, roi_xlim, roi_ylim, color="w",linestyle="-", linewidth=0.6)
 
    haxe.text(0.05, 0.95, r"$\rm{(a)}$", transform=haxe.transAxes, fontsize=10, ha="left", va="top", color="white", bbox=dict(boxstyle="round,pad=0.2", facecolor=(0.0, 0.0, 0.0, 0.25), edgecolor="none"), zorder=50, clip_on=False)


    ########################################################
    # Amplified local panel in helioprojective coordinates
    ########################################################

    haxe_zoom = hfig.add_axes(pos_zoom1, projection=aia_wcs,zorder=20)

    haxe_zoom.imshow(aia_data, **imshow_args)

    tx_zoom = haxe_zoom.coords[0]
    ty_zoom = haxe_zoom.coords[1]

    tx_zoom.set_format_unit(units.arcsec)
    ty_zoom.set_format_unit(units.arcsec)

    #tx_zoom.set_axislabel(r"$T_x$", fontsize=fontsize_label, color="white")
    #ty_zoom.set_axislabel(r"$T_y$", fontsize=fontsize_label, color="white")

    tx_zoom.set_axislabel("")
    ty_zoom.set_axislabel("")

    dx = roi_xlim[1] - roi_xlim[0]
    dy = roi_ylim[1] - roi_ylim[0]
    tx_zoom.set_ticks(spacing=max(20.0, round(dx / 4.0 / 10.0) * 10.0) * units.arcsec, size=2)
    ty_zoom.set_ticks(spacing=max(20.0, round(dy / 4.0 / 10.0) * 10.0) * units.arcsec, size=2)

    #haxe_zoom.coords.grid(True, color="white", alpha=0.35, linestyle="--", linewidth=0.4)

    set_helioprojective_limits(haxe_zoom, aia_wcs, roi_xlim, roi_ylim)
    haxe_zoom.set_aspect("equal", adjustable="datalim")
    haxe_zoom.set_position(pos_zoom1, which="both")
    style_subfigure_axes_white(haxe_zoom, [tx_zoom, ty_zoom], tick_size=11, spine_linewidth=1.0)

    tx_zoom.set_ticklabel(size=fontsize_tick_zoom, color="white")
    ty_zoom.set_ticklabel(size=fontsize_tick_zoom, color="white")

    # modify border
    haxe_zoom.coords.frame.set_linewidth(0)

    for spine in haxe_zoom.spines.values():
      spine.set_visible(False)

    haxe_zoom.patch.set_edgecolor("white")
    haxe_zoom.patch.set_linewidth(0.3)

    
    haxe_zoom.text(0.03, 0.97, r"$\rm{(a1)}AIA\ 171\AA$", transform=haxe_zoom.transAxes, fontsize=7, ha="left", va="top", color="white", bbox=dict(boxstyle="round,pad=0.2", facecolor=(0.0, 0.0, 0.0, 0.25), edgecolor="none"), zorder=50, clip_on=False)
    


    add_connection_patches(hfig, haxe, haxe_zoom, roi_xpix_lim, roi_ypix_lim, color="w", linewidth=0.3)


    ########################################################
    # Second subfigure: HMI Br in helioprojective coordinates
    ########################################################

    # Transform the native SHARP CEA coordinates to the same helioprojective
    # frame used by the AIA image.  The HMI data values themselves are not
    # interpolated here; only their pixel-center coordinates are transformed.
    hmi_tx_deg, hmi_ty_deg = hmi_to_helioprojective_mesh(hmi_data, hmi_wcs, aia_wcs)

    finite_hmi = hmi_data[numpy.isfinite(hmi_data)]
    if finite_hmi.size == 0:
        raise ValueError("HMI image contains no finite values.")

    # Fixed HMI display range to match the requested colorbar ticks.
    hmi_abs_max = 1600.0
    hmi_norm = matplotlib.colors.TwoSlopeNorm(vmin=-hmi_abs_max, vcenter=0.0, vmax=hmi_abs_max)

    # Use the AIA helioprojective WCS for the HMI subfigure as well.
    haxe_hmi = hfig.add_axes(pos_zoom2, projection=aia_wcs,zorder=20)

    hmi_image = haxe_hmi.pcolormesh(hmi_tx_deg, hmi_ty_deg, hmi_data, transform=haxe_hmi.get_transform("world"), cmap="coolwarm", norm=hmi_norm, shading="auto", rasterized=True,)

    hmi_tx = haxe_hmi.coords[0]
    hmi_ty = haxe_hmi.coords[1]

    hmi_tx.set_format_unit(units.arcsec)
    hmi_ty.set_format_unit(units.arcsec)

    #hmi_tx.set_axislabel(r"$T_x$", fontsize=fontsize_label, color="white")
    #hmi_ty.set_axislabel(r"$T_y$", fontsize=fontsize_label, color="white")

    hmi_tx.set_axislabel("")
    hmi_ty.set_axislabel("")



    hmi_tx.set_ticks(spacing=max(20.0, round(dx / 4.0 / 10.0) * 10.0) * units.arcsec,size=2)
    hmi_ty.set_ticks(spacing=max(20.0, round(dy / 4.0 / 10.0) * 10.0) * units.arcsec,size=2)

    #haxe_hmi.coords.grid(True, color="white", alpha=0.30, linestyle="--", linewidth=0.35)
    set_helioprojective_limits(haxe_hmi, aia_wcs, roi_xlim, roi_ylim)
    haxe_hmi.set_aspect("equal", adjustable="datalim")
    haxe_hmi.set_position(pos_zoom2, which="both")
    style_subfigure_axes_white(haxe_hmi, [hmi_tx, hmi_ty], tick_size=11, spine_linewidth=1.0)

    hmi_tx.set_ticklabel(size=fontsize_tick_zoom, color="white")
    hmi_ty.set_ticklabel(size=fontsize_tick_zoom, color="white")

    # modify border
    haxe_hmi.coords.frame.set_linewidth(0)

    for spine in haxe_hmi.spines.values():
      spine.set_visible(False)

    haxe_hmi.patch.set_edgecolor("white")
    haxe_hmi.patch.set_linewidth(0.3)


    haxe_hmi.text(0.03, 0.97, r"$\rm{(a2)}HMI\ B_r$", transform=haxe_hmi.transAxes, fontsize=7, ha="left", va="top", color="white", bbox=dict(boxstyle="round,pad=0.2", facecolor=(0.0, 0.0, 0.0, 0.25), edgecolor="none"), zorder=50, clip_on=False)

    # Connect the same full-disk helioprojective ROI rectangle to the HMI panel.
    add_connection_patches(hfig, haxe, haxe_hmi, roi_xpix_lim, roi_ypix_lim, color="w", linewidth=0.3)


    ########################################################
    # Bottom colorbars
    ########################################################

    haxe_bar_aia = hfig.add_axes(pos_bar_aia)
    aia_cbar_ticks = [10, 200, 400, 800, 1600]
    cbar_aia = hfig.colorbar(him, cax=haxe_bar_aia, orientation="horizontal", ticks=aia_cbar_ticks)
    cbar_aia.ax.xaxis.set_zorder(10)
    cbar_aia.ax.tick_params(axis="x", which="major", bottom=True, top=False, direction="in", length=2.0, width=0.4, color="white", labelcolor="k", labelsize=5)
    cbar_aia.outline.set_visible(False)
    cbar_aia.set_label(r"$\rm{AIA\ 171\AA\ Intensity}$", fontsize=6)


    haxe_bar_hmi = hfig.add_axes(pos_bar_hmi)
    hmi_cbar_ticks = [-1600, -800, 0, 800, 1600]
    cbar_hmi = hfig.colorbar(hmi_image, cax=haxe_bar_hmi, orientation="horizontal", ticks=hmi_cbar_ticks)
    cbar_hmi.ax.xaxis.set_zorder(10)
    cbar_hmi.ax.tick_params(axis="x", which="major", bottom=True, top=False, direction="in", length=2.0, width=0.4, color="white", labelcolor="k", labelsize=5)
    cbar_hmi.outline.set_visible(False)
    cbar_hmi.set_label(r"$B_r\ [\rm{G}]$", fontsize=6)




    ########################################################
    # NLFFF Field
    ########################################################


    plot_every = 1

    selected_bz = [fieldline_bz[fieldline_id] for fieldline_id in range(0, len(fieldlines), plot_every)]

    if not selected_bz:
        raise ValueError("No field lines were selected for rendering.")

    vmin, vmax = srmt_fieldline_color_limits(selected_bz, FIELDLINE_COLOR_MIN, FIELDLINE_COLOR_MAX)
    normalizer = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)




    ########################################################
    # Full-disk panel in helioprojective coordinates
    ########################################################

    haxe = add_axes_3d_exact(hfig, pos_nlfff)
    haxe.view_init(elev=VIEW_ELEVATION, azim=VIEW_AZIMUTH)
    haxe.set_box_aspect(None, zoom=BOX_ZOOM)

    ########################################################
    # Axes: helioprojective tick labels and viewing angle
    ########################################################


    legend_handles: list[Patch] = []
    rendered_isosurface_count = 0
    rendered_fieldline_count = 0

    for isovalue_id, isovalue in enumerate(isovalues):
        level = float(isovalue["level"])
        level_rendered = False
        for surface in srmt_isovalue_components(isovalue):
            faces = numpy.asarray(surface["faces"], dtype=numpy.float64)
            if faces.size == 0:
                continue
            faces = to_helioprojective_geometry(faces, stored_isosurface_coordinates, hmi_wcs, aia_wcs)
            collection = Poly3DCollection(faces, facecolors=[ISOSURFACE_COLORS[isovalue_id]], edgecolors="none", linewidths=0.0, alpha=float(ISOSURFACE_OPACITIES[isovalue_id]), zsort="average", zorder=20)
            haxe.add_collection3d(collection)
            rendered_isosurface_count += 1
            level_rendered = True

        if level_rendered:
            B_tmp   = level
            wce_tmp = 2.79925e6*B_tmp*1e-9
            legend_handles.append(Patch(facecolor=ISOSURFACE_COLORS[isovalue_id], edgecolor="none", alpha=float(ISOSURFACE_OPACITIES[isovalue_id]), label=r"$|B|=%.2f\ \rm{G},\ $"%(B_tmp)+r"$f_{ce}=%.1f\ \rm{GHz}$"%(wce_tmp)))





    if rendered_isosurface_count == 0:
        raise ValueError("No non-empty SRMT isosurface components were rendered.")

    segments_all: list[numpy.ndarray] = []
    segment_bz_all: list[numpy.ndarray] = []
    for fieldline_id in range(0, len(fieldlines), plot_every):
        line = to_helioprojective_geometry(fieldlines[fieldline_id], stored_fieldline_coordinates, hmi_wcs, aia_wcs)
        bz = numpy.asarray(fieldline_bz[fieldline_id], dtype=numpy.float64)
        if line.shape[0] < 2:
            continue
        if bz.shape != (line.shape[0],):
            raise ValueError(f"Field line {fieldline_id} has {line.shape[0]} points but {bz.size} Bz values.")

        segments = numpy.stack((line[:-1], line[1:]), axis=1)
        segment_bz = 0.5 * (bz[:-1] + bz[1:])
        valid = numpy.all(numpy.isfinite(segments), axis=(1, 2)) & numpy.isfinite(segment_bz)

        if numpy.any(valid):
            segments_all.append(segments[valid])
            segment_bz_all.append(segment_bz[valid])
            rendered_fieldline_count += 1

    if segments_all:
        segments = numpy.concatenate(segments_all, axis=0)
        segment_bz = numpy.concatenate(segment_bz_all)
        collection = Line3DCollection(segments, cmap=FIELDLINE_COLOR_CMAP, norm=normalizer, linewidth=FIELD_LINEWIDTH, alpha=FIELDLINE_COLOR_ALPHA, zorder=20)
        collection.set_array(segment_bz)
        haxe.add_collection3d(collection)

    if rendered_fieldline_count == 0:
        raise ValueError("No finite field-line segments were rendered.")

    print("rendered isosurface components =", rendered_isosurface_count)
    print("rendered field lines           =", rendered_fieldline_count)


    #colorbar_mappable = ScalarMappable(norm=normalizer, cmap="coolwarm")
    #colorbar_mappable.set_array(numpy.empty(0, dtype=numpy.float64))
    #hfig.colorbar(colorbar_mappable, ax=haxe, label=r"$B_z\ \rm{[G]}$")

    ########################################################
    # 3-D axis box: 12 edges with labels on selected edges
    ########################################################

    haxe.autoscale_view()

    haxe.set_xlim(FIELDLINE_XMIN, FIELDLINE_XMAX)
    haxe.set_ylim(FIELDLINE_YMIN, FIELDLINE_YMAX)

    haxe.set_zlim(FIELDLINE_ZMIN, FIELDLINE_ZMAX)

    style_axes_3d_box(haxe, tick_size=fontsize_tick, label_size=fontsize_label, axis_linewidth=axis_linewidth, tick_count=5, xlabel_pad=xlabel_pad, ylabel_pad=ylabel_pad, zlabel_pad=zlabel_pad, xticklabel_pad=xticklabel_pad, yticklabel_pad=yticklabel_pad, zticklabel_pad=zticklabel_pad)


    xmin, xmax = haxe.get_xlim3d()
    ymin, ymax = haxe.get_ylim3d()
    zmin, zmax = haxe.get_zlim3d()
    panel_label_offset = 0.02 * (zmax - zmin)
    haxe.text(xmin, ymax, zmax + panel_label_offset, r"$\rm{(b)}$", fontsize=10, ha="center", va="bottom")


    ########################################################
    # Legend: three isosurfaces
    ########################################################

    if legend_handles:
        haxe.legend(handles=legend_handles, loc=legend_location, bbox_to_anchor=legend_bbox_to_anchor, fontsize=legend_fontsize, frameon=False)


    ########################################################
    # Save
    ########################################################

    fig_path = path_fig
    fig_name = os.path.splitext(os.path.basename(__file__))[0]

    fig_save(plt, figpath=fig_path, figname=fig_name, extension=fig_fmts,)


    plt.close(hfig)
