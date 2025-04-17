# Step 1: Load Libraries
Download necessary NLTK data files for tokenisation and stopwords
nltk.download('punkt')
nltk.download('stopwords')
 
- Imports necessary libraries for data manipulation, natural language processing, machine learning, and visualisation.
- Downloads necessary NLTK data files for tokenisation and stopwords

# Step 2: Load the dataset from CSV files in the raw data path
raw_data_path = "/Users/lanahumphrys/Documents/Project1/ForkNatNew/data/raw"
processed_data_path = "/Users/lanahumphrys/Documents/Project1/ForkNatNew/data/processed"

files = [os.path.join(raw_data_path, file) for file in os.listdir(raw data_path) if file ends with('.csv')]
data_frames = []
for file in files:
    try:
        df = pd.read_csv(file, on_bad_lines='skip', delimiter=',')  
Adjust delimiter if necessary
        data_frames.append(df)
    except pd.errors.ParserError as e:
        print(f"Error parsing {file}: {e}")

data = pd.concat(data_frames, ignore_index=True)

- Defines the paths to the raw and processed data.
- Loads the dataset from CSV files in the raw data path.
- Concatenates all data frames into a single data frame.


# Step 3: Preprocess the text data and include additional features like category and tone
    
if 'category' not in data.columns:
    data['category'] = 
if 'tone' not in data.columns:
    data['tone'] = ""

def preprocess_text(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r'\\d+', '', text)
        text = re.sub(r'\\s+', ' ', text).strip()
    else:
        text = ""
    return text

data['text'] = data['text'].apply(preprocess_text)
data['category'] = data['category'].apply(preprocess_text)
data['tone'] = data['tone'].apply(preprocess_text)


- Checks if 'category' and 'tone' columns exist, if not create them with empty strings.
- Defines a function to preprocess text by converting to lowercase, removing digits, and extra spaces.
- Applies preprocessing to relevant columns.

# Step 4: Load the spaCy model for named entity recognition (NER) and annotate the text data using NER
   
nlp = spacy.load('en_core_web_sm')
data['annotations'] = data['text'].apply(lambda x: [(ent.text, ent.label_) for ent in nlp(x).ents])
    
Explanation:
- Loads the spaCy model for named entity recognition (NER).
- Annotates the text data using NER by extracting entities and their labels.

# Step 5: Exploratory Data Analysis (EDA)
def plot_class_distribution(data):
    fig = px.histogram(data, x='category', title='Class Distribution')
    fig.show()

if 'category' in data.columns:
    plot_class_distribution(data)
Explanation:
- Defines a function to plot class distribution using Plotly Express.
- Checks if 'category' column is present in the data and plots class distribution.
 

# Step 6: Model Selection and Design
data['clean_text'] = data['clean_text'].fillna("")

def assign_category(text):
    if 'contract' in text:
        return 'Contract'
    elif 'royalty' in text:
        return 'Royalty'
    elif 'editor' in text:
        return 'Editor'
    elif 'impact factor' in text:
        return 'Impact Factor'
    elif 'meeting' in text:
        return 'Meeting'
    else:
        return 'Other'

data['category'] = data['text'].apply(assign_category)

vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(data['clean_text'])
y = data['category']

unique_categories = y.unique()
print(f"Unique categories in 'category' column: {unique_categories}")

if len(unique_categories) < 2:
    raise ValueError("The 'category' column needs to have at least two unique classes for model training.")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

Explanation:
- Replaces NaN values with empty strings in 'clean_text' column to avoid ValueError.
- Defines a rule-based categorisation function to assign categories based on keywords.
- Applies categorisation to the 'text' column.
- Uses TfidfVectorizer to convert text data into numerical features.
- Checks unique values in the 'category' column and ensures there are at least two unique classes.
- Splits the data into training and testing sets.
 

# Step 7: Hyperparameter Tuning and Model Training

models = {
    'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
    'LogisticRegression': LogisticRegression(random_state=42),
    'SVM': SVC(probability=True, random_state=42),
    'GradientBoosting': GradientBoostingClassifier(random_state=42)
}

param_grid = {
    'RandomForest': {'n_estimators': [50, 100, 200]},
    'LogisticRegression': {'C': [0.1, 1, 10]},
    'SVM': {'C': [0.1, 1, 10]},
    'GradientBoosting': {'n_estimators': [50, 100, 200]}
}

