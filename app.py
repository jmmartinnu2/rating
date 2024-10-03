import streamlit as st
import pandas as pd
import numpy as np
import os
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import altair as alt

# ====================================
# Configuración Inicial de la Aplicación
# ====================================

# Asegurarse de que el directorio 'data' exista
os.makedirs('data', exist_ok=True)

# Configuración de la página
st.set_page_config(
    page_title="Reputación - Gestión de Relaciones con Clubes de Fútbol",
    layout="wide"  # Usar layout "wide" para aprovechar mejor el espacio
)

# Diccionario de traducciones
languages = {
    "es": {
        "title": "Reputación - Gestión de Relaciones con Clubes de Fútbol",
        "welcome": "Bienvenido a **Reputación**, una herramienta diseñada para agentes FIFA para evaluar y gestionar la reputación de los departamentos técnicos de los clubes de fútbol.",
        "evaluation": "Evaluación por Criterios",
        "clarity": "Claridad en la Comunicación (1-5)",
        "speed": "Rapidez en las Respuestas (1-5)",
        "professionalism": "Actitud Profesional (1-5)",
        "courtesy": "Cortesía y Amabilidad (1-5)",
        "efficiency": "Eficiencia en Procesos (1-5)",
        "problem_solving": "Solución de Problemas (1-5)",
        "reliability": "Fiabilidad de la Información (1-5)",
        "commitment": "Cumplimiento de Compromisos (1-5)",
        "accessibility": "Accesibilidad (1-5)",
        "flexibility": "Flexibilidad (1-5)",
        "comments": "Comentarios Generales",
        "submit_rating": "Enviar Valoración",
        "no_data": "No hay datos disponibles para visualizar.",
        "recent_ratings": "Valoraciones Recientes",
        "data_visualization": "Visualización de Datos",
        "country": "País",
        "club": "Club",
        "position": "Cargo",
        "stars": "Estrellas",
        "name": "Nombre",
        "distributions": "Distribución de Confiabilidad",
        "average_ratings": "Promedio de Valoraciones por Criterio",
        "number_by_country": "Número de Valoraciones por País",
        "number_by_club": "Número de Valoraciones por Club",
        "average_reliability": "Promedio de Confiabilidad por País",
    },
    "en": {
        "title": "Reputation - Management of Football Club Relations",
        "welcome": "Welcome to **Reputation**, a tool designed for FIFA agents to evaluate and manage the reputation of technical departments of football clubs.",
        "evaluation": "Evaluation by Criteria",
        "clarity": "Clarity in Communication (1-5)",
        "speed": "Speed of Response (1-5)",
        "professionalism": "Professional Attitude (1-5)",
        "courtesy": "Courtesy and Kindness (1-5)",
        "efficiency": "Efficiency in Processes (1-5)",
        "problem_solving": "Problem Solving (1-5)",
        "reliability": "Reliability of Information (1-5)",
        "commitment": "Commitment Fulfillment (1-5)",
        "accessibility": "Accessibility (1-5)",
        "flexibility": "Flexibility (1-5)",
        "comments": "General Comments",
        "submit_rating": "Submit Rating",
        "no_data": "No data available for visualization.",
        "recent_ratings": "Recent Ratings",
        "data_visualization": "Data Visualization",
        "country": "Country",
        "club": "Club",
        "position": "Position",
        "stars": "Stars",
        "name": "Name",
        "distributions": "Distribution of Reliability",
        "average_ratings": "Average Ratings by Criterion",
        "number_by_country": "Number of Ratings by Country",
        "number_by_club": "Number of Ratings by Club",
        "average_reliability": "Average Reliability by Country",
    }
}

# Inicializar idioma por defecto
if 'language' not in st.session_state:
    st.session_state.language = "en"  # Establecer inglés como idioma por defecto

# Selección de idioma en el sidebar
st.sidebar.header("Idioma")
selected_language = st.sidebar.selectbox("Seleccionar idioma", options=["es", "en"], index=0 if st.session_state.language == "es" else 1)

if selected_language != st.session_state.language:
    st.session_state.language = selected_language

# Título y Descripción de la Aplicación en la Página Principal
st.title(languages[st.session_state.language]["title"])
st.markdown(languages[st.session_state.language]["welcome"])

