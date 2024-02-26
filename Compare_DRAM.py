
import streamlit as st
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
from io import BytesIO
from collections import OrderedDict

st.set_page_config(layout="wide")
@st.cache_data
def read_DRAM(uploadFile):
    B = uploadFile.getvalue()
    A = BytesIO(B);
    #C = pd.ExcelFile(A)
    #D = list(C.sheet_names);
    E = pd.read_excel(A,sheet_name='Info');
    DRAM=E.iloc[5,3]
    return DRAM
@st.cache_data
def read_Project(uploadFile):
    B = uploadFile.getvalue()
    A = BytesIO(B);
    #C = pd.ExcelFile(A)
    #D = list(C.sheet_names);
    E = pd.read_excel(A,sheet_name='Info');
    Project=E.iloc[0,3]
    return Project
@st.cache_data
def read_Freq(uploadFile):
    B = uploadFile.getvalue()
    A = BytesIO(B);
    C = pd.ExcelFile(A)
    D = list(C.sheet_names);
    #E = pd.read_excel(A,sheet_name='Info');
    return D
@st.cache_data
def read_Data(uploadFile,Freq,Vendor,Proj_name):
    B = uploadFile.getvalue()
    A = BytesIO(B);
    C = pd.ExcelFile(A)
    D = list(C.sheet_names);
    E = pd.read_excel(A, sheet_name='Info');
    DRAM = E.iloc[5, 3]
    Project_name = E.iloc[0, 3]
    if DRAM==Vendor and Project_name==Proj_name:
        E = pd.read_excel(A,sheet_name=Freq);
        return E
    else:
        return

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a Summary Result",
        ("Scenario_Compare", "Compare_Total_Die","Compare_Power Domain","VDD2H VS VDD2L percentage")
    )
    if add_radio == "Compare_Total_Die":
        Plot_Y = st.text_input('Y axis', 100)
        Plot_X = st.text_input('X axis',1000)
    if add_radio == "Scenario_Compare":
        Screnario = st.sidebar.selectbox('Select Screnario', ('Light load for DOU','Medium load for DOU, VR Camera..','Heavy load for game','User Manual'));
        if Screnario=='User Manual':
            DOU = st.text_input('MB/s', 300)
    if add_radio == "VDD2H VS VDD2L percentage":
        DOU = st.text_input('MB/s', 76800)
    if add_radio == "Compare_Power Domain":
        Plot_Y = st.text_input('Y axis', 10)
        Plot_X = st.text_input('X axis', 1000)
    #iterations = st.slider("Current(mA)", 0, 3000,(0, 3000))
    #separation = st.slider("BW(MB/s)", 0, 76800,(0, 76800))

meaFiles=st.file_uploader('Choose Measure file',accept_multiple_files=True,type=['xlsx','xlsm'])

