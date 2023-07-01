import os
import streamlit as st
import pandas as pd

# Fashion Choices
fashion_choices = {
    "Casual Streetwear": [
        "Denim jeans, a graphic T-shirt, and sneakers",
        "Hoodie, leggings, and athletic shoes",
        "Distressed jeans, oversized hoodie, and sneakers"
    ],
    "Bohemian/Boho Chic": [
        "Flowy maxi dress and sandals",
        "Floral sundress and wedges",
        "Embroidered peasant top, flared jeans, and wedges"
    ],
    "Vintage-inspired": [
        "High-waisted pants, a blouse, and heels",
        "Polka dot swing dress, cat-eye sunglasses, and slingback heels",
        "Crochet top, flared pants, and platform sandals"
    ],
    "Minimalist": [
        "A-line skirt, tucked-in blouse, and ballet flats",
        "Cuffed chinos, a polo shirt, and loafers",
        "Flowy culottes, a structured top, and mules"
    ],
    "Preppy": [
        "Tailored blazer, trousers, and oxford shoes",
        "Plaid skirt, cashmere sweater, and pointed-toe flats",
        "Tailored jumpsuit, statement necklace, and stiletto pumps"
    ],
    "Edgy/Rock-inspired": [
        "Leather jacket, band T-shirt, ripped jeans, and ankle boots",
        "Plaid shirt, leather pants, combat boots, and spikes",
        "Leather biker jacket, striped tee, skinny jeans, and boots"
    ],
    "Athleisure": [
        "Athletic leggings, sports bra, and sneakers",
        "Track pants, hoodie, and trainers",
        "Sports shorts, tank top, and running shoes"
    ],
    "Glamorous": [
        "Sequin gown, statement earrings, and high heels",
        "Silk slip dress, faux fur coat, and strappy sandals",
        "Form-fitting cocktail dress, statement clutch, and stiletto heels"
    ]
    # Add more fashion types and outfit choices here
}

# CSV file path
csv_file = "./csvfiles/fashion_data_forHkz_run.csv"


# Function to append data to CSV file
def append_data_to_csv(data):
    if not os.path.isfile(csv_file) or os.path.getsize(csv_file) == 0:
        pd.DataFrame([data]).to_csv(csv_file, index=False)
    else:
        df = pd.read_csv(csv_file)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv(csv_file, index=False)


def main():
    st.title("Fashion Outfit Selector")
    
    # User inputs
    user_id = st.text_input("User ID")
    age = st.text_input("Age")
    gender = st.selectbox("Gender", ["Male", "Female"])
    
    # Fashion Type selection
    fashion_type = st.selectbox("Select Fashion Type", list(fashion_choices.keys()))
    
    # Outfit Choices based on selected Fashion Type
    if fashion_type:
        outfit_choices = fashion_choices[fashion_type]
        outfit_choice = st.selectbox("Select Outfit Choice", outfit_choices)
        # st.subheader("Selected Outfit:")
        # st.write(outfit_choice)
        
        # Save Outfit button
        if st.button("Save Outfit"):
            data = {
                "UserID": user_id,
                "Age": age,
                "Gender": gender,
                "FashionType": fashion_type,
                "OutfitChoice": outfit_choice
            }
            append_data_to_csv(data)
            st.success("Outfit saved successfully!")

if __name__ == "__main__":
    main()
