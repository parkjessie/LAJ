#!/bin/bash 

source var.txt 
PREVIOUS_DIR=$(pwd)

# Beginning the actual script
echo "$(tput setaf 3) --- Current dir is: $PREVIOUS_DIR --- $(tput sgr 0)"

# Change directory to the project directory 
cd $PROJECT_DIR && echo "$(tput setaf 3) --- Changed dir to /home/ubuntu/FOSSite/ --- $(tput sgr 0)" 

git pull  # Does 'git pull'
EXIT_CODE=$?
# Assigns "$EXIT_CODE" to the exit code of the previous command (which in this case is 'git pull')
if [ "`git pull`" == "Already up to date." ] 
then
  # If the result of 'git pull' outputs "Already up to date.", we will just 
  # echo this text and exit the if-statement
  echo "$(tput setaf 3) --- Directory is already up to date. No need to restart service --- $(tput sgr 0)"
elif [ "$EXIT_CODE" = "0" ]
then 
  # If the exit code of 'git pull' is "0" (0 means the command was successful), we
  # will restart our service with 'systemctl'
  echo "$(tput setaf 2) --- 'git pull' was successful. Trying to restart service file... --- $(tput sgr 0)"
  sudo systemctl restart $SERVICE_FILE
  if [ "$?" == "0" ]
  then 
    # If the exit code of 'sudo systemctl restart $SERVICE_FILE' is 0, we will ask 
    # user if they want to check the status of $SERVICE_FILE
    read -p "$(tput setaf 1) --- Do you want to see the status of $SERVICE_FILE? This could be useful for debugging or making sure everything is all good. [Y/n] --- $(tput sgr 0)" SERVICE_FILE_STATUS
    if [ "$SERVICE_FILE_STATUS" == "y" ] || [ "$SERVICE_FILE_STATUS" == " "] 
    then
        # If the user answered "y" or just pressed the enter key, we will display the
        # status of $SERVICE FILE
        systemctl status $SERVICE_FILE_STATUS
    else
        # If the user answered "n" to the question, we will not show the status of $SERVICE_FILE
        echo "$(tput setaf 3) --- Ok, will not show the status of the file... --- $(tput sgr 0)"
    fi
  fi
else
  # If the exit code is NOT 0, we will just echo this text and exit the if-statement
  echo "$(tput setab 1) --- Could not complete 'git pull'... :( --- $(tput sgr 0)"        
fi

cd $PREVIOUS_DIR && echo "$(tput setaf 3) --- Changed dir back to $PREVIOUS_DIR --- $(tput sgr 0)" 
echo "$(tput setab 5) --- Done! --- $(tput sgr 0)"
# Changes back into the directory that the user was in before they ran this script,
# then exits the entire script
exit