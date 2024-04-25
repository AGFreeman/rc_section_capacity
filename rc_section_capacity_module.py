import concreteproperties.stress_strain_profile as ssp
import matplotlib.axes
from typing import Tuple

import numpy as np
import pandas as pd
from concreteproperties import (
    Concrete,
    ConcreteSection,
    SteelBar,
    add_bar_rectangular_array,
)

from concreteproperties.results import MomentCurvatureResults, MomentInteractionResults
from plotly import graph_objects as go
from sectionproperties.pre.library import rectangular_section

from eng_module import utils as ut

from PIL import Image
import io


def define_concrete_material(
    c_class: str = "B30",
    density: float = 2.4e-6,
    diag_type: str = "Bilinear",
    load_type: str = "Transient",
    conc_tension: bool = False,
    humidity: str = "<40",
) -> list[Concrete, Concrete, go.Figure]:
    """_summary_

    Args:
        c_class (str, optional): _description_. Defaults to "B30".
        density (float, optional): _description_. Defaults to 2.4e-6.
        diag_type (str, optional): _description_. Defaults to "Bilinear".
        load_type (str, optional): _description_. Defaults to "Transient".
        no_tension (bool, optional): _description_. Defaults to False.
        humidity (str, optional): _description_. Defaults to "<40".

    Returns:
        Tuple[Concrete, Concrete, go.Figure]: _description_
    """

    mat_df = pd.read_excel("concrete.xlsx").set_index("Class")

    Rbn = mat_df.loc[c_class, "Rbn"]
    Rbtn = mat_df.loc[c_class, "Rbtn"]
    Rb = mat_df.loc[c_class, "Rb"]
    Rbt = mat_df.loc[c_class, "Rbt"]
    Eb = mat_df.loc[c_class, "Eb"]
    eps_b0_st = mat_df.loc[c_class, "eps_b0_st"]
    eps_b0_lt_to40 = mat_df.loc[c_class, "eps_b0_lt_to40"]
    eps_b0_lt_40to75 = mat_df.loc[c_class, "eps_b0_lt_40to75"]
    eps_b0_lt_75up = mat_df.loc[c_class, "eps_b0_lt_75up"]
    eps_b2_lt_to40 = mat_df.loc[c_class, "eps_b2_lt_to40"]
    eps_b2_lt_40to75 = mat_df.loc[c_class, "eps_b2_lt_40to75"]
    eps_b2_lt_75up = mat_df.loc[c_class, "eps_b2_lt_75up"]
    eps_b1red_lt_to40 = mat_df.loc[c_class, "eps_b1red_lt_to40"]
    eps_b1red_lt_40to75 = mat_df.loc[c_class, "eps_b1red_lt_40to75"]
    eps_b1red_lt_75up = mat_df.loc[c_class, "eps_b1red_lt_75up"]
    eps_bt0_st = mat_df.loc[c_class, "eps_bt0_st"]
    eps_bt0_lt_to40 = mat_df.loc[c_class, "eps_bt0_lt_to40"]
    eps_bt0_lt_40to75 = mat_df.loc[c_class, "eps_bt0_lt_40to75"]
    eps_bt0_lt_75up = mat_df.loc[c_class, "eps_bt0_lt_75up"]
    eps_bt2_lt_to40 = mat_df.loc[c_class, "eps_bt2_lt_to40"]
    eps_bt2_lt_40to75 = mat_df.loc[c_class, "eps_bt2_lt_40to75"]
    eps_bt2_lt_75up = mat_df.loc[c_class, "eps_bt2_lt_75up"]
    eps_bt1red_lt_to40 = mat_df.loc[c_class, "eps_bt1red_lt_to40"]
    eps_bt1red_lt_40to75 = mat_df.loc[c_class, "eps_bt1red_lt_40to75"]
    eps_bt1red_lt_75up = mat_df.loc[c_class, "eps_bt1red_lt_75up"]
    eps_b2_st = mat_df.loc[c_class, "eps_b2_st"]
    eps_b1red_st = mat_df.loc[c_class, "eps_b1red_st"]
    eps_bt2_st = mat_df.loc[c_class, "eps_bt2_st"]
    eps_bt1red_st = mat_df.loc[c_class, "eps_bt1red_st"]

    # conc_service_strain_trilin_curve_lt_to40 = [-1.2*eps_bt2_lt_to40,-1.1*eps_bt2_lt_to40,-eps_bt2_lt_to40,-eps_bt0_lt_to40,-0.6*Rbtn/Eb,0,0.6*Rbn/Eb,eps_b0_lt_to40,eps_b2_lt_to40]
    # conc_service_strain_trilin_curve_lt_40to75 = [-1.2*eps_bt2_lt_40to75,-1.1*eps_bt2_lt_40to75,-eps_bt2_lt_40to75,-eps_bt0_lt_40to75,-0.6*Rbtn/Eb,0,0.6*Rbn/Eb,eps_b0_lt_40to75,eps_b2_lt_40to75]
    # conc_service_strain_trilin_curve_lt_75up = [-1.2*eps_bt2_lt_75up,-1.1*eps_bt2_lt_75up,-eps_bt2_lt_75up,-eps_bt0_lt_75up,-0.6*Rbtn/Eb,0,0.6*Rbn/Eb,eps_b0_lt_75up,eps_b2_lt_75up]
    # conc_service_strain_trilin_curve_st = [-1.2*eps_bt2_st,-1.1*eps_bt2_st,-eps_bt2_st,-eps_bt0_st,-0.6*Rbtn/Eb,0,0.6*Rbn/Eb,eps_b0_st,eps_b2_st]

    # conc_service_strain_bilin_curve_lt_to40 = [-1.2*eps_bt2_lt_to40,-1.1*eps_bt2_lt_to40,-eps_bt2_lt_to40,-eps_bt1red_lt_to40,0,eps_b1red_lt_to40,eps_b2_lt_to40]
    # conc_service_strain_bilin_curve_lt_40to75 = [-1.2*eps_bt2_lt_40to75,-1.1*eps_bt2_lt_40to75,-eps_bt2_lt_40to75,-eps_bt1red_lt_40to75,0,eps_b1red_lt_40to75,eps_b2_lt_40to75]
    # conc_service_strain_bilin_curve_lt_75up = [-1.2*eps_bt2_lt_75up,-1.1*eps_bt2_lt_75up,-eps_bt2_lt_75up,-eps_bt1red_lt_75up,0,eps_b1red_lt_75up,eps_b2_lt_75up]
    # conc_service_strain_bilin_curve_st = [-1.2*eps_bt2_st,-1.1*eps_bt2_st,-eps_bt2_st,-eps_bt1red_st,0,eps_b1red_st,eps_b2_st]

    # conc_ultimate_strain_trilin_curve_lt_to40 = [-1.2*eps_bt2_lt_to40,-1.1*eps_bt2_lt_to40,-eps_bt2_lt_to40,-eps_bt0_lt_to40,-0.6*Rbt/Eb,0,0.6*Rb/Eb,eps_b0_lt_to40,eps_b2_lt_to40]
    # conc_ultimate_strain_trilin_curve_lt_40to75 = [-1.2*eps_bt2_lt_40to75,-1.1*eps_bt2_lt_40to75,-eps_bt2_lt_40to75,-eps_bt0_lt_40to75,-0.6*Rbt/Eb,0,0.6*Rb/Eb,eps_b0_lt_40to75,eps_b2_lt_40to75]
    # conc_ultimate_strain_trilin_curve_lt_75up = [-1.2*eps_bt2_lt_75up,-1.1*eps_bt2_lt_75up,-eps_bt2_lt_75up,-eps_bt0_lt_75up,-0.6*Rbt/Eb,0,0.6*Rb/Eb,eps_b0_lt_75up,eps_b2_lt_75up]
    # conc_ultimate_strain_trilin_curve_st = [-1.2*eps_bt2_st,-1.1*eps_bt2_st,-eps_bt0_st,-eps_bt2_st,-eps_bt0_st,-0.6*Rbt/Eb,0,0.6*Rb/Eb,eps_b0_st,eps_b2_st]

    # conc_ultimate_strain_bilin_curve_lt_to40 = [-1.2*eps_bt2_lt_to40,-1.1*eps_bt2_lt_to40,-eps_bt2_lt_to40,-eps_bt1red_lt_to40,0,eps_b1red_lt_to40,eps_b2_lt_to40]
    # conc_ultimate_strain_bilin_curve_lt_40to75 = [-1.2*eps_bt2_lt_40to75,-1.1*eps_bt2_lt_40to75,-eps_bt2_lt_40to75,-eps_bt1red_lt_40to75,0,eps_b1red_lt_40to75,eps_b2_lt_40to75]
    # conc_ultimate_strain_bilin_curve_lt_75up = [-1.2*eps_bt2_lt_75up,-1.1*eps_bt2_lt_75up,-eps_bt2_lt_75up,-eps_bt1red_lt_75up,0,eps_b1red_lt_75up,eps_b2_lt_75up]
    # conc_ultimate_strain_bilin_curve_st = [-1.2*eps_bt2_st,-1.1*eps_bt2_st,-eps_bt2_st,-eps_bt1red_st,0,eps_b1red_st,eps_b2_st]

    # conc_service_stress_trilin_curve_lt_to40 = [0,0,-Rbtn,-Rbtn,-0.6*Rbtn,0,0.6*Rbn,Rbn,Rbn]
    # conc_service_stress_trilin_curve_lt_40to75 = [0,0,-Rbtn,-Rbtn,-0.6*Rbtn,0,0.6*Rbn,Rbn,Rbn]
    # conc_service_stress_trilin_curve_lt_75up = [0,0,-Rbtn,-Rbtn,-0.6*Rbtn,0,0.6*Rbn,Rbn,Rbn]
    # conc_service_stress_trilin_curve_st = [0,0,-Rbtn,-Rbtn,-0.6*Rbtn,0,0.6*Rbn,Rbn,Rbn]

    # conc_service_stress_bilin_curve_lt_to40 = [0,0,-Rbtn,-Rbtn,0,Rbn,Rbn]
    # conc_service_stress_bilin_curve_lt_40to75 = [0,0,-Rbtn,-Rbtn,0,Rbn,Rbn]
    # conc_service_stress_bilin_curve_lt_75up = [0,0,-Rbtn,-Rbtn,0,Rbn,Rbn]
    # conc_service_stress_bilin_curve_st = [0,0,-Rbtn,-Rbtn,0,Rbn,Rbn]

    # conc_ultimate_stress_trilin_curve_lt_to40 = [0,0,-Rbt,-Rbt,-0.6*Rbt,0,0.6*Rb,Rb,Rb]
    # conc_ultimate_stress_trilin_curve_lt_40to75 = [0,0,-Rbt,-Rbt,-0.6*Rbt,0,0.6*Rb,Rb,Rb]
    # conc_ultimate_stress_trilin_curve_lt_75up = [0,0,-Rbt,-Rbt,-0.6*Rbt,0,0.6*Rb,Rb,Rb]
    # conc_ultimate_stress_trilin_curve_st = [0,0,-Rbt,-Rbt,-0.6*Rbt,0,0.6*Rb,Rb,Rb]

    # conc_ultimate_stress_bilin_curve_lt_to40 = [0,0,-Rbt,-Rbt,0,Rb,Rb]
    # conc_ultimate_stress_bilin_curve_lt_40to75 = [0,0,-Rbt,-Rbt,0,Rb,Rb]
    # conc_ultimate_stress_bilin_curve_lt_75up = [0,0,-Rbt,-Rbt,0,Rb,Rb]
    # conc_ultimate_stress_bilin_curve_st = [0,0,-Rbt,-Rbt,0,Rb,Rb]

    conc_service_strain_trilin_curve_lt_to40 = [
        -1.2 * eps_bt2_lt_to40,
        -1.1 * eps_bt2_lt_to40,
        -eps_bt2_lt_to40,
        -eps_bt0_lt_to40,
        -0.6 * Rbtn / Eb,
        0,
        0.6 * Rbn / Eb,
        eps_b0_lt_to40,
        eps_b2_lt_to40,
    ]
    conc_service_strain_trilin_curve_lt_40to75 = [
        -1.2 * eps_bt2_lt_40to75,
        -1.1 * eps_bt2_lt_40to75,
        -eps_bt2_lt_40to75,
        -eps_bt0_lt_40to75,
        -0.6 * Rbtn / Eb,
        0,
        0.6 * Rbn / Eb,
        eps_b0_lt_40to75,
        eps_b2_lt_40to75,
    ]
    conc_service_strain_trilin_curve_lt_75up = [
        -1.2 * eps_bt2_lt_75up,
        -1.1 * eps_bt2_lt_75up,
        -eps_bt2_lt_75up,
        -eps_bt0_lt_75up,
        -0.6 * Rbtn / Eb,
        0,
        0.6 * Rbn / Eb,
        eps_b0_lt_75up,
        eps_b2_lt_75up,
    ]
    conc_service_strain_trilin_curve_st = [
        -1.2 * eps_bt2_st,
        -1.1 * eps_bt2_st,
        -eps_bt2_st,
        -eps_bt0_st,
        -0.6 * Rbtn / Eb,
        0,
        0.6 * Rbn / Eb,
        eps_b0_st,
        eps_b2_st,
    ]

    conc_service_strain_bilin_curve_lt_to40 = [
        -1.2 * eps_bt2_lt_to40,
        -1.1 * eps_bt2_lt_to40,
        -eps_bt2_lt_to40,
        -eps_bt1red_lt_to40,
        0,
        eps_b1red_lt_to40,
        eps_b2_lt_to40,
    ]
    conc_service_strain_bilin_curve_lt_40to75 = [
        -1.2 * eps_bt2_lt_40to75,
        -1.1 * eps_bt2_lt_40to75,
        -eps_bt2_lt_40to75,
        -eps_bt1red_lt_40to75,
        0,
        eps_b1red_lt_40to75,
        eps_b2_lt_40to75,
    ]
    conc_service_strain_bilin_curve_lt_75up = [
        -1.2 * eps_bt2_lt_75up,
        -1.1 * eps_bt2_lt_75up,
        -eps_bt2_lt_75up,
        -eps_bt1red_lt_75up,
        0,
        eps_b1red_lt_75up,
        eps_b2_lt_75up,
    ]
    conc_service_strain_bilin_curve_st = [
        -1.2 * eps_bt2_st,
        -1.1 * eps_bt2_st,
        -eps_bt2_st,
        -eps_bt1red_st,
        0,
        eps_b1red_st,
        eps_b2_st,
    ]

    conc_ultimate_strain_trilin_curve_lt_to40 = conc_service_strain_trilin_curve_lt_to40
    conc_ultimate_strain_trilin_curve_lt_40to75 = (
        conc_service_strain_trilin_curve_lt_40to75
    )
    conc_ultimate_strain_trilin_curve_lt_75up = conc_service_strain_trilin_curve_lt_75up
    conc_ultimate_strain_trilin_curve_st = conc_service_strain_trilin_curve_st

    conc_ultimate_strain_bilin_curve_lt_to40 = conc_service_strain_bilin_curve_lt_to40
    conc_ultimate_strain_bilin_curve_lt_40to75 = (
        conc_service_strain_bilin_curve_lt_40to75
    )
    conc_ultimate_strain_bilin_curve_lt_75up = conc_service_strain_bilin_curve_lt_75up
    conc_ultimate_strain_bilin_curve_st = conc_service_strain_bilin_curve_st

    conc_service_stress_trilin_curve = [
        0,
        0,
        -Rbtn,
        -Rbtn,
        -0.6 * Rbtn,
        0,
        0.6 * Rbn,
        Rbn,
        Rbn,
    ]
    conc_service_stress_trilin_curve_lt_to40 = conc_service_stress_trilin_curve
    conc_service_stress_trilin_curve_lt_40to75 = conc_service_stress_trilin_curve
    conc_service_stress_trilin_curve_lt_75up = conc_service_stress_trilin_curve
    conc_service_stress_trilin_curve_st = conc_service_stress_trilin_curve

    conc_service_stress_bilin_curve = [0, 0, -Rbtn, -Rbtn, 0, Rbn, Rbn]
    conc_service_stress_bilin_curve_lt_to40 = conc_service_stress_bilin_curve
    conc_service_stress_bilin_curve_lt_40to75 = conc_service_stress_bilin_curve
    conc_service_stress_bilin_curve_lt_75up = conc_service_stress_bilin_curve
    conc_service_stress_bilin_curve_st = conc_service_stress_bilin_curve

    conc_ultimate_stress_trilin_curve = [
        0,
        0,
        -Rbt,
        -Rbt,
        -0.6 * Rbt,
        0,
        0.6 * Rb,
        Rb,
        Rb,
    ]
    conc_ultimate_stress_trilin_curve_lt_to40 = conc_ultimate_stress_trilin_curve
    conc_ultimate_stress_trilin_curve_lt_40to75 = conc_ultimate_stress_trilin_curve
    conc_ultimate_stress_trilin_curve_lt_75up = conc_ultimate_stress_trilin_curve
    conc_ultimate_stress_trilin_curve_st = conc_ultimate_stress_trilin_curve

    conc_ultimate_stress_bilin_curve = [0, 0, -Rbt, -Rbt, 0, Rb, Rb]
    conc_ultimate_stress_bilin_curve_lt_to40 = conc_ultimate_stress_bilin_curve
    conc_ultimate_stress_bilin_curve_lt_40to75 = conc_ultimate_stress_bilin_curve
    conc_ultimate_stress_bilin_curve_lt_75up = conc_ultimate_stress_bilin_curve
    conc_ultimate_stress_bilin_curve_st = conc_ultimate_stress_bilin_curve

    if diag_type == "Bilinear":
        if load_type == "Transient":
            conc_service_strain = conc_service_strain_bilin_curve_st
            conc_service_stress = conc_service_stress_bilin_curve_st
            conc_ultimate_strain = conc_ultimate_strain_bilin_curve_st
            conc_ultimate_stress = conc_ultimate_stress_bilin_curve_st
        elif load_type == "Sustained":
            if humidity == "<40":
                conc_service_strain = conc_service_strain_bilin_curve_lt_to40
                conc_service_stress = conc_service_stress_bilin_curve_lt_to40
                conc_ultimate_strain = conc_ultimate_strain_bilin_curve_lt_to40
                conc_ultimate_stress = conc_ultimate_stress_bilin_curve_lt_to40
            elif humidity == "40-75":
                conc_service_strain = conc_service_strain_bilin_curve_lt_40to75
                conc_service_stress = conc_service_stress_bilin_curve_lt_40to75
                conc_ultimate_strain = conc_ultimate_strain_bilin_curve_lt_40to75
                conc_ultimate_stress = conc_ultimate_stress_bilin_curve_lt_40to75
            elif humidity == ">75":
                conc_service_strain = conc_service_strain_bilin_curve_lt_75up
                conc_service_stress = conc_service_stress_bilin_curve_lt_75up
                conc_ultimate_strain = conc_ultimate_strain_bilin_curve_lt_75up
                conc_ultimate_stress = conc_ultimate_stress_bilin_curve_lt_75up
    elif diag_type == "Trilinear":
        if load_type == "Transient":
            conc_service_strain = conc_service_strain_trilin_curve_st
            conc_service_stress = conc_service_stress_trilin_curve_st
            conc_ultimate_strain = conc_ultimate_strain_trilin_curve_st
            conc_ultimate_stress = conc_ultimate_stress_trilin_curve_st
        elif load_type == "Sustained":
            if humidity == "<40":
                conc_service_strain = conc_service_strain_trilin_curve_lt_to40
                conc_service_stress = conc_service_stress_trilin_curve_lt_to40
                conc_ultimate_strain = conc_ultimate_strain_trilin_curve_lt_to40
                conc_ultimate_stress = conc_ultimate_stress_trilin_curve_lt_to40
            elif humidity == "40-75":
                conc_service_strain = conc_service_strain_trilin_curve_lt_40to75
                conc_service_stress = conc_service_stress_trilin_curve_lt_40to75
                conc_ultimate_strain = conc_ultimate_strain_trilin_curve_lt_40to75
                conc_ultimate_stress = conc_ultimate_stress_trilin_curve_lt_40to75
            elif humidity == ">75":
                conc_service_strain = conc_service_strain_trilin_curve_lt_75up
                conc_service_stress = conc_service_stress_trilin_curve_lt_75up
                conc_ultimate_strain = conc_ultimate_strain_trilin_curve_lt_75up
                conc_ultimate_stress = conc_ultimate_stress_trilin_curve_lt_75up

    if conc_tension == False:
        conc_service_strain = conc_service_strain[conc_service_strain.index(0) - 1 :]
        conc_ultimate_strain = conc_ultimate_strain[conc_ultimate_strain.index(0) - 1 :]
        conc_service_stress = [0] + conc_service_stress[
            conc_service_stress.index(0, 2) :
        ]
        conc_ultimate_stress = [0] + conc_ultimate_stress[
            conc_ultimate_stress.index(0, 2) :
        ]

    print(f"conc_service_strain={conc_service_strain}")
    print(f"conc_service_stress={conc_service_stress}")
    print(f"conc_ultimate_strain={conc_ultimate_strain}")
    print(f"conc_ultimate_stress={conc_ultimate_stress}")

    # Service profile in concreteproperties is used for calculation of area properties,
    # moment-curvature analysis, elastic and service stress analysis.
    # We will create 2 concrete materials: 1 for service loads and 2 for ultimate loads
    # Each material will use same curve for both service and ultimate curve
    # Do I need service curve and material? What for?

    ultimate_concrete_material = Concrete(
        name=c_class,
        density=density,
        stress_strain_profile=ssp.ConcreteServiceProfile(
            conc_ultimate_strain, conc_ultimate_stress, conc_ultimate_strain[-1]
        ),
        ultimate_stress_strain_profile=ssp.ConcreteUltimateProfile(
            conc_ultimate_strain, conc_ultimate_stress, Rb
        ),
        flexural_tensile_strength=Rbt,
        colour="lightgrey",
    )

    service_concrete_material = Concrete(
        name=c_class,
        density=density,
        stress_strain_profile=ssp.ConcreteServiceProfile(
            conc_service_strain, conc_service_stress, conc_service_strain[-1]
        ),
        ultimate_stress_strain_profile=ssp.ConcreteUltimateProfile(
            conc_service_strain, conc_service_stress, Rbn
        ),
        flexural_tensile_strength=Rbtn,
        colour="lightgrey",
    )

    # ssp_service_plot = service_concrete_material.stress_strain_profile.plot_stress_strain()
    # ssp_ultimate_plot = ultimate_concrete_material.ultimate_stress_strain_profile.plot_stress_strain()

    ssp_plot = go.Figure()

    ssp_plot.add_scatter(
        x=conc_service_strain,
        y=conc_service_stress,
        name="SLS",
        line=dict(color="darkcyan"),
    )
    ssp_plot.add_scatter(
        x=conc_ultimate_strain,
        y=conc_ultimate_stress,
        name="ULS",
        line=dict(color="cyan"),
    )

    ssp_plot.update_layout(
        title=f"Concrete {c_class} diagrams",
        title_font=dict(size=20),
        title_x=0.5,
        title_xanchor="center",
        xaxis=dict(
            title="Strain, mm/mm",
            title_font=dict(size=16),
            tickfont=dict(size=14),
            tickformat=".5f",
            showgrid=True,
        ),
        yaxis=dict(
            title="Stress, MPa",
            title_font=dict(size=16),
            tickfont=dict(size=14),
            showgrid=True,
        ),
        legend=dict(font=dict(size=16)),
    )

    return service_concrete_material, ultimate_concrete_material, ssp_plot


