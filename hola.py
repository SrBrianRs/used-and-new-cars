import streamlit as st
import pandas as pd
import codecs
import plotly.express as px


st.image("baner1.png")
st.title('Netflix Complete List')
st.header('Itzel Karina Fernandez Rios')
st.header('zS20006763@estudiantes.uv.mx')
#--- LOGO ---#
st.sidebar.image("Logo.jpeg")
st.sidebar.markdown("##")
sidebar= st.sidebar


DATA_URL = ('netflix.csv')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
   
    return data

def filtro_title(title):
    title_filt = data[data['title'].str.upper().str.contains(title)]
    return title_filt

def filtro_director(director):
    director_filt = data[data['director'] == director]
    return director_filt

data_load_state= st.text("Loading data...")
data= load_data(8000)
data_load_state.text("Done!")

titulofilme = st.sidebar.text_input('Titulo de la Pelicula <3 :')
botonBuscar = st.sidebar.button('Buscar Pelicula')

if (botonBuscar):
   peliculas = filtro_title(titulofilme.upper())
   count_row = peliculas.shape[0]
   st.header("Peliculas")
   st.write(f"Total de Peliculas mostradas : {count_row}")
   st.write(peliculas)

seldirector = st.sidebar.selectbox("Director  <3 :", data['director'].unique())
botonFiltrodirector = st.sidebar.button('Filtrar director')

if (botonFiltrodirector):
   director = filtro_director(seldirector)
   count_row = director.shape[0]
   st.write(f"Total de peliculas por director : {count_row}")

   st.dataframe(director)

   ##Histograma
fig_duration = px.histogram(data,
                   x="duration",
                   title="Duracion de una pelicula",
                    labels=dict(duration="Duracion"),
                   color_discrete_sequence=["#1abc9c"],
                   template="plotly_white"
                   )
fig_duration.update_layout(plot_bgcolor="rgba(0,0,0,0)") 

##Grafica de barras
directorBytitle = data.groupby('director')['title'].count().reset_index(name='count')
directorBytitle = directorBytitle.sort_values(by='count', ascending=False).head(10)

fig_director = px.bar(directorBytitle,
                      x='director',
                      y='count',
                      title='Top 10 directores con numero de peliculas de cada uno',
                      labels={'count': 'Numero de Titulos', 'director': 'Director'},
                      color_discrete_sequence=['#F633FF'],
                      template='plotly_white')
fig_director.update_layout(plot_bgcolor='rgba(0,0,0,0)')

#Grafica Scatter
caps=data['release_year']
scor=data['country']
tipe=data['type']
fig_scatter=px.scatter(data,
                         x=caps,
                         y=scor,
                         color=tipe,
                         title="Posicion por país y su año",
                         labels=dict(Score="Año _Lanzamiento", country="País", type="Categoria"),
                         template="plotly_white")
fig_scatter.update_layout(plot_bgcolor="rgba(0,0,0,0)")


#Checkbox
titulofilme = st.sidebar.text('Graficas <3 :')
agree=sidebar.checkbox("Mostrar graficas")
if agree:
    st.header("Histograma")
    st.plotly_chart(fig_duration)
    st.write("En este diagramase muestra la relacion entre la duracion de las peliculas.")
    st.header("Grafica de barras")
    st.plotly_chart(fig_director)
    st.write("En este diagrama se muestra la cantidad de Peliculas que fueron creados por 10 directores.")
    st.header("Grafica de Scatter")
    st.plotly_chart(fig_scatter)
    st.write("En esta grafica se muestra una visualización de las películas en función de su año de lanzamiento y su país.")