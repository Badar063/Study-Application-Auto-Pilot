"""
CONFIGURATION TEMPLATE
Copy this file to 'my_config.json' and customize it.
DO NOT COMMIT YOUR PERSONAL CONFIG TO GITHUB!
"""

SAMPLE_CONFIG = {
    "user_profile": {
        "research_interests": [
            "Machine Learning",
            "Artificial Intelligence", 
            "Data Science",
            "Computer Vision",
            "Deep Learning",
            "Natural Language Processing"
        ],
        "technical_skills": {
            "programming": ["Python", "SQL", "R", "Java", "C++"],
            "big_data": ["Spark", "Hadoop", "HDFS", "Kafka"],
            "ml_frameworks": ["TensorFlow", "PyTorch", "scikit-learn", "Keras"],
            "tools": ["Docker", "Git", "Linux", "AWS", "Azure"]
        },
        "education_level": "Masters",  # or "Bachelors", "PhD"
        "experience_years": "3+"
    },
    "scanning": {
        "max_entries_per_feed": 10,
        "request_delay": 2,  # seconds between requests
        "min_relevance_score": 0.3
    },
    "privacy": {
        "hash_identifiers": True,
        "log_sensitive_data": False,
        "clean_temp_files": True
    }
}

# Instructions for users:
print("""
INSTRUCTIONS:
1. Copy this template to 'my_config.json'
2. Customize with your research interests and skills
3. Run: python phd_application_bot.py
4. Your personal data stays local and private
""")
