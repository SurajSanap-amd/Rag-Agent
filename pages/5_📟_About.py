import json
import streamlit as st
from streamlit_lottie import st_lottie 

def show_thank_you_emoji():
    st.text("  💖  ")


def main():
    a = "<h1><center>About</center></h1>"

    st.write(a, unsafe_allow_html=True)
    with open('About.json') as anim_source:
        animation = json.load(anim_source)
    st_lottie(animation, 1, True, True, "high", 200, -200)

    st.title("About Me")

    st.write("""
    Hi! I'm 
            <p style="font-size: 40px; font-weight: bold;">
            <span style="color: orange;">Suraj Sanap,</span>
            </p>
            Software Engineer @Amdocs with expertise in **AI**, **Machine Learning**, and building web applications. 
    I love solving real-world problems using innovative technologies.
    """, 
        unsafe_allow_html=True)
    
    # Define URLs for GitHub and LinkedIn
    github_url = "https://github.com/SurajSanap"
    linkedin_url = "https://www.linkedin.com/in/SurajSanap01"
    
    st.markdown("### Connect with me:")
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    # GitHub button on the left
    with col1:
        st.markdown(
            f"""
            <a href="{github_url}" target="_blank">
                <button style="padding: 10px; font-size: 16px; color: white; background-color: #333; border: none; border-radius: 5px; width: 100%;">
                    GitHub
                </button>
            </a>
            """,
            unsafe_allow_html=True,
        )
    
    # LinkedIn button on the right
    with col2:
        st.markdown(
            f"""
            <a href="{linkedin_url}" target="_blank">
                <button style="padding: 10px; font-size: 16px; color: white; background-color: #0072b1; border: none; border-radius: 5px; width: 100%;">
                    LinkedIn
                </button>
            </a>
            """,
            unsafe_allow_html=True,
        )
    

    st.header('', divider='rainbow')
    #st.header('_Streamlit_ is :blue[cool] :sunglasses:')

    st.write("\n")
    st.write("\n")

    st.divider()
    
    # Contributor data
   


if __name__=="__main__":
    main()

