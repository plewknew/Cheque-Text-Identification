# Cheque Text Identification 
 
 The purpose of this repo is to explore the potential use of the Azure text recognition model as a way to identify where and what the text is on a cheque. This could be used to verify or identify individuals based on the name and text inputted.
 
 One additional potential extension of this project is to do some basic identification on an individual's signature. If someone submits a signature that is unlike the previous signatures that they submitted, it could be flagged as being potentially fraudulent.
 
 Note that the main() function was not included in this repo, as it would include my Azure subscription code. As such, an additional python script must be created locally using the following text. This is then the main function that will be run in order to run the image recognition script.  
 
 Main function:<br/>
<br/>
import numpy as np<br/>
import pandas as pd<br/>
import requests<br/>
import Cheque_Recog<br/>

def main():<br/>
    subscription_key = "INSERT_SUB_KEY"<br/>
    pic_url = input("Enter a picture of a cheque URL: ") <br/>
    Cheque_Recog.check_cheque(subscription_key,pic_url)<br/>
    <br/>
main()<br/>
 <br/>
This repo is still a work in progress.
