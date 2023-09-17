from django.shortcuts import render
from django.http import HttpResponse
from joblib import load
import pandas as pd  # Import pandas for data handling

# Load the trained machine learning model
model = load('./savedmodels/model.joblib')

def recommend_track(request):
    if request.method == 'POST':
        # Get the track_genre input from the form
        track_genre = request.POST.get('track_genre', '')

        # Load your new dataset (you might have to adjust the path)
        dataset_path = 'C:\pythonPrac\Djnago_Spotify\p1\SpotifyProject\Songs.csv'
        Songs = pd.read_csv(dataset_path)

        # Filter the dataset for the given track_genre
        genre_df = Songs[Songs['track_genre'] == track_genre]

        try:
            if genre_df.empty:
                recommendations = ["No tracks found for the genre: " + track_genre]
            else:
                # Sort the filtered DataFrame by popularity (or any other relevant metric)
                sorted_genre_df = genre_df.sort_values(by='popularity', ascending=False)

                # Get the top 10 recommendations
                top_n = min(10, len(sorted_genre_df))
                top_recommendations = sorted_genre_df.head(top_n)

                # Extract track_name_artists from the recommendations
                recommendations = top_recommendations['track_name_artists'].tolist()
        except Exception as e:
            # Handle any errors that may occur during recommendation or data processing
            error_message = str(e)
            return HttpResponse(f"Error: {error_message}")

        # Pass the recommendations to the template for rendering
        return render(request, 'recommend.html', {'recommendations': recommendations})

    # If the request method is not POST or no input provided, render the empty form
    return render(request, 'recommend.html', {})
