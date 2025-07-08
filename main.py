import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from matplotlib import cm


df = pd.read_csv("assets/sleep_health_and_lifestyle_dataset.csv")

st.title("🛌 Sleep Health and Lifestyle Dataset")

st.caption("Let's explore the dataset using pandas and Streamlit.")

st.divider()

st.subheader("First 5 Rows")
st.dataframe(df.head())

st.subheader("Last 5 Rows")
st.dataframe(df.tail())

st.divider()

st.subheader("First 5 Rows Where Gender is 🟠 Male")
filtered_df = df[df['Gender'].str.lower() == 'male']
st.dataframe(filtered_df.head())

st.divider()

genders = ['All'] + df['Gender'].dropna().unique().tolist()
selected_gender = st.selectbox("Select Gender", genders)
row_position = st.radio("Show first or last rows?", ['First', 'Last'])
num_rows = st.slider("Number of rows to show", 1, 20, 5)

if selected_gender != 'All':
    filtered_df = df[df['Gender'].str.lower() == selected_gender.lower()]
else:
    filtered_df = df

display_df = filtered_df.head(num_rows) if row_position == 'First' else filtered_df.tail(num_rows)
st.subheader(f"{row_position} {num_rows} rows for gender: {selected_gender}")
st.dataframe(display_df)

st.divider()

st.subheader("People Who Sleep Better (Highest Quality of Sleep)")
if not filtered_df.empty:
    max_quality = filtered_df['Quality of Sleep'].max()
    best_sleepers = filtered_df[filtered_df['Quality of Sleep'] == max_quality]
    st.write(f"Highest Quality of Sleep: {max_quality}")
    st.dataframe(best_sleepers[['Person ID', 'Gender', 'Age', 'Occupation', 'Sleep Duration', 'Quality of Sleep']])
else:
    st.info("No data available for the selected filters.")

st.divider()

st.subheader("Sleep Quality Analysis by Gender")
sleep_summary = df.groupby('Gender')[['Quality of Sleep', 'Sleep Duration']].mean().round(2).reset_index()
st.dataframe(sleep_summary)

best_quality = sleep_summary.loc[sleep_summary['Quality of Sleep'].idxmax()]
best_duration = sleep_summary.loc[sleep_summary['Sleep Duration'].idxmax()]
st.success(f"🛌 Best sleep quality: {best_quality['Gender']} — {best_quality['Quality of Sleep']}")
st.info(f"⏰ Longest sleep duration: {best_duration['Gender']} — {best_duration['Sleep Duration']} hrs")

st.divider()

st.subheader("Sleep Quality Analysis by Occupation")
occupation_summary = df.groupby('Occupation')[['Quality of Sleep', 'Sleep Duration']].mean().round(2).reset_index()
st.dataframe(occupation_summary)

best_occ = occupation_summary.loc[occupation_summary['Quality of Sleep'].idxmax()]
longest_sleep_occ = occupation_summary.loc[occupation_summary['Sleep Duration'].idxmax()]
st.success(f"🛌 Best average sleep quality: {best_occ['Occupation']} — {best_occ['Quality of Sleep']}")
st.info(f"⏰ Longest average sleep duration: {longest_sleep_occ['Occupation']} — {longest_sleep_occ['Sleep Duration']} hrs")

st.divider()

st.subheader("Physical Activity Level by Gender")
pa_gender = df.groupby('Gender')['Physical Activity Level'].mean().round(2).reset_index()
st.dataframe(pa_gender)
best_pa_gender = pa_gender.loc[pa_gender['Physical Activity Level'].idxmax()]
st.success(f"🏃‍♂️ Most active gender: {best_pa_gender['Gender']} — {best_pa_gender['Physical Activity Level']}")

st.divider()

st.subheader("Physical Activity Level by Occupation")
pa_occupation = df.groupby('Occupation')['Physical Activity Level'].mean().round(2).reset_index()
st.dataframe(pa_occupation)
best_pa_occ = pa_occupation.loc[pa_occupation['Physical Activity Level'].idxmax()]
st.success(f"🏃‍♀️ Most active occupation: {best_pa_occ['Occupation']} — {best_pa_occ['Physical Activity Level']}")

st.divider()

st.subheader("Stress Level by Gender")
stress_gender = df.groupby('Gender')['Stress Level'].mean().round(2).reset_index()
st.dataframe(stress_gender)

most_stressed_gender = stress_gender.loc[stress_gender['Stress Level'].idxmax()]
least_stressed_gender = stress_gender.loc[stress_gender['Stress Level'].idxmin()]
st.warning(f"😟 Most stressed: {most_stressed_gender['Gender']} — {most_stressed_gender['Stress Level']}")
st.success(f"😊 Least stressed: {least_stressed_gender['Gender']} — {least_stressed_gender['Stress Level']}")

st.divider()

st.subheader("Stress Level by Occupation")
stress_occupation = df.groupby('Occupation')['Stress Level'].mean().round(2).reset_index()
st.dataframe(stress_occupation)

most_stressed_occ = stress_occupation.loc[stress_occupation['Stress Level'].idxmax()]
least_stressed_occ = stress_occupation.loc[stress_occupation['Stress Level'].idxmin()]
st.warning(f"💼 Most stressful job: {most_stressed_occ['Occupation']} — {most_stressed_occ['Stress Level']}")
st.success(f"🧘 Least stressful job: {least_stressed_occ['Occupation']} — {least_stressed_occ['Stress Level']}")

st.divider()

st.subheader("Stress Level by Gender (Bar Chart)")
colors = ['red' if val == stress_gender['Stress Level'].max()
          else 'green' if val == stress_gender['Stress Level'].min()
          else 'gray' for val in stress_gender['Stress Level']]

fig1, ax1 = plt.subplots()
ax1.bar(stress_gender['Gender'], stress_gender['Stress Level'], color=colors)
ax1.set_ylabel("Average Stress Level")
ax1.set_title("Average Stress Level by Gender")
st.pyplot(fig1)

st.divider()

st.subheader("Stress Level by Occupation (Low ➜ High)")
sorted_stress_occ = stress_occupation.sort_values('Stress Level').reset_index(drop=True)

num_items = len(sorted_stress_occ)
colors = [cm.get_cmap('RdYlGn_r')(i / (num_items - 1)) for i in range(num_items)]

fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.barh(sorted_stress_occ['Occupation'], sorted_stress_occ['Stress Level'], color=colors)
ax2.set_xlabel("Average Stress Level")
ax2.set_title("Stress Level by Occupation (Green ➜ Red)")
st.pyplot(fig2)

st.divider()

st.subheader("Stress vs. Quality of Sleep")
fig3 = px.scatter(
    df,
    x='Stress Level',
    y='Quality of Sleep',
    color='Gender',
    title='Stress Level vs. Quality of Sleep',
    opacity=0.7,
    hover_data=['Occupation'],
    color_discrete_map={
        'Male': 'darkblue',
        'Female': 'pink'
    }
)
st.plotly_chart(fig3)

st.divider()
