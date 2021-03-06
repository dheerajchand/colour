# -*- coding: utf-8 -*-
"""
Colour Quality Plotting
=======================

Defines the colour quality plotting objects:

-   :func:`colour.plotting.single_spd_colour_rendering_index_bars_plot`
-   :func:`colour.plotting.multi_spd_colour_rendering_index_bars_plot`
-   :func:`colour.plotting.single_spd_colour_quality_scale_bars_plot`
-   :func:`colour.plotting.multi_spd_colour_quality_scale_bars_plot`
"""

from __future__ import division

import matplotlib.pyplot as plt
import numpy as np
from itertools import cycle

from colour.constants import DEFAULT_FLOAT_DTYPE
from colour.plotting import (COLOUR_STYLE_CONSTANTS,
                             XYZ_to_plotting_colourspace, artist,
                             label_rectangles, override_style, render)
from colour.quality import (colour_quality_scale, colour_rendering_index)
from colour.quality.cri import TCS_ColorimetryData

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013-2018 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = [
    'colour_quality_bars_plot', 'single_spd_colour_rendering_index_bars_plot',
    'multi_spd_colour_rendering_index_bars_plot',
    'single_spd_colour_quality_scale_bars_plot',
    'multi_spd_colour_quality_scale_bars_plot'
]


@override_style()
def colour_quality_bars_plot(specifications,
                             labels=True,
                             hatching=None,
                             hatching_repeat=2,
                             **kwargs):
    """
    Plots the colour quality data of given illuminants or light sources colour
    quality specifications.

    Parameters
    ----------
    specifications : array_like
        Array of illuminants or light sources colour quality specifications.
    labels : bool, optional
        Add labels above bars.
    hatching : bool or None, optional
        Use hatching for the bars.
    hatching_repeat : int, optional
        Hatching pattern repeat.

    Other Parameters
    ----------------
    \**kwargs : dict, optional
        {:func:`colour.plotting.artist`, :func:`colour.plotting.render`},
        Please refer to the documentation of the previously listed definitions.

    Returns
    -------
    tuple
        Current figure and axes.

    Examples
    --------
    >>> from colour import (ILLUMINANTS_SPDS,
    ...                     LIGHT_SOURCES_SPDS, SpectralShape)
    >>> illuminant = ILLUMINANTS_SPDS['F2']
    >>> light_source = LIGHT_SOURCES_SPDS['Kinoton 75P']
    >>> light_source = light_source.copy().align(SpectralShape(360, 830, 1))
    >>> cqs_i = colour_quality_scale(illuminant, additional_data=True)
    >>> cqs_l = colour_quality_scale(light_source, additional_data=True)
    >>> colour_quality_bars_plot([cqs_i, cqs_l])  # doctest: +SKIP

    .. image:: ../_static/Plotting_Colour_Quality_Bars_Plot.png
        :align: center
        :alt: colour_quality_bars_plot
    """

    settings = {'uniform': True}
    settings.update(kwargs)

    figure, axes = artist(**settings)

    bar_width = 0.5
    y_ticks_interval = 10
    count_s, count_Q_as = len(specifications), 0
    patterns = cycle(COLOUR_STYLE_CONSTANTS.hatch.patterns)
    if hatching is None:
        hatching = False if count_s == 1 else True
    for i, specification in enumerate(specifications):
        Q_a, Q_as, colorimetry_data = (specification.Q_a, specification.Q_as,
                                       specification.colorimetry_data)

        count_Q_as = len(Q_as)
        colours = ([[1] * 3] + [
            np.clip(XYZ_to_plotting_colourspace(x.XYZ), 0, 1)
            for x in colorimetry_data[0]
        ])

        x = (i + np.arange(
            0, (count_Q_as + 1) * (count_s + 1), (count_s + 1),
            dtype=DEFAULT_FLOAT_DTYPE)) * bar_width
        y = [s[1].Q_a for s in sorted(Q_as.items(), key=lambda s: s[0])]
        y = np.array([Q_a] + list(y))

        bars = plt.bar(
            x,
            np.abs(y),
            color=colours,
            width=bar_width,
            edgecolor=COLOUR_STYLE_CONSTANTS.colour.dark,
            label=specification.name)

        hatches = ([next(patterns) * hatching_repeat] * (count_Q_as + 1)
                   if hatching else np.where(y < 0, next(patterns),
                                             None).tolist())

        for j, bar in enumerate(bars.patches):
            bar.set_hatch(hatches[j])

        if labels:
            label_rectangles(
                y,
                bars,
                rotation='horizontal' if count_s == 1 else 'vertical',
                offset=(0 if count_s == 1 else 3 / 100 * count_s + 65 / 1000,
                        0.025),
                text_size=-5 / 7 * count_s + 12.5)

    axes.axhline(
        y=100, color=COLOUR_STYLE_CONSTANTS.colour.dark, linestyle='--')

    axes.set_xticks(
        (np.arange(
            0, (count_Q_as + 1) * (count_s + 1), (count_s + 1),
            dtype=DEFAULT_FLOAT_DTYPE) * bar_width +
         (count_s * bar_width / 2)), ['Qa'] +
        ['Q{0}'.format(index + 1) for index in range(0, count_Q_as + 1, 1)])
    axes.set_yticks(range(0, 100 + y_ticks_interval, y_ticks_interval))

    aspect = 1 / (120 / (bar_width + len(Q_as) + bar_width * 2))
    bounding_box = (-bar_width, ((count_Q_as + 1) * (count_s + 1)) / 2, 0, 120)

    settings = {
        'axes': axes,
        'aspect': aspect,
        'bounding_box': bounding_box,
        'legend': hatching,
        'title': 'Colour Quality',
    }
    settings.update(kwargs)

    return render(**settings)


