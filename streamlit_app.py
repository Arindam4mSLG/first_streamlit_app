import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title ('My Parents New Healthy Diner..')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# New sction

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruits_asked)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list ")
    return my_cur.fetchall()
  

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruits_asked = streamlit.text_input("Fruit Asked")
  if not fruits_asked:
    streamlit.error("Please enter a fruit")
  else:
      streamlit.text("You entered:" + fruits_asked)
      tabFruits = get_fruityvice_data(fruits_asked)
      # write your own comment - what does this do?
      streamlit.dataframe(tabFruits)
except URLError as e:
  streamlit.error()

# streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

streamlit.header("The fruit load list:")
my_data_rows = get_fruit_load_list()
streamlit.dataframe(my_data_rows)

fruits_2b_added = streamlit.text_input("Fruit Asked","")
if fruits_2b_added is None or fruits_asked == "" :
  streamlit.text("blank")
else:
  my_cur.execute("insert into fruit_load_list values('From Streamlite')")