def define_rebar_material(
    r_class: str = "A500", density: float = 7.85e-6, load_type: str = "Transient"
) -> list[SteelBar, SteelBar, go.Figure]:
    """ """
    mat_df = pd.read_excel("rebar.xlsx").set_index("Class")

    Rsn = mat_df.loc[r_class, "Rsn"]
    Rs = mat_df.loc[r_class, "Rs"]
    Rsc_st = mat_df.loc[r_class, "Rsc_st"]
    Rsc_lt = mat_df.loc[r_class, "Rsc_lt"]
    Es = mat_df.loc[r_class, "Es"]
    eps_s2_bl = mat_df.loc[r_class, "eps_s2_bl"]
    eps_s2_tl = mat_df.loc[r_class, "eps_s2_tl"]

    if r_class not in ("A600", "A800", "A1000"):
        eps_sn0 = Rsn / Es
        eps_s0 = Rs / Es
        eps_sc0_st = Rsc_st / Es
        eps_sc0_lt = Rsc_lt / Es
    else:
        eps_sn0 = Rsn / Es + 0.002
        eps_s0 = Rs / Es + 0.002
        eps_sc0_st = Rsc_st / Es + 0.002
        eps_sc0_lt = Rsc_lt / Es + 0.002

    rebar_service_strain_bilin_curve_lt = [-eps_s2_bl, -eps_sn0, 0, eps_sn0, eps_s2_bl]
    rebar_service_strain_bilin_curve_st = rebar_service_strain_bilin_curve_lt

    rebar_ultimate_strain_bilin_curve_lt = [
        -eps_s2_bl,
        -eps_s0,
        0,
        eps_sc0_lt,
        eps_s2_bl,
    ]
    rebar_ultimate_strain_bilin_curve_st = [
        -eps_s2_bl,
        -eps_s0,
        0,
        eps_sc0_st,
        eps_s2_bl,
    ]

    rebar_service_strain_trilin_curve_lt = [
        -eps_s2_tl,
        -2 * eps_sn0 + 0.9 * Rsn / Es,
        -eps_sn0,
        -0.9 * Rsn / Es,
        0,
        0.9 * Rsn / Es,
        eps_sn0,
        2 * eps_sn0 - 0.9 * Rsn / Es,
        eps_s2_tl,
    ]
    rebar_service_strain_trilin_curve_st = rebar_service_strain_trilin_curve_lt

    rebar_ultimate_strain_trilin_curve_lt = [
        -eps_s2_tl,
        -2 * eps_s0 + 0.9 * Rs / Es,
        -eps_s0,
        -0.9 * Rs / Es,
        0,
        0.9 * Rsc_lt / Es,
        eps_sc0_lt,
        2 * eps_sc0_lt - 0.9 * Rsc_lt / Es,
        eps_s2_tl,
    ]
    rebar_ultimate_strain_trilin_curve_st = [
        -eps_s2_tl,
        -2 * eps_s0 + 0.9 * Rs / Es,
        -eps_s0,
        -0.9 * Rs / Es,
        0,
        0.9 * Rsc_st / Es,
        eps_sc0_st,
        2 * eps_sc0_st - 0.9 * Rsc_st / Es,
        eps_s2_tl,
    ]

    rebar_service_stress_bilin_curve_lt = [-Rsn, -Rsn, 0, Rsn, Rsn]
    rebar_service_stress_bilin_curve_st = rebar_service_stress_bilin_curve_lt

    rebar_ultimate_stress_bilin_curve_lt = [-Rs, -Rs, 0, Rsc_lt, Rsc_lt]
    rebar_ultimate_stress_bilin_curve_st = [-Rs, -Rs, 0, Rsc_st, Rsc_st]

    rebar_service_stress_trilin_curve_lt = [
        -1.1 * Rsn,
        -1.1 * Rsn,
        -Rsn,
        -0.9 * Rsn,
        0,
        0.9 * Rsn,
        Rsn,
        1.1 * Rsn,
        1.1 * Rsn,
    ]
    rebar_service_stress_trilin_curve_st = rebar_service_stress_trilin_curve_lt

    rebar_ultimate_stress_trilin_curve_lt = [
        -1.1 * Rs,
        -1.1 * Rs,
        -Rs,
        -0.9 * Rs,
        0,
        0.9 * Rsc_lt,
        Rsc_lt,
        1.1 * Rsc_lt,
        1.1 * Rsc_lt,
    ]
    rebar_ultimate_stress_trilin_curve_st = [
        -1.1 * Rs,
        -1.1 * Rs,
        -Rs,
        -0.9 * Rs,
        0,
        0.9 * Rsc_st,
        Rsc_st,
        1.1 * Rsc_st,
        1.1 * Rsc_st,
    ]

    if r_class not in ("A600", "A800", "A1000"):
        if load_type == "Transient":
            rebar_service_strain = rebar_service_strain_bilin_curve_st
            rebar_service_stress = rebar_service_stress_bilin_curve_st
            rebar_ultimate_strain = rebar_ultimate_strain_bilin_curve_st
            rebar_ultimate_stress = rebar_ultimate_stress_bilin_curve_st
        elif load_type == "Sustained":
            rebar_service_strain = rebar_service_strain_bilin_curve_lt
            rebar_service_stress = rebar_service_stress_bilin_curve_lt
            rebar_ultimate_strain = rebar_ultimate_strain_bilin_curve_lt
            rebar_ultimate_stress = rebar_ultimate_stress_bilin_curve_lt
    else:
        if load_type == "Transient":
            rebar_service_strain = rebar_service_strain_trilin_curve_st
            rebar_service_stress = rebar_service_stress_trilin_curve_st
            rebar_ultimate_strain = rebar_ultimate_strain_trilin_curve_st
            rebar_ultimate_stress = rebar_ultimate_stress_trilin_curve_st
        elif load_type == "Sustained":
            rebar_service_strain = rebar_service_strain_trilin_curve_lt
            rebar_service_stress = rebar_service_stress_trilin_curve_lt
            rebar_ultimate_strain = rebar_ultimate_strain_trilin_curve_lt
            rebar_ultimate_stress = rebar_ultimate_stress_trilin_curve_lt

    print(
        rebar_service_strain,
        rebar_service_stress,
        rebar_ultimate_strain,
        rebar_ultimate_stress,
    )

    service_rebar_material = SteelBar(
        name=r_class,
        density=density,
        stress_strain_profile=ssp.SteelProfile(
            rebar_service_strain,
            rebar_service_stress,
            rebar_service_stress[-1],
            Es,
            rebar_service_strain[-1],
        ),
        colour="grey",
    )

    ultimate_rebar_material = SteelBar(
        name=r_class,
        density=density,
        stress_strain_profile=ssp.SteelProfile(
            rebar_ultimate_strain,
            rebar_ultimate_stress,
            rebar_ultimate_stress[-1],
            Es,
            rebar_ultimate_strain[-1],
        ),
        colour="grey",
    )

    ssp_plot = go.Figure()

    ssp_plot.add_scatter(
        x=rebar_service_strain,
        y=rebar_service_stress,
        name="SLS",
        line=dict(color="darkred"),
    )
    ssp_plot.add_scatter(
        x=rebar_ultimate_strain,
        y=rebar_ultimate_stress,
        name="ULS",
        line=dict(color="red"),
    )

    ssp_plot.update_layout(
        title=f"Rebar {r_class} diagram",
        title_font=dict(size=20),
        title_x=0.5,
        title_xanchor="center",
        xaxis=dict(
            title="Strain, mm/mm",
            title_font=dict(size=16),
            tickfont=dict(size=14),
            tickformat=".5f",
            showgrid=True,
        ),
        yaxis=dict(
            title="Stress, MPa",
            title_font=dict(size=16),
            tickfont=dict(size=14),
            showgrid=True,
        ),
        legend=dict(font=dict(size=16)),
    )

    return service_rebar_material, ultimate_rebar_material, ssp_plot


