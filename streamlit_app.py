# Import python packages.
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app.
st.title(":cup_with_straw: Customise Your Smoothie!:cup_with_straw:")
st.write(" Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:',name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table(
    "smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()

# ✅ multiselect must receive a list, not a Snowpark DataFrame
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe['FRUIT_NAME'].tolist(),
    max_selections=5
)

if ingredients_list:
        
    ingredients_string =''
    
    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen+' '

   

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('"""+ingredients_string+"""','"""+name_on_order+"""')"""
    st.write(my_insert_stmt)
    

    
    time_to_insert=st.button('Submit Order')
    if time_to_insert:
        
        session.sql(my_insert_stmt, params=[ingredients_string.strip()]).collect()


        st.success('Your Smoothie is ordered!', icon="✅")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
st.text(smoothiefroot_response.json())
#st.json(smoothiefroot_response.json())
