RCH_ONimport streamlit as st
from snowflake.snowpark.functions import col
import requests

cnx = st.connection("snowflake")
session = cnx.session()

st.title(":cup_with_straw: Customise Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom **Smoothie!**")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('SEARCH_ON'))
#st.dataframe(data =my_dataframe, use_container_width =True)
#st.stop()

#fruit_list = fruit_df.to_pandas()['fruit_name'].tolist()
pd_df=my_dataframe.to_pandas()
#fruit_list = pd_df['fruit_name'].tolist()
#st.dataframe(pd_df)
#st.stop()
ingredients_list = st.multiselect("Choose up to 5 ingredients:", my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
            ingredients_string += fruit_chosen + ' '
            search_on=pd_df.loc[pd_df['fruit_name'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
            st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

            st.subheader(fruit_chosen + ' Nutrition Information')
            smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
            # st.text(smoothiefroot_response.json())
            sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
            my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

            time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")


    
