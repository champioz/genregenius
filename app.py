from model import classify_input
import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container

    
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
    st.session_state['LABEL'] = None

DESC = ""

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

    st.write('''
    Genre Genius is an alternative view of readership trends using machine-learned labels built on state-of-the-art semantic clustering and text summarization techniques. Our genres were built using book descriptions from the <a href="https://mengtingwan.github.io/data/goodreads#datasets">large Goodreads dataset for recommender systems</a>. Submit your book's description below to gain insights about the popularity and thematic content of similar titles!
    ''', unsafe_allow_html=True)

    if not DESC:
        with st.form("desc", True, border=False) as desc_form:
            
            DESC = st.text_area("Enter your description:", height=200, key="desc")
            st.session_state['DESC'] = DESC
            submitted = st.form_submit_button("Submit")

    st.write('''<br><br>
    Not an author but want to try? Use one of these:<br><em>(Hover and click to copy)</em>   
    ''', unsafe_allow_html=True)

    if DESC:
        LABEL = str(classify_input(DESC))
        st.session_state['LABEL'] = LABEL
        st.switch_page('./pages/results.py')

with stylable_container(
    "codeblock",
    """
    code {
        white-space: pre-wrap !important;
    }
    """,
):
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.code('''
        Twenty-two-year-old Skeeter has just returned home after graduating from Ole Miss. She may have a degree, but it is 1962, Mississippi, and her mother will not be happy till Skeeter has a ring on her finger. Skeeter would normally find solace with her beloved maid Constantine, the woman who raised her, but Constantine has disappeared and no one will tell Skeeter where she has gone. Aibileen is a black maid, a wise, regal woman raising her seventeenth white child. Something has shifted inside her after the loss of her own son, who died while his bosses looked the other way. She is devoted to the little girl she looks after, though she knows both their hearts may be broken. Minny, Aibileen's best friend, is short, fat, and perhaps the sassiest woman in Mississippi. She can cook like nobody's business, but she can't mind her tongue, so she's lost yet another job. Minny finally finds a position working for someone too new to town to know her reputation. But her new boss has secrets of her own.
        ''', language=None)
        st.write('-<em>The Help</em>, Kathryn Stockett', unsafe_allow_html=True)
    
    with col2:
        st.code('''
        It is the year 2058, and technology now completely rules the world. But New York City Detective Eve Dallas knows that the irresistible impulses of the human heart are still ruled by just one thing: passion. When a senator's daughter is killed, the secret life of prostitution she'd been leading is revealed. The high-profile case takes Lieutenant Eve Dallas into the rarefied circles of Washington politics and society. Further complicating matters is Eve's growing attraction to Roarke, who is one of the wealthiest and most influential men on the planet, devilishly handsome... and the leading suspect in the investigation.
        ''', language=None)
        st.write('-<em>Naked in Death</em>, J.D. Robb', unsafe_allow_html=True)

    with col3:
        st.code('''
        It’s a small city, a place as hauntingly familiar as your own hometown. Only in Derry the haunting is real... They were seven teenagers when they first stumbled upon the horror. Now they are grown-up men and women who have gone out into the big world to gain success and happiness. But none of them can withstand the force that has drawn them back to Derry to face the nightmare without an end, and the evil without a name.
        ''', language=None)
        st.write('-<em>It</em>, Stephen King', unsafe_allow_html=True)
      
      
cols2 = st.columns([1, 2, 1])

with cols2[1]:  

    st.write("<br><br><br><em>Part of a project by Cyndi Campbell, Zach Champion, Paul Kim, and Thuy Nguyen at Georgia Tech</em>",
            unsafe_allow_html=True)

