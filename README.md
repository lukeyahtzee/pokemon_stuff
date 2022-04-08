# pokemon_stuff

In engineering phase, laying groundwork for later data science insights, battles are conducted by user inputting an enumerated move value

Pokemon is cool, hope y'all enjoy

Proposed next steps: 
  - write function to assign a damage values to moves 
  - scale HP to coordinate with the damage dealt by each move

If extra time allows: 
  - transition from Jupyter to shell-based script

Once proposed changed are synced and concise, we will merge changes to master and begin next iteration!

## set_up

This will go throught the basics needed to:
1. Set up SSH keys for your local machine to update the repo remotely
2. Clone the pokemon_stuff repot as a local copy on your machine
3. Create your own branch and push to the main repot

### Setting up SSH Keys

You can see github's documentation for setting up SSH keys [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

1. Open your terminal

2. Check to see if you have any SSH keys on your machine already by running 'ls -al ~/.ssh'
'''

$ ls -al ~/.ssh
# Lists the files in your .ssh directory, if they exist
'''
3. In the ouput check and see if you have any existing keys. (Should be a file called one of the following)
'''
- id_rsa.pub
- id_ecdsa.pub
- id_ed25519.pub
'''

4. copy the SSH file by running:
'''

pbcopy < ~/.ssh/{your_file_name}.pub
# Copies the contents of the {your_file_name}.pub file to your clipboard
'''

5. Go to github.com and click on your icon in the top right and go to settings.
![dropdown to settings](/imgs/settings.png)

6. 

