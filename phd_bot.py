#!/usr/bin/env python3
"""
PhD Application AutoPilot - Secure Version
A privacy-focused, secure automation system for PhD applications
"""

import feedparser
import requests
import json
import pandas as pd
import time
import random
from datetime import datetime
from bs4 import BeautifulSoup
import os
import hashlib

class SecurePhDBot:
    def __init__(self, config_path=None):
        self.opportunities = []
        self.config = self.load_config(config_path)
        self.setup_secure_environment()
    
    def setup_secure_environment(self):
        """Set up secure working environment"""
        # Create secure directories
        os.makedirs('data', exist_ok=True)
        os.makedirs('output', exist_ok=True)
        
        # Security headers for web requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Academic Research Bot (https://github.com/username/PhD-Application-AutoPilot)',
            'Accept': 'application/rss+xml, application/atom+xml, application/xml, text/xml'
        })
    
    def load_config(self, config_path):
        """Load configuration securely"""
        default_config = {
            "user_profile": {
                "research_interests": [
                    "Machine Learning", "Artificial Intelligence", 
                    "Data Science", "Computer Vision", "Deep Learning"
                ],
                "technical_skills": {
                    "programming": ["Python", "SQL", "R", "C++"],
                    "big_data": ["Spark", "Hadoop", "HDFS"],
                    "ml_frameworks": ["TensorFlow", "PyTorch", "scikit-learn"]
                },
                "education_level": "Masters",
                "experience_years": "5+"
            },
            "scanning": {
                "max_entries_per_feed": 10,
                "request_delay": 1,
                "min_relevance_score": 0.4
            },
            "privacy": {
                "hash_identifiers": True,
                "log_sensitive_data": False,
                "clean_temp_files": True
            }
        }
        
        # Load user config if provided
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    # Deep merge with default config
                    self.deep_merge(default_config, user_config)
            except Exception as e:
                print(f"⚠️  Config load error: {e}. Using defaults.")
        
        return default_config
    
    def deep_merge(self, base, update):
        """Safely merge configurations"""
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self.deep_merge(base[key], value)
            else:
                base[key] = value
    
    def scan_opportunities(self):
        """Scan for PhD opportunities securely"""
        print("🔍 Scanning for PhD opportunities...")
        
        # Use only public, academic RSS feeds
        rss_feeds = [
            # Academic job boards
            "https://www.findaphd.com/rss/latestphds.aspx",
            "https://academicpositions.com/find-jobs/rss",
            "https://www.nature.com/nature/articles?type=career-column",
            
            # University feeds (public information)
            "https://career.cornell.edu/feed/",
            "https://career.stanford.edu/feed/",
        ]
        
        for feed_url in rss_feeds:
            try:
                print(f"  Checking: {self.hash_url(feed_url)}")
                
                # Add delay to be respectful to servers
                time.sleep(self.config['scanning']['request_delay'])
                
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:self.config['scanning']['max_entries_per_feed']]:
                    opportunity = self.process_opportunity(entry, feed_url)
                    if opportunity and opportunity['relevance'] >= self.config['scanning']['min_relevance_score']:
                        self.opportunities.append(opportunity)
                        
            except Exception as e:
                if self.config['privacy']['log_sensitive_data']:
                    print(f"    ❌ Error with feed: {e}")
                else:
                    print(f"    ❌ Error with feed: {self.hash_url(feed_url)}")
    
    def process_opportunity(self, entry, source):
        """Process and score an opportunity"""
        # Extract basic info
        title = entry.get('title', 'Unknown Title')
        link = entry.get('link', '')
        summary = entry.get('summary', entry.get('description', ''))
        
        # Calculate relevance
        relevance = self.calculate_relevance(title + " " + summary)
        
        # Apply privacy measures
        if self.config['privacy']['hash_identifiers']:
            opportunity_id = self.hash_data(title + link)
        else:
            opportunity_id = hashlib.md5((title + link).encode()).hexdigest()[:8]
        
        return {
            'id': opportunity_id,
            'title': title,
            'link': link,
            'summary': summary[:200] + '...' if len(summary) > 200 else summary,
            'published': entry.get('published', datetime.now().isoformat()),
            'source': self.hash_url(source),
            'relevance': relevance,
            'processed_date': datetime.now().isoformat()
        }
    
    def calculate_relevance(self, text):
        """Calculate relevance score without exposing personal data"""
        text_lower = text.lower()
        
        # Generic academic keywords (not user-specific)
        academic_keywords = [
            'phd', 'doctoral', 'research', 'graduate', 'assistant',
            'funded', 'scholarship', 'fellowship', 'studentship'
        ]
        
        # Field-specific keywords from config (not personal data)
        field_keywords = self.config['user_profile']['research_interests']
        field_keywords_lower = [kw.lower() for kw in field_keywords]
        
        # Technical skills from config
        tech_skills = []
        for category in self.config['user_profile']['technical_skills'].values():
            tech_skills.extend([skill.lower() for skill in category])
        
        all_keywords = academic_keywords + field_keywords_lower + tech_skills
        
        # Calculate score
        score = 0
        for keyword in all_keywords:
            if keyword in text_lower:
                score += 1
        
        # Normalize and return
        max_possible_score = len(all_keywords)
        return min(score / max_possible_score * 1.5, 1.0) if max_possible_score > 0 else 0
    
    def generate_cover_letter_template(self, opportunity):
        """Generate a generic cover letter template"""
        templates = [
            """
Subject: Inquiry About PhD Opportunity - {field_interest}

Dear Search Committee,

I am writing to express my interest in the {title} position. With my background in {field_interest} and experience in {technical_domain}, I believe I would be a strong candidate for this research opportunity.

My qualifications include:
- Advanced degree in a relevant field
- Experience with {technical_skills}
- Research interests aligned with {research_area}
- Strong analytical and programming skills

I am particularly interested in opportunities that involve {specific_interests} and believe my background would allow me to contribute meaningfully to your research program.

Thank you for your consideration.

Sincerely,
[Your Name]
[Your Contact Information]
            """,
            """
Subject: PhD Application - {title}

Dear Professor,

I am excited to apply for the {title} position. My research background in {field_interest} and technical skills in {technical_domain} align well with the requirements of this role.

During my academic and professional career, I have developed:
- Expertise in {key_skills}
- Experience with research methodologies in {research_area}
- Strong problem-solving abilities in technical domains

I am eager to contribute to research in {specific_interests} and believe my background in {matching_skills} would be valuable to your team.

Thank you for considering my application.

Best regards,
[Your Name]
            """
        ]
        
        template = random.choice(templates)
        
        # Fill template with generic placeholders
        filled_template = template.format(
            title=opportunity['title'],
            field_interest="computer science and artificial intelligence",
            technical_domain="data science and machine learning",
            technical_skills="programming and data analysis",
            research_area="artificial intelligence",
            specific_interests="machine learning applications",
            key_skills="data analysis and algorithm development",
            matching_skills="computational research methods"
        )
        
        return filled_template
    
    def create_dashboard(self):
        """Create an anonymous opportunity dashboard"""
        if not self.opportunities:
            print("📊 No opportunities found to display.")
            return None
        
        # Sort by relevance
        self.opportunities.sort(key=lambda x: x['relevance'], reverse=True)
        
        # Create DataFrame for dashboard
        dashboard_data = []
        for opp in self.opportunities:
            dashboard_data.append({
                'ID': opp['id'],
                'Title': opp['title'],
                'Relevance_Score': round(opp['relevance'], 3),
                'Source': opp['source'],
                'Published': opp['published'][:10] if opp['published'] else 'Unknown',
                'Status': 'Not Applied'
            })
        
        df = pd.DataFrame(dashboard_data)
        
        # Display summary
        print(f"\n📊 OPPORTUNITY DASHBOARD")
        print("=" * 60)
        print(f"Total Opportunities Found: {len(df)}")
        print(f"High Relevance (>0.7): {len(df[df['Relevance_Score'] > 0.7])}")
        print(f"Medium Relevance (0.5-0.7): {len(df[(df['Relevance_Score'] >= 0.5) & (df['Relevance_Score'] <= 0.7)])}")
        print(f"Low Relevance (<0.5): {len(df[df['Relevance_Score'] < 0.5])}")
        
        print(f"\n🎯 TOP OPPORTUNITIES:")
        print(df[['Title', 'Relevance_Score', 'Source']].head(5).to_string(index=False))
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/opportunities_dashboard_{timestamp}.csv"
        df.to_csv(filename, index=False)
        print(f"\n💾 Dashboard saved: {filename}")
        
        return df
    
    def hash_data(self, data):
        """Hash sensitive data for privacy"""
        return hashlib.md5(data.encode()).hexdigest()[:12]
    
    def hash_url(self, url):
        """Hash URL for privacy while maintaining usefulness"""
        domain = url.split('//')[-1].split('/')[0]
        return f"https://{self.hash_data(domain)}.edu"
    
    def cleanup(self):
        """Clean up temporary files"""
        if self.config['privacy']['clean_temp_files']:
            temp_files = ['cv_data.json', 'sample_cover_letter.txt']
            for file in temp_files:
                if os.path.exists(file):
                    os.remove(file)
    
    def run_complete_scan(self):
        """Run complete scanning process"""
        print("🚀 Starting Secure PhD Application Scan...")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Scan for opportunities
            self.scan_opportunities()
            
            # Create dashboard
            dashboard = self.create_dashboard()
            
            # Generate sample cover letter if opportunities found
            if self.opportunities:
                sample_opp = self.opportunities[0]
                cover_letter = self.generate_cover_letter_template(sample_opp)
                
                # Save sample cover letter
                with open('output/sample_cover_letter_template.txt', 'w') as f:
                    f.write(cover_letter)
                print(f"\n📝 Sample cover letter template saved: output/sample_cover_letter_template.txt")
            
            print(f"\n✅ Scan completed! Found {len(self.opportunities)} opportunities.")
            
        except Exception as e:
            print(f"❌ Error during scan: {e}")
        
        finally:
            self.cleanup()

def main():
    """Main execution function"""
    bot = SecurePhDBot()
    bot.run_complete_scan()

if __name__ == "__main__":
    main()
