import streamlit as st
import csv

# Define the Fashion Types and their corresponding Outfit Choices
fashion_outfits = {
    "Casual Streetwear": "Denim jeans, a graphic T-shirt, and sneakers",
    "Bohemian/Boho Chic": "Flowy maxi dress and sandals",
    "Vintage-inspired": "High-waisted pants, a blouse, and heels",
    "Minimalist": "A-line skirt, tucked-in blouse, and ballet flats",
    "Preppy": "Tailored blazer, trousers, and oxford shoes",
    "Edgy/Rock-inspired": "Leather jacket, band T-shirt, ripped jeans, and ankle boots",
    "Romantic/Feminine": "Floral sundress and wedges",
    "Sporty/Active": "Hoodie, leggings, and athletic shoes",
    "Professional/Business": "Pencil skirt, button-down shirt, and pumps",
    "Artsy/Eclectic": "Wide-leg pants, a crop top, and platform sandals",
    "Classic": "Trench coat, white button-down shirt, black trousers, and loafers",
    "Glamorous": "Sequin dress, high heels, and statement jewelry",
    "Punk": "Plaid shirt, leather pants, combat boots, and spikes",
    "Retro": "Polka dot swing dress, cat-eye sunglasses, and slingback heels",
    "Urban": "Distressed jeans, oversized hoodie, and sneakers",
    "Boho Rock": "Fringe jacket, band T-shirt, ripped jeans, and ankle boots",
    "Casual Chic": "Tailored blazer, jeans, a basic tee, and ankle boots",
    "Preppy Glam": "Plaid skirt, cashmere sweater, and pointed-toe flats",
    "Artsy Minimalist": "Flowy culottes, a structured top, and mules",
    "Romantic Boho": "Floral maxi skirt, lace blouse, and strappy sandals",
    "Sporty Chic": "Track pants, a fitted top, and chunky sneakers",
    "Vintage Glam": "Velvet dress, retro accessories, and kitten heels",
    "Boho Minimalist": "Wide-leg trousers, a linen shirt, and slide sandals",
    "Futuristic": "Metallic jacket, asymmetrical dress, and platform boots",
    "Sophisticated": "Tailored jumpsuit, statement necklace, and stiletto pumps",
    "Street Style": "Oversized hoodie, distressed jeans, and chunky sneakers",
    "Ethereal": "Flowing white dress, flower crown, and strappy sandals",
    "Military-Inspired": "Cargo pants, army green jacket, and combat boots",
    "Casual Elegance": "Midi skirt, tucked-in blouse, and block heels",
    "Retro Hipster": "High-waisted shorts, graphic tee, denim jacket, and sneakers",
    "Chic Bohemian": "Embroidered peasant top, flared jeans, and wedges",
    "Effortlessly Cool": "Leather biker jacket, striped tee, skinny jeans, and boots",
    "Vintage Boho": "Crochet top, flared pants, and platform sandals",
    "Playful Retro": "Printed playsuit, cat-eye sunglasses, and espadrilles",
    "Artistic Edge": "Abstract print top, pleated skirt, and ankle strap heels"
}

# Create a Streamlit app
def main():
    st.title("Fashion Outfit Selector")

    # Input fields for User ID, Age, and Gender
    user_id = st.text_input("User ID")
    age = st.number_input("Age", min_value=0, max_value=100)
    gender = st.radio("Gender", ["Male", "Female", "Other"])

    # Select the Fashion Type from a dropdown with auto-suggest
    selected_fashion_type = st.selectbox("Fashion Type", list(fashion_outfits.keys()), key="fashion_type")

    # Display the selected Fashion Type
    st.write("Selected Fashion Type:", selected_fashion_type)

    # Display the corresponding Outfit Choice
    st.write("Outfit Choice:", fashion_outfits[selected_fashion_type])

    # Button to save the data to a CSV file
    if st.button("Save"):
        save_data(user_id, age, gender, selected_fashion_type)

def save_data(user_id, age, gender, fashion_type):
    # Prepare the data as a dictionary
    data = {
        "User ID": user_id,
        "Age": age,
        "Gender": gender,
        "Fashion Type": fashion_type,
        "Outfit Choice": fashion_outfits[fashion_type]
    }

    # Append the data to the CSV file
    with open("./csvfiles/fashion_data.csv", "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        writer.writerow(data)

    # Display success message
    st.success("Data saved successfully!")

if __name__ == "__main__":
    main()
