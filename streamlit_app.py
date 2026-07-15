import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Dashboard de Unidades Económicas - Reserva Forestal",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced design and typography
st.markdown("""
    <style>
    .main {
        background-color: #f7f9fa;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #2e7d32;
        margin-bottom: 15px;
    }
    .metric-title {
        font-size: 0.9rem;
        color: #555555;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 1.8rem;
        color: #1b5e20;
        font-weight: 700;
    }
    .metric-value-negative {
        color: #c62828 !important;
    }
    .section-header {
        color: #1b5e20;
        border-bottom: 2px solid #a5d6a7;
        padding-bottom: 8px;
        margin-top: 25px;
        margin-bottom: 15px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Application Header
st.title("🌳 Dashboard Integral de Unidades Económicas (Unit Economics)")
st.markdown("##### Análisis de Viabilidad, Valoración y Monitoreo del Negocio de Reserva Forestal & Eco-living")

# Sidebar navigation / interactive controls
st.sidebar.image("https://img.icons8.com/color/96/000000/forest.png", width=90)
st.sidebar.title("Configuración")
st.sidebar.markdown("---")

# --- NUEVO SIMULADOR DE ESCENARIOS (Amarrado al supuesto de 32,000M) ---
st.sidebar.subheader("🎛️ Simulador Financiero (Supuesto 32k Millones)")

# Cantidad de usuarios (Aportantes activos) - Por defecto 16
active_users_sim = st.sidebar.slider(
    "Usuarios Activos (Aportantes)", 
    min_value=1, 
    max_value=100, 
    value=16, 
    step=1,
    help="Número de usuarios aportando al proyecto de forma mensual. Por defecto: 16."
)

# Mensualidad simulada por usuario (De 10M a 50M) - Por defecto 15M
mrr_per_user_sim = st.sidebar.slider(
    "Aporte Mensual por Usuario ($ COP)", 
    min_value=10000000,     # 10 Millones
    max_value=50000000,     # 50 Millones
    value=15000000,         # 15 Millones por defecto
    step=1000000,           # Incrementos de 1 Millón
    format="$%d",
    help="Monto de la cuota mensual que aporta cada usuario."
)

# Plazo de aportes - Por defecto 133 meses
months_sim = st.sidebar.slider(
    "Plazo del Proyecto (Meses)", 
    min_value=12, 
    max_value=240, 
    value=133, 
    step=1,
    help="Tiempo estimado para completar el recaudo total del proyecto."
)

# --- CÁLCULOS FINANCIEROS SIMULADOS ---
simulated_mrr = active_users_sim * mrr_per_user_sim
simulated_arr = simulated_mrr * 12
total_recaudo_proyectado = simulated_mrr * months_sim
meta_recaudo = 32000000000.0  # 32,000 Millones COP
brecha_meta = total_recaudo_proyectado - meta_recaudo

# Raw Data values (Static baseline values)
unit_economics_static = {
    "Área Vendible (m²)": 48000,
    "Área de Reserva (m²)": 500000,
    "Tons CO2 por Hectárea / Año": 2.0,
    "Total Toneladas de Carbono Año Capturadas": 100,
    "Ingresos Toneladas CO2 (Año) * 50 Ha": 8000000.0,
    "Mensualidad Eco Senior": 15000000.0,
    "Costos Mes Eco Senior": 12000000.0,
    "Volumen Residuo Compostado Mes (Tons)": 4.0,
    "Pollos": 400.0,
    "Margen Bruto Eco Senior (Mensual)": 3000000.0,
    "Costo Mes Plan Padrino": 800000.0,
    "Active Users (Usuarios Activos)": 684,
    "ARPU (Ingreso Promedio por Usuario)": 14181.0,
    "Bookings (Reservas / Facturación Contratada)": 2,
    "Burn Rate Mensual": -316686667.0,
    "Cashflow": 316686666.67,
    "Churn Rate Adultos Mayores": 0.44,
    "Churn Rate Jóvenes": 1.17,
    "CAC Jóvenes": 159040.0,
    "CAC Senior": 1000000.0,
    "LTV Promedio": 32333.33,
    "LTV Jóven": 12000000.0,
    "LTV / CAC Jóvenes": 75.0,
    "LTV Adulto Mayor (10 años)": 1800000000.0,
    "LTV / CAC Adultos Mayores": 1800.0,
    "Margen Bruto (%)": 91.72,
    "Gross Profit": 36686666.67,
    "Efectos de Red (Network Effects)": 1.13,
    "MRR (Mensual)": 150000000.0,
    "ARR (Anual)": 1800000000.0,
    "Usuarios Registrados": 684,
    "Tasa de Retención (%)": 100.0,
    "TAM (Mercado Total Direccionable)": 4.9e12,
    "SAM (Mercado Disponible Servido)": 7.64e11,
    "SOM (Mercado Objetivo Capturable)": 1250000000.0,
    "Ratio Subsidio Cruzado (RSC)": 3.75
}

gross_burn_actual = {
    "Hosting / Año": 90000.0,
    "Dominio / Año": 70000.0,
    "Sala de ventas / Mes": 1000000.0,
    "Impulsadora sala / Mes": 2000000.0,
    "Costos variables / Mes": 300000.0,
    "Total Mensual Actual": 3313333.33
}

gross_burn_proyectado = {
    "Hosting / Mes": 7500.0,
    "Dominio / Mes": 5833.33,
    "Sala de ventas / Mes": 1000000.0,
    "Impulsadora sala / Mes": 2000000.0,
    "Costos variables / Mes": 300000.0,
    "Salario Jose / Mes": 6000000.0,
    "Salario Guillermo / Mes": 4000000.0,
    "Salario Felipe / Mes": 4000000.0,
    "Salario Yoiner / Mes": 2000000.0,
    "Total Mensual Proyectado": 19313333.33
}

ingresos_operativos = {
    "Advisor 1": 40000000.0,
    "Advisor 2": 40000000.0,
    "Advisor 3": 40000000.0,
    "Advisor 4": 40000000.0,
    "Advisor 5": 40000000.0,
    "Advisor 6": 40000000.0,
    "Advisor 7": 40000000.0,
    "Advisor 8": 40000000.0,
    "Total Inicial": 320000000.0
}

# Layout tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Resumen Ejecutivo & Unit Economics", 
    "💸 Burn Rate & Proyecciones de Costos", 
    "📈 Ingresos Operativos & Tracción", 
    "🛡️ Métricas Ambientales (CO2) & Valoración"
])

# TAB 1: EXECUTIVE RESUME & UNIT ECONOMICS
with tab1:
    st.markdown('<h3 class="section-header">Métricas de Escenario Simulado (MRR, ARR & Recaudo)</h3>', unsafe_allow_html=True)
    
    # Tarjetas con las variables simuladas basadas en la barra lateral
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-title">MRR Simulado ({active_users_sim} usuarios)</div>
            <div class="metric-value">${simulated_mrr:,.2f} COP</div>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
        <div class="metric-card" style="border-left-color: #1976d2;">
            <div class="metric-title">ARR Simulado (Anual)</div>
            <div class="metric-value">${simulated_arr:,.2f} COP</div>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        # Mostramos la proyección final de recaudo
        color_recaudo = "#2e7d32" if total_recaudo_proyectado >= meta_recaudo else "#c62828"
        st.markdown(f'''
        <div class="metric-card" style="border-left-color: {color_recaudo};">
            <div class="metric-title">Recaudo Total Proyectado ({months_sim} meses)</div>
            <div class="metric-value" style="color: {color_recaudo};">${total_recaudo_proyectado:,.2f} COP</div>
        </div>
        ''', unsafe_allow_html=True)
    with col4:
        # Metas financieras del proyecto
        estado_meta = "CUBIERTA" if brecha_meta >= 0 else "PENDIENTE"
        color_meta = "#2e7d32" if brecha_meta >= 0 else "#c62828"
        st.markdown(f'''
        <div class="metric-card" style="border-left-color: {color_meta};">
            <div class="metric-title">Cumplimiento Meta (32k M COP)</div>
            <div class="metric-value" style="font-size: 1.5rem; color: {color_meta};">{estado_meta} (Brecha: ${brecha_meta:,.2f} COP)</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('<h3 class="section-header">Análisis de Clientes & Relación LTV / CAC</h3>', unsafe_allow_html=True)
    col_ltv1, col_ltv2 = st.columns(2)
    
    with col_ltv1:
        st.subheader("Segmento Jóvenes")
        df_jovenes = pd.DataFrame({
            "Métrica": ["Costo de Adquisición (CAC)", "Lifetime Value (LTV)", "LTV / CAC Ratio", "Churn Rate"],
            "Valor": [
                f"${unit_economics_static['CAC Jóvenes']:,.2f} COP",
                f"${unit_economics_static['LTV Jóven']:,.2f} COP",
                f"{unit_economics_static['LTV / CAC Jóvenes']}x",
                f"{unit_economics_static['Churn Rate Jóvenes']*100}%"
            ]
        })
        st.table(df_jovenes)
        
    with col_ltv2:
        st.subheader("Segmento Adultos Mayores (Senior) - Simulación Dinámica")
        # Calculamos el LTV dinámico en base al aporte simulado y el plazo simulado
        dynamic_ltv_senior = mrr_per_user_sim * months_sim
        dynamic_ratio_senior = dynamic_ltv_senior / unit_economics_static['CAC Senior']
        
        df_seniors = pd.DataFrame({
            "Métrica": ["Costo de Adquisición (CAC)", "LTV Simulado (Plazo de Proyecto)", "LTV / CAC Ratio Simulado", "Churn Rate", "Mensualidad Simulada"],
            "Valor": [
                f"${unit_economics_static['CAC Senior']:,.2f} COP",
                f"${dynamic_ltv_senior:,.2f} COP",
                f"{dynamic_ratio_senior:,.2f}x",
                f"{unit_economics_static['Churn Rate Adultos Mayores']*100}%",
                f"${mrr_per_user_sim:,.2f} COP"
            ]
        })
        st.table(df_seniors)

    st.markdown("💡 **Ratio de Subsidio Cruzado (RSC):** {:.2f} (El margen de contribución de un senior subsidia de manera óptima el costo variable de un joven)".format(unit_economics_static["Ratio Subsidio Cruzado (RSC)"]))

# TAB 2: BURN RATE & PROJECTIONS
with tab2:
    st.markdown('<h3 class="section-header">Análisis Comparativo: Burn Rate Actual vs Proyectado</h3>', unsafe_allow_html=True)
    
    col_burn1, col_burn2 = st.columns(2)
    
    with col_burn1:
        st.subheader("Gross Burn Rate Actual")
        actual_items = list(gross_burn_actual.items())[:-1]
        df_actual = pd.DataFrame(actual_items, columns=["Ítem de Costo", "Valor COP / Mes"])
        st.dataframe(df_actual.style.format({"Valor COP / Mes": "${:,.2f}"}))
        st.info(f"**Total Mensual Actual:** ${gross_burn_actual['Total Mensual Actual']:,.2f} COP")

    with col_burn2:
        st.subheader("Gross Burn Rate Proyectado")
        proy_items = list(gross_burn_proyectado.items())[:-1]
        df_proy = pd.DataFrame(proy_items, columns=["Ítem de Costo Proyectado", "Valor COP / Mes"])
        st.dataframe(df_proy.style.format({"Valor COP / Mes": "${:,.2f}"}))
        st.warning(f"**Total Mensual Proyectado (con nómina):** ${gross_burn_proyectado['Total Mensual Proyectado']:,.2f} COP")

    # Bar chart comparing the two
    burn_chart_data = pd.DataFrame({
        "Estado": ["Actual", "Proyectado"],
        "Burn Rate Mensual ($ COP)": [gross_burn_actual['Total Mensual Actual'], gross_burn_proyectado['Total Mensual Proyectado']]
    })
    st.bar_chart(burn_chart_data.set_index("Estado"))

# TAB 3: OPERATING REVENUE & TRACCION
with tab3:
    st.markdown('<h3 class="section-header">Ingresos Operativos Iniciales (Cuotas de Separación)</h3>', unsafe_allow_html=True)
    
    col_adv, col_adv_chart = st.columns([1, 1])
    
    with col_adv:
        st.write("Aportes Iniciales de Advisors contratados para el proyecto:")
        adv_items = list(ingresos_operativos.items())[:-1]
        df_adv = pd.DataFrame(adv_items, columns=["Advisor / Inversionista", "Cuota de Separación"])
        st.dataframe(df_adv.style.format({"Cuota de Separación": "${:,.2f}"}))
        st.success(f"**Total Capital Inicial Recaudado:** ${ingresos_operativos['Total Inicial']:,.2f} COP")
        
    with col_adv_chart:
        st.metric(label="Total de Advisors Participantes", value="8 Activos")
        st.metric(label="Cuota de Separación Estándar", value="$40,000,000 COP")
        st.progress(0.8) # Representative progress toward standard capitalization goals

# TAB 4: ENVIRONMENTAL METRICS & TOTAL VALUE
with tab4:
    st.markdown('<h3 class="section-header">Métricas de Sostenibilidad y Carbono (Calima)</h3>', unsafe_allow_html=True)
    
    col_env1, col_env2 = st.columns(2)
    
    with col_env1:
        st.write("🌳 **Métricas de Captura (50 Hectáreas de Reserva):**")
        st.write(f"- **Área de Reserva Total:** {unit_economics_static['Área de Reserva (m²)']:,} m²")
        st.write(f"- **Tasa de captura por Ha:** {unit_economics_static['Tons CO2 por Hectárea / Año']} toneladas/año")
        st.write(f"- **Total CO2 Capturado Anual:** {unit_economics_static['Total Toneladas de Carbono Año Capturadas']} toneladas")
        
    with col_env2:
        st.write("📊 **Mercado Potencial (TAM / SAM / SOM):**")
        st.metric("TAM (Total Addressable Market)", f"${unit_economics_static['TAM (Mercado Total Direccionable)']:,.1e} COP")
        st.metric("SAM (Serviceable Addressable Market)", f"${unit_economics_static['SAM (Mercado Disponible Servido)']:,.1e} COP")
        st.metric("SOM (Serviceable Obtainable Market)", f"${unit_economics_static['SOM (Mercado Objetivo Capturable)']:,.2f} COP")

    st.markdown('<h3 class="section-header">Análisis de Sensibilidad de Ingresos en Tiempo Real</h3>', unsafe_allow_html=True)
    
    # Análisis dinámico interactivo en base a la simulación actual
    st.markdown(f"""
    **Análisis de Sensibilidad de la Meta de Recaudo:**
    * **Aporte Individual Mensual:** `${mrr_per_user_sim:,.2f} COP`
    * **MRR Total Simulado:** `${simulated_mrr:,.2f} COP`
    * **ARR Total Simulado (Ingreso Anualizado):** `${simulated_arr:,.2f} COP`
    * **Recaudo Proyectado a {months_sim} meses:** `${total_recaudo_proyectado:,.2f} COP`
    
    """)
    if total_recaudo_proyectado >= meta_recaudo:
        st.success(f"🎉 ¡Escenario Viable! Con este aporte mensual, superas la meta de recaudo de 32,000 millones por **${brecha_meta:,.2f} COP**.")
    else:
        st.error(f"⚠️ Escenario Insuficiente. Faltan **${abs(brecha_meta):,.2f} COP** para alcanzar la meta de 32,000 millones. Considera aumentar el aporte por usuario o extender el plazo.")