def create_rectangular_section(
    h: float = None,
    b: float = None,
    c_mat: Concrete = None,
    r_mat: SteelBar = None,
    dr_top: float = None,
    nr_top: float = None,
    nrl_top: float = None,
    srl_top: float = None,
    cc_top: float = None,
    dr_bot: float = None,
    nr_bot: float = None,
    nrl_bot: float = None,
    srl_bot: float = None,
    cc_bot: float = None,
    dr_side: float = None,
    nr_side: float = None,
    nrl_side: float = None,
    srl_side: float = None,
    cc_side: float = None,
) -> list[ConcreteSection, Image.Image]:

    # TODO
    # Don't convert from sec_ax, just plot circles?
    # Make toggle to set all covers equal
    # Make side bars between top and bottom row
    # Toggle consider minimum spacing
    # Change plot margins to be by extents of section

    # calculate rebar area and spacing
    As1_top = np.pi * dr_top**2 / 4
    sr_top = (b - 2 * cc_side - dr_top) / (nr_top - 1) if nr_top > 1 else 0

    As1_bot = np.pi * dr_bot**2 / 4
    sr_bot = (b - 2 * cc_side - dr_bot) / (nr_bot - 1) if nr_bot > 1 else 0

    As1_side = np.pi * dr_side**2 / 4
    nr_side_excl = max(nr_side - nrl_top - nrl_bot, 0)
    if nr_side_excl > 1:
        sr_side = (
            h
            - (
                cc_top
                + dr_top / 2
                + srl_top * (nrl_top - 1)
                + cc_bot
                + dr_bot / 2
                + srl_bot * (nrl_bot - 1)
            )
        ) / (nr_side_excl + 1)
    else:
        sr_side = 0

    # create concrete
    geom = rectangular_section(h, b, c_mat)

    # add top rebars
    geom = add_bar_rectangular_array(
        geometry=geom,
        area=As1_top,
        material=r_mat,
        n_x=nr_top,
        x_s=sr_top,
        n_y=nrl_top,
        y_s=srl_top,
        anchor=(
            cc_side + dr_top / 2 if nr_top > 1 else b / 2,
            (
                h - (cc_top + dr_top / 2 + srl_top * (nrl_top - 1))
                if nrl_top > 1
                else h - (cc_top + dr_top / 2)
            ),
        ),
        exterior_only=False,
        n=4,
    )

    # add bottom rebars
    geom = add_bar_rectangular_array(
        geometry=geom,
        area=As1_bot,
        material=r_mat,
        n_x=nr_bot,
        x_s=sr_bot,
        n_y=nrl_bot,
        y_s=srl_bot,
        anchor=(
            cc_side + dr_bot / 2 if nr_bot > 1 else b / 2,
            cc_bot + dr_bot / 2,
        ),
        exterior_only=False,
        n=4,
    )

    # add left side rebar
    geom = add_bar_rectangular_array(
        geometry=geom,
        area=As1_side,
        material=r_mat,
        n_x=nrl_side,
        x_s=srl_side,
        n_y=nr_side_excl,
        y_s=sr_side,
        anchor=(
            cc_side + dr_side / 2,
            (
                cc_bot + dr_bot / 2 + srl_bot * (nrl_bot - 1) + sr_side
                if nr_side_excl > 1
                else h / 2
            ),
        ),
        exterior_only=False,
        n=4,
    )

    # add right side rebar
    geom = add_bar_rectangular_array(
        geometry=geom,
        area=As1_side,
        material=r_mat,
        n_x=nrl_side,
        x_s=srl_side,
        n_y=nr_side_excl,
        y_s=sr_side,
        anchor=(
            (
                b - (cc_side + dr_side / 2 + srl_side * (nrl_side - 1))
                if nrl_side > 1
                else b - (cc_side + dr_side / 2)
            ),
            (
                cc_bot + dr_bot / 2 + srl_bot * (nrl_bot - 1) + sr_side
                if nr_side_excl > 1
                else h / 2
            ),
        ),
        exterior_only=False,
        n=4,
    )

    # create section onject
    sec = ConcreteSection(geom)

    # create section plot and convert it to image with transparent background
    sec_ax = sec.plot_section()
    sec_ax.set_title("")

    # Remove labels from lines
    for line in sec_ax.lines:
        line.set_label(None)

    # Remove labels from collections (e.g., scatter plots)
    for collection in sec_ax.collections:
        collection.set_label(None)

    # Remove legend
    sec_ax.legend().remove()

    buf = io.BytesIO()
    sec_ax.figure.savefig(
        buf, format="png", dpi=600, transparent=True, pad_inches="tight"
    )
    buf.seek(0)
    sec_img = Image.open(buf)

    # Plot section in Plotly

    # Create concrete outline in plotly
    # sec_fig = go.Figure()

    # sec_fig.add_scatter(
    #     x=[0, b, b, 0],
    #     y=[0, 0, h, h],
    #     name=c_mat.name,
    #     fill="toself",
    #     fillcolor="lightgray",
    #     line=dict(color="black", width=2),
    #     mode="lines",
    # )

    # Convert matplotlib pathes representing rebars into plotly filled scatters
    # patches = sec_ax.patches
    # for idx, polygon in enumerate(patches):
    #     vertices = polygon.get_path().vertices
    #     x_coords, y_coords = vertices[:, 0], vertices[:, 1]
    #     if idx == 0:
    #         sec_fig.add_scatter(
    #             x=np.append(x_coords, x_coords[0]),
    #             y=np.append(y_coords, y_coords[0]),
    #             name=r_mat.name,
    #             fill="toself",
    #             fillcolor="firebrick",
    #             line=dict(color="black", width=1),
    #             mode="lines",
    #         )
    #     else:
    #         sec_fig.add_scatter(
    #             x=np.append(x_coords, x_coords[0]),
    #             y=np.append(y_coords, y_coords[0]),
    #             fill="toself",
    #             name=r_mat.name,
    #             showlegend=False,
    #             fillcolor="firebrick",
    #             line=dict(color="black", width=1),
    #             mode="lines",
    #         )

    # sec_fig.layout.xaxis.scaleanchor = "y"
    # sec_fig.layout.xaxis.scaleratio = 1

    # sec_fig.update_layout(
    #     title=f"Сечение {h}x{b}",
    #     title_font=dict(size=20),
    #     title_x=0.5,
    #     title_xanchor="center",
    #     height=400,
    #     autosize=False,
    #     margin=dict(
    #         l=50,
    #         r=50,
    #         b=50,
    #         pad=0,
    #     ),
    #     legend=dict(
    #         orientation="h",
    #         yanchor="bottom",
    #         y=-0.25,
    #         xanchor="center",
    #         x=0.5,
    #         font=dict(size=16),
    #     ),
    #     xaxis=dict(
    #         tickmode="array",
    #         tickvals=np.linspace(0, b, 2),
    #         title_font=dict(size=16),
    #         tickfont=dict(size=14),
    #         showgrid=True,
    #     ),
    #     yaxis=dict(
    #         tickmode="array",
    #         tickvals=np.linspace(0, h, 2),
    #         title_font=dict(size=16),
    #         tickfont=dict(size=14),
    #         showgrid=True,
    #     ),
    # )

    return sec, sec_img


