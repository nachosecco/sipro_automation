#
command -v curl >/dev/null 2>&1 || { echo >&2 "I require curl but it's not installed.  Aborting."; exit 1; }


#Installing ChromeDriver

CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`

      echo "Installing Chrome Driver latest - $CHROMEDRIVER_VERSION"

      mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION
      curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip
      unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION
      rm /tmp/chromedriver_linux64.zip
      chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver
      ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver

      echo 'Success Installing latest'