DRAM=[]
Speed=[]
Project=[]
Projects=[]
Total_speed=[]
if len(meaFiles) != 0:
    print(meaFiles)
    for meaFile in meaFiles:
        DRAM.append(read_DRAM(meaFile))
        Project.append(read_Project(meaFile))
        Projects=OrderedDict.fromkeys(Project)
        Speed.extend(read_Freq(meaFile))
        Total_speed=list(set(Speed))
        Total_speed.remove("Info")
        Total_speed=sorted(Total_speed,key=len)
    if Projects is not None:
        Project_List = st.sidebar.multiselect('Select Project', Projects);
        #st.write(Project_List)
    else:
        Project_List = []
    if add_radio == "Compare_Total_Die":
        if Total_speed is not None:
            DRAM_SPEED = st.sidebar.multiselect('Select Speed Sheets', Total_speed);
            #st.write(DRAM_SPEED)
        else:
            DRAM_SPEED = []
    elif add_radio == "Scenario_Compare":
        if Screnario=='Light load for DOU':
            DRAM_SPEED = st.sidebar.multiselect('Select Speed Sheets', ('752M','1536M'));
        elif Screnario=='Medium load for DOU, VR Camera..':
            DRAM_SPEED = st.sidebar.multiselect('Select Speed Sheets', ('3088M','4208M'));
        elif Screnario=='Heavy load for game':
            DRAM_SPEED = st.sidebar.multiselect('Select Speed Sheets', ('5480M','6368M_LP'));
        elif Screnario=='User Manual':
            DRAM_SPEED = st.sidebar.multiselect('Select Speed Sheets', Total_speed);
    elif add_radio == "VDD2H VS VDD2L percentage":
        if Total_speed is not None:
            DRAM_SPEED = st.sidebar.multiselect('Select Speed Sheets', Total_speed);
            #st.write(DRAM_SPEED)
        else:
            DRAM_SPEED = []
    elif add_radio == "Compare_Power Domain":
        if Total_speed is not None:
            DRAM_SPEED = st.sidebar.multiselect('Select Speed Sheets', Total_speed);
            Power_domain = st.sidebar.selectbox('Select Power Domain', ('VDDQ(mA)', 'VDD2H(mA)','VDD2L(mA)','VDD1(mA)'));
            #st.write(DRAM_SPEED)
        else:
            DRAM_SPEED = []
    if add_radio == "VDD2H VS VDD2L percentage":
        if DRAM is not None:
            DRAM_List = st.sidebar.multiselect('Select Single DRAM', DRAM);
            #st.write(DRAM_List)
        else:
            DRAM_List = []
    else:
        if DRAM is not None:
            DRAM_List = st.sidebar.multiselect('Select DRAM', DRAM);
            #st.write(DRAM_List)
        else:
            DRAM_List = []

    fig = go.Figure();fig1 = go.Figure();fig2 = go.Figure();fig3 = go.Figure();fig4 = go.Figure();fig5 = go.Figure();fig6 = go.Figure();fig7 = go.Figure();fig8 = go.Figure();fig9 = go.Figure()
    figure1=0;figure2=0;figure3=0;figure4=0;figure5=0;figure6=0;figure=0;figure7=0;figure8=0;figure9=0

    for DRAM_Vendor in DRAM_List:
        for DRAM_Freq in DRAM_SPEED:
            for Project_name in Project_List:
                for meaFile in meaFiles:
                    Raw_data=read_Data(meaFile,DRAM_Freq,DRAM_Vendor,Project_name)
                    if Raw_data is not None:
                        #st.write(Raw_data)
                        if add_radio == "Compare_Total_Die":
                            if int(''.join(filter(str.isdigit, DRAM_Freq))) > 3200:
                                VDDQ=Raw_data['VDDQ(mA)']*0.5
                                VDD2H=Raw_data['VDD2H(mA)']*1.05
                                VDD2L=Raw_data['VDD2L(mA)']*0.9
                                VDD1=Raw_data['VDD1(mA)']*1.8
                                Raw_data['DRAM Die Total(mW)']=VDDQ+VDD2H+VDD2L+VDD1
                                #st.write(Raw_data)
                            else:
                                VDDQ=Raw_data['VDDQ(mA)']*0.3
                                VDD2H=Raw_data['VDD2H(mA)']*1.05
                                VDD2L=Raw_data['VDD2L(mA)']*0.9
                                VDD1=Raw_data['VDD1(mA)']*1.8
                                Raw_data['DRAM Die Total(mW)'] = VDDQ + VDD2H + VDD2L + VDD1
                            fig.add_trace(go.Scatter(x=Raw_data["MB/s"], y=Raw_data["DRAM Die Total(mW)"], mode='lines+markers', name=Project_name+"_"+DRAM_Vendor+"_"+DRAM_Freq))
                        elif add_radio == "Scenario_Compare":
                            if int(''.join(filter(str.isdigit, DRAM_Freq))) > 3200:
                                VDDQ = Raw_data['VDDQ(mA)'] * 0.5
                                VDD2H = Raw_data['VDD2H(mA)'] * 1.05
                                VDD2L = Raw_data['VDD2L(mA)'] * 0.9
                                VDD1 = Raw_data['VDD1(mA)'] * 1.8
                                Raw_data['DRAM Die Total(mW)'] = VDDQ + VDD2H + VDD2L + VDD1
                                # st.write(Raw_data)
                            else:
                                VDDQ = Raw_data['VDDQ(mA)'] * 0.3
                                VDD2H = Raw_data['VDD2H(mA)'] * 1.05
                                VDD2L = Raw_data['VDD2L(mA)'] * 0.9
                                VDD1 = Raw_data['VDD1(mA)'] * 1.8
                                Raw_data['DRAM Die Total(mW)'] = VDDQ + VDD2H + VDD2L + VDD1
                            if int(''.join(filter(str.isdigit, DRAM_Freq))) <= 800:
                                if Screnario == 'User Manual':
                                    index=np.searchsorted(Raw_data["MB/s"], int(DOU))
                                else:
                                    index = np.searchsorted(Raw_data["MB/s"], 300)
                                fig1.update_layout(title=f"DDR {DRAM_Freq}")
                                fig1.add_trace(
                                    go.Bar(x=[Raw_data["MB/s"][index]], y=[Raw_data["DRAM Die Total(mW)"][index]],
                                           name=Project_name + "_" + DRAM_Vendor + "_" + DRAM_Freq))
                                figure1=1
                            elif int(''.join(filter(str.isdigit, DRAM_Freq))) <= 1600:
                                if Screnario == 'User Manual':
                                    index = np.searchsorted(Raw_data["MB/s"], int(DOU))
                                else:
                                    index = np.searchsorted(Raw_data["MB/s"], 1200)
                                fig2.update_layout(title=f"DDR {DRAM_Freq}")
                                fig2.add_trace(
                                    go.Bar(x=[Raw_data["MB/s"][index]], y=[Raw_data["DRAM Die Total(mW)"][index]],
                                           name=Project_name + "_" + DRAM_Vendor + "_" + DRAM_Freq))
                                figure2 = 1
                            elif int(''.join(filter(str.isdigit, DRAM_Freq))) <= 2133:
                                if Screnario == 'User Manual':
                                    index = np.searchsorted(Raw_data["MB/s"], int(DOU))

                                fig7.update_layout(title=f"DDR {DRAM_Freq}")
                                fig7.add_trace(
                                    go.Bar(x=[Raw_data["MB/s"][index]], y=[Raw_data["DRAM Die Total(mW)"][index]],
                                           name=Project_name + "_" + DRAM_Vendor + "_" + DRAM_Freq))
                                figure7 = 1
                            elif int(''.join(filter(str.isdigit, DRAM_Freq))) <= 3200:
                                if Screnario == 'User Manual':
                                    index = np.searchsorted(Raw_data["MB/s"], int(DOU))
                                else:
                                    index = np.searchsorted(Raw_data["MB/s"], 2400)
                                fig3.update_layout(title=f"DDR {DRAM_Freq}")
                                fig3.add_trace(
                                    go.Bar(x=[Raw_data["MB/s"][index]], y=[Raw_data["DRAM Die Total(mW)"][index]],
                                           name=Project_name + "_" + DRAM_Vendor + "_" + DRAM_Freq))
                                figure3 = 1
                            elif int(''.join(filter(str.isdigit, DRAM_Freq))) <= 4266:
                                if Screnario == 'User Manual':
                                    index = np.searchsorted(Raw_data["MB/s"], int(DOU))
                                else:
                                    index = np.searchsorted(Raw_data["MB/s"], 6700)
                                fig4.update_layout(title=f"DDR {DRAM_Freq}")
                                fig4.add_trace(
                                    go.Bar(x=[Raw_data["MB/s"][index]], y=[Raw_data["DRAM Die Total(mW)"][index]],
                                           name=Project_name + "_" + DRAM_Vendor + "_" + DRAM_Freq))
                                figure4 = 1
                            elif int(''.join(filter(str.isdigit, DRAM_Freq))) <= 5500:
                                if Screnario == 'User Manual':
                                    index = np.searchsorted(Raw_data["MB/s"], int(DOU))
                                else:
                                    index = np.searchsorted(Raw_data["MB/s"], 8700)
                                fig5.update_layout(title=f"DDR {DRAM_Freq}")
                                fig5.add_trace(
                                    go.Bar(x=[Raw_data["MB/s"][index]], y=[Raw_data["DRAM Die Total(mW)"][index]],
                                           name=Project_name + "_" + DRAM_Vendor + "_" + DRAM_Freq))
                                figure5 = 1
                            elif int(''.join(filter(str.isdigit, DRAM_Freq))) <= 6400:
                                if Screnario == 'User Manual':
                                    index = np.searchsorted(Raw_data["MB/s"], int(DOU))
                                else:
                                    index = np.searchsorted(Raw_data["MB/s"], 15300)
                                fig6.update_layout(title=f"DDR {DRAM_Freq}")
                                fig6.add_trace(
                                    go.Bar(x=[Raw_data["MB/s"][index]], y=[Raw_data["DRAM Die Total(mW)"][index]],
                                           name=Project_name + "_" + DRAM_Vendor + "_" + DRAM_Freq))
                                figure6 = 1
                            elif int(''.join(filter(str.isdigit, DRAM_Freq))) <= 7500:
                                if Screnario == 'User Manual':
                                    index = np.searchsorted(Raw_data["MB/s"], int(DOU))
                                    fig8.update_layout(title=f"DDR {DRAM_Freq}")
                                    fig8.add_trace(
                                        go.Bar(x=[Raw_data["MB/s"][index]], y=[Raw_data["DRAM Die Total(mW)"][index]],
                                               name=Project_name + "_" + DRAM_Vendor + "_" + DRAM_Freq))
                                figure8 = 1

                            elif int(''.join(filter(str.isdigit, DRAM_Freq))) <= 8533:
                                if Screnario == 'User Manual':
                                    index = np.searchsorted(Raw_data["MB/s"], int(DOU))
                                    fig9.update_layout(title=f"DDR {DRAM_Freq}")
                                    fig9.add_trace(
                                        go.Bar(x=[Raw_data["MB/s"][index]], y=[Raw_data["DRAM Die Total(mW)"][index]],
                                               name=Project_name + "_" + DRAM_Vendor + "_" + DRAM_Freq))
                                figure9 = 1
                            elif int(''.join(filter(str.isdigit, DRAM_Freq))) <= 9600:
                                if Screnario == 'User Manual':
                                    index = np.searchsorted(Raw_data["MB/s"], int(DOU))
                                    fig.update_layout(title=f"DDR {DRAM_Freq}")
                                    fig.add_trace(
                                        go.Bar(x=[Raw_data["MB/s"][index]], y=[Raw_data["DRAM Die Total(mW)"][index]],
                                               name=Project_name + "_" + DRAM_Vendor + "_" + DRAM_Freq))
                                figure = 1
                        elif add_radio == "VDD2H VS VDD2L percentage":
                            if int(''.join(filter(str.isdigit, DRAM_Freq))) > 3200:
                                VDDQ=Raw_data['VDDQ(mA)']*0.5
                                VDD2H=Raw_data['VDD2H(mA)']*1.05
                                VDD2L=Raw_data['VDD2L(mA)']*0.9
                                VDD1=Raw_data['VDD1(mA)']*1.8
                                Raw_data['DRAM Die Total(mW)']=VDDQ+VDD2H+VDD2L+VDD1
                                #st.write(Raw_data)
                            else:
                                VDDQ=Raw_data['VDDQ(mA)']*0.3
                                VDD2H=Raw_data['VDD2H(mA)']*1.05
                                VDD2L=Raw_data['VDD2L(mA)']*0.9
                                VDD1=Raw_data['VDD1(mA)']*1.8
                                Raw_data['DRAM Die Total(mW)'] = VDDQ + VDD2H + VDD2L + VDD1

                            if int(''.join(filter(str.isdigit, DRAM_Freq))) <= 800:
                                index = np.searchsorted(Raw_data["MB/s"], int(DOU))
                                VDD2H_P=VDD2H[index-1]/(VDD2H[index-1]+VDD2L[index-1])
                                VDD2L_P = VDD2L[index-1] / (VDD2H[index-1] + VDD2L[index-1])
                                if VDD2H_P >1:
                                    VDD2H_P=1
                                    VDD2L_P=0
                                fig1.update_layout(title=f"{DRAM_Vendor} @DDR{DRAM_Freq} ")
                                fig1.add_trace(
                                    go.Pie(labels=['VDD2H','VDD2L'], values=[VDD2H_P,VDD2L_P]))
                                figure1=1
                            elif int(''.join(filter(str.isdigit, DRAM_Freq))) <= 1600:
                                index = np.searchsorted(Raw_data["MB/s"], int(DOU))
                                VDD2H_P=VDD2H[index-1]/(VDD2H[index-1]+VDD2L[index-1])
                                VDD2L_P = VDD2L[index-1] / (VDD2H[index-1] + VDD2L[index-1])
                                if VDD2H_P >1:
                                    VDD2H_P=1
                                    VDD2L_P=0
                                fig2.update_layout(title=f"{DRAM_Vendor} @DDR{DRAM_Freq} ")
                                fig2.add_trace(
                                    go.Pie(labels=['VDD2H','VDD2L'], values=[VDD2H_P,VDD2L_P]))
                                figure2=1
                            elif int(''.join(filter(str.isdigit, DRAM_Freq))) <= 2133:
                                index = np.searchsorted(Raw_data["MB/s"], int(DOU))
                                VDD2H_P=VDD2H[index-1]/(VDD2H[index-1]+VDD2L[index-1])
                                VDD2L_P = VDD2L[index-1] / (VDD2H[index-1] + VDD2L[index-1])
                                if VDD2H_P >1:
                                    VDD2H_P=1
                                    VDD2L_P=0
                                fig3.update_layout(title=f"{DRAM_Vendor} @DDR{DRAM_Freq} ")
                                fig3.add_trace(
                                    go.Pie(labels=['VDD2H','VDD2L'], values=[VDD2H_P,VDD2L_P]))
                                figure3=1
                            elif int(''.join(filter(str.isdigit, DRAM_Freq))) <= 3200:
                                index = np.searchsorted(Raw_data["MB/s"], int(DOU))
                                VDD2H_P=VDD2H[index-1]/(VDD2H[index-1]+VDD2L[index-1])
                                VDD2L_P = VDD2L[index-1] / (VDD2H[index-1] + VDD2L[index-1])
                                if VDD2H_P >1:
                                    VDD2H_P=1
                                    VDD2L_P=0
                                fig4.update_layout(title=f"{DRAM_Vendor} @DDR{DRAM_Freq} ")
                                fig4.add_trace(
                                    go.Pie(labels=['VDD2H','VDD2L'], values=[VDD2H_P,VDD2L_P]))
                                figure4=1
                            elif int(''.join(filter(str.isdigit, DRAM_Freq))) <= 4266:
                                index = np.searchsorted(Raw_data["MB/s"], int(DOU))
                                VDD2H_P=VDD2H[index-1]/(VDD2H[index-1]+VDD2L[index-1])
                                VDD2L_P = VDD2L[index-1] / (VDD2H[index-1] + VDD2L[index-1])
                                if VDD2H_P >1:
                                    VDD2H_P=1
                                    VDD2L_P=0
                                fig5.update_layout(title=f"{DRAM_Vendor} @DDR{DRAM_Freq} ")
                                fig5.add_trace(
                                    go.Pie(labels=['VDD2H','VDD2L'], values=[VDD2H_P,VDD2L_P]))
                                figure5=1
                            elif int(''.join(filter(str.isdigit, DRAM_Freq))) <= 5500:
                                index = np.searchsorted(Raw_data["MB/s"], int(DOU))
                                VDD2H_P=VDD2H[index-1]/(VDD2H[index-1]+VDD2L[index-1])
                                VDD2L_P = VDD2L[index-1] / (VDD2H[index-1] + VDD2L[index-1])
                                if VDD2H_P >1:
                                    VDD2H_P=1
                                    VDD2L_P=0
                                fig6.update_layout(title=f"{DRAM_Vendor} @DDR{DRAM_Freq} ")
                                fig6.add_trace(
                                    go.Pie(labels=['VDD2H','VDD2L'], values=[VDD2H_P,VDD2L_P]))
                                figure6=1
                            elif int(''.join(filter(str.isdigit, DRAM_Freq))) <= 6400:
                                index = np.searchsorted(Raw_data["MB/s"], int(DOU))
                                VDD2H_P=VDD2H[index-1]/(VDD2H[index-1]+VDD2L[index-1])
                                VDD2L_P = VDD2L[index-1] / (VDD2H[index-1] + VDD2L[index-1])
                                if VDD2H_P >1:
                                    VDD2H_P=1
                                    VDD2L_P=0
                                fig7.update_layout(title=f"{DRAM_Vendor} @DDR{DRAM_Freq} ")
                                fig7.add_trace(
                                    go.Pie(labels=['VDD2H','VDD2L'], values=[VDD2H_P,VDD2L_P]))
                                figure7=1
                            elif int(''.join(filter(str.isdigit, DRAM_Freq))) <= 7500:
                                index = np.searchsorted(Raw_data["MB/s"], int(DOU))
                                VDD2H_P=VDD2H[index-1]/(VDD2H[index-1]+VDD2L[index-1])
                                VDD2L_P = VDD2L[index-1] / (VDD2H[index-1] + VDD2L[index-1])
                                if VDD2H_P >1:
                                    VDD2H_P=1
                                    VDD2L_P=0
                                fig8.update_layout(title=f"{DRAM_Vendor} @DDR{DRAM_Freq} ")
                                fig8.add_trace(
                                    go.Pie(labels=['VDD2H','VDD2L'], values=[VDD2H_P,VDD2L_P]))
                                figure8=1
                            elif int(''.join(filter(str.isdigit, DRAM_Freq))) <= 8533:
                                index = np.searchsorted(Raw_data["MB/s"], int(DOU))
                                VDD2H_P=VDD2H[index-1]/(VDD2H[index-1]+VDD2L[index-1])
                                VDD2L_P = VDD2L[index-1] / (VDD2H[index-1] + VDD2L[index-1])
                                if VDD2H_P >1:
                                    VDD2H_P=1
                                    VDD2L_P=0
                                fig9.update_layout(title=f"{DRAM_Vendor} @DDR{DRAM_Freq} ")
                                fig9.add_trace(
                                    go.Pie(labels=['VDD2H','VDD2L'], values=[VDD2H_P,VDD2L_P]))
                                figure9=1
                            elif int(''.join(filter(str.isdigit, DRAM_Freq))) <= 9600:
                                index = np.searchsorted(Raw_data["MB/s"], int(DOU))
                                VDD2H_P=VDD2H[index-1]/(VDD2H[index-1]+VDD2L[index-1])
                                VDD2L_P = VDD2L[index-1] / (VDD2H[index-1] + VDD2L[index-1])
                                if VDD2H_P >1:
                                    VDD2H_P=1
                                    VDD2L_P=0
                                fig.update_layout(title=f"{DRAM_Vendor} @DDR{DRAM_Freq} ")
                                fig.add_trace(
                                    go.Pie(labels=['VDD2H','VDD2L'], values=[VDD2H_P,VDD2L_P]))
                                figure=1
                        elif add_radio == "Compare_Power Domain":
                            if int(''.join(filter(str.isdigit, DRAM_Freq))) > 3200:
                                VDDQ=Raw_data['VDDQ(mA)']*0.5
                                VDD2H=Raw_data['VDD2H(mA)']*1.05
                                VDD2L=Raw_data['VDD2L(mA)']*0.9
                                VDD1=Raw_data['VDD1(mA)']*1.8
                                Raw_data['DRAM Die Total(mW)']=VDDQ+VDD2H+VDD2L+VDD1
                                #st.write(Raw_data)
                            else:
                                VDDQ=Raw_data['VDDQ(mA)']*0.3
                                VDD2H=Raw_data['VDD2H(mA)']*1.05
                                VDD2L=Raw_data['VDD2L(mA)']*0.9
                                VDD1=Raw_data['VDD1(mA)']*1.8
                                Raw_data['DRAM Die Total(mW)'] = VDDQ + VDD2H + VDD2L + VDD1
                            fig.update_layout(title=f" @{Power_domain}")
                            fig.add_trace(go.Scatter(x=Raw_data["MB/s"], y=Raw_data[Power_domain], mode='lines+markers', name=Project_name+"_"+DRAM_Vendor+"_"+DRAM_Freq))

    if add_radio == "Compare_Total_Die":
        if len(Plot_X) == 0:
            Plot_X = 1000
            st.write('Please key value >= 1, X value reture default(1000)')
        if len(Plot_Y) == 0:
            Plot_Y = 100
            st.write('Please key value >= 1, Y value reture default(100)')

        fig.update_layout(
            xaxis=dict(tickmode='linear', tick0=0, dtick=Plot_X),
            yaxis=dict(tickmode='linear', tick0=0, dtick=Plot_Y),
            xaxis_title = "MB/s",
            yaxis_title = "(mW)",
            height = 500
        )
        st.plotly_chart(fig,use_container_width=True)
    elif add_radio == "Scenario_Compare":
        if figure1==1:
            fig1.update_layout(
                xaxis_title="MB/s",
                yaxis_title="(mW)"
            )
            st.plotly_chart(fig1, use_container_width=False)
        if figure2 == 1:
            fig2.update_layout(
                xaxis_title="MB/s",
                yaxis_title="(mW)"
            )
            st.plotly_chart(fig2, use_container_width=False)
        if figure3 == 1:
            fig3.update_layout(
                xaxis_title="MB/s",
                yaxis_title="(mW)"
            )
            st.plotly_chart(fig3, use_container_width=False)
        if figure4 == 1:
            fig4.update_layout(
                xaxis_title="MB/s",
                yaxis_title="(mW)"
            )
            st.plotly_chart(fig4, use_container_width=False)
        if figure5 == 1:
            fig5.update_layout(
                xaxis_title="MB/s",
                yaxis_title="(mW)"
            )
            st.plotly_chart(fig5, use_container_width=False)
        if figure6 == 1:
            fig6.update_layout(
                xaxis_title="MB/s",
                yaxis_title="(mW)"
            )
            st.plotly_chart(fig6, use_container_width=False)
        if figure == 1:
            fig.update_layout(
                xaxis_title="MB/s",
                yaxis_title="(mW)"
            )
            st.plotly_chart(fig, use_container_width=False)
        if figure7 == 1:
            fig7.update_layout(
                xaxis_title="MB/s",
                yaxis_title="(mW)"
            )
            st.plotly_chart(fig7, use_container_width=False)
        if figure8 == 1:
            fig8.update_layout(
                xaxis_title="MB/s",
                yaxis_title="(mW)"
            )
            st.plotly_chart(fig8, use_container_width=False)
        if figure9 == 1:
            fig9.update_layout(
                xaxis_title="MB/s",
                yaxis_title="(mW)"
            )
            st.plotly_chart(fig9, use_container_width=False)
    elif add_radio == "VDD2H VS VDD2L percentage":
        if figure1==1:
            fig1.update_layout(
                xaxis_title="MB/s",
                yaxis_title="(mW)"
            )
            st.plotly_chart(fig1, use_container_width=False)
        if figure2 == 1:
            fig2.update_layout(
                xaxis_title="MB/s",
                yaxis_title="(mW)"
            )
            st.plotly_chart(fig2, use_container_width=False)
        if figure3 == 1:
            fig3.update_layout(
                xaxis_title="MB/s",
                yaxis_title="(mW)"
            )
            st.plotly_chart(fig3, use_container_width=False)
        if figure4 == 1:
            fig4.update_layout(
                xaxis_title="MB/s",
                yaxis_title="(mW)"
            )
            st.plotly_chart(fig4, use_container_width=False)
        if figure5 == 1:
            fig5.update_layout(
                xaxis_title="MB/s",
                yaxis_title="(mW)"
            )
            st.plotly_chart(fig5, use_container_width=False)
        if figure6 == 1:
            fig6.update_layout(
                xaxis_title="MB/s",
                yaxis_title="(mW)"
            )
            st.plotly_chart(fig6, use_container_width=False)
        if figure == 1:
            fig.update_layout(
                xaxis_title="MB/s",
                yaxis_title="(mW)"
            )
            st.plotly_chart(fig, use_container_width=False)
        if figure7 == 1:
            fig7.update_layout(
                xaxis_title="MB/s",
                yaxis_title="(mW)"
            )
            st.plotly_chart(fig7, use_container_width=False)
        if figure8 == 1:
            fig8.update_layout(
                xaxis_title="MB/s",
                yaxis_title="(mW)"
            )
            st.plotly_chart(fig8, use_container_width=False)
        if figure9 == 1:
            fig9.update_layout(
                xaxis_title="MB/s",
                yaxis_title="(mW)"
            )
    elif add_radio == "Compare_Power Domain":
        if len(Plot_X) == 0:
            Plot_X = 1000
            st.write('Please key value >= 1, X value reture default(1000)')
        if len(Plot_Y) == 0:
            Plot_Y = 100
            st.write('Please key value >= 1, Y value reture default(100)')

        fig.update_layout(
            xaxis=dict(tickmode='linear', tick0=0, dtick=Plot_X),
            yaxis=dict(tickmode='linear', tick0=0, dtick=Plot_Y),
            xaxis_title = "MB/s",
            yaxis_title = "(mA)",
            height = 500
        )
        st.plotly_chart(fig, use_container_width=True)





