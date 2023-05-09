import matplotlib.pyplot as plt
from wordcloud import WordCloud

def make_wordcloud(df):
    # define the frequency of each job title
    job_title_freq = df['job_title'].value_counts(normalize=True)

    # create the wordcloud object
    wc = WordCloud(width=800, height=600, background_color='white', max_words=50)

    # generate the wordcloud
    wc.generate_from_frequencies(job_title_freq)

    # plot the wordcloud
    plt.figure(figsize=(12, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()
