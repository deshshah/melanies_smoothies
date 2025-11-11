import streamlit as st
from snowflake.snowpark.functions import col

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

st.title(":cup_with_straw: Customise Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom **Smoothie!**")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

fruit_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
fruit_list = fruit_df.to_pandas()['FRUIT_NAME'].tolist()

ingredients_selected = st.multiselect("Choose up to 5 ingredients:", fruit_list, max_selections=5)

if ingredients_selected and st.button('Submit Order'):
    ingredients_string = ' '.join(ingredients_selected)
    session.sql(
        "INSERT INTO smoothies.public.orders(ingredients, name_on_order) VALUES (?, ?)",
        params=[ingredients_string, name_on_order]
    ).collect()
    st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
