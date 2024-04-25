import streamlit as st
import plotly.graph_objects as go
import rc_section_capacity_module as rcscm
import pandas as pd


# ----- Global Streamlit Settings -----

st.set_page_config(layout="wide")

# ----- Global Streamlit Settings -----


# ----- Load External data -----

conc_class_names = pd.read_excel("concrete.xlsx")["Class"]
rebar_class_names = pd.read_excel("rebar.xlsx")["Class"]
rebar_sizes = pd.read_excel("rebar_size.xlsx")["d"]

# ----- Load External data -----


# ----- Input - Sidebar -----

# Forces
st.sidebar.subheader("Forces")
N = st.sidebar.number_input("Axial force ($N$)", value=800000, step=10000)
M = st.sidebar.number_input("Moment ($Nmm$)", value=10000000, step=10000)
load_type = st.sidebar.selectbox("Тип нагрузки", ["Кратковременная", "Длительная"], 0)

# Materials
st.sidebar.subheader("Материалы")
st.sidebar.subheader("Бетон")
conc_class = st.sidebar.selectbox(
    "Класс бетона",
    conc_class_names,
    8,
)
conc_diag_type = st.sidebar.selectbox(
    "Тип диаграммы бетона", ["Двухлинейная", "Трехлинейная"], 0
)
no_tension = st.sidebar.toggle("Не учитывать растяжение")
humidity = st.sidebar.selectbox("Влажность, %", ["<40", "40-75", ">75"], 1)

st.sidebar.subheader("Арматура")
rebar_class = st.sidebar.selectbox("Класс арматуры", rebar_class_names, 2)

show_diag = st.sidebar.toggle("Показать диаграммы материалов")

# Section
st.sidebar.subheader("Section")
st.sidebar.subheader("Dimensions")
h = st.sidebar.slider("Height ($mm$)", 100, 3000, 1000, 50)
b = st.sidebar.slider("Width ($mm$)", 100, 3000, 1000, 50)

st.sidebar.subheader("Top Rebars")
nrc_top = st.sidebar.slider("Top rebars", 0, 20, 1)
nrr_top = st.sidebar.slider("Top rebars row", 0, 6, 1)
dr_top = st.sidebar.select_slider("Top rebar \u2300 ($mm$)", rebar_sizes)
srr_top = st.sidebar.slider("Top row spacing ($mm$)", 10, 100, 30, 5)
cc_top = st.sidebar.slider("Top clear cover ($mm$)", 10, 100, 30, 5)

st.sidebar.subheader("Bottom Rebars")
nrc_bot = st.sidebar.slider("Bottom rebars", 0, 20, 2)
nrr_bot = st.sidebar.slider("Bottom rebars row", 0, 6, 1)
dr_bot = st.sidebar.select_slider("Bottom rebar \u2300 ($mm$)", rebar_sizes)
srr_bot = st.sidebar.slider("Bottom row spacing ($mm$)", 10, 100, 30, 5)
cc_bot = st.sidebar.slider("Bottom clear cover ($mm$)", 10, 100, 30, 5)

st.sidebar.subheader("Side Rebars")
nrc_side = st.sidebar.slider("Side rebars", 0, 20, 2)
nrr_side = st.sidebar.slider("Side rebars row", 0, 6, 1)
dr_side = st.sidebar.select_slider("Side rebar \u2300 ($mm$)", rebar_sizes)
src_side = st.sidebar.slider("Side column spacing ($mm$)", 10, 100, 30, 5)
srr_side = st.sidebar.slider("Side row spacing ($mm$)", 10, 100, 30, 5)
cc_side = st.sidebar.slider("Side clear cover ($mm$)", 10, 100, 30, 5)

# ----- Input - Sidebar -----


# ----- Engine -----

# No density input - add later
service_conc_mat, ultimate_conc_mat, conc_ssp_plot = rcscm.define_concrete_material(
    c_class=conc_class,
    diag_type=conc_diag_type,
    load_type=load_type,
    conc_tension=no_tension,
    humidity=humidity,
)

# No density input - add later
service_rebar_mat, ultimate_rebar_mat, rebar_ssp_plot = rcscm.define_rebar_material(
    r_class=rebar_class, load_type=load_type
)

# TODO
# Ultimate concrete used only!!!!
# Add section type selector and functions for other section types in main module

sec, fig = rcscm.create_rectangular_section(
    h=h,
    b=b,
    c_mat=ultimate_conc_mat,
    nr_top=nrc_top,
    nrl_top=nrr_top,
    dr_top=dr_top,
    srl_top=srr_top,
    cc_top=cc_top,
    nr_bot=nrc_bot,
    nrl_bot=nrr_bot,
    dr_bot=dr_bot,
    srl_bot=srr_bot,
    cc_bot=cc_bot,
    r_mat=ultimate_rebar_mat,
    nrl_side=nrc_side,
    nr_side=nrr_side,
    dr_side=dr_side,
    srl_side=src_side,
    sr_side=srr_side,
    cc_side=cc_side,
)

# ----- Engine -----


# ----- Output -----

st.write(
    """
    <div style="text-align:center">
        <h1>Расчет железобетенных сечений</h1>
    </div>
""",
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)


if show_diag:
    with col1:
        st.plotly_chart(conc_ssp_plot, True)
    with col2:
        st.plotly_chart(rebar_ssp_plot, True)

st.plotly_chart(
    fig,
    True,
)

# int_diag = rcscm.concrete_section_analysis(sec=sec, N=N, Mx=M)
mx_pos, mx_neg, my_pos, my_neg = rcscm.concrete_section_capacity(sec=sec, n=N)


# st.pyplot(int_diag.figure)

ult_res = {
    "Factor": [
        f"$$M_{{x-}},\,N \cdot mm$$",
        f"$$M_{{x+}},\,N \cdot mm$$",
        f"$$M_{{y+}},\,N \cdot mm$$",
        f"$$M_{{y-}},\,N \cdot mm$$",
    ],
    "Value": [mx_pos, mx_neg, my_pos, my_neg],
}

st.dataframe(ult_res)
# st.write(f"$M_{{x+}} = {mx_ult}\,N \cdot mm$")
# st.pyplot(stress_plot.figure)


# ----- Output -----
