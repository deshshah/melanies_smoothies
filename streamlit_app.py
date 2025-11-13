import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# App title
st.title(":cup_with_straw: Customise Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom **Smoothie!**")

# Name input
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Load data from Snowflake
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()

# ✅ Normalise column names to lowercase for safe access
pd_df.columns = [c.lower() for c in pd_df.columns]

# Diagnostic: Show columns and preview
st.write("Columns in DataFrame:", pd_df.columns.tolist())
st.write("Preview of data:", pd_df.head())

# Multiselect for ingredients
ingredients_list = st.multiselect("Choose up to 5 ingredients:", pd_df['fruit_name'].tolist(), max_selections=5)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        # ✅ Safe lookup: If 'search_on' exists, use it; else fallback to fruit_name
        if 'search_on' in pd_df.columns:
            search_on = pd_df.loc[pd_df['fruit_name'] == fruit_chosen, 'search_on'].iloc[0]
        else:
            search_on = fruit_chosen  # fallback

        st.write(f'The search value for {fruit_chosen} is {search_on}.')

        # Nutrition info
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # Insert order into Snowflake
    my_insert_stmt = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS(ingredients, name_on_order)
        VALUES ('{ingredients_string.strip()}', '{name_on_order}')
    """

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
