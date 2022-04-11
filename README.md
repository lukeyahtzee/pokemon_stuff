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
1. [Setting up SSH Keys](https://github.com/lukeyahtzee/pokemon_stuff/tree/main#setting-up-ssh-keys)
2. [Clone Repo Using SSH](https://github.com/lukeyahtzee/pokemon_stuff/tree/main#clone-repo-using-ssh)
3. [Create your own branch and push to the main repo](https://github.com/lukeyahtzee/pokemon_stuff/tree/main#create-your-own-branch-and-push-to-the-main-repo)

### Setting up SSH Keys

You can see github's documentation for setting up SSH keys [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

1. Open your terminal

2. Check to see if you have any SSH keys on your machine already by running 'ls -al ~/.ssh

```
$ ls -al ~/.ssh
# Lists the files in your .ssh directory, if they exist
```
3. In the ouput check and see if you have any existing keys. (Should be a file called one of the following)

```
- id_rsa.pub
- id_ecdsa.pub
- id_ed25519.pub
```

4. copy the SSH file by running:

```
pbcopy < ~/.ssh/your_file_name.pub
# Copies the contents of the your_file_name.pub file to your clipboard
```
This will copy the SSH key to your clipboard

5. Add ssh to your github account. 
  - go to github.com, click on your profile in the top right, and click on settings. 

  ![dropdown to settings](/imgs/settings.png)

  - Navigate to SSH and GPG keys and hit the green New SSH key button

  ![nav to  new ssh key button](/imgs/new_ssh_key.png)

  - Name your SSh key (whatever you want) and past your key in the box. 

  ![nav to add new ssh key](/imgs/add_ssh_keys.png)

Once SSH keys are update you can now clone repos to your machine using SSH. 

### Clone Repo Using SSH

1. Open Terminal
2. Navigate to the directory where you want to store your code on your machine. 
  I created a pokemon folder in my Documents folder. 
  ```
  cd Documents/pokemon
  ```
3. Go to the github repo you want to clone [here](https://github.com/lukeyahtzee/pokemon_stuff). 
4. Click on the green code button, select SSH, and copy the text that populates.

  ![copy ssh key from repo](/imgs/clone_via_ssh.png)

5. Open Terminal again and enter the below command. 
This will create a -local- copy of the repository on your machine. 
```
git clone paste_text_here
```

### Create your own branch and push to the main repo

1. Now that you have a local copy of the repo, you can create your own branch by running:
```
git checkout -b your-branch-name
```

2. This creates a branch on your -local- copy of the repo. We want it to be added to the main repo, so we need to push our updates. 

``` 
git push -u origin your-branch-name
```

3. Once you complete the updates, you can go to the github repo, refresh and see your branch on the Main repo

![see the new branch on the main repo](/imgs//see_new_branch.png)