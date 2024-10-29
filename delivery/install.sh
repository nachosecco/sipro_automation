command -v curl >/dev/null 2>&1 || { echo >&2 "I require curl but it's not installed.  Aborting."; exit 1; }


#Installing ChromeDriver

CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`

if [ ! -d "/opt/chromedriver-$CHROMEDRIVER_VERSION"]
then
      mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION
      curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip 
      unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION
      rm /tmp/chromedriver_linux64.zip 
      chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver 
      ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver
fi     



if [[ $OSTYPE == 'linux-gnu'* ]]; then
    echo 'linux, asuming is ubuntu'

    command -v curl >/dev/null 2>&1 || { echo >&2 "I require curl but it's not installed.  Aborting."; exit 1; }
  
    curl https://pyenv.run | bash

    
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc

    source ~/.bashrc
fi

if [[ $OSTYPE == 'darwin'* ]]; then
  #https://faun.pub/pyenv-multi-version-python-development-on-mac-578736fb91aa
  echo 'macOS, for installing this is required Homebrew'
  
  command -v brew >/dev/null 2>&1 || { echo >&2 "I require brew but it's not installed.  Aborting."; exit 1; }

    
  xattr -d com.apple.quarantine /usr/local/bin/chromedriver


  brew update
  brew install pyenv
  FILE=~/.zprofile

  if test -f "$FILE"; then
        echo "Configuring zprofile"

        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zprofile
        echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zprofile
        echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.zprofile  
  else 
        echo "Configuring bash_profile"

        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
        echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
        echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile  

  fi

fi

exec "$SHELL"


echo 'Installing required python version'
pyenv install 3.8.10 -f

echo 'Selecting required python version'

pyenv local 3.8.10

pyenv virtualenv 3.8.10 c6-autodelivery

pyenv activate c6-autodelivery

pip3 install -r requirements.txt

pyenv deactivate 
