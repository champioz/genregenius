import polars as pl
import pandas as pd
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
    
    datasheet_path = f'./public/data/{lab}_datasheet.json'
    timedata_path = f'./public/data/{lab}_timedata.json'
    ratings_path = f'./public/data/{lab}_ratings.json'
    datasheet = pl.read_json(datasheet_path)
    ratings = pl.read_json(ratings_path)
    label_desc = pl.read_csv('./public/data/label_desc.csv',infer_schema_length=0)
    sentences = pl.read_csv('./public/data/sentences.csv', infer_schema_length=0)
    timedata = pl.read_json(timedata_path)
    words = pl.read_csv('./public/data/words.csv', infer_schema_length=0)
    
    label_desc = label_desc.filter(pl.col('Group') == lab)
    sentences = sentences.filter(pl.col('Group') == lab)
    words = words.filter(pl.col('Group') == lab)
    words = words.with_columns(
        pl.col('Freq').cast(pl.Float32)
    )
    
    datasheet = datasheet.fill_null(0)
    
    return datasheet, label_desc, sentences, timedata, words, ratings

def to_altair_datetime(dt):
    dt = pd.to_datetime(dt)
    return alt.DateTime(year=dt.year, month=dt.month, date=dt.day,
                        hours=dt.hour, minutes=dt.minute, seconds=dt.second,
                        milliseconds=0.001 * dt.microsecond)

    
st.set_page_config(layout="wide", 
                   initial_sidebar_state="collapsed",
                   page_title='Genre Genius',
                   page_icon='./public/img/favicon.png')
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
DESC = st.session_state['DESC']
        
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
    
    st.write('The description you input:')
    
    with stylable_container(
    "codeblock",
    """
    code {
        white-space: pre-wrap !important;
    }
    """,
    ):
        st.code(DESC, language=None)
    st.write('<br>', unsafe_allow_html=True)
     

## BODY ##

cols = st.columns([1, 1, 7, 1])

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
    
    #text = ', '.join(words['Word'].to_list())
    wordcloud = WordCloud(background_color="white", 
                          colormap="Purples_r", width=800, height=400)
    weights = dict(zip(words['Word'].to_list(), words['Freq'].to_list()))
    
    wordcloud.generate_from_frequencies(weights)
    
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
    
    
## RIGHT COL ##
    
with cols[2]:
    st.write('<h4>Genre Activity Over Time</h4>', unsafe_allow_html=True)
    
    line_data = st.selectbox(
        'Select a metric',
        ('Reader count', 'Written review count', 'Rating count')
    )
    if line_data == 'Reader count': line_filter='read_count:Q'
    if line_data == 'Written review count': line_filter='review_count:Q'
    if line_data == 'Rating count': line_filter='rate_count:Q'
    
    domain = [to_altair_datetime('2012-01-01'), 
              to_altair_datetime('2017-05-31')]
    
    line_c = alt.Chart(timedata).mark_line(clip=True).encode(
        x=alt.X('date_added:T', timeUnit='yearmonthdate', 
                title="Date", scale= alt.Scale(domain=list(domain))),
        y=alt.Y(line_filter, title=line_data)
    ).interactive()
    
    st.altair_chart(line_c, use_container_width=True)
   
    st.write('<h4>Rating Distribution</h4>', unsafe_allow_html=True)
   
    st.bar_chart(ratings, x='Rating', y='Count', color='#9071CE')
    



## BOTTOM SECTION ##

cols2 = st.columns([1, 6, 1])

with cols2[1]:
    
    st.write('<h4>Popularity Distribution</h4>', unsafe_allow_html=True)
    st.write("This plot shows how many books in this group of similar titles were rated, reviewed, or saved to a Goodreads user's bookshelf. Each bin in the histogram shows how many books were saved by N users, where N is the count given on the x-axis.")


cols2 = st.columns([1, 3, 3, 1])

with cols2[1]:
    bar_data = st.selectbox(
        'Select metric',
        ('Bookshelf save count', 'Rating count', 'Written review count')
    )
    if bar_data == 'Rating count': 
        bar_data='# Ratings'
        max_val = 5000
    if bar_data == 'Bookshelf save count': 
        bar_data='# of Bookshelves'
        max_val = 10000
    if bar_data == 'Written review count': 
        bar_data='# Text Reviews'
        max_val = 10000
    
with cols2[2]:
    lower, upper = st.slider(
        'Publication Year',
        1800, 2017, (2005, 2017),
        step=1,
        key=alt.Key('slider1')
    )
    
cols2 = st.columns([1, 6, 1])
    
with cols2[1]:

    st.write(f'Max value: {datasheet.select(pl.max(bar_data)).item()}')
    
    hist = alt.Chart(
        datasheet.filter(
            (pl.col('Pub Date').dt.year() >= lower) & (pl.col('Pub Date').dt.year() <= upper)
            )
        ).mark_bar(color='#9071CE').encode(
        alt.X(bar_data, bin=alt.Bin(step=100),
              scale=alt.Scale(domain=[0, max_val])),
        alt.Y('count()')
    ).interactive()
    
    st.altair_chart(hist, use_container_width=True)
    
    st.write('<h4>Most Popular Similar Books by Readership and Rating</h4>', unsafe_allow_html=True)
    

cols2 = st.columns([1, 3, 3, 1])

with cols2[1]:
    table_data = st.selectbox(
        'Sort by:',
        ('Bookshelf save count', 'Average rating')
    )
    if table_data == 'Average rating': table_data='Avg Rating'
    if table_data == 'Bookshelf save count': table_data='# of Bookshelves'
    
with cols2[2]:
    lower2, upper2 = st.slider(
        'Publication Year',
        1800, 2017, (2005, 2017),
        step=1,
        key=alt.Key('slider2')
    )
    
cols2 = st.columns([1, 6, 1])

with cols2[1]:

        
    st.dataframe(
        datasheet.filter(
            (pl.col('Pub Date').dt.year() >= lower2) & (pl.col('Pub Date').dt.year() <= upper2)
            ).select(
            ['Title', 
             'Authors', 
             'Pub Date', 
             'Avg Rating', 
             '# of Bookshelves', 
             '# Ratings', 
             '# Text Reviews', 
             'URL']).sort(
                 by=[table_data, '# of Bookshelves'], 
                 descending=True).limit(10),
        hide_index=True,
        use_container_width=True,
        column_config={
            "URL": st.column_config.LinkColumn(),
            "Pub Date":st.column_config.DateColumn()
        }
    )
    
    st.write("<br><br><br><em>Part of a project by Cyndi Campbell, Zach Champion, Paul Kim, and Thuy Nguyen at Georgia Tech</em>",
         unsafe_allow_html=True)