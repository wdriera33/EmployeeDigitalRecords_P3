import streamlit as st
from dataclasses import dataclass
from typing import Any, List
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

# @TODO:
# From `crypto_wallet.py import the functions generate_account, get_balance,
#  and send_transaction
from crypto_wallet import w3, generate_account, get_balance, send_transaction

################################################################################
# Fintech Finder Candidate Information

# Database of Fintech Finder candidates including their name, digital address, rating and hourly cost per Ether.
# A single Ether is currently valued at $1,500
candidate_database = {
    "AmauryBatista": ["AmauryBatista", "0x3d3951af5E268D9A50e5Be510bFfd0A3A9ad15dA", "4.3", .20, "Images/AmauryBatista.jpeg"],          
    "CamiloArias": ["CamiloArias", "0x11e53Fa0b78793dAd5b5e899ef77fA389e793ee0", "5.0", .33, "Images/CamiloArias.jpeg"],
    "YosMelGarcia": ["YosMelGarcia", "0x1964EB9775E0E08f5D26882B646F44c5df5ace24", "4.7", .19, "Images/YosMelGarcia.jpeg"],  
    "YulietMesa": ["YulietMesa", "0x87387F1101f539e288f338DB706B1209c59eE74A", "4.1", .16, "Images/YulietMesa.jpeg"]
}

# A list of the FinTech Finder candidates first names
people = ["AmauryBatista", "CamiloArias", "YosMelGarcia", "YulietMesa"]


def get_people():
    """Display the database of Fintech Finders candidate information."""
    db_list = list(candidate_database.values())

    for number in range(len(people)):
        st.image(db_list[number][4], width=200)
        st.write("Name: ", db_list[number][0])
        st.write("Ethereum Account Address: ", db_list[number][1])
        st.write("Driving Score: ", db_list[number][2])
       #  st.write("Hourly Rate per Ether: ", db_list[number][3], "eth")
        st.text(" \n")

################################################################################
# Streamlit Code

# Streamlit application headings
st.image("https://gateway.pinata.cloud/ipfs/QmeajV7L4NSDv2NiDiabxMQwiXRDfagbbsa8UKs57wwKxZ", width=200)
st.markdown("# Employee Bonus Program")
st.markdown("## Employee Score Improvement Review")
st.text(" \n")

################################################################################
# Streamlit Sidebar Code - Start
st.sidebar.markdown("## Employee DigitalWallet Ethereum Balance")

# @TODO:
#  Call the `generate_account` function and save it as the variable `account`
account = generate_account()

##########################################

# Write the client's Ethereum account address to the sidebar
st.sidebar.write(account.address)

# @TODO
# Call `get_balance` function and pass it your account address
# Write the returned ether balance to the sidebar
ether = get_balance(w3, account.address)
st.sidebar.write(ether)

st.sidebar.markdown("## Company Balance of Ether")
st.sidebar.markdown(ether)
st.sidebar.markdown("---------")
##########################################

# Create a select box to chose a FinTech Hire candidate
person = st.sidebar.selectbox('Select a Person', people)

# Create a input field to record the Bonus in Ether the candidate worked
# hours = st.sidebar.number_input("Bonus in Ether")

st.sidebar.markdown("## Candidate Name and Ethereum Address")

# Identify the FinTech Hire candidate
candidate = candidate_database[person][0]

# Write the Fintech Finder candidate's name to the sidebar
st.sidebar.write(candidate)

# Identify the FinTech Finder candidate's hourly rate
#hourly_rate = candidate_database[person][3]

# Write the inTech Finder candidate's hourly rate to the sidebar
# st.sidebar.write(hourly_rate)

# Identify the FinTech Finder candidate's Ethereum Address
candidate_address = candidate_database[person][1]

# Write the inTech Finder candidate's Ethereum Address to the sidebar
st.sidebar.write(candidate_address)

# Write the Fintech Finder candidate's name to the sidebar

st.sidebar.markdown("## Total Wage in Ether")


# @TODO
# Calculate total `wage` for the candidate by multiplying the candidate’s hourly
# rate from the candidate database (`candidate_database[person][3]`) by the
# value of the `hours` variable
#wage = candidate_database[person][3] * hours
wage = 10 
# @TODO
# Write the `wage` calculation to the Streamlit sidebar
st.sidebar.write(wage)


if st.sidebar.button("Send Transaction"):

    # @TODO
    # Call the `send_transaction` function and pass it 3 parameters:
    # Your `account`, the `candidate_address`, and the `wage` as parameters
    # Save the returned transaction hash as a variable named `transaction_hash`
    transaction_hash = send_transaction(w3, account, candidate_address, wage)
    # Markdown for the transaction hash
    st.sidebar.markdown("#### Validated Transaction Hash")

    # Write the returned transaction hash to the screen
    st.sidebar.write(transaction_hash)

    # Celebrate your successful payment
    # st.balloons()

# The function that starts the Streamlit application
# Writes FinTech Finder candidates to the Streamlit page
get_people()

