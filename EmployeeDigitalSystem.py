import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

load_dotenv()

# Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))


# Load_Contract Function
@st.cache(allow_output_mutation=True)
def load_contract():

    # ABI Contract
    with open(Path('./contracts/compiled/EmployeeRegistration_abi.json')) as f:
        contract_abi = json.load(f)

    # Contract address 
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract


# Load the contract
contract = load_contract()


#Pin files and json to Pinata
def pin_ertwork(employee_name, ertwork_file):
    
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(ertwork_file.getvalue())

    # Token metadata file for the employee digital wallet
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
#st.title("Employee DigitalWallet System")
#st.write("Choose a digitalwallet for driver")

#accounts = w3.eth.accounts
#address = st.selectbox("Select Account", options=accounts)
#st.markdown("---")


# Register New Employee
st.title("Employee DigitalWallet System")


st.markdown("---")
#st.markdown("---")


st.markdown("## Register New Employee")
employee_name = st.text_input("Enter the first & last name of the driver")
birth_year = st.text_input("Enter the birth year of the driver")        
original_cld_year = st.text_input("Enter the original cld year of the driver")
employee_violations = st.text_input("Enter the number of violations of the driver")
employee_accidents = st.text_input("Enter the number of accidents of the driver")
initial_employee_value = st.text_input("Enter the initial employee score")

st.write("Choose a digitalwallet for driver")

accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)

# Streamlit `file_uploader` function create the list of digital image file types(jpg, jpeg, or png) that will be uploaded to Pinata.
file = st.file_uploader("Upload Employee Document", type=["jpg", "jpeg", "png"])

if st.button("Click to Register New Employee"):

    # Use the `pin_ertwork` function to pin the file to IPFS
    ertwork_ipfs_hash, token_json = pin_ertwork(employee_name, file)

    ertwork_uri = f"ipfs://{ertwork_ipfs_hash}"

    tx_hash = contract.functions.registerEmployee(
        address,
        employee_name,
        birth_year,
        original_cld_year,
        employee_violations,
        employee_accidents,
        int(initial_employee_value),
        ertwork_uri,
        token_json['image']
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))

st.markdown("---")



# Update Employee Score
st.markdown("## Employee Score Improvement Review")
tokens = contract.functions.totalSupply().call()
token_id = st.selectbox("Choose an ERT Token ID", list(range(tokens)))
new_employee_score = st.text_input("Enter the new score")
employee_report_content = st.text_area("Enter details for the Driver Report")


if st.button("Click to Update Employee Score"):

    # Make a call to the contract to get the image uri
    image_uri = str(contract.functions.imageUri(token_id).call())
    
    # Use Pinata to pin a report for the report content
    employee_report_ipfs_hash =  pin_employee_report(employee_report_content+image_uri)

    # Copy and save the URI to this report for later use as the smart contract’s `reportURI` parameter.
    report_uri = f"ipfs://{employee_report_ipfs_hash}"

    tx_hash = contract.functions.newScore(
        token_id,
        int(new_employee_score),
        report_uri,
        image_uri

    ).transact({"from": w3.eth.accounts[0]})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(receipt)
st.markdown("---")


# Get Employee History

#st.markdown("## Employee Digital Record History")
#ERT_token_id = st.number_input("Employee ID", value=0, step=1)
#if st.button("Get Employee Records"):
    #employee_filter = contract.events.employee.createFilter(
        #fromBlock=0, argument_filters={"tokenId": ERT_token_id}
    #)
    #reports = employee_filter.get_all_entries()
    #if reports:
        #for report in reports:
            #report_dictionary = dict(report)
            #st.markdown("### Employee Records Event Log")
            #st.write(report_dictionary)
            #st.markdown("### Pinata IPFS Report URI")
            #report_uri = report_dictionary["args"]["reportURI"]
            #report_ipfs_hash = report_uri[7:]
            #image_uri = report_dictionary["args"]["artJson"]
            #st.markdown(
            #    f"The report is located at the following URI: "
            #    f"{report_uri}"
            # )
            #st.write("You can also view the report URI with the following ipfs gateway link")
            #st.markdown(f"[IPFS Gateway Link](https://ipfs.io/ipfs/{report_ipfs_hash})")
            #st.markdown("### Employee Event Details")
            #st.write(report_dictionary["args"])
            #st.image(f'https://ipfs.io/ipfs/{image_uri}')
    #else:
        #st.write("This employee has no new history")

        ########################################################################
st.markdown("## Employee Digital Records")
ert_token_id = st.number_input("Employee ERT Token #", value=0, step=1)
if st.button("Get Employee Records"):
    employee_filter = contract.events.Score.createFilter(
        fromBlock=0, argument_filters={"tokenId": ert_token_id}
    )
    reports = employee_filter.get_all_entries()
    if reports:
        for report in reports:
            report_dictionary = dict(report)
            st.markdown("### Employee Records Event Log")
            st.write(report_dictionary)
            st.markdown("### Pinata IPFS Report URI")
            report_uri = report_dictionary["args"]["reportURI"]
            report_ipfs_hash = report_uri[7:]
            image_uri = report_dictionary["args"]["ertJson"]
            st.markdown(
                f"The report is located at the following URI: "
                f"{report_uri}"
            )
            st.write("You can also view the report URI with the following ipfs gateway link")
            #st.markdown(f"[IPFS Gateway Link](https://ipfs.io/ipfs/{report_ipfs_hash})")
            st.markdown("### Employee Event Details")
            st.write(report_dictionary["args"])
            st.image(f'https://ipfs.io/ipfs/{image_uri}')
    else:
        st.write("This employee has no new history")