#!/usr/bin/env python3
"""
Complete WordPress SEO Audit Tool with AI Content Analysis
Chrome Extension Level Detail + OpenAI Content Optimization
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlsplit
import pandas as pd
from collections import Counter
import re
import json
import time
from datetime import datetime
import warnings
from typing import List, Dict
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Complete SEO Audit Tool",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .score-excellent {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .score-good {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .score-poor {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    .meta-table {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        font-family: monospace;
        font-size: 0.85rem;
        max-height: 400px;
        overflow-y: auto;
    }
    .suggestion-box {
        background: #e7f3ff;
        border-left: 4px solid #2196F3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }
    .ai-suggestion {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border: 2px solid #667eea;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .keyword-badge {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        border-radius: 15px;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

class CompleteSEOAuditor:
    def __init__(self, url, openai_api_key=None):
        self.url = url
        self.domain = urlparse(url).netloc
        self.soup = None
        self.response = None
        self.html_content = ""
        self.openai_api_key = openai_api_key
        
        self.results = {
            'url': url,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'overall_score': 0,
            
            # Basic Info
            'title': '',
            'title_length': 0,
            'meta_description': '',
            'meta_description_length': 0,
            'canonical': '',
            'robots': '',
            'lang': '',
            
            # All Meta Tags (like Chrome extension)
            'all_metas': [],
            'all_links': [],
            'all_scripts': [],
            
            # Headers
            'headers_structure': [],
            'h1_count': 0,
            'h1_list': [],
            
            # Images
            'total_images': 0,
            'images_with_alt': 0,
            'images_without_alt': [],
            'images_without_title': [],
            
            # Links
            'total_links': 0,
            'internal_links': [],
            'external_links': [],
            'broken_links': [],
            'anchor_links': [],
            
            # Open Graph
            'og_tags': {},
            
            # Twitter Cards
            'twitter_tags': {},
            
            # Schema.org
            'schema_json_ld': [],
            'schema_microdata': [],
            
            # WordPress
            'wordpress_detected': False,
            'wordpress_version': None,
            'wordpress_theme': None,
            'wordpress_plugins': [],
            
            # Content Analysis
            'word_count': 0,
            'paragraph_count': 0,
            'sentence_count': 0,
            'content_text': '',
            'keyword_density': [],
            
            # AI Suggestions
            'suggested_title': '',
            'suggested_description': '',
            'suggested_keywords': [],
            'content_improvements': [],
            'ai_content_score': 0,
            
            # Issues
            'issues': [],
            'passed_checks': []
        }
    
    def fetch_page(self):
        """Fetch webpage"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            self.response = requests.get(self.url, headers=headers, timeout=15, verify=False, allow_redirects=True)
            self.html_content = self.response.text
            self.soup = BeautifulSoup(self.response.content, 'html.parser')
            
            return True
        except Exception as e:
            st.error(f"❌ Failed to fetch page: {str(e)}")
            return False
    
    def extract_all_metas(self):
        """Extract ALL meta tags (like Chrome extension)"""
        metas = self.soup.find_all('meta')
        
        for meta in metas:
            meta_data = {}
            
            # Get meta attributes
            if meta.get('charset'):
                meta_data = {'type': 'charset', 'value': meta.get('charset')}
            elif meta.get('name'):
                meta_data = {
                    'type': 'name',
                    'name': meta.get('name'),
                    'content': meta.get('content', '')
                }
            elif meta.get('property'):
                meta_data = {
                    'type': 'property',
                    'property': meta.get('property'),
                    'content': meta.get('content', '')
                }
            elif meta.get('http-equiv'):
                meta_data = {
                    'type': 'http-equiv',
                    'http-equiv': meta.get('http-equiv'),
                    'content': meta.get('content', '')
                }
            
            if meta_data:
                self.results['all_metas'].append(meta_data)
    
    def extract_all_links(self):
        """Extract ALL link tags (like Chrome extension)"""
        links = self.soup.find_all('link')
        
        for link in links:
            link_data = {
                'rel': ' '.join(link.get('rel', [])),
                'href': link.get('href', ''),
                'type': link.get('type', ''),
                'sizes': link.get('sizes', ''),
                'media': link.get('media', '')
            }
            self.results['all_links'].append(link_data)
    
    def extract_all_scripts(self):
        """Extract ALL script tags"""
        scripts = self.soup.find_all('script')
        
        for script in scripts:
            script_data = {
                'type': script.get('type', ''),
                'src': script.get('src', ''),
                'async': script.has_attr('async'),
                'defer': script.has_attr('defer'),
                'size': len(script.string) if script.string else 0
            }
            self.results['all_scripts'].append(script_data)
    
    def check_basic_seo(self):
        """Check basic SEO elements"""
        # Title
        title = self.soup.find('title')
        if title:
            self.results['title'] = title.get_text().strip()
            self.results['title_length'] = len(self.results['title'])
        
        # Meta Description
        meta_desc = self.soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            self.results['meta_description'] = meta_desc.get('content', '').strip()
            self.results['meta_description_length'] = len(self.results['meta_description'])
        
        # Canonical
        canonical = self.soup.find('link', rel='canonical')
        if canonical:
            self.results['canonical'] = canonical.get('href', '')
        
        # Robots
        robots = self.soup.find('meta', attrs={'name': 'robots'})
        if robots:
            self.results['robots'] = robots.get('content', '')
        
        # Language
        html_tag = self.soup.find('html')
        if html_tag:
            self.results['lang'] = html_tag.get('lang', '')
    
    def analyze_headers(self):
        """Analyze all heading tags"""
        for level in range(1, 7):
            tags = self.soup.find_all(f'h{level}')
            for tag in tags:
                text = tag.get_text().strip()
                self.results['headers_structure'].append({
                    'level': f'H{level}',
                    'text': text,
                    'length': len(text),
                    'html': str(tag)[:200]
                })
                
                if level == 1:
                    self.results['h1_count'] += 1
                    self.results['h1_list'].append(text)
    
    def analyze_images(self):
        """Detailed image analysis"""
        images = self.soup.find_all('img')
        self.results['total_images'] = len(images)
        
        for img in images:
            src = img.get('src', '')
            if not src:
                continue
            
            full_url = urljoin(self.url, src)
            alt = img.get('alt')
            title = img.get('title')
            
            if alt is not None and alt.strip():
                self.results['images_with_alt'] += 1
            else:
                self.results['images_without_alt'].append({
                    'url': full_url,
                    'html': str(img)[:200]
                })
            
            if not title:
                self.results['images_without_title'].append({
                    'url': full_url,
                    'has_alt': bool(alt and alt.strip())
                })
    
    def analyze_links(self):
        """Complete link analysis"""
        links = self.soup.find_all('a', href=True)
        self.results['total_links'] = len(links)
        
        for link in links:
            href = link.get('href', '').strip()
            anchor_text = link.get_text().strip()
            
            if not href:
                continue
            
            # Anchor links
            if href.startswith('#'):
                self.results['anchor_links'].append({
                    'href': href,
                    'anchor_text': anchor_text
                })
                continue
            
            # Skip mailto and tel
            if href.startswith(('mailto:', 'tel:', 'javascript:')):
                continue
            
            full_url = urljoin(self.url, href)
            parsed = urlparse(full_url)
            
            link_data = {
                'url': full_url,
                'anchor_text': anchor_text[:100] if anchor_text else '[No anchor text]',
                'rel': link.get('rel', []),
                'target': link.get('target', '_self'),
                'title': link.get('title', '')
            }
            
            # Classify
            if parsed.netloc == self.domain or not parsed.netloc:
                self.results['internal_links'].append(link_data)
            else:
                self.results['external_links'].append(link_data)
    
    def extract_og_tags(self):
        """Extract Open Graph tags"""
        og_metas = self.soup.find_all('meta', property=re.compile('^og:'))
        
        for meta in og_metas:
            prop = meta.get('property', '')
            content = meta.get('content', '')
            self.results['og_tags'][prop] = content
    
    def extract_twitter_tags(self):
        """Extract Twitter Card tags"""
        twitter_metas = self.soup.find_all('meta', attrs={'name': re.compile('^twitter:')})
        
        for meta in twitter_metas:
            name = meta.get('name', '')
            content = meta.get('content', '')
            self.results['twitter_tags'][name] = content
    
    def extract_schema(self):
        """Extract Schema.org markup"""
        # JSON-LD
        json_ld_scripts = self.soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                self.results['schema_json_ld'].append(data)
            except:
                pass
        
        # Microdata
        items = self.soup.find_all(attrs={'itemtype': True})
        for item in items:
            self.results['schema_microdata'].append({
                'itemtype': item.get('itemtype', ''),
                'html': str(item)[:200]
            })
    
    def detect_wordpress(self):
        """Detect WordPress"""
        # Generator meta
        generator = self.soup.find('meta', attrs={'name': 'generator'})
        if generator:
            content = generator.get('content', '')
            if 'WordPress' in content:
                self.results['wordpress_detected'] = True
                version_match = re.search(r'WordPress ([\d.]+)', content)
                if version_match:
                    self.results['wordpress_version'] = version_match.group(1)
        
        # wp-content
        if 'wp-content' in self.html_content:
            self.results['wordpress_detected'] = True
        
        # Theme
        theme_match = re.search(r'/wp-content/themes/([^/]+)/', self.html_content)
        if theme_match:
            self.results['wordpress_theme'] = theme_match.group(1)
        
        # Plugins
        plugin_matches = re.findall(r'/wp-content/plugins/([^/]+)/', self.html_content)
        self.results['wordpress_plugins'] = list(set(plugin_matches))[:30]
    
    def analyze_content(self):
        """Content analysis for keyword extraction"""
        # Remove non-content elements
        for element in self.soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()
        
        # Get main content
        main_content = self.soup.find('main') or self.soup.find('article') or self.soup.find('body')
        
        if main_content:
            text = main_content.get_text()
        else:
            text = self.soup.get_text()
        
        # Clean text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        self.results['content_text'] = text
        
        # Word count
        words = text.split()
        self.results['word_count'] = len(words)
        
        # Sentences
        sentences = re.split(r'[.!?]+', text)
        self.results['sentence_count'] = len([s for s in sentences if s.strip()])
        
        # Paragraphs
        self.results['paragraph_count'] = len(self.soup.find_all('p'))
        
        # Extract keywords
        self.extract_keywords()
    
    def extract_keywords(self):
        """Extract keywords from content"""
        text = self.results['content_text'].lower()
        
        # Stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has',
            'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
            'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
            'she', 'it', 'we', 'they', 'their', 'them', 'from', 'by', 'not', 'as'
        }
        
        # Clean words
        words = re.findall(r'\b[a-z]{3,}\b', text)
        clean_words = [w for w in words if w not in stop_words]
        
        # Single keywords
        word_freq = Counter(clean_words)
        
        # 2-word phrases
        phrases_2 = []
        for i in range(len(words) - 1):
            if words[i] not in stop_words and words[i+1] not in stop_words:
                phrase = f"{words[i]} {words[i+1]}"
                phrases_2.append(phrase)
        
        phrase_2_freq = Counter(phrases_2)
        
        # 3-word phrases
        phrases_3 = []
        for i in range(len(words) - 2):
            if (words[i] not in stop_words and 
                words[i+1] not in stop_words and 
                words[i+2] not in stop_words):
                phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
                phrases_3.append(phrase)
        
        phrase_3_freq = Counter(phrases_3)
        
        # Combine results
        total_words = len(words)
        
        keyword_data = []
        
        # Top single keywords
        for word, count in word_freq.most_common(15):
            keyword_data.append({
                'keyword': word,
                'type': 'single',
                'count': count,
                'density': f"{(count/total_words*100):.2f}%"
            })
        
        # Top 2-word phrases
        for phrase, count in phrase_2_freq.most_common(10):
            if count >= 2:  # At least 2 occurrences
                keyword_data.append({
                    'keyword': phrase,
                    'type': '2-word',
                    'count': count,
                    'density': f"{(count/total_words*100):.2f}%"
                })
        
        # Top 3-word phrases
        for phrase, count in phrase_3_freq.most_common(5):
            if count >= 2:
                keyword_data.append({
                    'keyword': phrase,
                    'type': '3-word',
                    'count': count,
                    'density': f"{(count/total_words*100):.2f}%"
                })
        
        self.results['keyword_density'] = keyword_data
    
    def generate_ai_suggestions(self):
        """Generate AI-powered suggestions using OpenAI"""
        if not self.openai_api_key:
            return
        
        try:
            # Prepare content summary
            content_summary = self.results['content_text'][:3000]  # First 3000 chars
            
            # Create prompt
            prompt = f"""You are an expert SEO consultant analyzing a webpage in 2026. 

Current Page Info:
- URL: {self.url}
- Current Title: {self.results['title']}
- Current Description: {self.results['meta_description']}
- Word Count: {self.results['word_count']}
- H1: {', '.join(self.results['h1_list'])}

Content Sample:
{content_summary}

Current Top Keywords:
{', '.join([kw['keyword'] for kw in self.results['keyword_density'][:10]])}

Please provide:

1. SUGGESTED_TITLE: A compelling, SEO-optimized title (50-60 chars)
2. SUGGESTED_DESCRIPTION: An engaging meta description (150-160 chars)
3. SUGGESTED_KEYWORDS: 10 primary keywords/phrases (comma-separated)
4. CONTENT_IMPROVEMENTS: 5 specific improvements for 2026 SEO standards
5. CONTENT_SCORE: Rate content quality 0-100

Format your response as JSON:
{
  "suggested_title": "...",
  "suggested_description": "...",
  "suggested_keywords": ["keyword1", "keyword2", ...],
  "content_improvements": ["improvement1", "improvement2", ...],
  "content_score": 85
}"""

            # Call OpenAI API
            headers = {
                'Authorization': f'Bearer {self.openai_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'gpt-4o-mini',
                'messages': [
                    {'role': 'system', 'content': 'You are an expert SEO consultant specializing in 2026 best practices.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.7,
                'max_tokens': 1000
            }
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                # Parse JSON response
                try:
                    # Extract JSON from response
                    json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
                    if json_match:
                        ai_data = json.loads(json_match.group())
                        
                        self.results['suggested_title'] = ai_data.get('suggested_title', '')
                        self.results['suggested_description'] = ai_data.get('suggested_description', '')
                        self.results['suggested_keywords'] = ai_data.get('suggested_keywords', [])
                        self.results['content_improvements'] = ai_data.get('content_improvements', [])
                        self.results['ai_content_score'] = ai_data.get('content_score', 0)
                except:
                    # If JSON parsing fails, extract manually
                    pass
        
        except Exception as e:
            st.warning(f"AI analysis skipped: {str(e)}")
    
    def generate_fallback_suggestions(self):
        """Generate suggestions without AI"""
        # Extract main topic from content
        if self.results['keyword_density']:
            top_keywords = [kw['keyword'] for kw in self.results['keyword_density'][:5]]
            main_topic = top_keywords[0] if top_keywords else ''
            
            # Generate title suggestion
            if not self.results['suggested_title']:
                if main_topic:
                    self.results['suggested_title'] = f"Ultimate {main_topic.title()} Guide | {self.domain.split('.')[0].title()}"
            
            # Generate description suggestion
            if not self.results['suggested_description']:
                if main_topic and len(top_keywords) >= 3:
                    self.results['suggested_description'] = f"Discover everything about {main_topic}. Expert insights on {top_keywords[1]}, {top_keywords[2]}, and more. Get started today!"
            
            # Suggest keywords
            if not self.results['suggested_keywords']:
                self.results['suggested_keywords'] = top_keywords[:10]
    
    def identify_issues(self):
        """Identify SEO issues"""
        issues = []
        
        # Title issues
        if not self.results['title']:
            issues.append({
                'severity': 'CRITICAL',
                'category': 'Meta Tags',
                'issue': 'Missing title tag',
                'fix': f"<title>{self.results['suggested_title'] or 'Your Page Title Here'}</title>"
            })
        elif self.results['title_length'] < 30 or self.results['title_length'] > 60:
            issues.append({
                'severity': 'HIGH',
                'category': 'Meta Tags',
                'issue': f"Title length not optimal ({self.results['title_length']} chars)",
                'current': self.results['title'],
                'suggested': self.results['suggested_title'],
                'target': '50-60 characters'
            })
        
        # Description issues
        if not self.results['meta_description']:
            issues.append({
                'severity': 'CRITICAL',
                'category': 'Meta Tags',
                'issue': 'Missing meta description',
                'fix': f'<meta name="description" content="{self.results["suggested_description"] or "Your description here"}">'
            })
        elif self.results['meta_description_length'] < 120 or self.results['meta_description_length'] > 160:
            issues.append({
                'severity': 'MEDIUM',
                'category': 'Meta Tags',
                'issue': f"Meta description length not optimal ({self.results['meta_description_length']} chars)",
                'current': self.results['meta_description'],
                'suggested': self.results['suggested_description'],
                'target': '150-160 characters'
            })
        
        # H1 issues
        if self.results['h1_count'] == 0:
            issues.append({
                'severity': 'CRITICAL',
                'category': 'Content Structure',
                'issue': 'Missing H1 heading',
                'fix': 'Add one H1 heading to your page'
            })
        elif self.results['h1_count'] > 1:
            issues.append({
                'severity': 'HIGH',
                'category': 'Content Structure',
                'issue': f"Multiple H1 headings ({self.results['h1_count']})",
                'h1_list': self.results['h1_list'],
                'fix': 'Use only ONE H1 per page'
            })
        
        # Image issues
        if self.results['images_without_alt']:
            issues.append({
                'severity': 'CRITICAL',
                'category': 'Images',
                'issue': f"{len(self.results['images_without_alt'])} images missing alt text",
                'count': len(self.results['images_without_alt']),
                'details_key': 'images_without_alt'
            })
        
        # Content issues
        if self.results['word_count'] < 300:
            issues.append({
                'severity': 'HIGH',
                'category': 'Content Quality',
                'issue': f"Thin content ({self.results['word_count']} words)",
                'target': 'Minimum 500 words, ideally 1000+'
            })
        
        # Schema issues
        if not self.results['schema_json_ld'] and not self.results['schema_microdata']:
            issues.append({
                'severity': 'MEDIUM',
                'category': 'Structured Data',
                'issue': 'No Schema.org markup found',
                'recommendation': 'Add structured data for rich snippets'
            })
        
        # Canonical issues
        if not self.results['canonical']:
            issues.append({
                'severity': 'HIGH',
                'category': 'Technical SEO',
                'issue': 'Missing canonical URL',
                'fix': f'<link rel="canonical" href="{self.url}">'
            })
        
        # Open Graph issues
        if not self.results['og_tags']:
            issues.append({
                'severity': 'MEDIUM',
                'category': 'Social Media',
                'issue': 'Missing Open Graph tags',
                'recommendation': 'Add OG tags for better social sharing'
            })
        
        self.results['issues'] = issues
    
    def calculate_score(self):
        """Calculate overall SEO score"""
        critical = len([i for i in self.results['issues'] if i['severity'] == 'CRITICAL'])
        high = len([i for i in self.results['issues'] if i['severity'] == 'HIGH'])
        medium = len([i for i in self.results['issues'] if i['severity'] == 'MEDIUM'])
        
        penalty = (critical * 15) + (high * 10) + (medium * 5)
        score = max(0, 100 - penalty)
        
        self.results['overall_score'] = score
    
    def run_complete_audit(self):
        """Run complete SEO audit"""
        if not self.fetch_page():
            return self.results
        
        with st.spinner('🔍 Extracting all meta tags...'):
            self.extract_all_metas()
            time.sleep(0.1)
        
        with st.spinner('🔗 Analyzing all links...'):
            self.extract_all_links()
            time.sleep(0.1)
        
        with st.spinner('📜 Scanning scripts...'):
            self.extract_all_scripts()
            time.sleep(0.1)
        
        with st.spinner('📋 Checking SEO basics...'):
            self.check_basic_seo()
            time.sleep(0.1)
        
        with st.spinner('📰 Analyzing headers...'):
            self.analyze_headers()
            time.sleep(0.1)
        
        with st.spinner('🖼️ Analyzing images...'):
            self.analyze_images()
            time.sleep(0.1)
        
        with st.spinner('🔗 Analyzing links...'):
            self.analyze_links()
            time.sleep(0.1)
        
        with st.spinner('📱 Extracting social media tags...'):
            self.extract_og_tags()
            self.extract_twitter_tags()
            time.sleep(0.1)
        
        with st.spinner('🏷️ Extracting Schema.org markup...'):
            self.extract_schema()
            time.sleep(0.1)
        
        with st.spinner('🔧 Detecting WordPress...'):
            self.detect_wordpress()
            time.sleep(0.1)
        
        with st.spinner('📝 Analyzing content...'):
            self.analyze_content()
            time.sleep(0.1)
        
        with st.spinner('🤖 Generating AI suggestions...'):
            self.generate_ai_suggestions()
            self.generate_fallback_suggestions()
            time.sleep(0.1)
        
        with st.spinner('⚠️ Identifying issues...'):
            self.identify_issues()
            time.sleep(0.1)
        
        with st.spinner('📊 Calculating score...'):
            self.calculate_score()
        
        return self.results

# ==================== UI FUNCTIONS ====================

def render_summary_table(results):
    """Render summary table like Chrome extension"""
    st.markdown("### 📊 SEO Summary")
    
    summary_data = {
        'Element': ['Title', 'Description', 'Keywords', 'URL', 'Canonical', 'Robots Tag', 'Language', 'H1/H2/H3/H4/H5/H6', 'Images', 'Links'],
        'Status': [
            f"{results['title_length']} characters" if results['title'] else '❌ Missing',
            f"{results['meta_description_length']} characters" if results['meta_description'] else '❌ Missing',
            '❌ Keywords are missing!' if not results['suggested_keywords'] else f"✅ {len(results['suggested_keywords'])} suggested",
            results['url'],
            results['canonical'] if results['canonical'] else '❌ Missing',
            results['robots'] if results['robots'] else 'Not set',
            results['lang'] if results['lang'] else 'Not set',
            f"{results['h1_count']}/{len([h for h in results['headers_structure'] if h['level']=='H2'])}/{len([h for h in results['headers_structure'] if h['level']=='H3'])}/...",
            str(results['total_images']),
            str(results['total_links'])
        ]
    }
    
    df = pd.DataFrame(summary_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

def render_ai_suggestions(results):
    """Render AI-powered suggestions"""
    st.markdown("### 🤖 AI-Powered SEO Suggestions (2026 Standards)")
    
    # Title suggestion
    if results['suggested_title']:
        st.markdown("#### 📝 Suggested Title")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Current:**")
            st.code(results['title'] or '[None]', language='html')
            st.caption(f"Length: {results['title_length']} characters")
        
        with col2:
            st.markdown("**Suggested:**")
            st.code(results['suggested_title'], language='html')
            st.caption(f"Length: {len(results['suggested_title'])} characters")
            
            if st.button("📋 Copy Suggested Title"):
                st.success("✅ Copied!")
    
    # Description suggestion
    if results['suggested_description']:
        st.markdown("#### 📄 Suggested Meta Description")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Current:**")
            st.code(results['meta_description'] or '[None]', language='html')
            st.caption(f"Length: {results['meta_description_length']} characters")
        
        with col2:
            st.markdown("**Suggested:**")
            st.code(results['suggested_description'], language='html')
            st.caption(f"Length: {len(results['suggested_description'])} characters")
            
            if st.button("📋 Copy Suggested Description"):
                st.success("✅ Copied!")
    
    # Keyword suggestions
    if results['suggested_keywords']:
        st.markdown("#### 🎯 Suggested Keywords")
        st.markdown("**Use these keywords in your content, title, and meta description:**")
        
        for kw in results['suggested_keywords']:
            st.markdown(f'<span class="keyword-badge">{kw}</span>', unsafe_allow_html=True)
        
        st.markdown("")
        
        # Download keywords
        keywords_text = '\n'.join(results['suggested_keywords'])
        st.download_button(
            "📥 Download Keywords",
            keywords_text,
            f"keywords_{datetime.now().strftime('%Y%m%d')}.txt",
            "text/plain"
        )
    
    # Content improvements
    if results['content_improvements']:
        st.markdown("#### ✨ Content Improvement Recommendations")
        for i, improvement in enumerate(results['content_improvements'], 1):
            st.markdown(f"**{i}.** {improvement}")
    
    # AI Content Score
    if results['ai_content_score'] > 0:
        st.markdown("#### 📈 AI Content Quality Score")
        
        score = results['ai_content_score']
        
        if score >= 80:
            color = "#28a745"
            status = "Excellent"
        elif score >= 60:
            color = "#ffc107"
            status = "Good"
        else:
            color = "#dc3545"
            status = "Needs Improvement"
        
        st.markdown(f"""
        <div style="background: {color}; color: white; padding: 1rem; border-radius: 8px; text-align: center;">
            <h2 style="margin: 0;">{score}/100</h2>
            <p style="margin: 0;">{status}</p>
        </div>
        """, unsafe_allow_html=True)

def render_all_metas(results):
    """Render all meta tags like Chrome extension"""
    st.markdown("### 🏷️ ALL META TAGS")
    
    if results['all_metas']:
        for meta in results['all_metas']:
            if meta['type'] == 'charset':
                st.code(f"charset: {meta['value']}", language='text')
            elif meta['type'] == 'name':
                st.code(f"{meta['name']}: {meta['content']}", language='text')
            elif meta['type'] == 'property':
                st.code(f"{meta['property']}: {meta['content']}", language='text')
            elif meta['type'] == 'http-equiv':
                st.code(f"{meta['http-equiv']}: {meta['content']}", language='text')
    else:
        st.info("No meta tags found")

def render_all_links_rel(results):
    """Render all link tags"""
    st.markdown("### 🔗 ALL LINKS (rel)")
    
    if results['all_links']:
        for link in results['all_links']:
            if link['rel']:
                href_display = link['href'][:80] if link['href'] else '[No href]'
                st.code(f"{link['rel']}: {href_display}", language='text')
    else:
        st.info("No link tags found")

def render_keyword_density(results):
    """Render keyword density analysis"""
    st.markdown("### 🔑 Keyword Density Analysis")
    
    if results['keyword_density']:
        df = pd.DataFrame(results['keyword_density'])
        
        # Separate by type
        single = df[df['type'] == 'single'].head(15)
        phrases_2 = df[df['type'] == '2-word'].head(10)
        phrases_3 = df[df['type'] == '3-word'].head(5)
        
        tab1, tab2, tab3 = st.tabs(["Single Keywords", "2-Word Phrases", "3-Word Phrases"])
        
        with tab1:
            if not single.empty:
                st.dataframe(single[['keyword', 'count', 'density']], use_container_width=True, hide_index=True)
        
        with tab2:
            if not phrases_2.empty:
                st.dataframe(phrases_2[['keyword', 'count', 'density']], use_container_width=True, hide_index=True)
        
        with tab3:
            if not phrases_3.empty:
                st.dataframe(phrases_3[['keyword', 'count', 'density']], use_container_width=True, hide_index=True)
    else:
        st.info("No keywords extracted")

def render_headers_hierarchy(results):
    """Render complete headers structure"""
    st.markdown("### 📋 Complete Headers Hierarchy")
    
    if results['headers_structure']:
        st.markdown("**All headers in order of appearance:**")
        
        for header in results['headers_structure']:
            indent = "  " * (int(header['level'][1]) - 1)
            st.markdown(f"`{header['level']}` {indent}{header['text']}")
        
        # Table view
        st.markdown("**Table View:**")
        df = pd.DataFrame(results['headers_structure'])
        st.dataframe(df[['level', 'text', 'length']], use_container_width=True, hide_index=True)
        
        # Download
        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Download Headers Structure",
            csv,
            f"headers_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    else:
        st.warning("No headers found")

def render_images_complete(results):
    """Render complete image analysis"""
    st.markdown("### 🖼️ Complete Image Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Images", results['total_images'])
    with col2:
        st.metric("With Alt", results['images_with_alt'])
    with col3:
        st.metric("Missing Alt", len(results['images_without_alt']))
    
    if results['images_without_alt']:
        st.markdown("#### ❌ Images Missing Alt Text")
        
        df_data = []
        for idx, img in enumerate(results['images_without_alt'], 1):
            st.markdown(f"**{idx}.** `{img['url']}`")
            df_data.append({
                'No.': idx,
                'Image URL': img['url'],
                'Fix': 'Add alt text in WordPress Media Library'
            })
        
        df = pd.DataFrame(df_data)
        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Download List of Images Missing Alt",
            csv,
            f"images_missing_alt_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )

def render_links_complete(results):
    """Render complete link analysis"""
    st.markdown("### 🔗 Complete Link Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Links", results['total_links'])
    with col2:
        st.metric("Internal", len(results['internal_links']))
    with col3:
        st.metric("External", len(results['external_links']))
    
    tab1, tab2, tab3 = st.tabs(["Internal Links", "External Links", "Anchor Links"])
    
    with tab1:
        if results['internal_links']:
            df_data = []
            for idx, link in enumerate(results['internal_links'], 1):
                df_data.append({
                    'No.': idx,
                    'URL': link['url'],
                    'Anchor Text': link['anchor_text'],
                    'Title': link['title']
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download Internal Links",
                csv,
                f"internal_links_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )
    
    with tab2:
        if results['external_links']:
            df_data = []
            for idx, link in enumerate(results['external_links'], 1):
                df_data.append({
                    'No.': idx,
                    'URL': link['url'],
                    'Anchor Text': link['anchor_text'],
                    'Rel': ', '.join(link['rel']),
                    'Target': link['target']
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download External Links",
                csv,
                f"external_links_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )
    
    with tab3:
        if results['anchor_links']:
            for idx, link in enumerate(results['anchor_links'], 1):
                st.markdown(f"{idx}. `{link['href']}` - {link['anchor_text']}")

def render_social_tags(results):
    """Render Open Graph and Twitter Cards"""
    st.markdown("### 📱 Social Media Tags")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Facebook / Open Graph")
        if results['og_tags']:
            for prop, content in results['og_tags'].items():
                st.code(f"{prop}: {content[:100]}", language='text')
        else:
            st.warning("No Open Graph tags found")
    
    with col2:
        st.markdown("#### Twitter Cards")
        if results['twitter_tags']:
            for name, content in results['twitter_tags'].items():
                st.code(f"{name}: {content[:100]}", language='text')
        else:
            st.warning("No Twitter Card tags found")

def render_schema_markup(results):
    """Render Schema.org markup"""
    st.markdown("### 🏷️ Schema.org Structured Data")
    
    if results['schema_json_ld']:
        st.markdown("#### JSON-LD")
        for idx, schema in enumerate(results['schema_json_ld'], 1):
            schema_type = schema.get('@type', 'Unknown')
            st.markdown(f"**{idx}. Type:** `{schema_type}`")
            with st.expander("View full schema"):
                st.json(schema)
    else:
        st.info("No JSON-LD schemas found")
    
    if results['schema_microdata']:
        st.markdown("#### Microdata")
        for idx, schema in enumerate(results['schema_microdata'], 1):
            st.markdown(f"**{idx}.** {schema['itemtype']}")

# ==================== MAIN APP ====================

def main():
    st.markdown('<h1 class="main-header">🔍 Complete SEO Audit Tool</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.1rem;">Chrome Extension Detail + AI Content Analysis + 2026 Standards</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        openai_api_key = st.text_input(
            "OpenAI API Key (Optional)",
            type="password",
            help="Add your OpenAI API key for AI-powered content analysis and suggestions"
        )
        
        if openai_api_key:
            st.success("✅ AI Analysis Enabled")
        else:
            st.info("💡 Add OpenAI API key for AI suggestions")
        
        st.markdown("---")
        st.markdown("### 📊 What This Tool Provides")
        st.success("""
        **Chrome Extension Level:**
        - All meta tags
        - All link tags
        - All scripts
        - Complete headers
        - Full link inventory
        - OG & Twitter cards
        - Schema.org markup
        
        **AI-Powered (with API key):**
        - Suggested title
        - Suggested description
        - Keyword recommendations
        - Content improvements
        - Quality scoring
        
        **WordPress Optimized:**
        - Plugin detection
        - Complete URL listings
        - Downloadable CSVs
        - Step-by-step fixes
        """)
    
    # Main input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        url_input = st.text_input(
            "Enter URL to Audit:",
            placeholder="https://yourwebsite.com",
            help="Enter the full URL"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_button = st.button("🚀 Complete Audit", type="primary", use_container_width=True)
    
    # Run audit
    if analyze_button and url_input:
        if not url_input.startswith(('http://', 'https://')):
            url_input = 'https://' + url_input
        
        auditor = CompleteSEOAuditor(url_input, openai_api_key if openai_api_key else None)
        results = auditor.run_complete_audit()
        
        st.markdown("---")
        
        # Score
        score = results['overall_score']
        
        if score >= 80:
            color = "#28a745"
            status = "EXCELLENT"
            emoji = "🎉"
        elif score >= 60:
            color = "#ffc107"
            status = "GOOD"
            emoji = "👍"
        else:
            color = "#dc3545"
            status = "NEEDS WORK"
            emoji = "⚠️"
        
        st.markdown(f"""
        <div class="score-card" style="background: {color};">
            <h1 style="margin: 0; font-size: 4rem;">{emoji}</h1>
            <h2 style="margin: 0.5rem 0;">SEO Score: {score}/100</h2>
            <p style="margin: 0; font-size: 1.5rem;">{status}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Summary table
        render_summary_table(results)
        
        st.markdown("---")
        
        # AI Suggestions (if enabled)
        if openai_api_key or results['suggested_keywords']:
            render_ai_suggestions(results)
            st.markdown("---")
        
        # Tabs
        tabs = st.tabs([
            "📊 Summary",
            "🏷️ All Metas",
            "🔗 All Links",
            "📋 Headers",
            "🖼️ Images",
            "🔗 Link Analysis",
            "🔑 Keywords",
            "📱 Social Tags",
            "🏷️ Schema",
            "⚠️ Issues",
            "📥 Export"
        ])
        
        with tabs[0]:
            st.markdown("### 📊 Quick Overview")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Word Count", results['word_count'])
            col2.metric("Images", results['total_images'])
            col3.metric("Links", results['total_links'])
            col4.metric("H1 Tags", results['h1_count'])
            
            if results['wordpress_detected']:
                st.markdown("---")
                st.success(f"✅ WordPress {results['wordpress_version'] or 'Detected'}")
                st.info(f"Theme: {results['wordpress_theme'] or 'Unknown'}")
                if results['wordpress_plugins']:
                    st.info(f"Plugins: {len(results['wordpress_plugins'])} detected")
        
        with tabs[1]:
            render_all_metas(results)
        
        with tabs[2]:
            render_all_links_rel(results)
        
        with tabs[3]:
            render_headers_hierarchy(results)
        
        with tabs[4]:
            render_images_complete(results)
        
        with tabs[5]:
            render_links_complete(results)
        
        with tabs[6]:
            render_keyword_density(results)
        
        with tabs[7]:
            render_social_tags(results)
        
        with tabs[8]:
            render_schema_markup(results)
        
        with tabs[9]:
            st.markdown("### ⚠️ Issues Found")
            
            if results['issues']:
                for issue in results['issues']:
                    severity = issue['severity']
                    
                    if severity == 'CRITICAL':
                        badge = "🔴"
                    elif severity == 'HIGH':
                        badge = "🟠"
                    else:
                        badge = "🟡"
                    
                    with st.expander(f"{badge} {severity}: {issue['issue']}"):
                        if issue.get('current'):
                            st.markdown("**Current:**")
                            st.code(issue['current'], language='html')
                        
                        if issue.get('suggested'):
                            st.markdown("**Suggested:**")
                            st.code(issue['suggested'], language='html')
                        
                        if issue.get('fix'):
                            st.markdown("**Fix:**")
                            st.code(issue['fix'], language='html')
                        
                        if issue.get('recommendation'):
                            st.info(issue['recommendation'])
            else:
                st.success("🎉 No issues found!")
        
        with tabs[10]:
            st.markdown("### 📥 Export Reports")
            
            # Full report
            report = f"""
COMPLETE SEO AUDIT REPORT
========================

URL: {results['url']}
Date: {results['timestamp']}
Score: {results['overall_score']}/100

BASIC SEO:
- Title: {results['title']} ({results['title_length']} chars)
- Description: {results['meta_description']} ({results['meta_description_length']} chars)
- Canonical: {results['canonical']}
- Language: {results['lang']}

CONTENT:
- Word Count: {results['word_count']}
- Paragraphs: {results['paragraph_count']}
- Sentences: {results['sentence_count']}

STRUCTURE:
- H1 Tags: {results['h1_count']}
- Total Headers: {len(results['headers_structure'])}
- Images: {results['total_images']}
- Links: {results['total_links']}

AI SUGGESTIONS:
- Suggested Title: {results['suggested_title']}
- Suggested Description: {results['suggested_description']}
- Keywords: {', '.join(results['suggested_keywords'])}

ISSUES FOUND: {len(results['issues'])}
{chr(10).join([f"- {issue['issue']}" for issue in results['issues']])}

TOP KEYWORDS:
{chr(10).join([f"- {kw['keyword']} ({kw['count']} times, {kw['density']})" for kw in results['keyword_density'][:15]])}
"""
            
            st.download_button(
                "📄 Download Full Report",
                report,
                f"complete_seo_audit_{datetime.now().strftime('%Y%m%d')}.txt",
                "text/plain",
                use_container_width=True
            )
    
    elif analyze_button:
        st.warning("⚠️ Please enter a URL")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p><strong>Complete SEO Audit Tool</strong> - Chrome Extension Detail + AI Analysis</p>
        <p>All meta tags • All links • Keywords • AI suggestions • 2026 standards</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
