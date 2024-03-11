import streamlit as st
import plotly.graph_objects as go
import rc_section_capacity_module as rcscm

st.write("# Rectangular RC section M-N curve")

# # Materials
# st.sidebar.subheader("Materials")
# conc_str = st.sidebar.number_input("Concrete strength ($MPa$)", value = 30.000, step = 1.0)
# rebar_str = st.sidebar.number_input("Rebar strength ($MPa$)", value = 400)

# Forces
# st.sidebar.subheader("Forces")
# N = st.sidebar.number_input("Axial force ($N$)", value = 800000, step = 10000)
# M = st.sidebar.number_input("Rebar strength ($Nmm$)", value = 10000000, step = 10000)

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

sec, sec_fig, int_diag = rcscm.concrete_section_analysis(height, width, trn, trd, trcc, brn, brd, brcc)

st.pyplot(sec_fig.figure)
st.pyplot(int_diag.figure)
