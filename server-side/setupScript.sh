#!/bin/bash 

echo "$(tput setaf 2) 
##################################################
#  Welcome to the setup script!                  #
#  We need to set up a few directories in order  #
#  for this to work properly.                    #
# $(tput setaf 1) Also, please only run this script once. $(tput setaf 2)      # 
##################################################
"
echo "
##############################################################
#  Please enter the directory where the project is stored.   #
#  Please use the full path (don't use '~' in the path).     #
# $(tput sgr 0) (Correct: /home/ubuntu/MySite/) (Incorrect: ~/MySite) $(tput setaf 2)    #
############################################################## $(tput sgr 0)
"

while : ; do    # loops forever until user enters "y"  
    read -p  "Enter your project's directory here: " PROJECT_DIR
    echo "$(tput setaf 3) You entered: $(tput sgr 0) $PROJECT_DIR"
    read -p "Is this correct? [y/n]: " confirm
    [[ "$confirm" != "y" ]] || break    # breaks loop with "y" 
done

touch ~/LAJ/server-side/var.txt

echo "export \$PROJECT_DIR=$PROJECT_DIR" > ~/LAJ/server-side/var.txt

sleep 0.5

# Systemd service file setup
echo "$(tput setaf 2) 
#################################################
#  Now please enter the systemd file            #
# $(tput sgr 0) (Example: MySite.service or FOSSite.service) $(tput setaf 2)# 
################################################# $(tput sgr 0)
"
while : ; do 
    read -p  "Enter your project's systemd service file here: " PROJECT_SYSTEMD_FILE
    echo "$(tput setaf 3) You entered: $(tput sgr 0) $PROJECT_SYSTEMD_FILE"
    read -p "Is this correct? [y/n]: " confirm1
    [[ "$confirm1" != "y" ]] || break    
done

echo "export \$PROJECT_SYSTEMD_FILE=$PROJECT_SYSTEMD_FILE" >> ~/LAJ/server-side/var.txt

exit