import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


st.markdown(
    """
    <style>
    /* Slider track and thumb */
    .stSlider > div > div > div > div[role="slider"] {
        background-color: #4CAF50 !important;  /* green thumb */
    }
    .stSlider > div > div > div > div[role="presentation"] {
        background-color: #A5D6A7 !important;  /* lighter green track */
    }

    /* Radio buttons selected label text color */
    div[role="radiogroup"] label[data-state="checked"] > div {
        color: #4CAF50 !important;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

df = pd.read_csv("assets/sleep_health_and_lifestyle_dataset.csv")


st.markdown(
    """
    <h2 style='text-align: center; 
               color: #4CAF50; 
               font-size: 48px; 
               font-weight: bold;
               margin-bottom: -25px;
               text-shadow: 0 0 10px #FFD700, 
               0 0 20px #FFD700, 
               0 0 20px #FFC107;'>
        Sleep Health and Lifestyle Dataset
    </h2>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h2 style='text-align: center; 
               color: black; 
               font-size: 23px; 
               margin-top: -25px;
               font-style: italic;'>
        Let's get started with pandas in Streamlit!
    </h2>
    """,
    unsafe_allow_html=True
)

st.subheader("First 5 Rows")
st.dataframe(df.head(5))

st.divider()

st.subheader("Last 5 Rows")
st.dataframe(df.tail(5))

st.divider()

st.markdown(
    """
    <h1 style='font-size: 36px;'>
        First 5 Rows Where Gender is <span style='color: orange;'>Male</span>
    </h1>
    """,
    unsafe_allow_html=True
)

filtered_df = df[df['Gender'].str.lower() == 'male']
st.dataframe(filtered_df.head(5))

genders = df['Gender'].dropna().unique().tolist()
genders = ['All'] + genders

st.divider()

selected_gender = st.selectbox("Select Gender", genders)

row_position = st.radio("Show first or last rows?", ['First', 'Last'])

num_rows = st.slider("Number of rows to show", min_value=1, max_value=20, value=5)

if selected_gender != 'All':
    filtered_df = df[df['Gender'].str.lower() == selected_gender.lower()]
else:
    filtered_df = df

if row_position == 'First':
    display_df = filtered_df.head(num_rows)
else:
    display_df = filtered_df.tail(num_rows)

st.divider()

st.subheader(f"Showing {row_position.lower()} {num_rows} rows for gender: {selected_gender}")
st.dataframe(display_df)

st.divider()

st.subheader("People Who Sleep Better (Highest Quality of Sleep)")

if filtered_df.empty:
    st.write("No data available for the selected filters.")
else:
    max_quality = filtered_df['Quality of Sleep'].max()
    best_sleepers = filtered_df[filtered_df['Quality of Sleep'] == max_quality]

    st.write(f"Highest Quality of Sleep: {max_quality}")
    st.dataframe(best_sleepers[['Person ID', 'Gender', 'Age', 'Occupation', 'Sleep Duration', 'Quality of Sleep']])

st.divider()

st.subheader("Sleep Quality Analysis by Gender")

sleep_data = df[['Gender', 'Quality of Sleep', 'Sleep Duration']].dropna()

sleep_summary = sleep_data.groupby('Gender').agg({
    'Quality of Sleep': 'mean',
    'Sleep Duration': 'mean'
}).reset_index()

sleep_summary['Quality of Sleep'] = sleep_summary['Quality of Sleep'].round(2)
sleep_summary['Sleep Duration'] = sleep_summary['Sleep Duration'].round(2)

st.dataframe(sleep_summary)

best_quality = sleep_summary.loc[sleep_summary['Quality of Sleep'].idxmax()]
st.write(f"🛌 The gender with better average sleep quality is **{best_quality['Gender']}** with a score of {best_quality['Quality of Sleep']}.")

best_duration = sleep_summary.loc[sleep_summary['Sleep Duration'].idxmax()]
st.write(f"⏰ The gender with longer average sleep duration is **{best_duration['Gender']}** with {best_duration['Sleep Duration']} hours on average.")

st.divider()

st.subheader("Sleep Quality Analysis by Occupation")

sleep_occupation_data = df[['Occupation', 'Quality of Sleep', 'Sleep Duration']].dropna()

sleep_occupation_summary = sleep_occupation_data.groupby('Occupation').agg({
    'Quality of Sleep': 'mean',
    'Sleep Duration': 'mean'
}).reset_index()

sleep_occupation_summary['Quality of Sleep'] = sleep_occupation_summary['Quality of Sleep'].round(2)
sleep_occupation_summary['Sleep Duration'] = sleep_occupation_summary['Sleep Duration'].round(2)

st.dataframe(sleep_occupation_summary)

best_quality_occupation = sleep_occupation_summary.loc[sleep_occupation_summary['Quality of Sleep'].idxmax()]
st.write(f"🛌 The occupation with the best average sleep quality is **{best_quality_occupation['Occupation']}** with a score of {best_quality_occupation['Quality of Sleep']}.")

best_duration_occupation = sleep_occupation_summary.loc[sleep_occupation_summary['Sleep Duration'].idxmax()]
st.write(f"⏰ The occupation with the longest average sleep duration is **{best_duration_occupation['Occupation']}** with {best_duration_occupation['Sleep Duration']} hours on average.")

st.divider()

st.subheader("Physical Activity Level Analysis by Gender")

pa_gender_data = df[['Gender', 'Physical Activity Level']].dropna()

pa_gender_summary = pa_gender_data.groupby('Gender')['Physical Activity Level'].mean().reset_index()

pa_gender_summary['Physical Activity Level'] = pa_gender_summary['Physical Activity Level'].round(2)

st.dataframe(pa_gender_summary)

best_pa_gender = pa_gender_summary.loc[pa_gender_summary['Physical Activity Level'].idxmax()]
st.write(f"🏃‍♂️ The gender with the highest average physical activity level is **{best_pa_gender['Gender']}** with a level of {best_pa_gender['Physical Activity Level']}.")

st.divider()

st.subheader("Physical Activity Level Analysis by Occupation")

pa_occupation_data = df[['Occupation', 'Physical Activity Level']].dropna()

pa_occupation_summary = pa_occupation_data.groupby('Occupation')['Physical Activity Level'].mean().reset_index()

pa_occupation_summary['Physical Activity Level'] = pa_occupation_summary['Physical Activity Level'].round(2)

st.dataframe(pa_occupation_summary)

best_pa_occupation = pa_occupation_summary.loc[pa_occupation_summary['Physical Activity Level'].idxmax()]
st.write(f"🏃‍♀️ The occupation with the highest average physical activity level is **{best_pa_occupation['Occupation']}** with a level of {best_pa_occupation['Physical Activity Level']}.")

st.divider()

st.subheader("Stress Level Analysis by Gender")

stress_gender_data = df[['Gender', 'Stress Level']].dropna()

stress_gender_summary = stress_gender_data.groupby('Gender')['Stress Level'].mean().reset_index()

stress_gender_summary['Stress Level'] = stress_gender_summary['Stress Level'].round(2)

st.dataframe(stress_gender_summary)

most_stressed_gender = stress_gender_summary.loc[stress_gender_summary['Stress Level'].idxmax()]
least_stressed_gender = stress_gender_summary.loc[stress_gender_summary['Stress Level'].idxmin()]

st.write(f"😟 The most stressed gender is **{most_stressed_gender['Gender']}** with an average level of {most_stressed_gender['Stress Level']}.")
st.write(f"😊 The least stressed gender is **{least_stressed_gender['Gender']}** with an average level of {least_stressed_gender['Stress Level']}.")

st.divider()

st.subheader("Stress Level Analysis by Occupation")

stress_occupation_data = df[['Occupation', 'Stress Level']].dropna()

stress_occupation_summary = stress_occupation_data.groupby('Occupation')['Stress Level'].mean().reset_index()

stress_occupation_summary['Stress Level'] = stress_occupation_summary['Stress Level'].round(2)

st.dataframe(stress_occupation_summary)

most_stressed_job = stress_occupation_summary.loc[stress_occupation_summary['Stress Level'].idxmax()]
least_stressed_job = stress_occupation_summary.loc[stress_occupation_summary['Stress Level'].idxmin()]

st.write(f"💼 The most stressful occupation is **{most_stressed_job['Occupation']}** with an average level of {most_stressed_job['Stress Level']}.")
st.write(f"🧘 The least stressful occupation is **{least_stressed_job['Occupation']}** with an average level of {least_stressed_job['Stress Level']}.")

st.divider()

st.subheader("Stress Level by Gender (Bar Chart)")

colors = []
max_val = stress_gender_summary['Stress Level'].max()
min_val = stress_gender_summary['Stress Level'].min()

for val in stress_gender_summary['Stress Level']:
    if val == max_val:
        colors.append('red')
    elif val == min_val:
        colors.append('green')
    else:
        colors.append('gray')  # Optional for multiple genders)))

fig1, ax1 = plt.subplots()
ax1.bar(stress_gender_summary['Gender'], stress_gender_summary['Stress Level'], color=colors)
ax1.set_ylabel("Average Stress Level")
ax1.set_title("Average Stress Level by Gender")
st.pyplot(fig1)


st.divider()

st.subheader("Stress Level by Occupation (Bar Chart)")

colors = []
max_val_occ = stress_occupation_summary['Stress Level'].max()
min_val_occ = stress_occupation_summary['Stress Level'].min()

for val in stress_occupation_summary['Stress Level']:
    if val == max_val_occ:
        colors.append('red')
    elif val == min_val_occ:
        colors.append('green')
    else:
        colors.append('gray')

fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.barh(stress_occupation_summary['Occupation'], stress_occupation_summary['Stress Level'], color=colors)
ax2.set_xlabel("Average Stress Level")
ax2.set_title("Average Stress Level by Occupation")
st.pyplot(fig2)

st.divider()
