import streamlit as st
import pandas as pd
import time

# Título del aplicativo
st.title("Arena Space - Gestión de Tiempos")

# Crear un dataframe para almacenar la información de los niños
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['Nombre', 'Tiempo Pagado', 'Tiempo Restante', 'Segundos Restantes'])

# Input de datos del niño
with st.form(key='entrada_nino'):
    nombre = st.text_input("Nombre del Niño")
    tiempo_pagado = st.number_input("Tiempo Pagado (en minutos)", min_value=1)
    submit_button = st.form_submit_button(label='Registrar')

    if submit_button:
        segundos_restantes = int(tiempo_pagado * 60)  # Convertimos a segundos
        nuevo_registro = pd.DataFrame({
            'Nombre': [nombre], 
            # 'Tiempo Pagado': [tiempo_pagado], 
            'Tiempo Restante': [f"{int(tiempo_pagado)}:00"],
            'Segundos Restantes': [segundos_restantes]
        })
        st.session_state.data = pd.concat([st.session_state.data, nuevo_registro], ignore_index=True)
        st.success(f"¡{nombre} ha sido registrado con éxito!")

# Verificar si la columna 'Segundos Restantes' existe en cada iteración y manejarla
if 'Segundos Restantes' in st.session_state.data.columns:
    for i, row in st.session_state.data.iterrows():
        if row['Segundos Restantes'] > 0:
            st.session_state.data.at[i, 'Segundos Restantes'] -= 1  # Restar un segundo
            minutos, segundos = divmod(int(st.session_state.data.at[i, 'Segundos Restantes']), 60)
            st.session_state.data.at[i, 'Tiempo Restante'] = f"{minutos}:{segundos:02d}"
        else:
            st.session_state.data.at[i, 'Tiempo Restante'] = "Tiempo finalizado"

# Mostrar la tabla de niños registrados con el tiempo restante actualizado
st.subheader("Niños Registrados")
st.table(st.session_state.data[['Nombre', 
                                # 'Tiempo Pagado', 
                                'Tiempo Restante']])

# Refrescar la aplicación cada segundo
time.sleep(1)
st.rerun()  # Usa experimental_rerun o st.rerun si está disponible
