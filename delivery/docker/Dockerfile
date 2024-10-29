FROM python:3.8

#ChromeDriver
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -yqq unzip



# Install Chrome WebDriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
    ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver



# Install Google Chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -yqq update && \
    apt-get -yqq install google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# set display port to avoid crash
ENV DISPLAY=:99

#This is automation build part
RUN mkdir automation && \
    mkdir results

WORKDIR /automation

COPY . /automation

RUN pip install -r /automation/requirements.txt

#Enviroment Variables that could be passed
ENV READ_LOG_STRATEGY="OPEN_SEARCH"
ENV DATA_FILE="data/data-file-env-dev.csv"
ENV DELIVERY_ROOT_URL="http://deliverydev.siprocalads.com"
ENV READ_LOG_OPEN_SEARCH_HOST="vpc-c6-dev-es-uw2-logs-dlfqhljpdvbm62vc4qfbsnckji.us-west-2.es.amazonaws.com"

VOLUME /results
CMD cd /automation
CMD /automation/run_tests.sh

CMD cp /automation/build -r /results

