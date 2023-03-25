import streamlit as st

import pandas as pd
import random
import spacy
import numpy as np

import random

st.sidebar.title("Chatbot BoTravel")
st.title("""
Chatbot BoTravel
""")


# Importation du dataset 
def import_dataset():
    df = pd.read_csv('data/Hotel_Chatbot.csv',header =0)
    df['all'] = df['name'].astype(str) +" - "+ df["country"].astype(str) +" - "+ df["street"].astype(str) +" - "+ df["region"].astype(str) +" - "+ df["amenities"].astype(str) +" - "+ df["rooms"].astype(str) +" - "+ df["types"].astype(str) +" - "+ df["official_description"].astype(str) +" - "+ df["Address"].astype(str) 
    # Preprocess the data
    df = df.drop(columns=['p']) # remove the Unnamed: 0 column
    df = df.dropna() # remove any rows with missing values
    df['price'] = df['price'].astype(int) # convert the price column data type to int
    return df 


#Importation du modèle spacy En-Core-Web-SM
def spacy_model():
    nlp = spacy.load("en_core_web_sm")
    return nlp

#Salutations 
#def generate_greeting():
#    greeting_inputs_start = ("Hey", "Good morning", "Good evening", "Morning", "Evening", "Hi", "Whatsup",'hello')
#    reeting_responses_start = ['How can I help you ?','Hello you looking for an hotel somewhere ?', 'Hi, Where are you planning to travel ?']
#    greeting_inputs_end = ('bye', 'see you')
#    print(random.choice(greeting_inputs_start))

# import du modele Spacy
nlp = spacy_model()
# Import du dataset des hotels
df = import_dataset()

####################################################### ajout partie Hatim
# Amenities in individual rooms
room_amenities = [
    "air conditioning",
    "calcony",
    "facilities",
    "desk",
    "electronic/magnetic keys",
    "tv",
    "free toiletries",
    "hairdryer",
    "iron",
    "minibar",
    "smoking",
    "refrigerator",
    "room service",
    "slippers",
    "soundproofed rooms",
    "telephone",
    "wake-up service",
    "wheelchair accessibility"
]

# Amenities common to the hotel
hotel_amenities = [
    "shuttle",
    "bar",
    "business center",
    "concierge services",
    "currency exchange",
    "dry cleaning/laundry service",
    "fitness center/gym",
    "breakfast",
    "wifi",
    "wi-fi",
    "garden",
    "pool",
    "luggage storage",
    "meeting rooms",
    "multilingual staff",
    "parking",
    "restaurant",
    "spa",
    "terrace"
]

room_types = [
    "non-smoking",
    "suites",
    "family",
    "smoking",
    "room",
    "view",
    "rooms"
]

def get_amenities(user_input):
  amenities = None
  rooms = None
  words = user_input.split()
  
  for i in words:
    if i.lower() in hotel_amenities or i.lower() in room_amenities:
      amenities = 'asked'

    if i.lower() in room_types:
      rooms = 'asked'

  return amenities,rooms

def get_features(city, region, price, price_range,user_input):
  doc = nlp(user_input)
  amenities, rooms = get_amenities(user_input)

  for ent in doc.ents:
      #print(ent.label)
      if ent.label_ == 'GPE':
          #print('City')
          city = str(ent.text)

      if ent.label_ == 'LOC':
          #print('Region')
          region = str(ent.text)

      if ent.label_ == 'MONEY' or ent.label_ == 'CARDINAL':
          
          if len(doc.ents) > 3:
              #print('CARDINAL')
              price_range = (ent.text.split(' ')[0], ent.text.split(' ')[-1])
   
          else :
              price = int(ent.text)
              
  return city, region, price, price_range, amenities, rooms