@override_style()
def single_spd_colour_rendering_index_bars_plot(spd, **kwargs):
    """
    Plots the *Colour Rendering Index* (CRI) of given illuminant or light
    source spectral power distribution.

    Parameters
    ----------
    spd : SpectralPowerDistribution
        Illuminant or light source spectral power distribution to plot the
        *Colour Rendering Index* (CRI).

    Other Parameters
    ----------------
    \**kwargs : dict, optional
        {:func:`colour.plotting.artist`, :func:`colour.plotting.render`},
        Please refer to the documentation of the previously listed definitions.
    labels : bool, optional
        {:func:`colour.plotting.quality.colour_quality_bars_plot`},
        Add labels above bars.
    hatching : bool or None, optional
        {:func:`colour.plotting.quality.colour_quality_bars_plot`},
        Use hatching for the bars.
    hatching_repeat : int, optional
        {:func:`colour.plotting.quality.colour_quality_bars_plot`},
        Hatching pattern repeat.

    Returns
    -------
    tuple
        Current figure and axes.

    Examples
    --------
    >>> from colour import ILLUMINANTS_SPDS
    >>> illuminant = ILLUMINANTS_SPDS['F2']
    >>> single_spd_colour_rendering_index_bars_plot(illuminant)
    ... # doctest: +SKIP

    .. image:: ../_static/Plotting_\
Single_SPD_Colour_Rendering_Index_Bars_Plot.png
        :align: center
        :alt: single_spd_colour_rendering_index_bars_plot
    """

    return multi_spd_colour_rendering_index_bars_plot([spd], **kwargs)


@override_style()
def multi_spd_colour_rendering_index_bars_plot(spds, **kwargs):
    """
    Plots the *Colour Rendering Index* (CRI) of given illuminants or light
    sources spectral power distributions.

    Parameters
    ----------
    spds : array_like
        Array of illuminants or light sources spectral power distributions to
        plot the *Colour Rendering Index* (CRI).

    Other Parameters
    ----------------
    \**kwargs : dict, optional
        {:func:`colour.plotting.artist`, :func:`colour.plotting.render`},
        Please refer to the documentation of the previously listed definitions.
    labels : bool, optional
        {:func:`colour.plotting.quality.colour_quality_bars_plot`},
        Add labels above bars.
    hatching : bool or None, optional
        {:func:`colour.plotting.quality.colour_quality_bars_plot`},
        Use hatching for the bars.
    hatching_repeat : int, optional
        {:func:`colour.plotting.quality.colour_quality_bars_plot`},
        Hatching pattern repeat.

    Returns
    -------
    tuple
        Current figure and axes.

    Examples
    --------
    >>> from colour import (ILLUMINANTS_SPDS,
    ...                     LIGHT_SOURCES_SPDS)
    >>> illuminant = ILLUMINANTS_SPDS['F2']
    >>> light_source = LIGHT_SOURCES_SPDS['Kinoton 75P']
    >>> multi_spd_colour_rendering_index_bars_plot([illuminant, light_source])
    ... # doctest: +SKIP

    .. image:: ../_static/Plotting_\
Multi_Spd_Colour_Rendering_Index_Bars_Plot.png
        :align: center
        :alt: multi_spd_colour_rendering_index_bars_plot
    """

    settings = dict(kwargs)
    settings.update({'standalone': False})

    specifications = [
        colour_rendering_index(spd, additional_data=True) for spd in spds
    ]

    # *colour rendering index* colorimetry data tristimulus values are
    # computed in [0, 100] domain however `colour_quality_bars_plot` expects
    # [0, 1] domain. As we want to keep `colour_quality_bars_plot` definition
    # agnostic from the colour quality data, we update the test spd
    # colorimetry data tristimulus values domain.
    for specification in specifications:
        colorimetry_data = specification.colorimetry_data
        for i, c_d in enumerate(colorimetry_data[0]):
            colorimetry_data[0][i] = TCS_ColorimetryData(
                c_d.name, c_d.XYZ / 100, c_d.uv, c_d.UVW)

    figure, axes = colour_quality_bars_plot(specifications, **settings)

    title = 'Colour Rendering Index - {0}'.format(', '.join(
        [spd.strict_name for spd in spds]))

    settings = {'axes': axes, 'title': title}
    settings.update(kwargs)

    return render(**settings)


