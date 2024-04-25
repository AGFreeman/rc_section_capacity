import streamlit as st
import plotly.graph_objects as go
import matplotlib as mpl
import rc_section_capacity_module as rcscm
from rc_section_capacity_module import (
    concrete_section_moment_curvature_analysis as _concrete_section_moment_curvature_analysis,
)

from concreteproperties.utils import AnalysisError
import pandas as pd
import numpy as np
import utils as ut

# TODO
# OPTIMIZATION
# Watch pfse lesson on optimization
# cProfile - standard library. Make .stat file - view with snakeviz
# Caching functions with lru_cache or streamlit stuff
# Multiprocess. Python standart library or streamlit?


# ======================== Global Streamlit Settings ========================

st.set_page_config(layout="wide")

COLOR = "white"
mpl.rcParams["text.color"] = COLOR
mpl.rcParams["axes.labelcolor"] = COLOR
mpl.rcParams["xtick.color"] = COLOR
mpl.rcParams["ytick.color"] = COLOR
mpl.rcParams["figure.edgecolor"] = "white"
mpl.rcParams["axes.edgecolor"] = "white"

# ======================== Global Streamlit Settings ========================


# =========================== Load External data ============================

conc_class_names = pd.read_excel("concrete.xlsx")["Class"]
rebar_class_names = pd.read_excel("rebar.xlsx")["Class"]
rebar_sizes = pd.read_excel("rebar_size.xlsx")["d"]

# =========================== Load External data ============================


# ============================ Input - Sidebar ==============================


# Forces
with st.sidebar.expander("Loads", True):
    # Converted to N and N*mm
    n = st.number_input("$N, kN$", value=1000, step=100) * 1000
    m_x = st.number_input("$M_{{x}},\,kN \cdot m$", value=100, step=100) * 1000 * 1000
    m_y = st.number_input("$M_{{y}},\,kN \cdot m$", value=0, step=100) * 1000 * 1000

    show_sign_convention = st.checkbox("Show sign convention")
    if show_sign_convention:
        st.image("sign_convention.png")

    load_type = st.selectbox("Load type", ["Transient", "Sustained"], 0)


# Materials
with st.sidebar.expander("Materials", True):
    col1, col2 = st.columns(2)

    with col1:
        conc_class = st.selectbox(
            "Concrete class",
            conc_class_names,
            8,
        )
        humidity = st.selectbox("Humidity, %", ["<40", "40-75", ">75"], 1)
    with col2:
        rebar_class = st.selectbox("Rebar class", rebar_class_names, 2)

    show_advanced_mat_data = st.checkbox("Advanced material data")

    if show_advanced_mat_data:
        conc_diag_type = st.selectbox(
            "Concrete curve type", ["Bilinear", "Trilinear"], 0
        )
        conc_tension = st.toggle("Concrete tension")
        show_diag = st.toggle("Show material curves")
    else:
        conc_diag_type = "Bilinear"
        conc_tension = False
        show_diag = False


# Section
with st.sidebar.expander("Section", True):
    sec_type = st.selectbox("Section type", ["Rectangular"], 0)
    if sec_type == "Rectangular":
        h = st.slider("Height, $mm$", 100, 3000, 600, 50)
        b = st.slider("Width, $mm$", 100, 3000, 300, 50)
