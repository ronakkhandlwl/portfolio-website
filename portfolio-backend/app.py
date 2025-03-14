from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../build', static_url_path='/')
CORS(app)  # Enable CORS for all routes

# Configuration
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS', 'your.email@example.com')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')  # Set this as an environment variable for security


@app.route('/')
def index():
    """Serve the React app's index.html when in production"""
    return app.send_static_file('index.html')


@app.route('/api/contact', methods=['POST'])
def contact():
    """Handle contact form submissions"""
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
        
        # Validate data
        if not all([name, email, subject, message]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        # Send email
        send_email(name, email, subject, message)
        
        return jsonify({'success': True, 'message': 'Message sent successfully!'})
    
    except Exception as e:
        logger.error(f"Error in contact form submission: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to send message. Please try again later.'}), 500


def send_email(name, email, subject, message):
    """Send an email with the contact form information"""
    if not EMAIL_PASSWORD:
        logger.warning("Email password not set. Email sending is disabled.")
        return
    
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS  # Sending to yourself
        msg['Subject'] = f"Portfolio Contact: {subject}"
        
        # Create email body
        body = f"""
        New contact form submission from your portfolio website:
        
        Name: {name}
        Email: {email}
        Subject: {subject}
        
        Message:
        {message}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to SMTP server (this example uses Gmail)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Email sent successfully for contact from {email}")
    
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        raise


@app.route('/api/projects', methods=['GET'])
def get_projects():
    """API endpoint to fetch projects data"""
    # In a real app, this would come from a database
    projects = [
        {
            "id": 1,
            "title": "AI Chatbot Integration",
            "description": "Trained auto-reply AI and integrated APIs for a Singapore-based client. The chatbot was designed to handle customer queries and provide relevant information.",
            "technologies": ["Python", "AI", "API Integration"],
            "category": "ai",
            "image": "chatbot-project.jpg",
            "githubUrl": "#",
            "liveUrl": "#"
        },
        {
            "id": 2,
            "title": "Data Copying Software",
            "description": "Developed a data copying software with error detection using checksum checks. Implemented real-time monitoring with Flask and WebSockets.",
            "technologies": ["Flask", "WebSockets", "Bootstrap", "JavaScript"],
            "category": "web",
            "image": "data-copy-project.jpg",
            "githubUrl": "#",
            "liveUrl": "#"
        },
        {
            "id": 3,
            "title": "Quotation Management System",
            "description": "Created a complex admin panel with various sections and checks. Developed both admin and customer-facing UIs with a focus on user experience.",
            "technologies": ["Django", "React", "Celery", "Redis", "MongoDB", "SQL"],
            "category": "web",
            "image": "quotation-project.jpg",
            "githubUrl": "#",
            "liveUrl": "#"
        },
        {
            "id": 4,
            "title": "CRM with WhatsApp Integration",
            "description": "Built a CRM system that integrates with WhatsApp API. Allows viewing and responding to customer chats directly from the CRM.",
            "technologies": ["WhatsApp API", "React", "Django", "MongoDB"],
            "category": "web",
            "image": "crm-project.jpg",
            "githubUrl": "#",
            "liveUrl": "#"
        }
    ]
    
    return jsonify(projects)


# Error handling routes
@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors by serving the React app"""
    return app.send_static_file('index.html')


if __name__ == '__main__':
    # Get port from environment variable or use 5000 as default
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
