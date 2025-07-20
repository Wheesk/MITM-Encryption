from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Paste your reviews as one string, or read from file
text = open('reviews.txt').read()
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.tight_layout()
plt.savefig('wordcloud.png', bbox_inches='tight')
