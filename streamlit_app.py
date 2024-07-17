import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie! 
    """
)

 

from snowflake.snowpark.functions import col

Name_on_order = st.text_input("Name on Smoothie :" )
st.write("The Name on your Smoothie will be", Name_on_order)
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
# st.dataframe(data=my_dataframe, use_container_width=True)
ingredient_list=st.multiselect(
    'Choose Upto 5 Ingredients :'
    ,my_dataframe
    ,max_selections=5
)

if ingredient_list:
   ingredients_string=''
   for fruit_choosen in ingredient_list:
     ingredients_string +=fruit_choosen+' '
     # st.write(ingredients_string)

   my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Name_on_order)
            values ('""" + ingredients_string + """','""" + Name_on_order+ """')"""

   # st.write(my_insert_stmt)
   # st.stop()
   time_to_insert=st.button('submit order')
   if time_to_insert: 
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")




