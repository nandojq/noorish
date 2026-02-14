# Noorish - Requirements Specification

## Document Overview
**Version:** 1.0 (Draft)  
**Last Updated:** January 10, 2026  
**Purpose:** Define functional and non-functional requirements for the Noorish nutrition analysis framework

---

## 1. Project Vision & Objectives

### 1.1 Project Vision
Noorish is a developer-focused nutrition analysis framework that empowers users to make informed dietary choices. The system collects and standardises nutritional information to enable the user to investigate and improve their dietary choices with the aim of easing the menu planning and grocery shopping optimising the nutritional health.

### 1.2 Core Objectives
1. **Data Standardization:** Create a unified nutritional database from multiple sources (APIs and manual entries)
2. **Recipe Intelligence:** Enable easy recipe creation, import, and nutritional analysis
3. **Menu Planning:** Support meal planning with nutritional insights at daily and weekly levels
4. **Informed Choice:** Highlight nutritional patterns, gaps, and trade-offs to support decision-making
5. **Menu Plan Exporting:** Export the investigated menu in an standarised PDF report with information about the menu plan, its nutritinoal analysis and the necessary shopping list
6. **Extensibility:** Design for future expansion (environmental impact, community sharing)

### 1.3 Success Criteria
- [ ] Successfully integrate and standardize data from at least 2 nutrition APIs
- [ ] Create and analyze 10+ personal recipes with full nutritional breakdowns
- [ ] Generate weekly menu plans with automated nutritional analysis
- [ ] Identify nutritional patterns and potential deficiencies in meal plans
- [ ] Maintain data integrity across all operations (no data loss or corruption)
- [ ] Export a prepare menu plan with all the expected outputs

---

## 2. User Personas & Scenarios

### 2.1 Primary User: Health-Conscious Developer (You)
**Background:** Software developer interested in optimizing personal nutrition through data and analysis  
**Technical Skills:** High - comfortable with JSON, APIs, command-line tools  
**Nutritional Knowledge:** Moderate - understands macros/micros but wants deeper insights  
**Goals:**
- Track and analyze personal nutrition intake
- Experiment with different dietary patterns
- Build a system that could eventually be shared with friends/community

### 2.2 Future User: Community Member
**Background:** Friend or family member interested in using the tool  
**Technical Skills:** Low to moderate - needs intuitive interface  
**Nutritional Knowledge:** Variable  
**Goals:**
- Easy recipe and menu creation
- Clear nutritional insights without complexity
- Meal planning support
- Access to these capabilities through an intuitive web application

---

## 3. Functional Requirements

### 3.1 Product Management

#### FR-1.1: Product Database Insert
**Priority:** HIGH (MVP)  
**Description:** The application must be able to add a new product to the products database from ingredient name entered by the user querying the nutritional product information from external nutrition APIs.

**Acceptance Criteria:**
- [ ] Import specific product with full standardised nutrition data from at least 2 different nutrition APIs for data robustness
- [ ] Handle API errors gracefully with fallback options
- [ ] Avoid duplicate ingredients (detect and merge)

**User Workflow:**
1. User enters ingredient name (e.g., "chicken breast")
2. System queries enabled APIs for nutritional data
3. System contrasts received data and checks for data value alignment
4. System processes the data to standardised and aligned it with the product database schema
5. System imports full nutritional data to local database
6. System checks database data consistency before saving
6. System saves new database state and confirms successful import

---

#### FR-1.3: View and Browse Ingredients
**Priority:** MEDIUM  
**Description:** Users can view their ingredient database and search/filter locally

**Acceptance Criteria:**
- [ ] List all ingredients with basic nutrition preview
- [ ] Search ingredients by name/alias
- [ ] Filter by category
- [ ] View detailed nutrition profile for any ingredient
- [ ] See ingredient metadata (source, last updated, data quality)
- [ ] Sort by various fields (name, calories, protein, etc.)

---

### 3.2 Recipe Management

#### FR-2.1: Create Recipe from Ingredients
**Priority:** HIGH (MVP)  
**Description:** Users can create recipes by selecting ingredients, adding pics and cooking instructions

**Acceptance Criteria:**
- [ ] Create recipe with name, description and portions
- [ ] Add ingredients from database with amounts and units
- [ ] Support common units (standardised)
- [ ] Add cooking instructions as ordered steps
- [ ] Automatically calculate recipe nutrition based on ingredients
- [ ] Calculate per-serving nutrition
- [ ] Add optional metadata (cook time, difficulty, tags)
- [ ] Save recipe to database

**User Workflow:**
1. User initiates "create recipe" action
2. System prompts for recipe name and servings
3. User searches and adds ingredients one by one
4. For each ingredient, user specifies amount and unit
5. User adds cooking instructions as steps
6. System calculates total and per-serving nutrition
7. User adds optional tags and metadata
8. System saves recipe
9. System displays nutrition summary

---

#### FR-2.2: Import Recipe from Web
**Priority:** LOW  
**Description:** Users can paste a recipe URL and have it parsed into the standard format

**Acceptance Criteria:**
- [ ] Accept recipe URL from popular sites
- [ ] Extract recipe name, ingredients, and instructions
- [ ] Attempt to match ingredients to database
- [ ] Highlight unmatched ingredients for user review
- [ ] Allow user to map ingredients or create new ones
- [ ] Calculate nutrition after ingredient mapping
- [ ] Save imported recipe

**User Workflow:**
1. User pastes recipe URL
2. System scrapes and parses recipe
3. System displays parsed data for review
4. System attempts ingredient matching
5. User reviews and maps unmatched ingredients
6. System calculates nutrition
7. User confirms and saves

