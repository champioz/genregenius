from model import classify_input
import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container

    
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
            submitted = st.form_submit_button("Submit")

    st.write('''<br><br>
    Not an author but want to try? Use one of these (hover and click to copy):   
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

        Despite the tumor-shrinking medical miracle that has bought her a few years, Hazel has never been anything but terminal, her final chapter inscribed upon diagnosis. But when a gorgeous plot twist named Augustus Waters suddenly appears at Cancer Kid Support Group, Hazel's story is about to be completely rewritten.
        ''', language=None)
        st.write('-<em>The Fault In Our Stars</em>, John Green', unsafe_allow_html=True)
    
    with col2:
        st.code('''
        Six days ago, astronaut Mark Watney became one of the first people to walk on Mars. Now, he’s sure he’ll be the first person to die there. After a dust storm nearly kills him and forces his crew to evacuate while thinking him dead, Mark finds himself stranded and completely alone with no way to even signal Earth that he’s alive—and even if he could get word out, his supplies would be gone long before a rescue could arrive. Chances are, though, he won’t have time to starve to death.
        ''', language=None)
        st.write('-<em>The Martian</em>, Andy Weir', unsafe_allow_html=True)

    with col3:
        st.code('''
        When Tate Collins meets airline pilot Miles Archer, she knows it isn’t love at first sight. They wouldn’t even go so far as to consider themselves friends. The only thing Tate and Miles have in common is an undeniable mutual attraction. Once their desires are out in the open, they realize they have the perfect set-up. He doesn’t want love, she doesn’t have time for love, so that just leaves the sex. Their arrangement could be surprisingly seamless, as long as Tate can stick to the only two rules Miles has for her. Never ask about the past. Don’t expect a future.
        ''', language=None)
        st.write('-<em>Ugly Love</em>, Colleen Hoover', unsafe_allow_html=True)
      
      
cols2 = st.columns([1, 6, 1])

with cols2[1]:  

    st.write("<br><br><br><em>Part of a project by Cyndi Campbell, Zach Champion, Paul Kim, and Thuy Nguyen at Georgia Tech</em>",
            unsafe_allow_html=True)

