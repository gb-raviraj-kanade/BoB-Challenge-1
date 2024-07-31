# BoB-Challenge-1 Reimagine Customer Service with Generative AI

**Idea:** BoB AI Assist - Your Personalized Banking Companion 

**Description:** BoB AI Assist is an intelligent virtual assistant that leverages Generative AI to provide customers with a personalized, conversational, and proactive banking experience across multiple channels (website, mobile app, WhatsApp, etc.).

**Proposed Solution:**

•	AI-Powered Conversational Interface: Customers interact with BoB AI Assist using natural language, asking questions, getting information, and completing transactions.

•	Contextual Understanding & Personalization: BoB AI Assist uses Generative AI to analyze past interactions, account history, and preferences to provide tailored responses and recommendations.

•	Proactive Assistance: The system identifies potential issues and proactively reaches out to customers with relevant information or solutions. For example, it could alert a customer about a potential overdraft or suggest a better savings plan based on their spending habits.

•	Seamless Integration: BoB AI Assist integrates with existing banking systems and customer service platforms for a unified experience.

**Prototype Implementation:**

We have developed APIs for four sub-applications within two main applications. These APIs are designed for integration with existing systems. For demonstration purposes, we have implemented user-friendly interfaces using Streamlit, Chainlit, and Javascript for visualization. We have utilized Azure speech services and Azure OpenAI services in the development of this solution. 

To showcase functionality, we utilized LLMs to generate a dummy transaction database for ten customers. The database is editable for user testing, and it can be found at https://bobaiassist.centralindia.cloudapp.azure.com/database 

**1) AI-Powered Conversational Interface:**

This category encompasses two applications: one for chat-based interaction and the other for handling customer calls. These applications demonstrate how customers can seamlessly connect with Bank of Baroda (BoB) without human intervention. 

By engaging with the BoB AI Assist through voice or text, customers can retrieve necessary information. The AI Assist addresses customer queries by accessing a comprehensive FAQ database sourced from https://www.bankofbaroda.in/faqs and providing individual’s transaction details. A RAG based system is implemented in order to generate the response. 

Leveraging Azure STT (Speech-to-Text) and TTS (Text-to-Speech) services, the voice call functionality supports all languages compatible with Azure AI services. For a complete list of supported languages, please refer to https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=stt. 

**A) Multilingual Chat:**

URL: https://bobaiassist.centralindia.cloudapp.azure.com/chat 

This application, designed for integration with existing BoB chat interfaces on web and mobile platforms, offers both text-based and voice input options. Voice inputs are seamlessly converted to text for user convenience. 

**B) Multilingual Calls:**

URL: https://bobaiassist.centralindia.cloudapp.azure.com/call 

This application has the potential to significantly reduce the volume of calls directed to customer care staff by enabling the BoB AI Assist to independently handle a substantial portion of customer inquiries. 

**2) Personalization and Proactive Assistance:**

URL: https://bobaiassist.centralindia.cloudapp.azure.com/p&passistant 

This category features two applications. The first provides customers with insights into their spending patterns and delivers tailored recommendations. The second application, designed for BoB's backend team, performs daily scans to predict potential cash flow issues, generate low-balance alerts, and flag suspicious transactions. 

**A) Contextual Understanding & Personalization (Custom Emails):**

To demonstrate this functionality, users can generate customer-specific content by clicking the "Generate" button and then selecting a customer. This action generates a personalized email tailored for all the customers and displays insights and recommendations for the selected customer. 

**B) Proactive Assistance (Custom Emails and Notifications):**

In this demonstration, clicking the "Scan" button initiates a database scan. The application then displays a list of customers flagged for potential cash flow issues or suspicious transactions. Selecting a specific customer from the list generates an email alongside a notification. The notification can be interpreted as a communication through text message, WhatsApp message, or BoB mobile app notification. 


 
**Folder Structure and Code Description:**

 

data > BOB_FAQs > Contains the Bank of Baroda FAQs in Markdown format which were used for ingestion in RAG. 

data > transactions.csv > Contains the dummy transactions for 10 customers which can be updated through the "database" dashboard. 

data > transactions_og.csv > Contains the original copy of dummy transactions for 10 customers. 

index > Contains the Vector Embeddings index of FAQs for RAG. 

pages > Proactive_Assistance.py > Represents the second page of Personalization and Proactive Assistance Application. 

templates > index.html > Represents the landing page of Call Application. 

Transaction_DB.py > Contains the "database" dashboard code for displaying/updating the dummy transactions for 10 customers. 

chat_app.py > Contains the Multilingual Chat Application code. 

call_app.py > Contains the Multilingual Call Application code. 

main.py > Contains the backend server code which serves API requests for "p&passistant". 

Personalization.py > Contains the Personalization and Proactive Assistance Application code. 

app > Contains the Source Code for BoB AI Assist. 


 

**Installation & Execution:**

 

1. Clone the repository 

```bash 

git clone https://github.com/gb-raviraj-kanade/BoB-Challenge-1.git 

``` 

 

2. Install the requirements 

```bash 

pip install -r requirements.txt 

``` 

 

3. Rename the .env.example to .env and add all the Keys 

 

4. Start the "database" dashboard 

```bash 

streamlit run Transaction_DB.py --server.headless true --server.address "127.0.0.1" --server.port 8501 --server.baseUrlPath "/database" --client.showSidebarNavigation False 

``` 

 

5. Start the Multilingual Chat Application 

```bash 

chainlit run cl_app.py --host 127.0.0.1 --port "8000" --headless --root-path "/chat" 

``` 

 

6. Start the Multilingual Call Application 

```bash 

python3 call_app.py 

``` 

 

7. Start the backend server which serves API requests for "p&passistant" 

```bash 

python3 main.py 

``` 

 

8. Start the Personalization and Proactive Assistance Application (p&passistant) 

```bash 

streamlit run Personalization.py --server.headless true --server.address "127.0.0.1" --server.port 8502 --server.baseUrlPath "/p&passistant" 

``` 
