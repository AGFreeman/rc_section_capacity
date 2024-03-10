import streamlit as st
import plotly.graph_objects as go
from eng_module import utils as ut
import rc_section_capacity_module as rcscm

st.write("# Ulimate moment capacity of a rectangular RC section")

conc_mat_data = ut.read_csv_file("concrete.csv")
rebar_mat_data = ut.read_csv_file("rebar.csv")

conc_mat_names = []
for dataline in conc_mat_data[1:]:
    conc_mat_names.append(dataline[0])

rebar_mat_names = []
for dataline in rebar_mat_data[1:]:
    rebar_mat_names.append(dataline[0])

# Forces
st.sidebar.subheader("Forces")
N = st.sidebar.number_input("Axial force ($N$)", value = 800000, step = 10000)
M = st.sidebar.number_input("Rebar strength ($Nmm$)", value = 10000000, step = 10000)
load_type = st.sidebar.selectbox("Тип нагрузки", ["Кратковременная","Длительная"], 0)


# Materials
st.sidebar.subheader("Материалы")
st.sidebar.subheader("Бетон")
conc_class = st.sidebar.selectbox("Класс бетона", conc_mat_names, 8)
conc_diag_type = st.sidebar.selectbox("Тип диаграммы бетона", ['Двухлинейная','Трехлинейная'], 0)
humidity = st.sidebar.selectbox("Влажность, %", ["<40","40-75",">70"], 1)

st.sidebar.subheader("Арматура")
st.sidebar.selectbox("Класс арматуры", rebar_mat_names, 2)
st.sidebar.selectbox("Тип диаграммы арматуры", ['Двухлинейная','Трехлинейная'], 0)

# No density input - add later
concrete_mat, conc_service_ssp, conc_ultimate_ssp = rcscm.define_concrete_material(conc_class=conc_class,conc_diag_type=conc_diag_type,load_type=load_type,humidity=humidity)

show_conc_diag = st.sidebar.toggle("Показать диаграммы бетона")

if show_conc_diag:
    st.pyplot(conc_service_ssp.figure)




# conc_str = st.sidebar.number_input("Concrete strength ($MPa$)", value = 30.000, step = 1.0)
# rebar_str = st.sidebar.number_input("Rebar strength ($MPa$)", value = 400)

# Section
st.sidebar.subheader("Section")
st.sidebar.subheader("Dimensions")
height = st.sidebar.slider("Height ($mm$)", 100, 3000, 1000, 50)
width = st.sidebar.slider("Width ($mm$)", 100, 3000, 1000, 50)
st.sidebar.subheader("Top Rebars")
trn = st.sidebar.slider("Top rebars", 0, 20, 2)
trd = st.sidebar.slider("Top rebar \u2300 ($mm$)", 0, 20, 2)
trcc = st.sidebar.slider("Top clear cover ($mm$)", 10, 100, 30, 5)
st.sidebar.subheader("Bottom Rebars")
brn = st.sidebar.slider("Bottom rebars", 0, 20, 2)
brd = st.sidebar.slider("Bottom rebar \u2300 ($mm$)", 0, 20, 2)
brcc = st.sidebar.slider("Bottom clear cover ($mm$)", 10, 100, 30, 5)

sec, sec_fig, int_diag = rcscm.concrete_section_analysis(height, width, trn, trd, trcc, brn, brd, brcc, N, M)

st.pyplot(sec_fig.figure)
st.pyplot(int_diag.figure)