# ====================================
# Gestión del Estado de la Aplicación
# ====================================

# Inicializar contador en Session State para resetear widgets después de enviar una valoración
if 'counter' not in st.session_state:
    st.session_state.counter = 0

# ====================================
# Carga y Preprocesamiento de Datos
# ====================================

def create_empty_data():
    return pd.DataFrame(columns=[
        'Pais', 'Club', 'Cargo', 'Nombre', 
        'Agente', 
        'Claridad en la Comunicación', 'Rapidez en las Respuestas',
        'Actitud Profesional', 'Cortesía y Amabilidad',
        'Eficiencia en Procesos', 'Solución de Problemas',
        'Fiabilidad de la Información', 'Cumplimiento de Compromisos',
        'Accesibilidad', 'Flexibilidad',
        'Comentarios Generales', 'Estrellas'
    ])

# Asegurarse de que el directorio 'data' exista
os.makedirs('data', exist_ok=True)

# Verificar si el archivo CSV existe y cargarlo
result_file_path = os.path.join('data', 'result-rating.csv')  # Ruta local
if os.path.exists(result_file_path):
    ratings = pd.read_csv(result_file_path)
else:
    ratings = create_empty_data()  # Iniciar el DataFrame vacío si no existe el archivo

# Guardar en el archivo result-rating.csv en la carpeta data
ratings.to_csv(result_file_path, mode='w', header=True, index=False)  # Sobrescribir el archivo con todos los datos


# ====================================
# Página Principal: Tabs
# ====================================

# Crear Tabs
tab1, tab2, tab3 = st.tabs([languages[st.session_state.language]["evaluation"], 
                                   languages[st.session_state.language]["recent_ratings"], 
                                   languages[st.session_state.language]["data_visualization"], 
                                   ])

# ----------------------------
# Tab 1: Evaluación por Criterios
# ----------------------------
with tab1:
    st.header(languages[st.session_state.language]["evaluation"])

    # Formulario para ingresar información y valoraciones
    with st.form("rating_form"):
        nuevo_nombre = st.text_input(languages[st.session_state.language]["name"])
        nuevo_cargo = st.selectbox(languages[st.session_state.language]["position"], options=[
            "Director Deportivo", "Entrenador", "Asistente", "Jefe de Scouting", "Scouting", "CEO", "Analista de Datos"
        ])
        nuevo_pais = st.selectbox(languages[st.session_state.language]["country"], options=["España", "Argentina", "México"])  # Lista de países de ejemplo
        nuevo_club = st.text_input(languages[st.session_state.language]["club"])

        st.markdown("### " + languages[st.session_state.language]["evaluation"])

        col1, col2 = st.columns(2)
        
        with col1:
            claridad_com = st.slider(languages[st.session_state.language]["clarity"], 1, 5, 3)
            rapidez_resp = st.slider(languages[st.session_state.language]["speed"], 1, 5, 3)
            actitud_prof = st.slider(languages[st.session_state.language]["professionalism"], 1, 5, 3)
            cortesía = st.slider(languages[st.session_state.language]["courtesy"], 1, 5, 3)
            
        with col2:
            eficiencia_proc = st.slider(languages[st.session_state.language]["efficiency"], 1, 5, 3)
            solucion_prob = st.slider(languages[st.session_state.language]["problem_solving"], 1, 5, 3)
            fiabilidad_info = st.slider(languages[st.session_state.language]["reliability"], 1, 5, 3)
            cumplimiento = st.slider(languages[st.session_state.language]["commitment"], 1, 5, 3)
            accesibilidad = st.slider(languages[st.session_state.language]["accessibility"], 1, 5, 3)
            flexibilidad = st.slider(languages[st.session_state.language]["flexibility"], 1, 5, 3)
        
        comentario = st.text_area(languages[st.session_state.language]["comments"])
        submit_rating = st.form_submit_button(languages[st.session_state.language]["submit_rating"])
    
        if submit_rating:
            # Validaciones
            if nuevo_nombre.strip() == "":
                st.error("Por favor, ingresa tu nombre.")
            elif comentario.strip() == "":
                st.error("Por favor, ingresa un comentario.")
            elif not (nuevo_nombre and nuevo_cargo and nuevo_club and nuevo_pais):
                st.error("Por favor, completa todos los campos del registro antes de enviar una valoración.")
            else:
                # Calcular las estrellas basadas en la media de las valoraciones
                estrellas = (claridad_com + rapidez_resp + actitud_prof + cortesía + eficiencia_proc + solucion_prob + fiabilidad_info + cumplimiento + accesibilidad + flexibilidad) / 10
                
                new_rating = pd.DataFrame({
                    'Pais': [nuevo_pais],
                    'Club': [nuevo_club],
                    'Cargo': [nuevo_cargo],
                    'Nombre': [nuevo_nombre],
                    'Agente': [nuevo_nombre],
                    'Claridad en la Comunicación': [claridad_com],
                    'Rapidez en las Respuestas': [rapidez_resp],
                    'Actitud Profesional': [actitud_prof],
                    'Cortesía y Amabilidad': [cortesía],
                    'Eficiencia en Procesos': [eficiencia_proc],
                    'Solución de Problemas': [solucion_prob],
                    'Fiabilidad de la Información': [fiabilidad_info],
                    'Cumplimiento de Compromisos': [cumplimiento],
                    'Accesibilidad': [accesibilidad],
                    'Flexibilidad': [flexibilidad],
                    'Comentarios Generales': [comentario],
                    'Estrellas': [estrellas]  # Añadir la columna de estrellas
                })
                
                ratings = pd.concat([ratings, new_rating], ignore_index=True)
                st.success("¡Valoración enviada exitosamente!")

                # Guardar en el archivo result-rating.csv en la carpeta data
                result_file_path = os.path.join('data', 'result-rating.csv')
                ratings.to_csv(result_file_path, mode='w', header=True, index=False)  # Sobrescribir el archivo con todos los datos

