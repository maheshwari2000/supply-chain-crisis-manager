Create a Bedrock Agent
Create and use a new service role
Select Nova pro Model
Use BedrockAgentPrompt.txt to provide Instructions to Agent
Add Action groups which act as supporting functions/tools for our agent to make better decisions
    - For which create a lambda function (lambda1.py)
    - Add Agent Group Functions (AgentGroupFunctions.json)
Add Bedrock Full Access and S3 Full Access permissions to Lambda IAM role
Also go to permission tab of Lambda Function and add resource-based policy 
    - Select AWS Service and select Other
    - Give custom Statement ID
    - Add bedrock.amazonaws.com as Principal
    - Add Bedrock Agent ARN as Source ARN
    - Choose Action as lambda:InvokeFunction
Go to AWS Bedrock, then open Settings and enable Model invocation logging (specify the CloudWatch log group you want to store logs in) 
Now we have everything setup from our Agent and its tools side, now we will create a streamlit application which will call that agent and we can chat with Agent using our Streamlit Frontend (app.py)

Setting up .env file
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_REGION=us-east-1
BEDROCK_AGENT_ID=                   # actual agent ID
BEDROCK_AGENT_ALIAS_ID=             # Actual Agent ALIAS ID
DEBUG=True

Run streamlit app using 'streamlit run app.py'

Demo Questions -
Query 1: 
“Analyze supplier risk for NVIDIA in Taiwan”
→ It combines supplier + location risk = high-risk scenario.

Query 2:
“Find alternative semiconductor suppliers for TSMC”
→ Pulls top alternatives from multiple regions.

Query 3:
“If an earthquake hits Taiwan, what’s the crisis impact?”
→ calculate_crisis_impact() gives multi-metric output.

Query 4:
“Generate procurement recommendations if Foxconn is affected by a strike.”


Deploying on EC2
- Create a instance
- Add Custom TCP with port 8501
- git clone the repo/create a app.py file and copy paste streamlit code
