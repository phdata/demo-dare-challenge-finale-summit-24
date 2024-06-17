import streamlit as st
import subprocess
import os
from snowflake.snowpark import Session
from datetime import datetime


@st.cache_data
def get_login_token():
    with open("/snowflake/session/token", "r") as f:
        return f.read()

def get_snowflake_connection():
    snowpark_config = {
        "account": os.environ.get("SNOWFLAKE_ACCOUNT"),
        "host": os.environ.get("SNOWFLAKE_HOST"),
        "authenticator": "oauth",
        "token": get_login_token(),
        "warehouse": os.environ.get("SNOWFLAKE_WAREHOUSE"),
        "database": os.environ.get("SNOWFLAKE_DATABASE"),
        "schema": os.environ.get("SNOWFLAKE_SCHEMA")
     }
    return Session.builder.configs(snowpark_config).create()

def get_images_from_stage():
    get_snowflake_connection().sql("GET @DOOM_SCREENSHOTS file:///;").show()

@st.cache_data
def run_setup():
    get_images_from_stage()
    subprocess.Popen(["ollama", "serve"])
    get_snowflake_connection().sql(
        '''
            CREATE TABLE IF NOT EXISTS image_analysis (
                model_name STRING,
                image_name STRING,
                prompt STRING,
                response STRING,
                insert_time TIMESTAMP
            );
        '''
    ).show()



#top text
st.write("## Data Operations and Observability in Manufacturing _with AI_ ##")

#initial loading
run_setup()
image_list = [file for file in os.listdir(".") if file.endswith(".png")]

#pick a model
model_option = st.selectbox(
    "Which LMM would you like to use?",
    ("llava:7b", "llava:13b", "llava:34b"))

st.write("You selected the model:", model_option)

#option image refresh
if st.button("Refresh Images"):
    get_images_from_stage()

#pick an image, or query them all
generate_all = st.checkbox("Answer for All Images")
image_name = st.selectbox(
    "Image Filename",
    image_list,
    disabled=generate_all,
)
st.write("You selected the file:", image_name)
if image_name:
    st.image(image_name, caption=image_name)

#prompt the LMM
st.subheader("Input a query for the LMM to answer")
prompt = st.text_area(
    "Image Query",
    "This picture contains screenshots from the classic video game DOOM. What is the main character holding?",
    height=300,
)

#generate results
if st.button("Answer"):
    if generate_all:
        for file in image_list:
            print(file)
            response = subprocess.run([
                'ollama',
                'run',
                model_option,
                prompt+" "+file
            ], capture_output=True)
            formatted_response = str(response.stdout)[2:-6].replace("'", "\\'")
            timestamp = str(datetime.now())
            insert_query =\
                f'''
                    INSERT INTO image_analysis
                    VALUES (
                        '{model_option}',
                        '{file}',
                        '{prompt}',
                        '{formatted_response}',
                        '{timestamp}'
                    )
                '''
            try:
                get_snowflake_connection().sql(
                    insert_query
                ).show()
            except:
                print("BAD RESPONSE. SKIPPING")
    else:
        print(image_name)
        response = subprocess.run([
            'ollama',
            'run',
            model_option,
            prompt+" "+image_name
        ], capture_output=True)
        st.write(str(response.stdout)[2:-6])

