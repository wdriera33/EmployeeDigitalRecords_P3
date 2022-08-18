import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Load_Contract Function
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('EmployeeRegistry_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract


# Load the contract
contract = load_contract()

st.write(contract.functions.totalSupply().call())
################################################################################
# Helper functions to pin files and json to Pinata
################################################################################


def pin_employee(employee_name, employee_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(employee_file.getvalue())
  
    # Build a token metadata file for the artwork
    token_json = {
        "name": employee_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash, token_json


def pin_employee_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash

st.image("https://gateway.pinata.cloud/ipfs/QmeajV7L4NSDv2NiDiabxMQwiXRDfagbbsa8UKs57wwKxZ", width=200)
st.title("Truck Driver DigitalWallet System")
st.write("Choose a wallet for new driver")
accounts = w3.eth.accounts
# address = st.selectbox("Select Account", options=accounts)
st.markdown("---")

################################################################################
# Register Employee
################################################################################
st.markdown("## Register New Truck Driver")
employee_wallet = st.text_input("Enter the employee wallet address")
employee_name = st.text_input("Enter the first & last name of the driver")
birth_year = st.text_input("Enter the birth year of the driver")        
original_cld_year = st.text_input("Enter the original cld year of the driver")
employee_violations = st.text_input("Enter the number of violations of the driver")
employee_accidents = st.text_input("Enter the number of accidents of the driver")
initial_employee_value = st.text_input("Enter the initial employee score")
attachment = st.text_input("Enter link to attachment")

# Use the Streamlit `file_uploader` function create the list of digital image file types(jpg, jpeg, or png) that will be uploaded to Pinata.
# file = st.file_uploader("Upload Employee Record", type=None)

if st.button("Validate Driver"):
   st.image(attachment, width=200)

st.markdown("---")
if st.button("Register Driver"):
    
    tx_hash = contract.functions.onboardingEmployee (
        employee_wallet,
        employee_name,
        birth_year,     
        original_cld_year, 
        employee_violations, 
        employee_accidents, 
        int(initial_employee_value), 
        attachment,
    
    ).transact({'from': employee_wallet, 'gas': 1000000})
   

    st.markdown("---")
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
    st.write("Look at the uploaded records using this link:")
  #  st.markdown(f"[Employee IPFS Gateway Link](https://ipfs.io/ipfs/{employee_ipfs_hash})")
  #  st.markdown(f"[Employee IPFS Image Link](https://ipfs.io/ipfs/{token_json['image']})")

st.markdown("---")

################################################################################
# Get Employee
################################################################################
st.markdown("## Employee Score")
tokens = contract.functions.totalSupply().call()
token_id = st.selectbox("Choose an ERT Token ID", list(range(tokens)))
new_employee_value = st.text_input("Enter the new appraisal amount")
employee_report_content = st.text_area("Enter details for the Driver Report")

if st.button("Employee Score"):

    # Make a call to the contract to get the image uri
    image_uri = str(contract.functions.imageUri(token_id).call())
    
    # Use Pinata to pin an appraisal report for the report content
    employee_report_ipfs_hash =  pin_employee_report(employee_report_content+image_uri)

    # Copy and save the URI to this report for later use as the smart contract’s `reportURI` parameter.
    report_uri = f"ipfs://{employee_report_ipfs_hash}"

    tx_hash = contract.functions.newEmployee(
        token_id,
        int(new_employee_value),
        report_uri,
        image_uri

    ).transact({"from": w3.eth.accounts[0]})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(receipt)
st.markdown("---")

################################################################################
# Get Employee Update
################################################################################
st.markdown("## Get the Employee report history")
ERT_token_id = st.number_input("Employee ID", value=0, step=1)
if st.button("Get Employee Reports"):
    employee_filter = contract.events.employee.createFilter(
        fromBlock=0, argument_filters={"tokenId": ERT_token_id}
    )
    reports = employee_filter.get_all_entries()
    if reports:
        for report in reports:
            report_dictionary = dict(report)
            st.markdown("### Employee Report Event Log")
            st.write(report_dictionary)
            st.markdown("### Pinata IPFS Report URI")
            report_uri = report_dictionary["args"]["reportURI"]
            report_ipfs_hash = report_uri[7:]
            image_uri = report_dictionary["args"]["artJson"]
            st.markdown(
                f"The report is located at the following URI: "
                f"{report_uri}"
            )
            st.write("You can also view the report URI with the following ipfs gateway link")
            st.markdown(f"[IPFS Gateway Link](https://ipfs.io/ipfs/{report_ipfs_hash})")
            st.markdown("### Employee Event Details")
            st.write(report_dictionary["args"])
            st.image(f'https://ipfs.io/ipfs/{image_uri}')
    else:
        st.write("This employee has no new history")
