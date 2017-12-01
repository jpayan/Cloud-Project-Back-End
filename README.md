# No Bull project
This project is developed with the chalice microframework on python 2.7 along with BOTO3.
The frontend that goes along with this project can be found here: https://github.com/Ma4nNi/TestAssistWebsite  
  
# Architecture  
The whole project is built to be serverless. It's meant to be deployed to Amazon Web Services. 
The services used in this project are:  
- **AWS Lambda**: service that executes functions without caring of where it will run, it is used to make this a serverless application. With the use of lambdas we create the application's back-end, where we interact with other services and follow a microservices architecture
- **API Gateway**:  a service that provides a structure for developers to create, maintain, monitor, edit, secure and publish APIs. Through this service, front-end and back-end can be connected together, using it to call lambdas.
- **DynamoDB**:  a NoSQL database service that is read/write intensive. As this application is focused in creating groups and tests, it is important to be able to read and write from tables as fast as possible, to access data about teachers, students, tests and answers.
- **Amazon SES**:  this service sends emails to help communicate with clients of an application. Integrated with our application, SES will help send notifications through email to students when their test is available and their code to access it.
- **Chalice Microframework**: serverless microframework to connect lambdas with an API with the use of Python.

# Natural Language Processing
This application is used to create open questions and grade them, to reduce teachers' time on applying and grading test for their students, but, how do we do this?
Natural Language Processing is a field of study in artificial intelligence that focuses in analyzing how a human would speak and how a machine could interpret it. To work with this, we use a python library called Natural Language Toolkit (NLTK).
NLTK provides many interfaces to help you work with NLP, such as classification, tokenization, stemming, tagging, parsing, and semantic reasoning.
You can view more about NLTK following this link: [NLTK](http://www.nltk.org/)
