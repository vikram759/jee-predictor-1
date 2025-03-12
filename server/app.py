from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

# Import your recommender code
class CollegeRecommender:
    def __init__(self, data):
        self.df = data.copy()

    def recommend(self, user_input):
        # Use JEE Advanced rank if preferring IITs, else use JEE Mains rank
        if user_input.get('prefer_iit', False):
            self.df['Closing Rank'] = pd.to_numeric(self.df['Closing Rank'], errors='coerce')
            rank_filter = (self.df['Type of Exam'] == 'JEE Advanced') & (self.df['Closing Rank'] >= user_input.get('jee_advanced_rank', 0))
        else:
            self.df['Closing Rank'] = pd.to_numeric(self.df['Closing Rank'], errors='coerce')
            rank_filter = (self.df['Type of Exam'] == 'JEE Mains') & (self.df['Closing Rank'].notna()) & (self.df['Closing Rank'] >= user_input.get('jee_mains_rank', 0))

        # Filter colleges based on category, rank, fee, and salary
        self.df['Average Package']=pd.to_numeric(self.df['Average Package'], errors='coerce')
        self.df['Fee Structure']=pd.to_numeric(self.df['Fee Structure'], errors='coerce')

        filtered = self.df[
            rank_filter &
            (self.df['Fee Structure'] <= user_input.get('max_fee', float('inf'))) &
            (self.df['Average Package'] >= user_input.get('min_salary', 0)) &
            (self.df['Seat Type'] == user_input.get('category', 'OPEN'))
        ].copy()

        if filtered.empty:
            return []
            
        # Define branch preferences
        branch_preferences = {
            'Computer Science': 10,
            'Computer Science (AI)': 9.5,
            'Computer Science (DS)': 9,
            'Electronics and Communication Engineering': 8,
            'Electrical Engineering': 7.5,
            'Mechanical Engineering': 7,
            'Aerospace Engineering': 6.5,
            'Production Engineering': 6,
            'Metallurgical Engineering': 5.5,
            'Bio Engineering': 5,
            'Civil Engineering': 4.5
        }
        
        # Function to get branch preference score
        def get_branch_score(branch_name):
            for preferred_branch in branch_preferences.keys():
                if preferred_branch in branch_name:
                    return branch_preferences[preferred_branch]
            return 0  # Default score if branch not found
            
        # Calculate score for each college
        def calculate_score(row):
            try:
                branch_score = get_branch_score(row['Academic Program Name'])
                avg_package_max = filtered['Average Package'].max() or 1  # Avoid division by zero
                branch_preference_max = max(branch_preferences.values()) or 1  # Avoid division by zero
        
                if row['Type of Exam'] == 'JEE Advanced':
                    return 0.2 * (row['Average Package'] / avg_package_max) + 0.25 * (1 - row['fee_norm']) + 0.4 * (1 - row['cutoff_norm']) + 0.15 * branch_score / branch_preference_max
                else:
                    return 0.25 * (row['Average Package'] / avg_package_max) + 0.2 * (1 - row['fee_norm']) + 0.35 * (1 - row['cutoff_norm']) + 0.2 + 0.1 * branch_score / branch_preference_max
            except Exception as e:
                print(f"Error calculating score: {e}")
                return 0  # Default score on error
        
        # Normalize cutoff rank and fees
        filtered['cutoff_norm'] = filtered['Closing Rank'] / filtered['Closing Rank'].max()
        filtered['fee_norm'] = filtered['Fee Structure'] / filtered['Fee Structure'].max()
        
        filtered['score'] = filtered.apply(lambda row: calculate_score(row), axis=1)

        # Sort by score and return top 5
        top_colleges = filtered[['Institute', 'Academic Program Name', 'score', 'Average Package', 'Fee Structure', 'Closing Rank']].sort_values(
            by='score', ascending=False
        ).head(5)
        
        # Convert to dictionary for JSON response
        return top_colleges.to_dict(orient='records')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load your data

def load_data():
    global recommender
    try:
        df = pd.read_csv("final_most.csv")
        recommender = CollegeRecommender(df)
    except Exception as e:
        print(f"Error loading data: {e}")
        # Create a dummy dataframe for testing if file isn't found
        dummy_data = pd.DataFrame({
            'Institute': ['IIT Test'],
            'Academic Program Name': ['Computer Science'],
            'Type of Exam': ['JEE Advanced'],
            'Closing Rank': [100],
            'Fee Structure': [250000],
            'Average Package': [1800000],
            'Seat Type': ['OPEN']
        })
        recommender = CollegeRecommender(dummy_data)

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    try:
        user_input = request.json
        print(f"Received user input: {user_input}")
        df = pd.read_csv("final_most.csv")
        ecommender = CollegeRecommender(df)
        
        # Basic validation
        required_fields = ['jee_advanced_rank', 'jee_mains_rank', 'max_fee', 
                          'min_salary', 'category', 'prefer_iit']
        
        for field in required_fields:
            if field not in user_input:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Convert string values to appropriate types
        try:
            user_input['jee_advanced_rank'] = int(user_input['jee_advanced_rank'])
            user_input['jee_mains_rank'] = int(user_input['jee_mains_rank'])
            user_input['max_fee'] = float(user_input['max_fee'])
            user_input['min_salary'] = float(user_input['min_salary'])
            user_input['prefer_iit'] = bool(user_input['prefer_iit'])
        except ValueError as e:
            return jsonify({"error": f"Invalid value format: {str(e)}"}), 400
        
        print("Calling recommender with processed input")
        recommendations = ecommender.recommend(user_input)
        print(f"Got recommendations: {len(recommendations)} items")
        
        # Format the response
        formatted_recommendations = []
        for rec in recommendations:
            formatted_rec = {
                'institute': rec['Institute'],
                'program': rec['Academic Program Name'],
                'score': round(rec['score'] * 100, 2),  # Convert to percentage
                'package': f"₹{rec['Average Package']:,}",
                'fees': f"₹{rec['Fee Structure']:,}",
                'rank': int(rec['Closing Rank'])
            }
            formatted_recommendations.append(formatted_rec)
        
        return jsonify(formatted_recommendations)
    
    except Exception as e:
        import traceback
        print(f"Error in recommendation API: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True, port=8080)