import streamlit as st
from utils.common import catalog, setup

COPY = {
    "English": ("From farm to market. Zero spoilage.",
                "When storage is hard to find and warm loads go unnoticed, farmers lose produce and income.",
                ("Find", "Compare cold rooms and reserve space."),
                ("Monitor", "Check the latest readings for your produce."),
                ("Move", "Choose a refrigerated truck for market day."),
                ("Storage sites", "Cold trucks", "Your reservations")),
    "हिन्दी": ("खेत से बाज़ार तक। उपज की बर्बादी शून्य।",
               "शीत भंडारण ढूँढना मुश्किल हो और बढ़ते तापमान का पता न चले तो किसानों की उपज और कमाई दोनों घटती हैं।",
               ("खोजें", "शीत भंडारों की तुलना करें और जगह आरक्षित करें।"),
               ("निगरानी करें", "अपनी उपज का तापमान और नमी देखें।"),
               ("परिवहन", "मंडी के लिए शीत वाहन चुनें।"),
               ("शीत भंडार", "शीत वाहन", "आपके आरक्षण")),
    "తెలుగు": ("పొలం నుంచి మార్కెట్ వరకు. పంట వృథా సున్నా.",
               "శీతల గిడ్డంగులు దొరకక, పెరుగుతున్న ఉష్ణోగ్రత తెలియక రైతులు పంటను, ఆదాయాన్ని కోల్పోతారు.",
               ("వెతకండి", "శీతల గిడ్డంగులను పోల్చి స్థలం బుక్ చేసుకోండి."),
               ("పర్యవేక్షించండి", "మీ పంట ఉష్ణోగ్రత, తేమను చూడండి."),
               ("రవాణా", "మార్కెట్‌కు శీతల వాహనాన్ని ఎంచుకోండి."),
               ("శీతల గిడ్డంగులు", "శీతల వాహనాలు", "మీ రిజర్వేషన్లు"))
}


def main():
    setup("Home", "🌱")
    lang = st.sidebar.radio("Language · भाषा · భాష", list(COPY))
    tagline, summary, *cards, metrics = COPY[lang]
    st.title("🌱 FreshChain")
    st.header(tagline)
    st.write(summary)
    pages = ["1_Find_Storage", "2_Live_Monitoring", "3_Book_Transport"]
    for col, (label, body), page, icon in zip(st.columns(3), cards, pages, ["📍", "🌡️", "🚚"]):
        with col.container(border=True):
            st.page_link(f"pages/{page}.py", label=label, icon=icon)
            st.write(body)
    counts = [len(catalog("storages.csv", ["name"])), len(catalog("transport.csv", ["truck"])),
              len(st.session_state.reservations)]
    for col, label, count in zip(st.columns(3), metrics, counts):
        col.metric(label, count)


if __name__ == "__main__":
    main()
