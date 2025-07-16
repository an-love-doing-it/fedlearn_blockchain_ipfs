###Python ver 3.13.3

To use this repo:

- create a virtual environment
- download/clone this repo to a another folder same level to the virtual env
- make sure the folder directly contain run.sh file
- install the requirements.txt
- change your model, and other utils through the model.py file in scripts/model
- make your solidity contract which must have:
  - a constructor which take the initiative model
  - a function to submit the model
  - any other function in order to call must be added to solidity_helper.py
- run the script through run.sh file
