#!/usr/bin/env bash

# ToDo
#
# Add BSD, SuSE options etc

# Check if sox is available already
if [[ -x "$(command -v sox)" ]]; then
    echo "SoX is already installed."
    sox_installed="True"
else
    sox_installed="False"
fi

# Install sox is not already present
if [[ $sox_installed = "False" ]]; then
        echo "This script will issue a sudo call to install SoX."
        echo "If you wish to keep it portable then maybe just install it yourself."
        echo -n "Would you like to continue? Y/n "
        read answer
        if [[ $answer == "y" || $answer == "Y" ]]; then
                # Check for different versions of Linux
                if [[ -x "$(command -v pacman)" ]]; then
                    echo "Installing for arch"
                    sudo pacman -S sox
                elif [[ -x "$(command -v apt)" ]]; then
                    echo "Debian/Ubuntu"
                    sudo apt install sox
                fi
        else
            # Exits if the user did not say yes
            exit
        fi
fi

# Copy soxnoise.py to /usr/bin
echo -n "The next step is to install soxnoise to /usr/bin. Would you like to continue? "
read answer
if [[ answer == "y" || answer == "Y" ]]; then
        sudo cp soxnoise.py /usr/bin/soxnoise.py
fi

