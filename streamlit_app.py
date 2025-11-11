import streamlit as st
from snowflake.snowpark.functions import col
import requests


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

if ingradients_lists: 
   ingredients_string =''

    for fruit_chosen in ingradients_lists:
        ingredients_string += fruit_chosen + ' '
       my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
           values ('""" +ingredients_string+ """','""" +name_on_order+ """')"""

        time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

    
