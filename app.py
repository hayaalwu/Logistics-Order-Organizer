import streamlit as st
from parser import parse_orders
from route_optimizer import generate_route


# Configure the page layout
st.set_page_config(page_title="Logistics Order Organizer", page_icon="📦", layout="wide")

# Display the application title
st.title("📦 Logistics Order Organizer")
st.write("Convert messy logistics orders into a structured delivery plan.")

# Read the sample input file
with open("sample_input.txt", "r") as file:
    default_text = file.read()

# Display the input text
order_text = st.text_area("Input Orders", value=default_text, height=150)

# Generate the delivery plan
if st.button("Organize Orders"):

    # Parse the input orders
    df = parse_orders(order_text)

    # Display the structured table
    st.subheader("Structured Delivery Plan")
    st.dataframe(df, use_container_width=True)

    # Display summary metrics
    st.subheader("Summary")
    st.metric("Total Jobs", len(df))
    st.metric("Urgent Jobs", len(df[df["Priority"] == "Urgent"]))

    # Generate the suggested visiting route
    st.subheader("Suggested Visiting Order")

    stops = df["Stop"].unique().tolist()
    route = generate_route(stops)

    st.write(" → ".join(route))

# Display a default message before parsing
else:
    st.subheader("Suggested Visiting Order")
    st.info("Waiting for order parsing...")