def recommend_hotels(df,city,region,price,price_range):

    # Filter the DataFrame based on the user's requirements
    df_filtered = df.copy()
    if city:
      # Remove strip and lower to find a similar word
      df_filtered = df_filtered[df_filtered['city'].apply(lambda x : np.char.strip((x.lower()))) == np.char.strip(city.lower())]
    if region:
      # Remove strip and lower to find a similar word
      df_filtered = df_filtered[df_filtered['city'].apply(lambda x : np.char.strip(x.lower())) == np.char.strip(region.lower())]
    if price_range:
      df_filtered = df_filtered[(df_filtered['price'] >= int(price_range[0])) & 
                                  (df['price'] <= int(price_range[1]))]
    if price:
      df_filtered = df_filtered[(df_filtered['price'] <= int(price))]
    
    df_filtered = df_filtered.sort_values('rating', ascending=False)

    return df_filtered

greeting_inputs_start = ("hey", "good morning", "good evening", "morning", "evening", "hi", "whatsup",'hello')
greeting_responses_start = ['Hey how can I help you ?','Hello, are you looking for an hotel somewhere ?', 'Hi, Where are you planning to travel ?']
greeting_inputs_end = ('bye', 'see you', 'see ya')
import random

#takes a user input and generate a random answer 
def generate_greeting(greeting):
    for token in greeting.split():
        if token.lower() in greeting_inputs_start:
            return random.choice(greeting_responses_start)
        if token.lower() in greeting_inputs_end:
          return 'bye'

def display_amenities(df,i):
  formatted_string = df['amenities'][i].replace(",", "\n- ")
  answer = "Here are amenities of the hotel:\n- " + formatted_string
  st.write(f"Chatbot: {answer}")

def display_room_types(df,i):
  formatted_string = df['types'][i].replace(",", "\n- ")
  answer = "Here are the rooms types of the hotel:\n- " + formatted_string
  st.write(f"Chatbot: {answer}")


def display_hotels(df,city,amenities,rooms):
    if len(df) > 0:
        answer = 'We have ' + str(len(df)) + ' hotels in ' + city.title() + ' recommanded for you.'
        st.write(f"Chatbot: {answer}")

        answer = 'Here are the best hotels : '
        st.write(f"Chatbot: {answer}")
    
        
        for i in range(1,4):
            try:
                answer = str(i) + ') : ' + df['name'][i] + ' rated ' + str(df['Average_Rating'][i]) + '/5'
                st.write(f"Chatbot: {answer}")

                if amenities:
                    display_amenities(df,i)
                if rooms:
                    display_room_types(df,i)
            except:
                pass
    else:
        answer ='Sorry, there is no hotel with your criterias.'
        st.write(f"Chatbot: {answer}")


def launch():
    df_test = df
    city = None
    region = None
    price_range = None
    price = None

    human_text = st.text_input("Hey ! Where do you want to go nd what's your budget for a night ?").lower()
    if st.button('Answer'):
        if generate_greeting(human_text)!= 'bye':
            
            if human_text == 'thanks' or human_text == 'thank you very much' or human_text == 'thank you':
                continue_dialogue = False
                answer ="My pleasure."
                st.write(f"Chatbot: {answer}")

                
            
            elif human_text in ['1','2','3']:
                answer = 'Welcome to : ' + df_test['name'][int(human_text)] + ' !'
                st.write(f"Chatbot: {answer}")

                display_room_types(df_test,int(human_text))
                display_amenities(df_test,int(human_text))

            else:
                if generate_greeting(human_text) != None:
                    answer = "Chatbot : " + generate_greeting(human_text)
                    st.write(f"Chatbot: {answer}")

                else:
                    city, region, price, price_range, amenities, rooms = get_features(city, region, price, price_range,human_text)
                    answer = 'City : ' + str(city),', Region : ' + str(region),', Price : ' + str(price),', Price range : ' + str(price_range),', Amenities : ' + str(amenities), ', Rooms : ' + str(rooms)
                    st.sidebar.write(f"{answer}")
                    if city:
                        df_test = recommend_hotels(df, city, region, price, price_range).reset_index()              
                        display_hotels(df_test,city,amenities,rooms)
                    else:
                        answer ='Sorry, we did not find any hotel in this city.'
                        st.write(f"Chatbot: {answer}")



        else:
            answer = "Good bye and enjoy your trip ;)"
            st.write(f"Chatbot: {answer}")

launch()

