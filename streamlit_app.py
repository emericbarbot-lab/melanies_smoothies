# Import python packages
import streamlit as st
import os
from snowflake.snowpark.functions import col
import requests
import pandas as pd


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
my_dataframe=session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()
                                                    
ingredients_list=st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe
)
        
if ingredients_list:
    ingredients_string=''
    for fruit_chosen in ingredients_list:
      ingredients_string+=ingredient+ ' '
      
      search_on=pd_df.loc[pd_df[fruit_name]==fruit_chosen,'SEARCH_ON'].iloc[0]

      
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
      #st.text(smoothiefroot_response.json)
      sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
      st.write('the search value for', fruit_chosen,' is ', search_on, '.')

  
    for ingredient in ingredients_list:
    st.write(ingredients_string)

    my_insert_stmt = f"""insert into smoothies.public.orders(ingredients, name_on_order)
            values ('{ingredients_string}', '{name_of_order}')"""


    

    time_to_insert=st.button('summit order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