# ----------------------------
# Tab 2: Valoraciones Recientes
# ----------------------------
with tab2:
    st.header(languages[st.session_state.language]["recent_ratings"])
    
    def display_ratings_table(df):
        # Configurar opciones de AgGrid
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(textAlign='left', sortable=True, filter=True, resizable=True)
        gb.configure_pagination(paginationAutoPageSize=True)  # Paginación automática
        gb.configure_side_bar()  # Barra lateral para herramientas
        
        # Añadir una columna de estrellas visualmente
        df['Estrellas'] = df['Estrellas'].fillna(0).astype(int)  # Llenar NaN con 0 y convertir a int
        df['Estrellas'] = df['Estrellas'].apply(lambda x: '★' * x + '☆' * (5 - x))  # Visualizar estrellas
        
        gb.configure_column("Estrellas", headerName=languages[st.session_state.language]["stars"])  # Nombre de la columna
        
        gridOptions = gb.build()
        
        # Renderizar AgGrid
        AgGrid(
            df,
            gridOptions=gridOptions,
            enable_enterprise_modules=False,
            height=400,  # Ajustar la altura según sea necesario
            fit_columns_on_grid_load=True,
            update_mode=GridUpdateMode.NO_UPDATE
        )
    
    # Mostrar la tabla usando AgGrid
    display_ratings_table(ratings)

