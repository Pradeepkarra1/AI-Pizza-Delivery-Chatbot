# 🍕 AI-Powered Pizza Delivery Chatbot

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![n8n](https://img.shields.io/badge/Built%20with-n8n-FF6D5A)](https://n8n.io/)
[![Google Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4)](https://ai.google.dev/)

An intelligent conversational AI chatbot for pizza delivery built with n8n automation platform and powered by Google Gemini. This project demonstrates advanced AI agent capabilities including tool use, conversation memory, and seamless order management.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Workflow Components](#workflow-components)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Menu Data](#menu-data)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Overview

This AI-powered chatbot streamlines the pizza ordering process by:
- Providing an interactive conversational interface
- Fetching real-time menu information
- Processing customer orders intelligently
- Tracking order status
- Maintaining conversation context across interactions

Built using n8n's AI Agent node with Google Gemini as the language model, this project showcases how no-code/low-code platforms can create sophisticated AI applications.

## ✨ Features

### 🤖 AI Capabilities
- **Natural Language Understanding**: Powered by Google Gemini 1.5 Flash model
- **Context Awareness**: Remembers previous messages in the conversation
- **Tool Integration**: Dynamically uses appropriate tools based on user requests
- **Intelligent Routing**: Automatically determines when to fetch menu, create orders, or check status

### 🛠️ Functional Features
- **Menu Retrieval**: Fetches complete pizza menu with categories, descriptions, and pricing
- **Order Creation**: Processes new pizza orders with customer details
- **Order Tracking**: Checks real-time order status using order IDs
- **Conversation Memory**: Maintains context throughout the chat session
- **Error Handling**: Gracefully manages API errors and invalid requests

## 🏗️ Architecture

### Workflow Structure

```
Chat Trigger (Entry Point)
       |
       v
Pizza Chatbot Agent (AI Orchestrator)
       |
       +--- Google Gemini Chat Model (LLM)
       +--- Conversation Memory (Context Storage)
       +--- Tools:
              +--- Get Menu Tool (HTTP Request)
              +--- Create Order Tool (HTTP Request)
              +--- Check Order Status Tool (HTTP Request)
```

### Components Breakdown

1. **Chat Trigger**: Initiates conversation when user sends a message
2. **Pizza Chatbot Agent**: Coordinates the AI response and tool usage
3. **Google Gemini Model**: Processes natural language and generates responses
4. **Conversation Memory**: Stores chat history for context
5. **Tools**: External API integrations for specific functions

## 🔧 Workflow Components

### 1. Chat Trigger Node
**Purpose**: Entry point for user messages
- **Type**: Trigger node
- **Function**: Captures incoming chat messages and initiates workflow
- **Output**: User message text and session information

### 2. Pizza Chatbot Agent Node
**Purpose**: Core AI orchestration
- **Type**: AI Agent
- **Model**: Google Gemini 1.5 Flash
- **System Prompt**: 
  ```
  You are a helpful pizza delivery assistant. You help customers:
  - Browse the menu
  - Place new orders
  - Check order status
  Always be friendly, clear, and efficient.
  ```
- **Features**:
  - Tool calling enabled
  - Conversation memory integration
  - Multi-turn conversations

### 3. Google Gemini Chat Model
**Purpose**: Language understanding and generation
- **Model**: gemini-1.5-flash
- **Temperature**: 0.7 (balanced creativity)
- **Max Tokens**: Configured for complete responses
- **Authentication**: Google Gemini API credentials

### 4. Conversation Memory
**Purpose**: Context retention
- **Type**: Window Buffer Memory
- **Function**: Stores recent conversation history
- **Benefit**: Enables contextual responses and follow-up questions

### 5. Get Menu Tool
**Purpose**: Retrieve pizza menu
- **Method**: HTTP GET
- **URL**: `https://gist.githubusercontent.com/Pradeepkarra1/770ee94f47281b8c952b744d3889ea00/raw/pizza_menu.json`
- **Description**: "Retrieves the current pizza menu with available pizzas, sizes, and prices. Use this when customers ask about menu options."
- **Returns**: Complete menu in JSON format

### 6. Create Order Tool
**Purpose**: Process new orders
- **Method**: HTTP POST
- **URL**: `https://httpbin.org/post`
- **Description**: "Creates a new pizza order. Use this when customers want to place an order."
- **Expected Parameters**:
  - Pizza selection
  - Size
  - Quantity
  - Customer details (name, address, phone)

### 7. Check Order Status Tool
**Purpose**: Track orders
- **Method**: HTTP GET
- **URL**: `https://httpbin.org/get`
- **Description**: "Checks the status of an existing order using the order ID."
- **Expected Parameter**: Order ID

## 🚀 Setup Instructions

### Prerequisites

- n8n instance (cloud or self-hosted)
- Google Gemini API key
- Basic understanding of n8n workflows

### Step-by-Step Setup

1. **Create n8n Account**
   ```
   Visit https://n8n.io and create an account
   ```

2. **Get Google Gemini API Key**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key for later use

3. **Import Workflow**
   - Download `pizza-chatbot-workflow.json` from this repository
   - In n8n, click "Import from File"
   - Select the downloaded JSON file

### Import & Run in n8n (Local)

If you'd like to run the workflow locally (recommended for development), you can run n8n via Docker or npm.

- Docker (quick start):

```bash
# Run n8n (no persistent DB) and expose the UI on http://localhost:5678
docker run -it --rm \
  -p 5678:5678 \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=user \
  -e N8N_BASIC_AUTH_PASSWORD=password \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

- npm (alternate):

```bash
npm install -g n8n
n8n start
```

- Import the workflow file: use the bundled `workflow.json` (or the longer-named workflow JSON in the repo) via **Import from File** in the n8n UI.

- Configure credentials:
  - Open the `Google Gemini Chat Model` node
  - Create a new Google Gemini/PaLM credential and paste your API key

- Activate & test the workflow:
  - Toggle the workflow to **Active**
  - Open the chat interface at the bottom of the workflow editor and send a message

### Quick Local Tool Tests (without n8n)

You can also test the tool endpoints used by the workflow directly from your terminal:

```bash
# Fetch the menu JSON
curl -sS https://gist.githubusercontent.com/Pradeepkarra1/770ee94f47281b8c952b744d3889ea00/raw/a6bdb41b0c7e1bda15c63ab8e7eb73dc9213b441/pizza_menu.json | jq '.' | head -n 20

# Simulate creating an order (POST)
curl -sS -H "Content-Type: application/json" \
  -d '{"pizza_type":"Margherita","size":"Large","quantity":2,"customer_name":"Test User","delivery_address":"123 Main St","phone_number":"555-0123"}' \
  https://httpbin.org/post | jq '.'

# Simulate checking order status (GET)
curl -sS "https://httpbin.org/get?order_id=12345" | jq '.'
```

Notes:
- The workflow file in this repo is named `workflow.json` and can be imported directly.
- Replace `httpbin.org` URLs in production with your real APIs that handle orders and status tracking.

### Local Simulator

A small CLI tool is provided to exercise the workflow tools locally:

- Install dependencies:

```bash
python3 -m pip install -r requirements.txt --user
```

- Run the simulator:

```bash
# Print menu
python scripts/simulate_agent.py menu

# Create an order (POST)
python scripts/simulate_agent.py create --pizza_type Margherita --size Large --quantity 2

# Check a status (GET)
python scripts/simulate_agent.py status --order_id 12345
```

The simulator attempts to use the workflow's configured endpoints (`httpbin.org`), and will fall back to `postman-echo.com` for transient server errors.

4. **Configure Google Gemini Credentials**
   - Open the "Google Gemini Chat Model" node
   - Click "Create New Credential"
   - Paste your API key
   - Save the credential

5. **Customize Menu Data** (Optional)
   - Create your own GitHub Gist with menu JSON
   - Update the "Get Menu Tool" URL

6. **Configure API Endpoints** (For Production)
   - Replace httpbin.org URLs with your actual API endpoints
   - Ensure endpoints accept the expected request formats

7. **Activate Workflow**
   - Click "Active" toggle in the top right
   - Test the chatbot in the chat interface

### Configuration Notes

- **Memory Settings**: Adjust memory window size in Conversation Memory node
- **Temperature**: Modify in Google Gemini node (0.0-1.0 range)
- **Tool Descriptions**: Update descriptions to improve AI tool selection
- **Error Handling**: Add error handling nodes for production use

## 💬 Usage

### Starting a Conversation

1. Open the workflow in n8n
2. Click "Open chat" button at the bottom
3. Start chatting with the AI assistant

### Example Interactions

**Viewing the Menu:**
```
User: Show me your menu
Bot: Here's our current menu:

Specialty Pizzas:
• Margherita - Fresh mozzarella, basil, olive oil, and pecorino cheese - $18.99
• Pepperoni Plain - Classic pepperoni with mozzarella - $17.99
...
```

**Placing an Order:**
```
User: I'd like to order 2 large Margherita pizzas
Bot: Great choice! I can help you place that order. 
Could you provide your delivery address and phone number?

User: 123 Main St, and my number is 555-0123
Bot: Perfect! I've created your order...
```

**Checking Order Status:**
```
User: What's the status of order #12345?
Bot: Let me check that for you...
[Order status information]
```

## 🍕 Menu Data

The menu is stored as JSON and includes:

### Categories
- **Specialty Pizzas**: Pre-designed pizza combinations
- **Build Your Own**: Customizable base pizza
- **Crust Options**: Thin, Hand-Tossed, Gluten-Free
- **Sauce Options**: Red, White, BBQ
- **Cheese Options**: Regular, Fresh Mozzarella, Vegan
- **Toppings**: Various meat and vegetable options

### Sample Menu Structure
```json
{
  "menu": [
    {
      "category": "Specialty Pizzas",
      "items": [
        {
          "name": "Margherita",
          "description": "Fresh mozzarella, basil, olive oil, and pecorino cheese",
          "price": 18.99
        }
      ]
    }
  ]
}
```

See `menu-data.json` for the complete menu structure.

## 🔌 API Endpoints

### Menu API
**Endpoint**: `GET /menu`
**Response**: JSON array of menu items

### Order Creation API
**Endpoint**: `POST /orders`
**Body**:
```json
{
  "items": [...],
  "customer": {
    "name": "string",
    "address": "string",
    "phone": "string"
  }
}
```

### Order Status API
**Endpoint**: `GET /orders/{orderId}`
**Response**: Order status and details

## 📸 Screenshots

### Workflow Overview
![Workflow Architecture](images/workflow-overview.png)

### Chat Interface
![Chat Interface](images/chat-interface.png)

### Tool Configuration
![Tool Setup](images/tool-configuration.png)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [n8n](https://n8n.io/) - The workflow automation platform
- Powered by [Google Gemini](https://ai.google.dev/) - Advanced AI capabilities
- Menu data hosted on [GitHub Gist](https://gist.github.com/)

## 📧 Contact

**Pradeep Karra** - Data Analyst | AI Enthusiast
- GitHub: [@Pradeepkarra1](https://github.com/Pradeepkarra1)
- LinkedIn: [Pradeep Karra](https://linkedin.com/in/pradeepkarra1)
- Email: Pradeepkarra1@gmail.com

---

⭐ If you found this project helpful, please consider giving it a star!

**Project Link**: [https://github.com/Pradeepkarra1/AI-Pizza-Delivery-Chatbot](https://github.com/Pradeepkarra1/AI-Pizza-Delivery-Chatbot)