best_models = {}
for model_name, model in models.items():
    grid_search = GridSearchCV(model, param_grid[model_name], cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    best_models[model_name] = grid_search.best_estimator_

- Defines a dictionary of models to be trained.
- Defines a parameter grid for hyperparameter tuning.
- Performs grid search with cross-validation to find the best model for each algorithm.

# Step 8: Model Evaluation with adjusted precision metric

for model_name, model in best_models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"Model: {model_name}")
    print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
    print(f"Precision: {precision_score(y_test, y_pred, average='weighted')}")
    print(f"Recall: {recall_score(y_test, y_pred, average='weighted')}")
    print(f"F1-Score: {f1_score(y_test, y_pred, average='weighted')}")
    if hasattr(model, "predict_proba"):
        try:
            roc_auc = roc_auc_score(y_test, model.predict_proba(X_test), multi_class='ovr', average='weighted')
            print(f"ROC-AUC: {roc_auc}")
        except ValueError as e:
            print(f"ROC-AUC calculation error: {e}")
    print(classification_report(y_test, y_pred))

- Evaluates the best models using the test data.
- Prints accuracy, precision, recall, F1-score, and ROC-AUC for each model.

# Step 9: Visualise Classification Results

def plot_classification_results(y_test, y_pred):
    plt.figure(figsize=(10, 6))
    plt.hist([y_test, y_pred], label=['True Labels', 'Predicted Labels'], bins=10, alpha=0.7)
    plt.legend(loc='upper right')
    plt.title('Classification Results')
    plt.show()

plot_classification_results(y_test, best_models['RandomForest'].predict(X_test))

Explanation:
- Defines a function to plot classification results using histograms.
- Plots the classification results for one of the models (e.g., RandomForest).
 
# Step 10: Email Template Generation (Example)

def generate_email_template(subject, body_text):
    template = f"Subject: {subject}\\n\\n{body_text}"
    return template

subject_example = "Meeting Request"
body_text_example = "Dear [Recipient],\\n\\nI would like to schedule a meeting to discuss our upcoming project.\\n\\nBest regards,\\n[Your Name]"
email_template_example = generate_email_template(subject_example, body_text_example)
print(email_template_example)

Explanation:
- Defines a function to generate email templates.
- Provides an example usage of email template generation.
 
Rule-Based Categorisation 
Defining Categories: Identify the categories that we would like to assign to the text data. For example, in the context of email responses, categories might include "Contract," "Royalty," "Editor," "Impact Factor," "Meeting," and "Other."
Creating Rules: Developing a set of rules that map specific keywords or phrases to each category. These rules are based on the presence of certain words or patterns in the text.
Assigning Categories: Applying the rules to the text data to assign categories. If a text contains a keyword or phrase that matches a rule, it is assigned the corresponding category.
Example of Rule-Based Categorisation
def assign_category(text):
    if 'contract' in text:
        return 'Contract'
    elif 'royalty' in text:
        return 'Royalty'
    elif 'editor' in text:
        return 'Editor'
    elif 'impact factor' in text:
        return 'Impact Factor'
    elif 'meeting' in text:
        return 'Meeting'
    else:
        return 'Other'
Explanation of the Function
•	Function Definition: The function assign_category takes a single argument text, which is the text data to be categorised.
•	Keyword Matching: The function checks if specific keywords are present in the text using the in operator. The keywords are chosen based on their relevance to the categories:
o	If the text contains the keyword 'contract', it is assigned the category 'Contract'.
o	If the text contains the keyword 'royalty', it is assigned the category 'Royalty'.
o	If the text contains the keyword 'editor', it is assigned the category 'Editor'.
o	If the text contains the keyword 'impact factor', it is assigned the category 'Impact Factor'.
o	If the text contains the keyword 'meeting', it is assigned the category 'Meeting'.
•	Default Category: If none of the keywords match, the text is assigned the default category 'Other'.
Applying the Function
The function is applied to the text data using the apply method in pandas:
data['category'] = data['text'].apply(assign_category)
This line of code applies the assign_category function to each element in the text column of the data DataFrame and stores the resulting categories in the category column.
Disadvantages
•	Limited Flexibility: May not handle complex or nuanced text data well.
•	Scalability: Difficult to scale for large datasets with diverse categories.
•	Accuracy: May not be as accurate as machine learning-based approaches, especially for ambiguous or context-dependent text.
Rule-based categorisation may not be suitable for more complex or large-scale text classification problems. For more advanced categorisation labelled data can provide better accuracy and flexibility.

