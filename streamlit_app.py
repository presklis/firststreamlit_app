import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


#CSV
streamlit.title('My Parents New Healty Dinner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
streamlit.dataframe(fruits_selected)

#API

def fruit_advice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized


streamlit.header("Fruityvice Fruit Advice!")

#new section to display fruityvice api
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    back_from_function = fruit_advice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
  
#streamlit.write('The user entered ', fruit_choice)
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#streamlit.text(fruityvice_response.json())
# write your own comment -what does the next line do? 
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
#streamlit.dataframe(fruityvice_normalized)
#streamlit.stop()

#SNOWFLAKE
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM fruit_load_list")
        return my_cur.fetchall()

    streamlit.header("Fruit Information")

if streamlit.button('Get Fruit Load List'):
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        my_data_rows = get_fruit_load_list()
        my_cnx.close();
        streamlit.dataframe(my_data_rows)
        
#allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('"+new_fruit+"')")
        return "thanks for adding " + new_fruit
 
add_my_fruit = streamlit.text_input('What fruit to add?')
if streamlit.button('Add a Fruit to the list'):
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        back_from_function = insert_row_snowflake(add_my_fruit)
        streamlit.text(back_from_function)
    
#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
#my_data_rows = my_cur.fetchall()
#add_my_fruit = streamlit.text_input('What fruit would you like to information about?')
#streamlit.write('Thanks for adding a new fruit',add_my_fruit)
#my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('from streamlit')")
#streamlit.dataframe(my_data_rows)
