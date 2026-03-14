# 🎒 Project Report: PocketPath
**An AI-Powered 'Jugaad' Travel Itinerary Generator**

**Developer:** Aryan Sunil Bendre  
**Institution:** B.K Birla College (B.Sc Data Science)  
**Live Demo:** [PocketPath on Hugging Face](https://huggingface.co/spaces/AryanBendre/PocketPath)

---

## 1. Abstract
PocketPath is a dynamic, AI-driven web application designed to generate highly optimized, budget-conscious travel itineraries. Targeted primarily at students and young travelers, the system utilizes Large Language Models (LLMs) to construct detailed day-wise plans, calculate expense splits, and suggest cost-saving travel hacks ("Jugaad"). The application features a responsive UI that dynamically adapts its color palette based on real-time destination imagery.

## 2. Problem Statement
Planning a budget-friendly trip is a time-consuming process. Current travel platforms offer generic, expensive packages that ignore student-specific constraints. There is a critical need for an intelligent tool that can:
* Analyze individual parameters (origin, destination, exact budget, group size).
* Calculate "Paisa Vasool" (value-for-money) metrics by dividing expenses per person.
* Generate a realistic itinerary that integrates travel hacks (e.g., overnight trains) to minimize accommodation costs and college/work leaves.

## 3. Proposed Solution
PocketPath acts as a personalized travel advisor. By replacing manual research with an automated AI pipeline, the system ensures users receive a comprehensive travel strategy. 

### Core Features:
* **Smart Itinerary Engine:** Generates a Morning/Afternoon/Evening schedule tailored to the user's specific budget and travel style.
* **AI Auto-Pilot:** Automatically overrides standard travel tiers if the user inputs a strict custom budget, forcing the AI to build a plan around that exact financial limit.
* **Chameleon UI:** Fetches real-time, high-resolution background images of the destination via the Unsplash API and calculates image luminance to dynamically adjust the application's text and button colors.
* **PDF Exporter:** Allows users to download their AI-generated travel roadmap as a professionally formatted PDF document.

## 4. Technology Stack
* **Frontend & UI:** Python, Streamlit
* **AI Engine:** Google Generative AI (Gemini 2.5 Flash)
* **Dynamic Media:** Unsplash Developer API
* **Document Generation:** Markdown-PDF
* **Version Control:** Git, GitHub
* **CI/CD & Deployment:** GitHub Actions, Hugging Face Spaces

## 5. System Architecture & Methodology
The application logic operates in three distinct phases:

1. **Data Collection:** A custom Streamlit interface captures structured user inputs (route, dates, travel mode, budget). 
2. **Dynamic Media & UI Layer:** The system queries the Unsplash API with the destination name. It mathematically evaluates the returned image's brightness to toggle UI text colors, ensuring accessibility and readability against any background.
3. **Reasoning & Synthesis:** The Gemini 2.5 Flash model performs high-speed synthesis of the user's constraints. It returns a prioritized list of travel hacks, a daily timeline, and a markdown-formatted budget table.

## 6. Deployment & CI/CD Pipeline
The project is deployed using a modern Continuous Integration and Continuous Deployment (CI/CD) pipeline to ensure high availability and seamless updates:
* **Source Management:** Source code (`app.py`, `requirements.txt`) is maintained in this GitHub repository. Local `.env` variables are strictly git-ignored.
* **Automation:** A YAML workflow file (`sync.yml`) detects pushes to the `main` branch.
* **Cloud Hosting:** GitHub Actions authenticates via a secure token and automatically pushes the codebase to a Hugging Face Space running a Streamlit SDK Docker container.

## 7. Future Scope        
* **Live Booking Integration:** Integrating APIs like IRCTC or Skyscanner to provide live ticket prices and direct booking links within the generated itinerary.
* **Group Expense Tracker:** Adding a built-in split-calculator module where users can log actual expenses during the trip.
* **Interactive Maps:** Integrating the Google Maps API to generate a visual route of the daily sightseeing spots suggested by the AI.

## 8. Conclusion
PocketPath successfully demonstrates the integration of Generative AI with dynamic web interfaces to solve real-world travel planning challenges. By combining the reasoning capabilities of Gemini 2.5 Flash with an automated CI/CD deployment pipeline, the project provides a scalable, highly interactive tool that empowers users to travel smarter and maximize their budgets.
