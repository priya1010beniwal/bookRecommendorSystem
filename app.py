from flask import Flask, render_template, request
import pickle
import numpy as np

# Load pickled data
popular_df = pickle.load(open('templates/popular.pkl', 'rb'))
pt = pickle.load(open('templates/pt.pkl', 'rb'))
books = pickle.load(open('templates/books.pkl', 'rb'))
similarity_score = pickle.load(open('templates/similarity_scores.pkl', 'rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=popular_df['Book-Title'].to_list(),
                           author=popular_df['Book-Author'].to_list(),
                           image=popular_df['Image-URL-M'].to_list(),
                           votes=popular_df['num_ratings'].to_list(),
                           rating=popular_df['Book-Rating'].to_list())


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    data = []
    try:
        index = np.where(pt.index == user_input)[0][0]

        # Get similarity scores for the book and sort them
        similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]

        # Iterate through the similar items to get book details
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)
    except IndexError:
        print(f"Book '{user_input}' not found in the dataset.")
    return render_template('recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
