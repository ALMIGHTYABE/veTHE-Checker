import time
import streamlit as st
import yaml
import requests
import pandas as pd

# App
st.set_page_config(
    page_title="🌊 OpenSea Listings",
    page_icon="icons/thena.png",
    layout="wide",
)

# Params
params_path = "params.yaml"


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


config = read_params(params_path)

# Title
st.title("🌊 OpenSea Listings")

try:
    listings_api = config["data"]["listings_api"]
except Exception as e:
    print(e)

# Listings Data
## Requests
response = requests.get(listings_api)
listings_data = response.json()

## Pandas Manipulation
listings_df = pd.DataFrame(listings_data)
listings_df = listings_df[listings_df["veLocked"] > 0]
listings_df["⏲️ Lock End Date"] = listings_df["veLockedTimestamp"].apply(lambda x: time.strftime("%Y-%m-%d", time.gmtime(int(x))))
listings_df["🛒 Discount %"] = (listings_df["valueUSD"] - listings_df["listedPriceUSD"]) / listings_df["valueUSD"]
listings_df.sort_values(by="🛒 Discount %", ascending=False, inplace=True)
listings_df["🔗 OS Link"] = listings_df["id"].apply(lambda x: '<a href="https://opensea.io/assets/bsc/0xfbbf371c9b0b994eebfcc977cef603f7f31c070d/' + str(x) + '">OS Link</a>')
listings_df.drop(
    columns=[
        "_id",
        "status",
        "listedThePrice",
        "currentThePrice",
        "currentBnbPrice",
        "veLockedEnd",
        "veLockedTimestamp",
        "voteLocked",
        "timeStamp",
        "events",
        "original",
    ],
    inplace=True,
)
listings_df.columns = [
    "🔢 Token ID",
    "🟨 Sale Price in BNB",
    "💰 Sale Price in USD",
    "🤑 veTHE Value in USD",
    "🧾 veTHE Balance",
    "🔒 Locked THE",
    "⏲️ Lock End Date",
    "🛒 Discount %",
    "🔗 OS Link",
]
listings_df = listings_df[
    [
        "🔢 Token ID",
        "🔒 Locked THE",
        "🧾 veTHE Balance",
        "🤑 veTHE Value in USD",
        "⏲️ Lock End Date",
        "🟨 Sale Price in BNB",
        "💰 Sale Price in USD",
        "🛒 Discount %",
        "🔗 OS Link",
    ]
]

# creating a single-element container
placeholder = st.empty()

# Empty Placeholder Filled
with placeholder.container():
    st.write(listings_df.to_html(escape=False, index=False, float_format="{:10.2f}".format), unsafe_allow_html=True)


# Note
st.markdown("#")
st.markdown("#")
st.caption(
    """
NFA, DYOR -- This web app is in beta, I am not responsible for any information on this page.

:red[The above list excludes veTHE which has not been vote reset or the locked value is very little or dust.]

:red[Negative Discount = Bad Deal = ngmi]
    
Special Thanks to **CryptoCult** for creating and providing access to the Listings API.
            """
)