def calculate_effective_depth(
    sec_type: str,
    h: float,
    b: float,
    dr_top: float,
    nrl_top: float,
    srl_top: float,
    cc_top: float,
    dr_bot: float,
    nrl_bot: float,
    srl_bot: float,
    cc_bot: float,
    dr_side: float = None,
    nrl_side: float = None,
    srl_side: float = None,
    cc_side: float = None,
) -> list[float, float, float]:
    """
    Caclulates effective depth for a section
    """
    if sec_type == "Rectangular":
        h_eff_x_pos = h - cc_bot - dr_bot / 2 - srl_bot * (nrl_bot - 1) / 2
        h_eff_x_neg = h - cc_top - dr_top / 2 - srl_top * (nrl_top - 1) / 2
        h_eff_y = b - cc_side - dr_side / 2 - srl_side * (nrl_side - 1) / 2

    return h_eff_x_pos, h_eff_x_neg, h_eff_y


def concrete_section_properties(sec: ConcreteSection, c_mat: Concrete) -> list[float]:
    """_summary_

    Args:
        sec (ConcreteSection): _description_

    Returns:
        list[float]: _description_
    """

    gross_props = sec.get_gross_properties()
    unit_mass = gross_props.mass
    a_gr = gross_props.total_area
    a_conc = gross_props.concrete_area
    a_rebar = gross_props.reinf_lumped_area
    e_conc = c_mat.elastic_modulus
    transformed_props = sec.get_transformed_gross_properties(e_conc)
    i_xx_c_uncr = transformed_props.ixx_c
    i_yy_c_uncr = transformed_props.iyy_c
    cracked_props_x_pos = sec.calculate_cracked_properties()
    cracked_props_x_pos.calculate_transformed_properties(e_conc)
    i_xx_pos_c_cr = cracked_props_x_pos.ixx_c_cr
    d_x_pos = cracked_props_x_pos.d_nc
    cracked_props_x_neg = sec.calculate_cracked_properties(theta=np.pi)
    cracked_props_x_neg.calculate_transformed_properties(e_conc)
    i_xx_neg_c_cr = cracked_props_x_neg.ixx_c_cr
    d_x_neg = cracked_props_x_neg.d_nc
    # check sign and change sign convention if needed
    cracked_props_y_pos = sec.calculate_cracked_properties(theta=np.pi / 2)
    cracked_props_y_pos.calculate_transformed_properties(e_conc)
    i_yy_pos_c_cr = cracked_props_y_pos.iyy_c_cr
    d_y_pos = cracked_props_y_pos.d_nc

    return (
        unit_mass,
        a_gr,
        a_conc,
        a_rebar,
        i_xx_c_uncr,
        i_yy_c_uncr,
        i_xx_pos_c_cr,
        d_x_pos,
        i_xx_neg_c_cr,
        d_x_neg,
        i_yy_pos_c_cr,
        d_y_pos,
    )