with st.sidebar.expander("Reinforcement", True):
    if sec_type == "Rectangular":
        show_advanced_rebar_data = st.toggle("Advanced rebar data")

        if show_advanced_rebar_data:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("Top rebars")
                st.write("Size \u2300, $mm$")
                dr_top = st.select_slider(
                    "Top rebar",
                    rebar_sizes,
                    12,
                    label_visibility="collapsed",
                )
                st.write("Number")
                nr_top = st.slider(
                    "Top rebar number",
                    2,
                    20,
                    2,
                    label_visibility="collapsed",
                )
                st.write("Layers")
                nrl_top = st.slider(
                    "Top rebar layers",
                    0,
                    6,
                    1,
                    label_visibility="collapsed",
                )
                st.write("Layer spacing, $mm$")
                srl_top = st.slider(
                    "Top layer spacing",
                    30,
                    300,
                    30,
                    5,
                    label_visibility="collapsed",
                )
                st.write("Clear cover, $mm$")
                cc_top = st.slider(
                    "Top clear cover",
                    30,
                    100,
                    30,
                    5,
                    label_visibility="collapsed",
                )
            with col2:
                st.write("Side Rebars")
                st.write("Size \u2300, $mm$")
                dr_side = st.select_slider(
                    "Side rebar",
                    rebar_sizes,
                    12,
                    label_visibility="collapsed",
                )
                st.write("Number")
                nr_side = st.slider(
                    "Side rebar number",
                    2,
                    20,
                    2,
                    label_visibility="collapsed",
                )
                st.write("Layers")
                nrl_side = st.slider(
                    "Side rebar layers",
                    0,
                    6,
                    0,
                    label_visibility="collapsed",
                )
                st.write("Layer spacing, $mm$")
                srl_side = st.slider(
                    "Side layer spacing",
                    30,
                    100,
                    30,
                    5,
                    label_visibility="collapsed",
                )
                st.write("Clear cover, $mm$")
                cc_side = st.slider(
                    "Side clear cover",
                    30,
                    100,
                    30,
                    5,
                    label_visibility="collapsed",
                )
            with col3:
                st.write("Bottom rebars")
                st.write("Size \u2300, $mm$")
                dr_bot = st.select_slider(
                    "Bottom rebar",
                    rebar_sizes,
                    12,
                    label_visibility="collapsed",
                )
                st.write("Number")
                nr_bot = st.slider(
                    "Bottom rebar number",
                    2,
                    20,
                    2,
                    label_visibility="collapsed",
                )
                st.write("Layers")
                nrl_bot = st.slider(
                    "Bottom rebar layers",
                    0,
                    6,
                    1,
                    label_visibility="collapsed",
                )
                st.write("Layer spacing, $mm$")
                srl_bot = st.slider(
                    "Bottom layer spacing",
                    30,
                    300,
                    30,
                    5,
                    label_visibility="collapsed",
                )
                st.write("Clear cover, $mm$")
                cc_bot = st.slider(
                    "Bottom clear cover",
                    30,
                    100,
                    30,
                    5,
                    label_visibility="collapsed",
                )

        else:
            dr = st.select_slider("Size \u2300, $mm$", rebar_sizes, 12)
            nr = st.slider("No per side", 2, 20, 2)
            cc = st.slider("Clear cover, $mm$", 30, 100, 30, 5)

            dr_top = dr
            nr_top = nr
            nrl_top = 1
            srl_top = 0
            cc_top = cc

            dr_bot = dr
            nr_bot = nr
            nrl_bot = 1
            srl_bot = 0
            cc_bot = cc

            dr_side = dr
            nr_side = nr
            nrl_side = 1
            srl_side = 0
            cc_side = cc


# ============================ Input - Sidebar ==============================


# ================================ Output ===================================

# Heading
st.write(
    """
        <div style="text-align:center">
            <h1>Reinforced Concrete Section Analysis</h1>
        </div>
    """,
    unsafe_allow_html=True,
)

# Warning in case no reinforcement
if nrl_top == 0 and nrl_bot == 0 and nrl_side == 0:
    st.warning("Please specify at least one layer of reinforcement", icon="⚠️")
