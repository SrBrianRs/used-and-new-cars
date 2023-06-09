import codecs
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


st.sidebar.image("logo.png")
st.sidebar.title('Cars App')
st.sidebar.title('Brian Sanchez Robles')
st.sidebar.text('s19004873')
st.sidebar.markdown("##")

DATE_COLUMN = 'released'
DATA_URL = ('car_data.csv')


@st.cache
def cargar_datos(nrows):
    doc = codecs.open('car_data.csv', 'r', 'latin1')
    data = pd.read_csv(doc, nrows=nrows)
    def lowercase(x): return str(x).lower()
    return data


def filtro_car(auto):
    filtered_data_auto = data[data['Model'].str.upper().str.contains(auto)]
    return filtered_data_auto


# file_size = os.path.getsize('car_data.csv')
data = cargar_datos(100000)


def filtro_year(year):
    filtered_data_director = data[data['Year'] == year]
    return filtered_data_director


# Filtra por año seleccionando con un selecbox
selec_year = st.sidebar.selectbox("Seleccionar Año", data['Year'].unique())
btnyear = st.sidebar.button('Filtrar año ')
if (btnyear):
    filtroyear = filtro_year(selec_year)
    count_row = filtroyear.shape[0]
    st.write(f"Total Autos mostrados por año : {count_row}")
    st.dataframe(filtroyear)


# Muestra lso datos filtrados por modelo, con una entrada de texto y un boton
modelauto = st.sidebar.text_input('Modelo del auto:')
btnBuscar = st.sidebar.button('Buscar Autos')
if (btnBuscar):
    data_auto = filtro_car(modelauto.upper())
    count_row = data_auto.shape[0]
    st.write(f"Total autos mostrados por modelo : {count_row}")
    st.write(data_auto)


# Muestra todos los datos del csv con un checkbox
if st.sidebar.checkbox('Mostrar todos los Autos'):
    st.subheader('Todos los autos')
    st.write(data)


# Histograma
if (st.sidebar.checkbox('Histograma')):
    fig, ax = plt.subplots()
    ax.hist(data['Year'])
    st.header("Histograma del el año")
    st.pyplot(fig)

#Grafica de dispersion
#if (st.sidebar.checkbox('Grafica de Dispersion')):
#    fig, ax = plt.subplots()
#    ax.scatter(data["Status"], data["Year"],s=5,c='r')
#    ax.set_xlabel("Estado")
#    ax.set_ylabel("Año")
#   ax.set_title("Grafica de los años con relacion al estado del auto")
#    st.pyplot(fig)

# Grafica de barras
if (st.sidebar.checkbox('Grafica de barras')):
    fig, ax = plt.subplots()

    x_pos = data['Status']
    y_pos = data['Year']

    ax.bar(x_pos, y_pos)
    ax.set_xlabel("Estado")
    ax.set_ylabel("Año")
    ax.set_title('Estado vs. Año de los Autos')
    ax.set_ylim([1950, ax.get_ylim()[1]])
    st.header("Gráfico de Estado y Modelo de Autos")
    st.pyplot(fig)


#Grafica de Scatter
if (st.sidebar.checkbox('Grafica de Scatter')):
    fig, ax = plt.subplots()

    fig_distribution_scatter = px.scatter(data, 
                                        x = "Price",
                                        y = "Model",
                                        size = "Year",
                                        color = "Year",
                                        title = "Grafica Scatter",
                                        template = "plotly_white"
                                        )
    fig_distribution_scatter.update_layout(xaxis_title = 'Precio', yaxis_title='Modelo')
    fig_distribution_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)')

    st.plotly_chart(fig_distribution_scatter)



# Grafica Nueva

car_counts = data.groupby('Model').size().reset_index(name='Year')

if st.sidebar.checkbox('Nueva grafica'):
    st.markdown("Histograma para analizar cuantos autos por modelo hay por año")
    fig_car = px.histogram(car_counts, 
                               x='Model', 
                               y='Year', 
                               title='Número autos por año')
    st.plotly_chart(fig_car, use_container_width=True)