def concrete_section_capacity(
    sec: ConcreteSection,
    n: float = None,
    m_x: float = None,
    m_y: float = None,
) -> list[float, float]:
    """ """
    # TODO
    # Add m_cr with N=N and N=0. See SP 63 8.2.14
    # Consider 8.1.30 SP 63 eps_b_ult is smaller than eps_b2 or eps_bt2 if stress is all tension or all compression

    # Resultant moment
    m_xy = (m_x**2 + m_y**2) ** 0.5

    m_theta = np.arctan2(m_x, -m_y) - np.pi / 2

    # Calculate ultimate moment at given neutral axis angle
    mu_xy = sec.ultimate_bending_capacity(theta=m_theta, n=n).m_xy
    mu_xy_n0 = sec.ultimate_bending_capacity(theta=m_theta, n=0).m_xy
    mu_x_pos_n0 = sec.ultimate_bending_capacity(theta=0, n=0).m_xy
    mu_x_neg_n0 = sec.ultimate_bending_capacity(theta=np.pi, n=0).m_xy
    mu_y_pos_n0 = sec.ultimate_bending_capacity(theta=np.pi / 2, n=0).m_xy

    return (m_theta, m_xy, mu_xy, mu_xy_n0, mu_x_pos_n0, mu_x_neg_n0, mu_y_pos_n0)


