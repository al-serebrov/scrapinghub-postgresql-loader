# Load items from Scrapy Cloud to PostgreSQL instance

## Installation
Install dependencies:
```bash
virtualenv venv
source venv/bin/activate
pip install .
pip install -r requirements.txt
```

Also you need to install PostgreSQL, or install docker and docker-compose to use the `docker-compose.yml` config from this project.

## Usage

### Fire up PostgreSQL
Launch it if you have local installation and make sure that it's running or use a configuration from this project and run PosgreSQL command:
```
docker-compose up -d
```

### Set environmental variables
In order to use this script you need you [Scrapy Cloud API key](https://app.scrapinghub.com/account/apikey), add it to environmenatal variable `SH_APIKEY`:
```bash
export SH_APIKEY="your_key"
```
Also, you need to setup your PostgreSQL user and password:
```bash
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
```

All of these variables could be added to config.env file (see `config.sample` file) and populated using a single command:
```bash
source config.env
```