else:
    # Basic Results

    # Create concrete material
    # No density input - add later
    service_conc_mat, ultimate_conc_mat, conc_ssp_plot = rcscm.define_concrete_material(
        c_class=conc_class,
        diag_type=conc_diag_type,
        load_type=load_type,
        conc_tension=conc_tension,
        humidity=humidity,
    )

    # Craeate rebar material
    # No density input - add later
    service_rebar_mat, ultimate_rebar_mat, rebar_ssp_plot = rcscm.define_rebar_material(
        r_class=rebar_class, load_type=load_type
    )

    # # TODO
    # # Ultimate concrete used only!!!!
    # # Add section type selector and functions for other section types in main module

    # Create section
    if sec_type == "Rectangular":
        if nrl_top > 0 or nrl_bot > 0 or nrl_side > 0:
            sec_ult, sec_img = rcscm.create_rectangular_section(
                h=h,
                b=b,
                c_mat=ultimate_conc_mat,
                r_mat=ultimate_rebar_mat,
                dr_top=dr_top,
                nr_top=nr_top,
                nrl_top=nrl_top,
                srl_top=srl_top,
                cc_top=cc_top,
                dr_bot=dr_bot,
                nr_bot=nr_bot,
                nrl_bot=nrl_bot,
                srl_bot=srl_bot,
                cc_bot=cc_bot,
                dr_side=dr_side,
                nr_side=nr_side,
                nrl_side=nrl_side,
                srl_side=srl_side,
                cc_side=cc_side,
            )

    # Caclulate section properties
    (
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
    ) = rcscm.concrete_section_properties(sec=sec_ult, c_mat=ultimate_conc_mat)

    # Write the results
    st.write(
        """
        <div style="border: 4px solid #4CAF50; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 20px;">
            <h2>Basic Results</h2>
        </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    # Dispay section properties table
    with col1:
        sec_prop_data = {
            "Mass": ["{:.0f}".format(unit_mass * 1000), "kg/m"],
            "Gross Area": ["{:.0f}".format(a_gr / 100), "cm^2"],
            "Concrete area": ["{:.0f}".format(a_conc / 100), "cm^2"],
            "Reinforcement area": [
                "{:.2f}".format(a_rebar / 100),
                "cm^2",
                "{:.2f}%".format(a_rebar / a_gr * 100),
            ],
            "Ix uncracked": ["{:.0f}".format(i_xx_c_uncr / 10000), "cm^4"],
            "Iy uncracked": ["{:.0f}".format(i_yy_c_uncr / 10000), "cm^4"],
            "Ix+ cracked": [
                "{:.0f}".format(i_xx_pos_c_cr / 10000),
                "cm^4",
                "{:.2f}%".format(i_xx_pos_c_cr / i_xx_c_uncr * 100),
            ],
            "NA depth x+": ["{:.2f}".format(d_x_pos / 10), "cm"],
            "Ix- cracked": [
                "{:.0f}".format(i_xx_neg_c_cr / 10000),
                "cm^4",
                "{:.2f}%".format(i_xx_neg_c_cr / i_xx_c_uncr * 100),
            ],
            "NA depth x-": ["{:.2f}".format(d_x_neg / 10), "cm"],
            "Iy cracked": [
                "{:.0f}".format(i_yy_pos_c_cr / 10000),
                "cm^4",
                "{:.2f}%".format(i_yy_pos_c_cr / i_yy_c_uncr * 100),
            ],
            "NA depth y": ["{:.2f}".format(d_y_pos / 10), "cm"],
        }

        html_table_sec_prop = (
            "<div style='overflow-x: auto;'>\n"
            "    <table style='width:100%;text-align:center;border-collapse: collapse; border: 4px solid #444; border-radius: 10px;'>\n"
            "        <tr>\n"
            "            <th colspan='4' style='border: 4px solid #444; font-size: 18pt;'>Section Properties</th>\n"
            "        </tr>\n"
            "        <tr>\n"
            "            <th style='border: 4px solid #444; font-size: 16pt;'>Parameter</th>\n"
            "            <th style='border: 4px solid #444; font-size: 16pt;'>Value</th>\n"
            "            <th style='border: 4px solid #444; font-size: 16pt;'>Units</th>\n"
            "            <th style='border: 4px solid #444; font-size: 16pt;'></th>\n"
            "        </tr>\n"
        )

        for param, values in sec_prop_data.items():
            value = values[0]
            units = values[1]
            if "^" in units:
                units, superscript = units.split("^")
                units = f"{units}<sup>{superscript}</sup>"
            additional = values[2] if len(values) > 2 else ""
            html_table_sec_prop += (
                f"<tr>\n"
                f"    <td style='text-align:right;padding: 2px;padding-right: 5px;border: 2px solid #444; font-size: 14pt;'>{param}</td>\n"
                f"    <td style='padding: 2px;border: 2px solid #444; font-size: 14pt;'>{value}</td>\n"
                f"    <td style='padding: 2px;border: 2px solid #444; font-size: 14pt;'>{units}</td>\n"
                f"    <td style='padding: 2px;border: 2px solid #444; font-size: 14pt;'>{additional}</td>\n"
                f"</tr>\n"
            )
        html_table_sec_prop += "</table></div>"

        st.write(html_table_sec_prop, unsafe_allow_html=True)

    # Display section
    with col2:
        st.image(sec_img, use_column_width="auto")

    # Calculate moment capacities and neutral axis angle
    with col3:
        cap_flag = 0
        try:
            (m_theta, m_xy, mu_xy, mu_xy_n0, mu_x_pos_n0, mu_x_neg_n0, mu_y_pos_n0) = (
                rcscm.concrete_section_capacity(sec=sec_ult, n=n, m_x=m_x, m_y=m_y)
            )
            cap_flag = 1
        except AnalysisError:
            st.warning("Axial capacity exceeded. Reduce N", icon="⚠️")

        # If analysis succeded calculate axial capacities
        if cap_flag == 1:
            # Calculate moment interaction diagram
            mi_res, mi_img = rcscm.concrete_section_moment_interaction_diagram(
                sec=sec_ult,
                m_theta=m_theta,
            )

            # Calculate axial capacities
            mi_points = mi_res.get_results_lists("m_xy")
            nu_max = mi_points[0][0]
            m_xy_nu_max = mi_points[1][0]
            nu_min = mi_points[0][-1]
            m_xy_nu_min = mi_points[1][-1]

            # Display capacities table
            m_theta_deg = "{:.1f}".format(np.degrees(m_theta))
            sec_capacity_data = {
                "θ": [m_theta_deg, "˚"],
                f"M": ["{:.0f}".format(m_xy / 1000 / 1000), "kNm"],
                f"Mu at θ={m_theta_deg}˚ and N={n/1000:.0f} kN": [
                    "{:.0f}".format(mu_xy / 1000 / 1000),
                    "kNm",
                    "{:.3f}".format(m_xy / mu_xy),
                ],
                f"Nu+ at θ={m_theta_deg}˚ and M={m_xy_nu_max/1000 /1000:.0f} kNm": [
                    "{:.0f}".format(nu_max / 1000),
                    "kN",
                    "{:.3f}".format(n / nu_max if n > 0 else 0),
                ],
                f"Nu- at θ={m_theta_deg}˚ and M={m_xy_nu_min/1000 /1000:.0f} kNm": [
                    "{:.0f}".format(nu_min / 1000),
                    "kN",
                    "{:.3f}".format(n / nu_min if n < 0 else 0),
                ],
                f"Mu at θ={m_theta_deg}˚ and N=0": [
                    "{:.0f}".format(mu_xy_n0 / 1000 / 1000),
                    "kNm",
                ],
                f"Mu at θ=0.0˚ and N=0": [
                    "{:.0f}".format(mu_x_pos_n0 / 1000 / 1000),
                    "kNm",
                ],
                f"Mu at θ=180.0˚ and N=0": [
                    "{:.0f}".format(mu_x_neg_n0 / 1000 / 1000),
                    "kNm",
                ],
                f"Mu at θ=90.0˚ and N=0": [
                    "{:.0f}".format(mu_y_pos_n0 / 1000 / 1000),
                    "kNm",
                ],
            }

            html_table_sec_cap = (
                "<div style='overflow-x: auto;'>\n"
                "    <table style='width:100%;text-align:center;border-collapse: collapse; border: 4px solid #444; border-radius: 10px;'>\n"
                "        <tr>\n"
                "            <th colspan='4' style='border: 4px solid #444; font-size: 18pt;'>Section Capacities</th>\n"
                "        </tr>\n"
                "        <tr>\n"
                "            <th style='border: 4px solid #444; font-size: 16pt;'>Parameter</th>\n"
                "            <th style='border: 4px solid #444; font-size: 16pt;'>Value</th>\n"
                "            <th style='border: 4px solid #444; font-size: 16pt;'>Units</th>\n"
                "            <th style='border: 4px solid #444; font-size: 16pt;'>D/C</th>\n"
                "        </tr>\n"
            )

            for param, values in sec_capacity_data.items():
                value = values[0]
                units = values[1]
                if "^" in units:
                    units, superscript = units.split("^")
                    units = f"{units}<sup>{superscript}</sup>"
                dc_ratio = values[2] if len(values) > 2 else ""

                # Apply style based on value
                try:
                    style = "color: red;" if float(dc_ratio) > 1 else "color: green;"
                except ValueError:
                    style = ""

                html_table_sec_cap += (
                    f"<tr>\n"
                    f"    <td style='text-align:right;padding: 2px;padding-right: 5px;border: 2px solid #444; font-size: 14pt;'>{param}</td>\n"
                    f"    <td style='padding: 2px;border: 2px solid #444; font-size: 14pt;'>{value}</td>\n"
                    f"    <td style='padding: 2px;border: 2px solid #444; font-size: 14pt;'>{units}</td>\n"
                    f"    <td style='padding: 2px;border: 2px solid #444; font-size: 14pt;{style}'>{dc_ratio}</td>\n"  # Apply style here
                    f"</tr>\n"
                )
            html_table_sec_cap += "</table></div>"

            st.write(html_table_sec_cap, unsafe_allow_html=True)

    # Display material diagrams
    col1, col2 = st.columns(2)
    if show_diag:
        with col1:
            st.plotly_chart(conc_ssp_plot, True)
        with col2:
            st.plotly_chart(rebar_ssp_plot, True)

    # Advanced Results

    if cap_flag == 1:
        # Use custom hash function for a combination of parameters
        # on which ConcreteSection object depends since ConcreteSecion
        # is a custom object that cannon be hashed
        if sec_type == "Rectangular":
            sec_hash = ut.generate_hash_rect_sec(
                h,
                b,
                dr_top,
                nr_top,
                nrl_top,
                srl_top,
                cc_top,
                dr_bot,
                nr_bot,
                nrl_bot,
                srl_bot,
                cc_bot,
                dr_side,
                nr_side,
                nrl_side,
                srl_side,
                cc_side,
                conc_class,
                humidity,
                conc_diag_type,
                conc_tension,
                rebar_class,
                load_type,
            )

        # Cache moment curvature analysis results exculding sec: ConcreteSecion object but using sec_hash
        @st.cache_data
        def concrete_section_moment_curvature_analysis(_sec, sec_hash, n, m_theta):
            return _concrete_section_moment_curvature_analysis(_sec, n, m_theta)

        # Calculate moment curvature
        mc_res, mc_img = concrete_section_moment_curvature_analysis(
            _sec=sec_ult, sec_hash=sec_hash, n=n, m_theta=m_theta
        )

        # Calculate moment interaction diagram
        mi_res, mi_img = rcscm.concrete_section_moment_interaction_diagram(
            sec=sec_ult, m_theta=m_theta
        )

        # Cap moment at mu_xy or last m at mc_res for stress display
        cap_m_flag = 1
        m_cap = min(mu_xy, mc_res.m_xy[-1])
        if m_xy > m_cap:
            cap_m_flag = 0
            m_xy = m_cap

        # Calculate section stresses
        sec_stress_img = rcscm.concrete_section_stress_analysis(
            sec=sec_ult, mc_res=mc_res, m=m_xy
        )

        # Calculate biaxial moment diagram
        bb_res, bb_img = rcscm.concrete_section_biaxial_moment_diagram(sec=sec_ult, n=n)

        st.write(
            """
            <div style="border: 4px solid #FFC0CB; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 20px;">
                <h2>Advanced Results</h2>
            </div>
        """,
            unsafe_allow_html=True,
        )

        # Rerun only part of the script to display plot
        @st.experimental_fragment
        def fragment_display_stress_plot():
            # Check button is in session state. Set button state to False
            if "section_stress_button_clicked" not in st.session_state:
                st.session_state.section_stress_button_clicked = False

            # Function to be called on click. Reverses button state
            def click_button():
                st.session_state.section_stress_button_clicked = (
                    not st.session_state.section_stress_button_clicked
                )

            st.button("Section Stress", use_container_width=True, on_click=click_button)

            # Display image if state is true
            if st.session_state.section_stress_button_clicked:
                st.image(sec_stress_img, use_column_width=True)

        # Rerun only part of the script to display plot
        @st.experimental_fragment
        def fragment_display_mc_plot():
            # Check button is in session state. Set button state to False
            if "mc_curve_button_clicked" not in st.session_state:
                st.session_state.mc_curve_button_clicked = False

            # Function to be called on click. Reverses button state
            def click_button():
                st.session_state.mc_curve_button_clicked = (
                    not st.session_state.mc_curve_button_clicked
                )

            st.button(
                "Moment-Curvature", use_container_width=True, on_click=click_button
            )

            # Display image if state is true
            if st.session_state.mc_curve_button_clicked:
                st.image(mc_img, use_column_width=True)

        # Rerun only part of the script to display plot
        @st.experimental_fragment
        def fragment_display_mi_plot():
            # Check button is in session state. Set button state to False
            if "mi_curve_button_clicked" not in st.session_state:
                st.session_state.mi_curve_button_clicked = False

            # Function to be called on click. Reverses button state
            def click_button():
                st.session_state.mi_curve_button_clicked = (
                    not st.session_state.mi_curve_button_clicked
                )

            st.button(
                "Moment Intraction", use_container_width=True, on_click=click_button
            )

            # Display image if state is true
            if st.session_state.mi_curve_button_clicked:
                st.image(mi_img, use_column_width=True)

        # Rerun only part of the script to display plot
        @st.experimental_fragment
        def fragment_display_bb_plot():
            # Check button is in session state. Set button state to False
            if "bb_curve_button_clicked" not in st.session_state:
                st.session_state.bb_curve_button_clicked = False

            # Function to be called on click. Reverses button state
            def click_button():
                st.session_state.bb_curve_button_clicked = (
                    not st.session_state.bb_curve_button_clicked
                )

            st.button("Biaxial Moment", use_container_width=True, on_click=click_button)

            # Display image if state is true
            if st.session_state.bb_curve_button_clicked:
                st.image(bb_img, use_column_width=True)

        col1, col2 = st.columns(2)

        with col1:
            # Display section stresses
            fragment_display_stress_plot()
            if cap_m_flag == 0:
                st.warning(
                    "Moment capacity exceeded. Showing results for Mu",
                    icon="⚠️",
                )
        # Display moment curvature plot
        with col2:
            fragment_display_mc_plot()

        col1, col2 = st.columns(2)
        # Display section stresses
        with col1:
            fragment_display_mi_plot()
        with col2:
            fragment_display_bb_plot()

    # # ================================ Output ===================================
