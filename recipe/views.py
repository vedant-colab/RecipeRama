from django.shortcuts import render,redirect
import joblib
from django.views.decorators.csrf import csrf_exempt
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import ast
import datetime 
from recipe.models import Contact
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    '''Handles the home page of website'''
    return render(request, r"index.html")

model = joblib.load(r'model/recipe_model.pkl') #importing the pretrained model from pkl extension
data = pd.read_csv(r"model/preprocessed_dataset.csv") #importing the processed dataset to filter queries
vectorizer = TfidfVectorizer()
vectorizer.fit_transform(data['name'] + ' ' + data['ingredients'])

def suggest_recipes(query, num_suggestions):
    '''This function handles the query and num of suggestions from user and fetches the result from dataset'''
    query_vector = vectorizer.transform([query]) # Transform the query into a TF-IDF vector
    distances, indices = model.kneighbors(query_vector, n_neighbors=num_suggestions) # Get the indices and distances of the nearest neighbors
    suggested_recipe_indices = indices.flatten() # Get the suggested recipe indices
    suggested_recipes = data.iloc[suggested_recipe_indices] # Get the suggested recipes from the dataset
    output = []

    for index, row in suggested_recipes.iterrows():
        recipe_name = row['name']
        minutes= row['minutes']
        steps = ast.literal_eval(str(row['steps']))
        ingredients = row['ingredients']
        ingredients = [f"{x.strip()}" for x in ingredients.strip("[]").split(", ")]
        output.append([recipe_name,minutes,steps,ingredients])
    
    return output

@login_required(login_url='/userauth/login')
@csrf_exempt
def recommend(request):
    '''Recommendation fetching function which will not work untill the user is authenticated'''
    auth = False
    if request.user is not None:
        auth = True
        if request.method == "POST":
            recipeName = request.POST.get('recipeName') #user query of recipe name
            num_recipes = int(request.POST.get('numRecipes')) #the number of recipes a user want to see
            prediction = suggest_recipes(recipeName,num_recipes) #fetches the predictions from suggest recipe function
            # print(prediction)
            predictions = [
            (title, minutes, steps, ingredients)
            for index, (title, minutes, steps, ingredients) in enumerate(prediction) #processing the list of prediction
            ]
            return render(request,"recommend.html", {'prediction':predictions})
        return render(request, "recommend.html")
    
    else:
        return redirect('/userauth/login',{'auth':auth})

def contact(request):
    '''Handles the contact form for user'''
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        msg = request.POST.get('msg')
        contact = Contact(name=name, email=email, msg=msg, date=datetime.datetime.today())
        contact.save()
    return render(request,"contact.html")

def about(request):
    '''Handles the about form and functionality'''
    return render(request,'about.html')