# ----------------------------
# Tab 3: Visualización de Datos
# ----------------------------
with tab3:
    st.header(languages[st.session_state.language]["data_visualization"])
    
    # Verificar si hay datos para visualizar
    if ratings.empty:
        st.warning(languages[st.session_state.language]["no_data"])
    else:
        # Crear una copia del DataFrame para no modificar el original
        ratings_with_confiable = ratings.copy()
        
        # Calcular 'Confiable' para cada valoración
        ratings_with_confiable['Confiable'] = ratings_with_confiable[ 
            ['Claridad en la Comunicación', 'Rapidez en las Respuestas',
             'Actitud Profesional', 'Cortesía y Amabilidad',
             'Eficiencia en Procesos', 'Solución de Problemas',
             'Fiabilidad de la Información', 'Cumplimiento de Compromisos',
             'Accesibilidad', 'Flexibilidad']
        ].mean(axis=1).apply(lambda x: 1 if x >= 3 else 0)
        
        # 1. Distribución de Confiabilidad
        st.subheader(languages[st.session_state.language]["distributions"])
        confiabilidad_counts = ratings_with_confiable.groupby('Confiable').size().reset_index(name='Counts')
        confiabilidad_counts['Confiable'] = confiabilidad_counts['Confiable'].map({1: 'Confiable', 0: 'No Confiable'})
        
        pie_chart = alt.Chart(confiabilidad_counts).mark_arc().encode(
            theta=alt.Theta(field="Counts", type="quantitative"),
            color=alt.Color(field="Confiable", type="nominal"),
            tooltip=['Confiable', 'Counts']
        ).properties(
            width=400,
            height=400,
            title=languages[st.session_state.language]["distributions"]
        )
        
        st.altair_chart(pie_chart, use_container_width=True)
        
        # 2. Promedio de Valoraciones por Criterio
        st.subheader(languages[st.session_state.language]["average_ratings"])
        criterios = [
            'Claridad en la Comunicación', 'Rapidez en las Respuestas',
            'Actitud Profesional', 'Cortesía y Amabilidad',
            'Eficiencia en Procesos', 'Solución de Problemas',
            'Fiabilidad de la Información', 'Cumplimiento de Compromisos',
            'Accesibilidad', 'Flexibilidad'
        ]
        promedio_criterios = ratings_with_confiable[criterios].mean().reset_index()
        promedio_criterios.columns = ['Criterio', 'Promedio']
        
        bar_chart = alt.Chart(promedio_criterios).mark_bar().encode(
            x=alt.X('Promedio:Q', title='Promedio'),
            y=alt.Y('Criterio:N', sort='-x', title='Criterio'),
            tooltip=['Criterio', 'Promedio']
        ).properties(
            width=600,
            height=400,
            title=languages[st.session_state.language]["average_ratings"]
        )
        
        st.altair_chart(bar_chart, use_container_width=True)
        
        # 3. Número de Valoraciones por País
        st.subheader(languages[st.session_state.language]["number_by_country"])
        valoraciones_pais = ratings_with_confiable['Pais'].value_counts().reset_index()
        valoraciones_pais.columns = ['Pais', 'Cantidad']
        
        bar_chart_pais = alt.Chart(valoraciones_pais).mark_bar().encode(
            x=alt.X('Cantidad:Q', title='Cantidad'),
            y=alt.Y('Pais:N', sort='-x', title='País'),
            tooltip=['Pais', 'Cantidad']
        ).properties(
            width=600,
            height=400,
            title=languages[st.session_state.language]["number_by_country"]
        )
        
        st.altair_chart(bar_chart_pais, use_container_width=True)
        
        # 4. Número de Valoraciones por Club
        st.subheader(languages[st.session_state.language]["number_by_club"])
        valoraciones_club = ratings_with_confiable['Club'].value_counts().reset_index().head(10)
        valoraciones_club.columns = ['Club', 'Cantidad']
        
        bar_chart_club = alt.Chart(valoraciones_club).mark_bar().encode(
            x=alt.X('Cantidad:Q', title='Cantidad'),
            y=alt.Y('Club:N', sort='-x', title='Club'),
            tooltip=['Club', 'Cantidad']
        ).properties(
            width=600,
            height=400,
            title=languages[st.session_state.language]["number_by_club"]
        )
        
        st.altair_chart(bar_chart_club, use_container_width=True)
        
        # 5. Promedio de Confiabilidad por País
        st.subheader(languages[st.session_state.language]["average_reliability"])
        confiabilidad_pais = ratings_with_confiable.groupby('Pais')['Confiable'].mean().reset_index()
        confiabilidad_pais.columns = ['Pais', 'Promedio Confiabilidad']
        
        bar_chart_confiabilidad_pais = alt.Chart(confiabilidad_pais).mark_bar().encode(
            x=alt.X('Promedio Confiabilidad:Q', title='Promedio Confiabilidad'),
            y=alt.Y('Pais:N', sort='-x', title='País'),
            tooltip=['Pais', 'Promedio Confiabilidad']
        ).properties(
            width=600,
            height=400,
            title=languages[st.session_state.language]["average_reliability"]
        )
        
        st.altair_chart(bar_chart_confiabilidad_pais, use_container_width=True)
