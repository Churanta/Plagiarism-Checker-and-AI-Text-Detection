
# Plagiarism Checker and AI Text Detection

This is a Flask web application that serves as a Plagiarism Checker and AI Text Detection tool. It allows users to input a query and checks for plagiarism by comparing it with a pre-existing database. Additionally, it includes a feature to detect if the input text is AI-generated.

## How to Use

1. Install the necessary dependencies by running the following command:

   
   pip install flask
   

2. Clone this repository to your local machine.

3. Navigate to the project directory and run the following command to start the application:

   
   python app.py
   

4. Open a web browser and visit `http://localhost:5000` to access the application.

5. Enter your query in the input field and click the "Check Plagiarism and Detect AI Text" button.

6. The application will display the plagiarism percentage, identified plagiarized texts, and whether the input text is AI-generated or not.

## Requirements

- Python 3.x
- Flask
- Chart.js

## File Structure

- `app.py`: The main Flask application file containing the routes and logic for plagiarism detection and AI text detection.
- `templates/index.html`: The HTML template file that defines the web page structure and content.
- `database1.txt`: The pre-existing database file containing the texts to compare with for plagiarism detection.

## Customization

- To customize the application, you can modify the HTML template (`index.html`) to change the appearance or add additional features.
- You can also update the pre-existing database (`database1.txt`) with your own texts for plagiarism detection.

## Acknowledgements

This project utilizes the following libraries:

- Flask: A Python web framework for creating web applications.
- Chart.js: A JavaScript library for creating charts and visualizations.

## License

<!-- This project is licensed under the [MIT License](LICENSE). -->

