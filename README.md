# **Noorish**

Welcome to the Nourish Application! This project aims to help users efficiently plan their weekly meals, track nutritional intake, and make informed decisions for a balanced diet. This README serves as the main documentation for the project, outlining its features, technology stack, and future enhancements.


## **Features**

### User Management

**Sign Up/Login:** Register or log in with OAuth providers (Google, Facebook).
**Profile Customization:** Add dietary preferences, allergies, and calorie goals.

### Recipe Management

Wide database containing nutritional information about food products and extra information such as average price and season.
Store recipes and consult aggregated nutritional details (calories, protein, fat, carbs, vitamins and much more). Add recipes manually or import them via our URLs recipe parser. 
Provide alternatives for unavailable, unwanted or allergy-triggering ingredients.
Filter recipes by ingredients, cuisine, or dietary restrictions. 

### Menu Planning

Organize meals using a drag-and-drop interface for main meals, snacks and beverages.
Get suggestions to fill nutritional gaps in the weekly menu. Recommend recipes to balance nutritional intake. Prioritise seasonal or cost-effective recipes.
Detailed breakdown of nutritional intake for the planned menu.
Generate a shopping list from selected recipes. Add, remove, or modify items directly in the list for optimised shopping. Get an estimated cost of the shopping for budget control.
                                         

## **Tech Stack**

Web Application Framework: NiceGUI
Database: PostgreSQL for structured data; Redis for caching.
API: RESTful APIs
Containerization: Docker
Hosting: Google Cloud


## **3rd Party Integrations**

Nutritional Data: Edamam, Spoonacular APIs
Authentication: OAuth for social logins


## **Getting Started**

Clone the Repository:
'''bash
git clone https://github.com/your-username/weekly-menu-app.git
'''

Install Dependencies:
'''bash
pip install -r requirements.txt
'''

Run the Application:
'''bash
uvicorn main:app --reload
'''

Access the App:
Open http://127.0.0.1:8000 in your browser.
 

## **License**

This project is licensed under the MIT License. See the LICENSE file for details.

We hope this application helps make meal planning and healthy eating effortless! If you have any questions or feedback, please open an issue or contact us through GitHub.