def concrete_section_moment_curvature_analysis(
    sec: ConcreteSection,
    n: float = None,
    m_theta: float = None,
) -> Tuple[MomentCurvatureResults, Image.Image]:
    """ """

    # TODO
    # Convert plot to plotly

    mc_res = sec.moment_curvature_analysis(theta=m_theta, n=n, progress_bar=False)
    mc_ax = mc_res.plot_results(fmt="-")

    # Convert plot to image with transparent background
    buf = io.BytesIO()
    mc_ax.figure.savefig(
        buf, format="png", dpi=600, transparent=True, pad_inches="tight"
    )
    buf.seek(0)
    mc_img = Image.open(buf)

    return mc_res, mc_img


def concrete_section_moment_interaction_diagram(
    sec: ConcreteSection, m_theta: float = None
) -> Tuple[MomentInteractionResults, Image.Image]:

    mi_res = sec.moment_interaction_diagram(theta=m_theta, progress_bar=False)
    mi_ax = mi_res.plot_diagram(moment="m_xy", fmt="-")

    # Convert plot to image with transparent background
    buf = io.BytesIO()
    mi_ax.figure.savefig(
        buf, format="png", dpi=600, transparent=True, pad_inches="tight"
    )
    buf.seek(0)
    mi_img = Image.open(buf)

    return mi_res, mi_img


