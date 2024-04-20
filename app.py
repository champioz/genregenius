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
        Harriet Vanger, a scion of one of Sweden’s wealthiest families disappeared over forty years ago. All these years later, her aged uncle continues to seek the truth. He hires Mikael Blomkvist, a crusading journalist recently trapped by a libel conviction, to investigate. He is aided by the pierced and tattooed punk prodigy Lisbeth Salander. Together they tap into a vein of unfathomable iniquity and astonishing corruption. An international publishing sensation, Stieg Larsson’s The Girl with the Dragon Tattoo combines murder mystery, family saga, love story, and financial intrigue into one satisfyingly complex and entertainingly atmospheric novel.
        ''', language=None)
        st.write('-<em>The Girl with the Dragon Tattoo</em>, Stieg Larsson', unsafe_allow_html=True)
    
    with col2:
        st.code('''
        Augustus Everett is an acclaimed author of literary fiction. January Andrews writes bestselling romance. When she pens a happily ever after, he kills off his entire cast. They’re polar opposites. In fact, the only thing they have in common is that for the next three months, they’re living in neighboring beach houses, broke, and bogged down with writer’s block. Until, one hazy evening, one thing leads to another and they strike a deal designed to force them out of their creative ruts: Augustus will spend the summer writing something happy, and January will pen the next Great American Novel. She’ll take him on field trips worthy of any rom-com montage, and he’ll take her to interview surviving members of a backwoods death cult (obviously). Everyone will finish a book and no-one will fall in love. Really.
        ''', language=None)
        st.write('-<em>Beach Read</em>, Emily Henry', unsafe_allow_html=True)

    with col3:
        st.code('''
        For years, rumors of the “Marsh Girl” haunted Barkley Cove, a quiet fishing village. Kya Clark is barefoot and wild; unfit for polite society. So in late 1969, when the popular Chase Andrews is found dead, locals immediately suspect her. But Kya is not what they say. A born naturalist with just one day of school, she takes life's lessons from the land, learning the real ways of the world from the dishonest signals of fireflies. But while she has the skills to live in solitude forever, the time comes when she yearns to be touched and loved. Drawn to two young men from town, who are each intrigued by her wild beauty, Kya opens herself to a new and startling world—until the unthinkable happens.
        ''', language=None)
        st.write('-<em>Where the Crawdads Sing</em>, Delia Owens', unsafe_allow_html=True)
      
      
cols2 = st.columns([1, 2, 1])

with cols2[1]:  

    st.write("<br><br><br><em>Part of a project by Cyndi Campbell, Zach Champion, Paul Kim, and Thuy Nguyen at Georgia Tech</em>",
            unsafe_allow_html=True)

