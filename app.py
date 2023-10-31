import streamlit as st
import pandas as pd
import numpy as np
# import joblib
import altair as alt

st.set_page_config(
    page_title="Predict Information Systems Students Income",
    layout="wide"
)

st.title('Predict Students Income')
url_editor_1 = "https://www.linkedin.com/in/marselius-agus-dhion/"
url_editor_2 = "https://www.linkedin.com/in/davidkurniawan947/"
st.markdown(f'Streamlit App by [Marselius Agus Dhion]({url_editor_1}) | [David Kurniawan]({url_editor_2})', unsafe_allow_html=True)

url_repo = "https://github.com/TheOX7/WIT"
st.markdown(f'GitHub Repository : {url_repo}', unsafe_allow_html=True)

st.write('____________')

df = pd.read_excel('WIT_2.xlsx')
df = df.set_index(df.index + 1)

tab_1, tab_2, tab_3 = st.tabs(['Dataset Overview', 'Dataset Insights', 'Predict Income'])

with tab_1 :

    st.subheader('Information Systems Student 2021 - Dataset')
    st.dataframe(df, use_container_width=True)
    st.write("""
             Data diatas ini merupakan data mahasiswa Sistem Informasi angkatan 2021 yang mengambil mata kuliah Manajemen Hubungan Pelanggan. \n
             Dimana untuk datanya sendiri terdapat kolom-kolom yang diisi secara random menggunakan library bernama "Faker", kolom tersebut seperti "Pendapatan", "Asuransi", dan "Umur". \n
             Sedangkan sisanya merupakan informasi asli dari mahasiswa tersebut, yaitu kolom "NRP", "Status", "Kota", dan "Gender" 
             """)
    
with tab_2:
    # Barchart perbandingan jumlah Laki-laki dan Perempuan
    st.subheader("Perbandingan Jumlah Laki-Laki dan Perempuan")
    gender_counts = df["Gender"].value_counts().reset_index()
    gender_counts.columns = ["Gender", "Count"]
    gender_counts["Color"] = gender_counts["Gender"].apply(lambda x: "Biru" if x == "L" else "Pink")

    chart = alt.Chart(gender_counts).mark_bar().encode(
        x=alt.X("Gender:N", title="Gender", axis=alt.Axis(labelAngle=360)),
        y=alt.Y("Count:Q", title="Jumlah", scale=alt.Scale(domain=[0, 20])),
        color=alt.Color("Color:N", scale=alt.Scale(domain=["Biru", "Pink"], range=["blue", "pink"]))
    )
    st.altair_chart(chart, use_container_width=True)

    # Scatterplot Persebaran Pendapatan
    st.subheader("Persebaran Pendapatan Mahasiswa")
    scatter = alt.Chart(df).mark_circle(size=100).encode(
        x=alt.X("NRP:N", title="NRP", axis=alt.Axis(labelAngle=360)),
        y=alt.Y("Pendapatan:Q", title="Pendapatan", scale=alt.Scale(zero=False)),
        color=alt.Color("Gender:N", scale=alt.Scale(domain=["L", "P"], range=["blue", "pink"])),
        tooltip=["Nama", "NRP", "Pendapatan"]
    )

    st.altair_chart(scatter, use_container_width=True)
    
    # Barchart perbandingan kota
    st.subheader("Perbandingan Jumlah Asal Kota Mahasiswa")
    city_counts = df["Kota"].value_counts().reset_index()
    city_counts.columns = ["Kota", "Jumlah"]
    city_colors = {
        "Cirebon": "red",
        "Bandung": "blue",
        "Bogor": "green",
        "Jakarta": "purple",
        "Tasikmalaya": "orange",
        "Surakarta": "pink",
        "Medan": "gray",
        "Pontianak": "brown",
        "Batam": "cyan",
        "Toraja": "magenta"
    }

    city_counts["Color"] = city_counts["Kota"].map(city_colors)
    chart_city = alt.Chart(city_counts).mark_bar().encode(
        x=alt.X("Kota:N", title="Kota", sort="-y"),
        y=alt.Y("Jumlah:Q", title="Jumlah", scale=alt.Scale(domain=[0, 15])),
        color=alt.Color("Kota:N", scale=alt.Scale(range=list(city_colors.values())))
    )
    st.altair_chart(chart_city, use_container_width=True)
    

    
with tab_3 :
    model = ('model_predict_income.joblib')
    st.subheader('Predict Students Income')
    
    # Mapping Gender
    gender_mapping = {
        0: 'Laki-laki',
        1: 'Perempuan'
    }

    # Mapping Kota
    kota_mapping = {
        0: 'Bandung',
        1: 'Batam',
        2: 'Bogor',
        3: 'Cirebon',
        4: 'Jakarta',
        5: 'Medan',
        6: 'Pontianak',
        7: 'Surakarta',
        8: 'Tasikmalaya',
        9: 'Toraja'
    }

    # Input Gender
    input_gender = st.selectbox('Pilih Gender', list(gender_mapping.values()))
    original_gender = [key for key, value in gender_mapping.items() if value == input_gender][0]

    # Input Kota
    input_kota = st.selectbox('Pilih Kota', list(kota_mapping.values()))
    original_kota = [key for key, value in kota_mapping.items() if value == input_kota][0]

    # Input Umur
    input_umur = st.slider('Umur', min_value=19, max_value=21, step=1)

    # MinMax Scaling untuk inputan Umur
    min_value_umur = 19
    max_value_umur = 21
    scaled_umur = (input_umur - min_value_umur) / (max_value_umur - min_value_umur)

    # Prediksi yang sudah diinput
    prediction = model.predict([[original_gender, original_kota, scaled_umur]])

    # Tombol untuk prediksi
    if st.button('Prediksi'):
        input_data = np.array([[original_gender, original_kota, scaled_umur]])
        prediction = model.predict(input_data)
        
        min_pendapatan = 1500000
        max_pendapatan = 3000000
        
        minmax_scaled_result = prediction[0]
        original_result = (minmax_scaled_result * (max_pendapatan - min_pendapatan)) + min_pendapatan
        original_result = f'Rp. {original_result / 1e6:.2f} juta'
        st.success(f'Hasil Prediksi: {(original_result)}')   