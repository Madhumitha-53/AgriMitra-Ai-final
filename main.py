import streamlit as st
from deep_translator.exceptions import RequestError
from dotenv import load_dotenv

load_dotenv()


from streamlit_mic_recorder import mic_recorder

from voice.speech import speech_to_text
from voice.speak import create_voice, cleanup_voice_file

from ai.llm import get_response
from graph.workflow import process_query

from language.translate import translate_text

from ui.styles import load_css
from ui.dashboard import show_dashboard

from chatbot.chat import chatbot_ui



# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AgriMitra AI",
    page_icon="🌱",
    layout="wide"
)


load_css()





# =========================
# LANGUAGE
# =========================


LANG_TEXT = {


"en":{
"title":"🌱 AgriMitra AI",
"sub":"AI Powered Voice Farming Assistant",
"start":"🎤 Start Speaking",
"stop":"⏹ Stop",
"farmer":"👨‍🌾 Farmer Said",
"answer":"🌾 AI Recommendation",
"listen":"🔊 Listen",
"welcome":"Ask about crops, fertilizer, pests, irrigation and government schemes"
},


"ta":{
"title":"🌱 அக்ரிமித்ரா AI",
"sub":"AI குரல் விவசாய உதவியாளர்",
"start":"🎤 பேச தொடங்கவும்",
"stop":"⏹ நிறுத்தவும்",
"farmer":"👨‍🌾 விவசாயி சொன்னது",
"answer":"🌾 AI பரிந்துரை",
"listen":"🔊 கேட்க",
"welcome":"பயிர், உரம், பூச்சி, நீர் மேலாண்மை பற்றி கேளுங்கள்"
},


"hi":{
"title":"🌱 एग्रीमित्र AI",
"sub":"AI कृषि सहायक",
"start":"🎤 बोलें",
"stop":"⏹ रोकें",
"farmer":"👨‍🌾 किसान ने कहा",
"answer":"🌾 सलाह",
"listen":"🔊 सुनें",
"welcome":"फसल, खाद, कीट और योजनाओं के बारे में पूछें"
},


"te":{
"title":"🌱 అగ్రిమిత్ర AI",
"sub":"AI వ్యవసాయ సహాయకుడు",
"start":"🎤 మాట్లాడండి",
"stop":"⏹ ఆపండి",
"farmer":"👨‍🌾 రైతు చెప్పింది",
"answer":"🌾 సలహా",
"listen":"🔊 వినండి",
"welcome":"పంటలు, ఎరువులు, నీటి గురించి అడగండి"
}

}





# =========================
# SIDEBAR
# =========================


language = st.sidebar.selectbox(

    "🌍 Language",

    [
        ("English","en"),
        ("தமிழ்","ta"),
        ("हिन्दी","hi"),
        ("తెలుగు","te")
    ],

    format_func=lambda x:x[0]

)[1]





theme = st.sidebar.radio(

    "🎨 Theme",

    [
        "☀️ Light Mode",
        "🌙 Dark Mode"
    ]

)



ui = LANG_TEXT[language]







# =========================
# FINAL THEME FIX
# =========================


if theme == "🌙 Dark Mode":


    st.markdown(
    """

<style>


.stApp {

background:
linear-gradient(
135deg,
#020617,
#0f172a,
#1e3a8a
) !important;

}




.stApp,
.stApp p,
.stApp span,
.stApp div,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp label {

color:white !important;

}




.card {

background:

rgba(15,23,42,.9) !important;

}



.card * {

color:white !important;

}





[data-testid="stChatMessage"] {


background:

rgba(30,41,59,.8) !important;

}



[data-testid="stChatMessage"] * {


color:white !important;

}





[data-testid="stChatInput"] {


background:#111827 !important;

}



[data-testid="stChatInput"] textarea {


background:#111827 !important;

color:white !important;

caret-color:white !important;

}




[data-testid="stChatInput"] textarea::placeholder {

color:#cbd5e1 !important;

}




section[data-testid="stSidebar"] {


background:

linear-gradient(
180deg,
#172554,
#020617
) !important;


}



section[data-testid="stSidebar"] * {


color:white !important;


}


</style>

""",

unsafe_allow_html=True
    )






else:


    st.markdown(
    """

<style>


.stApp {

background:

linear-gradient(
135deg,
#dbeafe,
#eff6ff,
#e0f2fe
) !important;

}




.card {

background:

rgba(255,255,255,.9) !important;

}



.card * {

color:#0f172a !important;

}




[data-testid="stChatMessage"] {


background:white !important;

}



[data-testid="stChatMessage"] * {


color:#0f172a !important;

}





[data-testid="stChatInput"] {


background:white !important;


}



[data-testid="stChatInput"] textarea {


background:white !important;

color:#0f172a !important;

caret-color:#0f172a !important;


}




[data-testid="stChatInput"] textarea::placeholder {


color:#64748b !important;


}




section[data-testid="stSidebar"] {


background:

linear-gradient(
180deg,
#2563eb,
#0f172a
) !important;


}



section[data-testid="stSidebar"] * {

color:white !important;

}


</style>

""",

unsafe_allow_html=True

    )









# =========================
# HEADER
# =========================


st.markdown(

f"""

<h1 class="main-title">

{ui['title']}

</h1>


<h3>

{ui['sub']}

</h3>

""",

unsafe_allow_html=True

)






# =========================
# VOICE INPUT
# =========================


audio = mic_recorder(

start_prompt=ui["start"],

stop_prompt=ui["stop"],

just_once=True,

use_container_width=True,

key="farmer_voice"

)







if audio:


    file="farmer_audio.webm"


    with open(file,"wb") as f:

        f.write(audio["bytes"])




    result=speech_to_text(file)



    text=result.get(
        "text",
        ""
    )


    detected=result.get(
        "language",
        language
    )



    if detected in LANG_TEXT:

        language=detected

        ui=LANG_TEXT[language]





    if text:


        st.markdown(

        f"""

<div class="card">

<h3>

{ui['farmer']}

</h3>

<p>

{text}

</p>

</div>

""",

        unsafe_allow_html=True

        )




        with st.spinner("🌱 Thinking..."):


            query = process_query(text)

            if not query:
                query = text

            answer = get_response(query)





        if language!="en":

            try:
                answer=translate_text(
                    answer,
                    language
                )
            except RequestError:
                st.warning(
                    "Translation is temporarily unavailable. "
                    "Showing the answer in English."
                )






        st.markdown(

        f"""

<h2>

{ui['answer']}

</h2>


<div class="card">

{answer}

</div>

""",

        unsafe_allow_html=True

        )






        try:

            audio_out = create_voice(answer, language)

            st.audio(audio_out)

            cleanup_voice_file(audio_out)

        except Exception as e:

            st.warning(f"Voice playback unavailable: {e}")







# =========================
# DASHBOARD
# =========================


show_dashboard(

crop="AI Crop Prediction",

fertilizer="AI Fertilizer Plan",

water="AI Water Schedule",

risk="AI Pest Risk",

scheme="Government Scheme",

language=language

)






# =========================
# CHATBOT
# =========================


st.divider()

chatbot_ui(language)