def concrete_section_biaxial_moment_diagram(
    sec: ConcreteSection, n: float = None
) -> Tuple[MomentInteractionResults, Image.Image]:

    bb_res = sec.biaxial_bending_diagram(n=n, progress_bar=False)
    bb_ax = bb_res.plot_diagram(fmt="-")

    # Convert plot to image with transparent background
    buf = io.BytesIO()
    bb_ax.figure.savefig(
        buf, format="png", dpi=600, transparent=True, pad_inches="tight"
    )
    buf.seek(0)
    bb_img = Image.open(buf)

    return bb_res, bb_img


def concrete_section_3d_interaction_surface(
    sec: ConcreteSection, n_curves: int
) -> matplotlib.axes.Axes:

    # thetas = np.linspace(0, 2 * np.pi, n_curves, endpoint=False)

    # mi_plot = go.Figure()

    # for theta in thetas:
    #     mi_res = sec.moment_interaction_diagram(theta=theta, progress_bar=False)
    #     n_vals, m_vals = mi_res.get_results_lists(
    #         "m_x",
    #     )
    #     mi_plot.add_scatter(
    #         x=m_vals,
    #         y=n_vals,
    #         line=dict(color="darkcyan"),
    #     )

    mi_res = sec.moment_interaction_diagram(progress_bar=False)
    n_vals, m_vals = mi_res.get_results_lists(
        "m_x",
    )

    # bb_res = sec.biaxial_bending_diagram(progress_bar=False)

    bb_plot = go.Figure()

    n_max = n_vals[0]
    n_min = n_vals[-1]

    n_vals = [n_vals[1], n_vals[round(len(n_vals) / 2)], n_vals[-2]]

    for n in n_vals:
        bb_res = sec.biaxial_bending_diagram(n=n, progress_bar=False)
        m_x_vals, m_y_vals = bb_res.get_results_lists()
        n_vals = []
        n_vals = [n] * len(m_x_vals)
        print(n_vals)
        bb_plot.add_scatter3d(x=m_x_vals, y=m_y_vals, z=n_vals)

    # plot = bb_res.plot_diagram()

    # zilisp()

    return bb_plot


def concrete_section_stress_analysis(
    sec: ConcreteSection,
    mc_res: MomentCurvatureResults,
    m: float = None,
) -> Image.Image:
    """ """

    m_init = mc_res.m_xy[0]

    if m < m_init:
        stress_res = sec.calculate_service_stress(mc_res, m, kappa=0)
    else:
        stress_res = sec.calculate_service_stress(mc_res, m)

    stress_ax = stress_res.plot_stress(
        "Stress",
        "RdYlBu",
    )

    # Convert plot to image with transparent background
    buf = io.BytesIO()
    stress_ax.figure.savefig(
        buf, format="png", dpi=600, transparent=True, pad_inches="tight"
    )
    buf.seek(0)
    stress_img = Image.open(buf)

    return stress_img
