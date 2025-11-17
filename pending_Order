# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched
session = get_active_session()

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders :cat:")
st.write("Oders that needed to be filled **Smoothies!** ")

my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==False).collect()
#editable_df = st.data_editor(my_dataframe)

if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')

    if submitted:

        og_dataset= session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        
        try:
            og_dataset.merge(edited_dataset
                        , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                        , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                        )
            st.success("Someone clicked the button",icon = '👍')
        except:
            st.write('Somthing went wrong.')

else:
    st.success('There are no pending orders right now',icon = '👍')
    
        # og_dataset = session.table("smoothies.public.orders")
        # edited_dataset = session.create_dataframe(editable_df)
        # og_dataset.merge(edited_dataset
        #                 , (

