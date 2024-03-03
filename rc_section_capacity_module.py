import numpy as np
from sectionproperties.pre.library import concrete_rectangular_section
import matplotlib.axes
from typing import Tuple

import concreteproperties.stress_strain_profile as ssp
from concreteproperties import (
    Concrete,
    ConcreteSection,
    SteelBar,
)

def concrete_section_analysis(
        height: float,
        width: float,
        top_rebar_number: float,
        top_rebar_size: float,
        top_clear_cover: float,
        bottom_rebar_number: float,
        bottom_rebar_size: float,
        bottom_clear_cover: float,
        axial_force: float,
        moment: float) -> Tuple[ConcreteSection, matplotlib.axes.Axes, matplotlib.axes.Axes]:
    
    """
    """

    # Hard Coded Concrete and Rebar Materials: B30 and A500
    # Service values not correct
    # Stress-strain profile - rectangular stress block

    conc_class = "B30"
    conc_Rb = 17
    conc_Rbt = 1.15
    conc_eb1 = 0.0005230769230769
    conc_eb2_short = 0.0035

    rebar_class = "A500"
    rebar_Rs = 435
    rebar_es2 = 0.025


    concrete_material = Concrete(
        name=conc_class,
        density=2.4e-6,
        stress_strain_profile=ssp.ConcreteLinear(elastic_modulus=34.8e3),
        ultimate_stress_strain_profile=ssp.BilinearStressStrain(
            compressive_strength=conc_Rb,
            compressive_strain=conc_eb1,
            ultimate_strain=conc_eb2_short,
        ),
        flexural_tensile_strength=conc_Rbt,
        colour="lightgrey",
    )

    rebar_material = SteelBar(
        name=rebar_class,
        density=7.85e-6,
        stress_strain_profile=ssp.SteelElasticPlastic(
            yield_strength=rebar_Rs,
            elastic_modulus=200e3,
            fracture_strain=rebar_es2,
        ),
        colour="grey",
    )

    top_single_rebar_area = np.pi * top_rebar_size ** 2 / 4
    bottom_single_rebar_area = np.pi * bottom_rebar_size ** 2 / 4
    
    geom = concrete_rectangular_section(
        height,
        width,
        top_rebar_size,
        top_single_rebar_area,
        top_rebar_number,
        top_clear_cover,
        bottom_rebar_size,
        bottom_single_rebar_area,
        bottom_rebar_number,
        bottom_clear_cover,
        conc_mat = concrete_material,
        steel_mat = rebar_material)

    conc_sec = ConcreteSection(geom)
    conc_sec_ax = conc_sec.plot_section()
    # conc_sec_ax.legend().set_visible(False)

    mi_res = conc_sec.moment_interaction_diagram(progress_bar=False)
    sec_int_diag = mi_res.plot_diagram()

    # ultimate_res = conc_sec.calculate_ultimate_stress()

    return conc_sec, conc_sec_ax, sec_int_diag