---

#### FR-2.3: Edit and Duplicate Recipes
**Priority:** MEDIUM  
**Description:** Users can modify existing recipes or create variations

**Acceptance Criteria:**
- [ ] Edit all recipe fields
- [ ] Recalculate nutrition on changes
- [ ] Duplicate recipe to create variations
- [ ] Delete recipe (with safety check if used in menus)
- [ ] View recipe history/modifications (future)

---

#### FR-2.4: Recipe Analysis and Insights
**Priority:** MEDIUM  
**Description:** System provides nutritional insights for individual recipes

**Acceptance Criteria:**
- [ ] Display complete macro and micronutrient breakdown
- [ ] Highlight nutrient-dense ingredients
- [ ] Flag potential nutritional concerns (high sodium, low fiber, etc.)
- [ ] Show percentage of daily values (based on standard 2000 cal diet)
- [ ] Suggest ingredient substitutions for better nutrition (future)

---

### 3.3 Menu Planning

#### FR-3.1: Create Weekly Menu
**Priority:** HIGH (MVP)  
**Description:** Users can create menu plans by assigning recipes to specific days

**Acceptance Criteria:**
- [ ] Create menu with name
- [ ] Add recipes to specific dates and categories (breakfast/lunch/dinner/snack)
- [ ] Automatically calculate daily nutrition totals
- [ ] Automatically calculate full menu nutrition totals
- [ ] Save menu plan and export all insights to PDF

**User Workflow:**
1. User creates new menu 
2. User drag and drops recipe to day/category
5. System calculates meal nutrition
6. User repeats for all days and gategories
7. System calculates daily and weekly totals
8. User saves menu plan

---

#### FR-3.2: Menu Analysis and Insights
**Priority:** HIGH (MVP)  
**Description:** System analyzes menu plans and provides nutritional insights

**Acceptance Criteria:**
- [ ] Calculate average daily calories and macros
- [ ] Calculate average daily micronutrients
- [ ] Compare against DRI/RDA standards
- [ ] Identify potential deficiencies (nutrients consistently below recommendations)
- [ ] Highlight nutrients consistently exceeding recommendations
- [ ] Analyze variety (ingredient diversity, food group distribution)
- [ ] Show daily nutrition trends (graphical representation)
- [ ] Generate summary report with key insights

---

#### FR-3.3: Set Nutrition Goals
**Priority:** MEDIUM  
**Description:** Users can set personal nutrition targets and track against them

**Acceptance Criteria:**
- [ ] Set daily calorie target
- [ ] Set macro targets (protein, carbs, fat in grams)
- [ ] Set micronutrient targets (optional)
- [ ] Compare menu against goals
- [ ] Highlight areas meeting/missing goals

---

#### FR-3.4: Menu Templates and Reuse
**Priority:** LOW  
**Description:** Users can save successful menus as templates and reuse them

**Acceptance Criteria:**
- [ ] Save menu as template
- [ ] Apply template to new menu
- [ ] Browse saved templates
- [ ] Modify template before applying

---

## 4. Non-Functional Requirements

### 4.1 Performance
- **NFR-1.1:** API requests complete within 3 seconds
- **NFR-1.2:** Local data queries complete within 500ms
- **NFR-1.3:** Menu nutrition calculations complete within 2 seconds
- **NFR-1.4:** Support ingredient database of 1000+ items without performance degradation

### 4.2 Reliability
- **NFR-2.1:** System maintains data integrity across all operations (no data loss)
- **NFR-2.2:** Automatic backup before any data modification
- **NFR-2.3:** Graceful degradation when APIs are unavailable
- **NFR-2.4:** Data validation prevents invalid entries

### 4.3 Usability
- **NFR-3.1:** Clear error messages for all failure scenarios
- **NFR-3.2:** Ingredient search returns results in under 5 interactions
- **NFR-3.3:** Recipe creation takes under 10 minutes for 5-ingredient recipe
- **NFR-3.4:** Menu creation for 7-day plan takes under 30 minutes

### 4.4 Maintainability
- **NFR-4.1:** Code follows consistent style guidelines
- **NFR-4.2:** All data structures validated against JSON schemas
- **NFR-4.3:** Clear separation between data, business logic, and presentation
- **NFR-4.4:** Comprehensive documentation for all modules

### 4.5 Portability
- **NFR-5.1:** All data stored in standard JSON format
- **NFR-5.2:** Easy data export/import for backup and migration
- **NFR-5.3:** Platform-agnostic design (works on Windows, Mac, Linux)
- **NFR-5.4:** No vendor lock-in for data storage

### 4.6 Security and Privacy
- **NFR-6.1:** No personal data sent to external APIs without consent
- **NFR-6.2:** API keys stored securely (not in version control)
- **NFR-6.3:** Local data encrypted at rest (future)
- **NFR-6.4:** No tracking or analytics without explicit consent

---

## 5. Technical Constraints

### 5.1 Development Environment
- **Primary Language:** Python 
- **Data Storage:** JSON files (start), MongoDB (future scale)
- **APIs:** USDA FoodData Central, Edamam, Open Food Facts
- **Version Control:** Git

### 5.2 Dependencies
- Minimal external dependencies preferred
- Standard libraries prioritized
- Well-maintained packages only
- Clear license compatibility

### 5.3 Platform
- Initial: Command-line interface (CLI)
- Future: Web application (lightweight, local-first)
- Future: Mobile app (consideration only)

---
