import numpy as np
from eng_module import utils as ut
from sectionproperties.pre.library import concrete_rectangular_section
import matplotlib.axes
from typing import Tuple

import concreteproperties.stress_strain_profile as ssp
from concreteproperties import (
    Concrete,
    ConcreteSection,
    SteelBar,
)


def convert_to_numeric(data: list[list[str]]) -> list[list[float]]:
    """
    Converts items in a list into floats
    """
    outside_acc = []
    for outside_item in data:
        inside_acc = []
        for inside_item in outside_item:
            inside_acc.append(ut.str_to_float(inside_item))
        outside_acc.append(inside_acc)
    return outside_acc

def define_concrete_material(
        conc_class: str = 'B30',
        conc_density: float = 2.4e-6,
        conc_diag_type: str = 'Двухлинейная',
        load_type: str = 'Кратковременная',
        humidity: str = '<40',
) -> Tuple[Concrete, matplotlib.axes.Axes, matplotlib.axes.Axes]:
        """
        """

        conc_mat_data = convert_to_numeric(ut.read_csv_file("concrete.csv"))
        for line in conc_mat_data:
            if conc_class == line[0]:
                Rbn = line[1]
                Rbtn = line[2]
                Rb = line[3]
                Rbt = line[4]
                Eb = line[5]
                eps_b0_st = line[6]
                eps_b0_lt_to40 = line[7]
                eps_b0_lt_40to75 = line[8]
                eps_b0_lt_75up = line[9]
                eps_b2_lt_to40 = line[10]
                eps_b2_lt_40to75 = line[11]
                eps_b2_lt_75up = line[12]
                eps_b1red_lt_to40 = line[13]
                eps_b1red_lt_40to75 = line[14]
                eps_b1red_lt_75up = line[15]
                eps_bt0_st = line[16]
                eps_bt0_lt_to40 = line[17]
                eps_bt0_lt_40to75 = line[18]
                eps_bt0_lt_75up = line[19]
                eps_bt2_lt_to40 = line[20]
                eps_bt2_lt_40to75 = line[21]
                eps_bt2_lt_75up = line[22]
                eps_bt1red_lt_to40 = line[23]
                eps_bt1red_lt_40to75 = line[24]
                eps_bt1red_lt_75up = line[25]
                eps_b2_st = line[26]
                eps_b1red_st = line[27]
                eps_bt2_st = line[28]
                eps_bt1red_st = line[29]

        conc_service_strain_trilin_curve_lt_to40 = [-1.2*eps_bt2_lt_to40,-1.1*eps_bt2_lt_to40,-eps_bt2_lt_to40,-eps_bt0_lt_to40,-0.6*Rbtn/Eb,0,0.6*Rbn/Eb,eps_b0_lt_to40,eps_b2_lt_to40]
        conc_service_strain_trilin_curve_lt_40to75 = [-1.2*eps_bt2_lt_40to75,-1.1*eps_bt2_lt_40to75,-eps_bt2_lt_40to75,-eps_bt0_lt_40to75,-0.6*Rbtn/Eb,0,0.6*Rbn/Eb,eps_b0_lt_40to75,eps_b2_lt_40to75]
        conc_service_strain_trilin_curve_lt_75up = [-1.2*eps_bt2_lt_75up,-1.1*eps_bt2_lt_75up,-eps_bt2_lt_75up,-eps_bt0_lt_75up,-0.6*Rbtn/Eb,0,0.6*Rbn/Eb,eps_b0_lt_75up,eps_b2_lt_75up]
        conc_service_strain_trilin_curve_st = [-1.2*eps_bt2_st,-1.1*eps_bt2_st,-eps_bt2_st,-eps_bt0_st,-0.6*Rbtn/Eb,0,0.6*Rbn/Eb,eps_b0_st,eps_b2_st]

        conc_service_strain_bilin_curve_lt_to40 = [-1.2*eps_bt2_lt_to40,-1.1*eps_bt2_lt_to40,-eps_bt2_lt_to40,-eps_bt1red_lt_to40,0,eps_b1red_lt_to40,eps_b2_lt_to40]
        conc_service_strain_bilin_curve_lt_40to75 = [-1.2*eps_bt2_lt_40to75,-1.1*eps_bt2_lt_40to75,-eps_bt2_lt_40to75,-eps_bt1red_lt_40to75,0,eps_b1red_lt_40to75,eps_b2_lt_40to75]
        conc_service_strain_bilin_curve_lt_75up = [-1.2*eps_bt2_lt_75up,-1.1*eps_bt2_lt_75up,-eps_bt2_lt_75up,-eps_bt1red_lt_75up,0,eps_b1red_lt_75up,eps_b2_lt_75up]
        conc_service_strain_bilin_curve_st = [-1.2*eps_bt2_st,-1.1*eps_bt2_st,-eps_bt2_st,-Rbtn/Eb,0,eps_b1red_st,eps_b2_st]

        conc_ultimate_strain_trilin_curve_lt_to40 = [-1.2*eps_bt2_lt_to40,-1.1*eps_bt2_lt_to40,-eps_bt2_lt_to40,-eps_bt0_lt_to40,-0.6*Rbt/Eb,0,0.6*Rb/Eb,eps_b0_lt_to40,eps_b2_lt_to40]
        conc_ultimate_strain_trilin_curve_lt_40to75 = [-1.2*eps_bt2_lt_40to75,-1.1*eps_bt2_lt_40to75,-eps_bt2_lt_40to75,-eps_bt0_lt_40to75,-0.6*Rbt/Eb,0,0.6*Rb/Eb,eps_b0_lt_40to75,eps_b2_lt_40to75]
        conc_ultimate_strain_trilin_curve_lt_75up = [-1.2*eps_bt2_lt_75up,-1.1*eps_bt2_lt_75up,-eps_bt2_lt_75up,-eps_bt0_lt_75up,-0.6*Rbt/Eb,0,0.6*Rb/Eb,eps_b0_lt_75up,eps_b2_lt_75up]
        conc_ultimate_strain_trilin_curve_st = [-1.2*eps_bt2_st,-1.1*eps_bt2_st,-eps_bt0_st,-eps_bt2_st,-eps_bt0_st,-0.6*Rbt/Eb,0,0.6*Rb/Eb,eps_b0_st,eps_b2_st]

        conc_ultimate_strain_bilin_curve_lt_to40 = [-1.2*eps_bt2_lt_to40,-1.1*eps_bt2_lt_to40,-eps_bt2_lt_to40,-eps_bt1red_lt_to40,0,eps_b1red_lt_to40,eps_b2_lt_to40]
        conc_ultimate_strain_bilin_curve_lt_40to75 = [-1.2*eps_bt2_lt_40to75,-1.1*eps_bt2_lt_40to75,-eps_bt2_lt_40to75,-eps_bt1red_lt_40to75,0,eps_b1red_lt_40to75,eps_b2_lt_40to75]
        conc_ultimate_strain_bilin_curve_lt_75up = [-1.2*eps_bt2_lt_75up,-1.1*eps_bt2_lt_75up,-eps_bt2_lt_75up,-eps_bt1red_lt_75up,0,eps_b1red_lt_75up,eps_b2_lt_75up]
        conc_ultimate_strain_bilin_curve_st = [-1.2*eps_bt2_st,-1.1*eps_bt2_st,-eps_bt2_st,-Rbt/Eb,0,eps_b1red_st,eps_b2_st]

        conc_service_stress_trilin_curve_lt_to40 = [0,0,-Rbtn,-Rbtn,-0.6*Rbtn,0,0.6*Rbn,Rbn,Rbn]
        conc_service_stress_trilin_curve_lt_40to75 = [0,0,-Rbtn,-Rbtn,-0.6*Rbtn,0,0.6*Rbn,Rbn,Rbn]
        conc_service_stress_trilin_curve_lt_75up = [0,0,-Rbtn,-Rbtn,-0.6*Rbtn,0,0.6*Rbn,Rbn,Rbn]
        conc_service_stress_trilin_curve_st = [0,0,-Rbtn,-Rbtn,-0.6*Rbtn,0,0.6*Rbn,Rbn,Rbn]

        conc_service_stress_bilin_curve_lt_to40 = [0,0,-Rbtn,-Rbtn,0,Rbn,Rbn]
        conc_service_stress_bilin_curve_lt_40to75 = [0,0,-Rbtn,-Rbtn,0,Rbn,Rbn]
        conc_service_stress_bilin_curve_lt_75up = [0,0,-Rbtn,-Rbtn,0,Rbn,Rbn]
        conc_service_stress_bilin_curve_st = [0,0,-Rbtn,-Rbtn,0,Rbn,Rbn]

        conc_ultimate_stress_trilin_curve_lt_to40 = [0,0,-Rbt,-Rbt,-0.6*Rbt,0,0.6*Rb,Rb,Rb]
        conc_ultimate_stress_trilin_curve_lt_40to75 = [0,0,-Rbt,-Rbt,-0.6*Rbt,0,0.6*Rb,Rb,Rb]
        conc_ultimate_stress_trilin_curve_lt_75up = [0,0,-Rbt,-Rbt,-0.6*Rbt,0,0.6*Rb,Rb,Rb]
        conc_ultimate_stress_trilin_curve_st = [0,0,-Rbt,-Rbt,-0.6*Rbt,0,0.6*Rb,Rb,Rb]

        conc_ultimate_stress_bilin_curve_lt_to40 = [0,0,-Rbt,-Rbt,0,Rb,Rb]
        conc_ultimate_stress_bilin_curve_lt_40to75 = [0,0,-Rbt,-Rbt,0,Rb,Rb]
        conc_ultimate_stress_bilin_curve_lt_75up = [0,0,-Rbt,-Rbt,0,Rb,Rb]
        conc_ultimate_stress_bilin_curve_st = [0,0,-Rbt,-Rbt,0,Rb,Rb]

        if conc_diag_type == "Двухлинейная":
            if load_type == "Кратковременная":
                conc_service_strain = conc_service_strain_bilin_curve_st
                conc_service_stress = conc_service_stress_bilin_curve_st
                conc_ultimate_strain = conc_ultimate_strain_bilin_curve_st
                conc_ultimate_stress = conc_ultimate_stress_bilin_curve_st
            elif load_type == "Длительная":
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
        elif conc_diag_type == "Трехлинейная":
            if load_type == "Кратковременная":
                conc_service_strain = conc_service_strain_trilin_curve_st
                conc_service_stress = conc_service_stress_trilin_curve_st
                conc_ultimate_strain = conc_ultimate_strain_trilin_curve_st
                conc_ultimate_stress = conc_ultimate_stress_trilin_curve_st
            elif load_type == "Длительная":
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
                     
                
        concrete_material = Concrete(
            name=conc_class,
            density=conc_density,
            stress_strain_profile=ssp.StressStrainProfile(conc_service_strain,conc_service_stress),
            ultimate_stress_strain_profile=ssp.StressStrainProfile(conc_ultimate_strain, conc_ultimate_stress),
            flexural_tensile_strength=Rbt,
            colour="lightgrey",
        )

        ssp_service = concrete_material.stress_strain_profile
        ssp_ultimate = concrete_material.ultimate_stress_strain_profile

        return concrete_material, ssp_service, ssp_ultimate
        
    
    

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