@override_style()
def single_spd_colour_quality_scale_bars_plot(spd, **kwargs):
    """
    Plots the *Colour Quality Scale* (CQS) of given illuminant or light source
    spectral power distribution.

    Parameters
    ----------
    spd : SpectralPowerDistribution
        Illuminant or light source spectral power distribution to plot the
        *Colour Quality Scale* (CQS).

    Other Parameters
    ----------------
    \**kwargs : dict, optional
        {:func:`colour.plotting.artist`, :func:`colour.plotting.render`},
        Please refer to the documentation of the previously listed definitions.
    labels : bool, optional
        {:func:`colour.plotting.quality.colour_quality_bars_plot`},
        Add labels above bars.
    hatching : bool or None, optional
        {:func:`colour.plotting.quality.colour_quality_bars_plot`},
        Use hatching for the bars.
    hatching_repeat : int, optional
        {:func:`colour.plotting.quality.colour_quality_bars_plot`},
        Hatching pattern repeat.

    Returns
    -------
    tuple
        Current figure and axes.

    Examples
    --------
    >>> from colour import ILLUMINANTS_SPDS
    >>> illuminant = ILLUMINANTS_SPDS['F2']
    >>> single_spd_colour_quality_scale_bars_plot(illuminant)
    ... # doctest: +SKIP

    .. image:: ../_static/Plotting_\
Single_SPD_Colour_Quality_Scale_Bars_Plot.png
        :align: center
        :alt: single_spd_colour_quality_scale_bars_plot
    """

    return multi_spd_colour_quality_scale_bars_plot([spd], **kwargs)


@override_style()
def multi_spd_colour_quality_scale_bars_plot(spds, **kwargs):
    """
    Plots the *Colour Quality Scale* (CQS) of given illuminants or light
    sources spectral power distributions.

    Parameters
    ----------
    spds : array_like
        Array of illuminants or light sources spectral power distributions to
        plot the *Colour Quality Scale* (CQS).

    Other Parameters
    ----------------
    \**kwargs : dict, optional
        {:func:`colour.plotting.artist`, :func:`colour.plotting.render`},
        Please refer to the documentation of the previously listed definitions.
    labels : bool, optional
        {:func:`colour.plotting.quality.colour_quality_bars_plot`},
        Add labels above bars.
    hatching : bool or None, optional
        {:func:`colour.plotting.quality.colour_quality_bars_plot`},
        Use hatching for the bars.
    hatching_repeat : int, optional
        {:func:`colour.plotting.quality.colour_quality_bars_plot`},
        Hatching pattern repeat.

    Returns
    -------
    tuple
        Current figure and axes.

    Examples
    --------
    >>> from colour import (ILLUMINANTS_SPDS,
    ...                     LIGHT_SOURCES_SPDS)
    >>> illuminant = ILLUMINANTS_SPDS['F2']
    >>> light_source = LIGHT_SOURCES_SPDS['Kinoton 75P']
    >>> multi_spd_colour_quality_scale_bars_plot([illuminant, light_source])
    ... # doctest: +SKIP

    .. image:: ../_static/Plotting_\
Multi_Spd_Colour_Quality_Scale_Bars_Plot.png
        :align: center
        :alt: multi_spd_colour_quality_scale_bars_plot
    """

    settings = dict(kwargs)
    settings.update({'standalone': False})

    specifications = [
        colour_quality_scale(spd, additional_data=True) for spd in spds
    ]

    figure, axes = colour_quality_bars_plot(specifications, **settings)

    title = 'Colour Quality Scale - {0}'.format(', '.join(
        [spd.strict_name for spd in spds]))

    settings = {'axes': axes, 'title': title}
    settings.update(kwargs)

    return render(**settings)
