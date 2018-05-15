# Case Harvester
Case Harvester is a project designed to mine the [Maryland Judiciary Case Search](http://casesearch.courts.state.md.us/casesearch/inquiry-index.jsp) (MJCS) and build a near-complete database of Maryland court cases that can be queried and analyzed without the limitations of the MJCS interface. It is designed to leverage [Amazon Web Services (AWS)](https://aws.amazon.com/) for scalability and performance.

If you are a researcher or journalist and would like access to our database, please reach out to us at [caseharvester@disman.tl](mailto:caseharvester@disman.tl).

# Installation
Case Harvester can be run or deployed from any workstation running Python 3, [GNU Make](https://www.gnu.org/software/make/), and [jq](https://stedolan.github.io/jq/). The required Python 3 modules are in `requirements.txt` and can be installed with `pip3 install -r requirements.txt`.

Next, configure AWS CLI with `aws configure` so that it can deploy Case Harvester. Here you'll use an Access Key ID and Secret Access Key either for your root AWS account, or an IAM user or role that has sufficient permissions.

## Deploy to AWS
Case Harvester uses [Cloudformation](https://aws.amazon.com/cloudformation/) stacks to deploy, configure, and connect all of the needed AWS resources. There are separate stacks for static resources (VPC, S3 bucket, RDS instance), spider, scraper, and parser. To deploy all of these stacks to a development environment, run:

```
make deploy
```

If you would like to deploy a specific stack, you can run any of the following (though keep in mind that spider, scraper, and parser rely on resources in the static stack):

```
make deploy_static
make deploy_spider
make deploy_scraper
make deploy_parser
```

Once everything is deployed, you can intialize the database and configure Case Harvester to use the newly deployed resources by running:

```
make init
```

Note that the above commands deploy and initialize a development environment. To deploy to a production environment:

```
make deploy_production
make init_production
```

# Architecture
Case Harvester is split into three main components: spider, scraper, and parser. Each component is a part of a pipeline that finds, downloads, and parses case data from the MJCS. The following diagram shows at a high level how each of these components interact:

![High level diagram](./img/main.png)

## Spider
The spider component is responsible for discovering case numbers. It does this by submitting search queries to the MJCS and iterating through the results. Because the MJCS only returns a maximum of 500 results, the search algorithm splits queries that return 500 results into a set of more narrowed queries which are then submitted. Each of these queries is then split again if more than 500 results are returned, and so forth, until the MJCS is exhaustively searched for case numbers. Each discovered case number is submitted to a PostgreSQL database, and then added to a queue for scraping:

![Spider diagram](./img/spider.png)

The spider can be run from any workstation, though for convenience it is usually run on an EC2 instance since the search process can take a long time.

## Scraper
The scraper component downloads and stores the case details for every case number discovered by the spider. The full HTML for each case ([for example](http://casesearch.courts.state.md.us/casesearch/inquiryDetail.jis?caseId=116090001&loc=69&detailLoc=DSK8)) is added to an S3 bucket. Version information is kept for each case, including a timestamp of when each version was downloaded, so changes to a case can be recorded and referenced.

![Scraper diagram](./img/scraper.png)

The scraper is a [Lambda function](https://aws.amazon.com/lambda/) that runs once an hour, as well as when the scraper queue has items in it. When the scraper is initially invoked by one of these triggers, it spawns a limited number of worker functions which can each scrape up to 10 cases from the queue. Each of the worker functions spawns another worker function upon completion, until the scraper queue is empty. The scraper is configured to spawn usually 1-2 concurrent worker functions, in order to limit the load on the MJCS. 

## Parser
The parser component is another Lambda function that parses the case details from the HTML for each case, and stores those in the PostgreSQL database ([see here](https://disman.tl/mjcs/docs/) for database schema information). Each new item added to the scraper S3 bucket spawns a parser function, which allows for significant scaling.

![Parser diagram](./img/parser.png)
