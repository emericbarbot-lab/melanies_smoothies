# Import python packages
import streamlit as st
import os
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_of_order=st.text_input('Name of smoothie:')
st.write('The name of the smoothie will be: ', name_of_order)


option=st.selectbox(
    "What's your favorite fruit?",
    ('Banana','stawberries','Peaches')
)

st.write('You selected:', option )

cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe=session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe
)

if ingredients_list:
    ingredients_string=''
    for ingredient in ingredients_list:
        ingredients_string+=ingredient+ ' '
    st.write(ingredients_string)

    my_insert_stmt = f"""insert into smoothies.public.orders(ingredients, name_on_order)
            values ('{ingredients_string}', '{name_of_order}')"""


    

    time_to_insert=st.button('summit order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


    import requests  
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
    st.text(smoothiefroot_response)
