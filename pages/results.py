import polars as pl
import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import path
import sys
import os
import altair as alt

dir = path.Path(__file__).abspath()
sys.path.append(dir.parent.parent)

@st.cache_data
def read_data(lab):
    
    datasheet_path = [file for file in os.listdir('./public/data/') if lab in file and 'datasheet' in file][0]
    timedata_path = [file for file in os.listdir('./public/data/') if lab in file and 'timedata' in file][0]
    ratings_path = [file for file in os.listdir('./public/data/') if lab in file and 'ratings' in file][0]
    datasheet = pl.read_json(f'./public/data/{datasheet_path}')
    ratings = pl.read_json(f'./public/data/{ratings_path}')
    label_desc = pl.read_csv('./public/data/label_desc.csv',infer_schema_length=0)
    sentences = pl.read_csv('./public/data/sentences.csv', infer_schema_length=0)
    timedata = pl.read_json(f'./public/data/{timedata_path}')
    words = pl.read_csv('./public/data/words.csv', infer_schema_length=0)
    
    label_desc = label_desc.filter(pl.col('Group') == lab)
    sentences = sentences.filter(pl.col('Group') == lab)
    words = words.filter(pl.col('Group') == lab)
    
    return datasheet, label_desc, sentences, timedata, words, ratings

    
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
st.markdown(
    """
    <style>
        [data-testid="collapsedControl"] {
            display:none
        }
    </style>
    """,
    unsafe_allow_html=True
)

if 'LABEL' not in st.session_state:
    st.switch_page('app.py')
    
LABEL = st.session_state['LABEL']
        
datasheet, label_desc, sentences, timedata, words, ratings = read_data(LABEL)


## HEADER ##

col_main1, col_main2, col_main3 = st.columns([1, 2, 1])

with col_main2:

    st.image('./public/img/logo.png')
    hide_img_fs = '''
    <style>
    button[title="View fullscreen"]{
        visibility: hidden;}
    </style>
    '''

    st.markdown(hide_img_fs, unsafe_allow_html=True)
     

## BODY ##

cols = st.columns([1, 8, 1])

with cols[1]:
    if st.button("Back"):
        st.switch_page("app.py")
    

cols = st.columns([1, 4, 2, 1])


## LEFT COL ##

with cols[1]:
    
    st.write('Your genre is...')
    st.title(label_desc['Label'].item())
    st.write('<h4>Description</h4>', unsafe_allow_html=True)
    with stylable_container(
    "codeblock",
    """
    code {
        white-space: pre-wrap !important;
    }
    """,
    ):
        st.code(label_desc['Description'].item(), language=None)
    st.write('<h4>Most Typical Description Sentences</h4>', unsafe_allow_html=True)
    st.dataframe(sentences.select(['Sentences']), hide_index=True,
        use_container_width=True,)
    st.write('<h4>Most Frequent Unique Words</h4>', unsafe_allow_html=True)
    text = ', '.join(words['Word'].to_list())
    wordcloud = WordCloud(background_color="white", 
                          colormap="Purples_r", width=800, height=400).generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
    
    
## RIGHT COL ##
    
with cols[2]:
    st.write('<h4>Genre Popularity</h4>', unsafe_allow_html=True)
    
    st.line_chart(timedata, x="date_added", y=['read_count', 'review_count', 'rate_count'], color=['#2A0C4E', '#9071CE', '#EEB6DB'])
   
    st.write('<h4>Rating Distribution</h4>', unsafe_allow_html=True)
   
    st.bar_chart(ratings, x='Rating', y='Count', color='#9071CE')


# BOTTOM SECTION ##

cols2 = st.columns([1, 6, 1])

with cols2[1]:
    
    st.write('<h4>Top Five Similar Books by Readership</h4>', unsafe_allow_html=True)
    st.dataframe(
        datasheet.select(['Title', 'URL', 'Authors', 'Pub Date', '# Ratings', 'Avg Rating', '# Text Reviews', '# of Bookshelves']).sort(by='Avg Rating', descending=True).limit(5),
        hide_index=True,
        use_container_width=True,
        column_config={
            "URL": st.column_config.LinkColumn()
        }
    )
    
    st.write("<br><br><br><em>Part of a project by Cyndi Campbell, Zach Champion, Paul Kim, and Thuy Nguyen at Georgia Tech</em>",
         unsafe_allow_html=True)