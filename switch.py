import streamlit as st
import pandas as pd
import plotly.express as px
import random
import streamlit_shadcn_ui as ui
from wordcloud import WordCloud 
import matplotlib.pyplot as plt

# Apply Custom CSS
st.markdown(
    """
    <style>
    body {
        background-color: #FAF3E0;
        color: #5C3D2E;
        font-family: 'Arial', sans-serif;
    }
    .stTitle {
        color: #D2691E;
        text-align: center;
        font-weight: bold;
    }
    .stSidebar {
        padding: 5px;
        border-radius: 5px;
    }
    .stDataFrame {
        background-color: #FFEBCD;
        border-radius: 10px;
        padding: 5px;
    }
    .block-container {
        padding: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load the data from the CSV file
# @st.cache_data  # Cache the data to improve performance
def load_data():
    file_path = "/home/rei/Documents/Project/AI/child_report.csv"
    df = pd.read_csv(file_path)
    df['time'] = pd.to_datetime(df['time'])  # Convert 'time' column to datetime
    return df

df = load_data()

def generate_random_topics():
    topics = ["识字", "数学", "认识世界", "艺术与设计"]
    topic_proportions = {topic: random.randint(10, 40) for topic in topics}  # Random proportions
    return topic_proportions

def generate_word_frequencies(topic):
    words = {
        "识字":["reading", "writing", "books", "story", "alphabet"],
        "数学": ["numbers", "counting", "addition", "subtraction", "shapes"],
        "认识世界": ["animals", "plants", "weather", "seasons", "space"],
        "艺术与设计": ["painting", "sketching", "music", "dancing", "colors"],
    }
    return {word: random.randint(5, 20) for word in words[topic]}  # Random word frequencies


# Cumulative unique words (mock data for demonstration)
df['Unique Words'] = [len(set(sentence.split())) for sentence in df['sentence']]
df['Cumulative Unique Words'] = df['Unique Words'].cumsum()

# Dashboard Title
st.title("EchooGrow")
st.warning("欢迎使用 EchooGrow 语言发展仪表盘！追踪您孩子的语言发展情况")

# Interactive Dashboard Summary
st.subheader("🐣 本月总结")

child_name = "猫猫"
total_words = df['sentence'].apply(lambda x: len(x.split())).sum()
avg_sentence_length = round(df['sentence'].apply(lambda x: len(x.split())).mean(), 2)
predominant_sentiment = df['emotion'].mode()[0]
topic_proportions = generate_random_topics()
top_topics = sorted(topic_proportions, key=topic_proportions.get, reverse=True)[:2]

summary = (
    f"本月，<span style='color:#EF8985; font-weight:bold;'>{child_name}</span> 总共说了 "
    f"<span style='color:#EF8985; font-weight:bold;'>{total_words}</span> 个单词。 "
    f"他们的平均句子长度为 <span style='color:#EF8985; font-weight:bold;'>{avg_sentence_length}</span> 个单词， "
    f"比上个月有所增加，表明语言复杂性在提高。 "
    f"他们主要表达了 <span style='color:#EF8985; font-weight:bold;'>{predominant_sentiment}</span> 的情绪， "
    f"偶尔在讨论 <span style='color:#EF8985; font-weight:bold;'>{top_topics[0]}</span> 时表现出 "
    f"<span style='color:#EF8985; font-weight:bold;'>{random.choice(df['emotion'].unique())}</span> 的情绪。 "
    f"讨论最多的主题是 <span style='color:#EF8985; font-weight:bold;'>{top_topics[0]}</span> 和 "
    f"<span style='color:#EF8985; font-weight:bold;'>{top_topics[1]}</span>。"
)
st.markdown(
    f"<div style= padding:10px; border-radius:10px;'>"
    f"{summary}</div>",
    unsafe_allow_html=True
)

# Language Proficiency Visualization
st.subheader("🗣️ 语言能力发展趋势")
ui.card()
fig_mlu = px.line(df, x='time', y=df['sentence'].apply(lambda x: len(x.split())), title="平均句子长度随时间变化", markers=True, color_discrete_sequence=["#5cd6c4"])
st.plotly_chart(fig_mlu, use_container_width=True)

ui.card()
fig_words = px.line(df, x='time', y=df['sentence'].apply(lambda x: len(x.split())).cumsum(), title="总单词数随时间变化", markers=True, color_discrete_sequence=["#EF8985"])
st.plotly_chart(fig_words, use_container_width=True)

ui.card()
fig_vocab = px.line(df, x='time', y='Cumulative Unique Words', title="累计唯一单词数随时间变化", markers=True, color_discrete_sequence=["#eec843"])
st.plotly_chart(fig_vocab, use_container_width=True)

# Emotional Trend Visualization
st.subheader("💖 情绪趋势")
ui.card()
fig_emotion = px.histogram(df, x='emotion', title="情绪分布随时间变化", color='emotion', color_discrete_map={"Joy": "#5cd6c4", "Sadness": "#e6d5f4", "Anger": "#EF8985", "Neutral": "#eec843", "Fear": "#a8d5e2", "Disgust": "#d4a5a5", "Excitement": "#ffcc99"})
st.plotly_chart(fig_emotion, use_container_width=True)

ui.card()
fig_sentiment_trend = px.line(df, x='time', y='sentiment_score', title="情绪得分随时间变化", markers=True, line_shape='spline', color_discrete_sequence=["#5cd6c4"])
fig_sentiment_trend.update_traces(line=dict(width=3))
st.plotly_chart(fig_sentiment_trend, use_container_width=True)


# Interests Tendencies Visualization
st.subheader("🎨 兴趣趋势")

topic_df = pd.DataFrame(list(topic_proportions.items()), columns=["Topic", "Proportion"])

# Pie chart for topic proportions
st.write("### 讨论主题比例")
fig_topics = px.pie(topic_df, names="Topic", values="Proportion", title="讨论主题比例", color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig_topics, use_container_width=True)


# Interactive Word Cloud
st.write("### 互动主题词云")
selected_topic = st.selectbox("选择一个主题进行探索", topic_df["Topic"].tolist())

# Generate word frequencies for the selected topic
word_frequencies = generate_word_frequencies(selected_topic)

# Create and display the word cloud
st.write(f"**Most Common Words in '{selected_topic}':**")
wordcloud = WordCloud(width=400, height=200, background_color="white").generate_from_frequencies(word_frequencies)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
st.pyplot(plt)

# Display word frequencies as a table
st.write("**Word Frequencies:**")
word_freq_df = pd.DataFrame(list(word_frequencies.items()), columns=["Word", "Frequency"])
st.dataframe(word_freq_df)


st.write("📊 Filtered Data:", df)