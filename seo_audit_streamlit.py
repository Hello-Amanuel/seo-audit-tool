#!/usr/bin/env python3
"""
Advanced SEO Intelligence Platform - MVP
Professional SEO analysis with AI-powered insights and comprehensive auditing
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
import math
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="SEO Intelligence Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional UI
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
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .issue-critical {
        background: #fee;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .issue-warning {
        background: #ffc;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .issue-passed {
        background: #efe;
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .code-snippet {
        background: #2d2d2d;
        color: #f8f8f2;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        overflow-x: auto;
        margin: 0.5rem 0;
    }
    .priority-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        margin: 0.2rem;
    }
    .priority-critical {
        background: #dc3545;
        color: white;
    }
    .priority-high {
        background: #fd7e14;
        color: white;
    }
    .priority-medium {
        background: #ffc107;
        color: #333;
    }
    .priority-low {
        background: #17a2b8;
        color: white;
    }
    .insight-box {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #667eea;
    }
    .tab-content {
        padding: 2rem 0;
    }
    .progress-ring {
        transform: rotate(-90deg);
    }
</style>
""", unsafe_allow_html=True)

class AdvancedSEOAuditor:
    def __init__(self, url):
        self.url = url
        self.domain = urlparse(url).netloc
        self.soup = None
        self.response = None
        self.html_content = ""
        self.results = {
            'url': url,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'overall_score': 0,
            'category_scores': {},
            'critical_issues': [],
            'high_priority': [],
            'medium_priority': [],
            'low_priority': [],
            'passed_checks': [],
            'insights': [],
            'action_plan': [],
            'metadata': {},
            'technical_data': {},
            'content_data': {},
            'performance_data': {}
        }
        
    def fetch_page(self):
        """Fetch webpage with detailed headers"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            self.response = requests.get(self.url, headers=headers, timeout=15, verify=False, allow_redirects=True)
            self.html_content = self.response.text
            self.soup = BeautifulSoup(self.response.content, 'html.parser')
            
            # Store response headers for analysis
            self.results['technical_data']['status_code'] = self.response.status_code
            self.results['technical_data']['response_time'] = self.response.elapsed.total_seconds()
            self.results['technical_data']['headers'] = dict(self.response.headers)
            self.results['technical_data']['redirects'] = len(self.response.history)
            
            return True
        except Exception as e:
            st.error(f"❌ Failed to fetch page: {str(e)}")
            return False
    
    # ==================== TECHNICAL SEO CHECKS ====================
    
    def check_title_tag(self):
        """Comprehensive title tag analysis"""
        title = self.soup.find('title')
        
        if not title:
            self.results['critical_issues'].append({
                'category': 'Technical SEO',
                'issue': "Missing <title> tag",
                'severity': 'CRITICAL',
                'impact': 'Severe negative impact on rankings. Title tags are one of the most important on-page SEO elements.',
                'fix': '<title>Primary Keyword - Secondary Keyword | Brand Name</title>',
                'how_to_fix': [
                    'Add a <title> tag in the <head> section',
                    'Include primary keyword near the beginning',
                    'Keep it between 50-60 characters',
                    'Make it compelling to increase CTR'
                ],
                'example': '<title>Omo Valley Cultural Tours - Authentic Ethiopian Experience | YourBrand</title>'
            })
            return
        
        title_text = title.get_text().strip()
        title_length = len(title_text)
        
        # Store metadata
        self.results['metadata']['title'] = title_text
        self.results['metadata']['title_length'] = title_length
        
        # Check for empty title
        if not title_text:
            self.results['critical_issues'].append({
                'category': 'Technical SEO',
                'issue': "Empty <title> tag",
                'severity': 'CRITICAL',
                'current': '<title></title>',
                'fix': '<title>Your Primary Keyword - Brand Name</title>'
            })
            return
        
        # Check title length
        if title_length < 30:
            self.results['high_priority'].append({
                'category': 'Technical SEO',
                'issue': f"Title too short ({title_length} characters)",
                'severity': 'HIGH',
                'current': title_text,
                'recommendation': f'Expand to 50-60 characters (add {50-title_length} more chars)',
                'impact': 'Missing opportunity to include more keywords and improve CTR'
            })
        elif title_length > 60:
            self.results['medium_priority'].append({
                'category': 'Technical SEO',
                'issue': f"Title too long ({title_length} characters)",
                'severity': 'MEDIUM',
                'current': title_text,
                'recommendation': 'Shorten to 50-60 characters to avoid truncation in SERPs',
                'truncated_preview': title_text[:60] + '...'
            })
        else:
            self.results['passed_checks'].append({
                'category': 'Technical SEO',
                'check': 'Title Tag Length',
                'status': f'Optimal ({title_length} characters)',
                'value': title_text
            })
        
        # Check for brand name
        if '|' not in title_text and '-' not in title_text:
            self.results['medium_priority'].append({
                'category': 'Technical SEO',
                'issue': "Title doesn't include brand separator",
                'severity': 'MEDIUM',
                'recommendation': 'Add brand name separated by | or - for better brand recognition',
                'example': f'{title_text} | Your Brand Name'
            })
        
        # Check for duplicate words
        words = title_text.lower().split()
        if len(words) != len(set(words)):
            duplicates = [word for word in set(words) if words.count(word) > 1]
            self.results['low_priority'].append({
                'category': 'Technical SEO',
                'issue': f"Duplicate words in title: {', '.join(duplicates)}",
                'severity': 'LOW',
                'recommendation': 'Remove duplicate words to make room for more keywords'
            })
    
    def check_meta_description(self):
        """Comprehensive meta description analysis"""
        meta_desc = self.soup.find('meta', attrs={'name': 'description'}) or \
                   self.soup.find('meta', attrs={'property': 'og:description'})
        
        if not meta_desc:
            self.results['critical_issues'].append({
                'category': 'Technical SEO',
                'issue': "Missing meta description",
                'severity': 'CRITICAL',
                'impact': 'Search engines will generate their own description, missing CTR optimization opportunity',
                'fix': '<meta name="description" content="Compelling description with primary keywords (150-160 chars)">',
                'best_practices': [
                    'Include primary keyword naturally',
                    'Add a call-to-action',
                    'Make it compelling and unique',
                    'Keep between 150-160 characters'
                ]
            })
            return
        
        desc_text = meta_desc.get('content', '').strip()
        desc_length = len(desc_text)
        
        self.results['metadata']['description'] = desc_text
        self.results['metadata']['description_length'] = desc_length
        
        if not desc_text:
            self.results['critical_issues'].append({
                'category': 'Technical SEO',
                'issue': "Empty meta description",
                'severity': 'CRITICAL'
            })
        elif desc_length < 120:
            self.results['high_priority'].append({
                'category': 'Technical SEO',
                'issue': f"Meta description too short ({desc_length} characters)",
                'severity': 'HIGH',
                'current': desc_text,
                'recommendation': f'Expand to 150-160 characters (add {150-desc_length} more)'
            })
        elif desc_length > 160:
            self.results['medium_priority'].append({
                'category': 'Technical SEO',
                'issue': f"Meta description too long ({desc_length} characters)",
                'severity': 'MEDIUM',
                'current': desc_text,
                'recommendation': f'Shorten by {desc_length-160} characters'
            })
        else:
            self.results['passed_checks'].append({
                'category': 'Technical SEO',
                'check': 'Meta Description',
                'status': f'Optimal ({desc_length} characters)'
            })
        
        # Check for call-to-action
        cta_words = ['learn', 'discover', 'get', 'find', 'explore', 'book', 'buy', 'start', 'try', 'contact']
        has_cta = any(word in desc_text.lower() for word in cta_words)
        
        if not has_cta:
            self.results['low_priority'].append({
                'category': 'Content Optimization',
                'issue': "Meta description lacks call-to-action",
                'severity': 'LOW',
                'recommendation': 'Add CTA words like "Discover", "Learn more", "Get started" to improve CTR'
            })
    
    def check_headings_structure(self):
        """Comprehensive heading hierarchy analysis"""
        headings_data = {}
        
        for i in range(1, 7):
            tags = self.soup.find_all(f'h{i}')
            if tags:
                headings_data[f'h{i}'] = {
                    'count': len(tags),
                    'texts': [tag.get_text().strip()[:100] for tag in tags[:5]]
                }
        
        self.results['content_data']['headings'] = headings_data
        
        # Check H1
        h1_tags = self.soup.find_all('h1')
        
        if not h1_tags:
            self.results['critical_issues'].append({
                'category': 'Technical SEO',
                'issue': "Missing H1 heading",
                'severity': 'CRITICAL',
                'impact': 'H1 helps search engines understand main page topic',
                'fix': '<h1>Primary Keyword - Main Topic</h1>',
                'best_practices': [
                    'Use only ONE H1 per page',
                    'Include primary keyword',
                    'Make it descriptive and compelling',
                    'Place near top of page'
                ]
            })
        elif len(h1_tags) > 1:
            self.results['high_priority'].append({
                'category': 'Technical SEO',
                'issue': f"Multiple H1 tags found ({len(h1_tags)})",
                'severity': 'HIGH',
                'h1_tags': [h1.get_text().strip()[:100] for h1 in h1_tags],
                'recommendation': 'Use only ONE H1 per page. Convert others to H2 or H3',
                'fix': 'Change <h1>Secondary Heading</h1> to <h2>Secondary Heading</h2>'
            })
        else:
            h1_text = h1_tags[0].get_text().strip()
            self.results['passed_checks'].append({
                'category': 'Technical SEO',
                'check': 'H1 Heading',
                'status': 'Found',
                'value': h1_text[:100]
            })
            
            # Check H1 length
            if len(h1_text) < 20:
                self.results['medium_priority'].append({
                    'category': 'Content Optimization',
                    'issue': f"H1 too short ({len(h1_text)} characters)",
                    'severity': 'MEDIUM',
                    'recommendation': 'Expand H1 to be more descriptive (aim for 20-70 characters)'
                })
        
        # Check heading hierarchy
        if headings_data:
            hierarchy_issues = []
            
            if 'h3' in headings_data and 'h2' not in headings_data:
                hierarchy_issues.append("H3 used without H2")
            if 'h4' in headings_data and 'h3' not in headings_data:
                hierarchy_issues.append("H4 used without H3")
            
            if hierarchy_issues:
                self.results['medium_priority'].append({
                    'category': 'Technical SEO',
                    'issue': "Broken heading hierarchy",
                    'severity': 'MEDIUM',
                    'issues': hierarchy_issues,
                    'recommendation': 'Maintain proper heading order: H1 → H2 → H3 → H4'
                })
            else:
                self.results['passed_checks'].append({
                    'category': 'Technical SEO',
                    'check': 'Heading Hierarchy',
                    'status': 'Proper structure maintained'
                })
    
    def check_images_optimization(self):
        """Comprehensive image SEO analysis"""
        images = self.soup.find_all('img')
        
        if not images:
            self.results['low_priority'].append({
                'category': 'Content Optimization',
                'issue': "No images found",
                'severity': 'LOW',
                'recommendation': 'Add relevant images to improve engagement and SEO'
            })
            return
        
        missing_alt = []
        empty_alt = []
        missing_title = []
        large_images = []
        non_optimized_format = []
        
        for img in images:
            src = img.get('src', '')
            alt = img.get('alt')
            title = img.get('title')
            width = img.get('width')
            height = img.get('height')
            
            # Check alt text
            if alt is None:
                missing_alt.append(src[:100])
            elif not alt.strip():
                empty_alt.append(src[:100])
            
            # Check title attribute
            if not title:
                missing_title.append(src[:100])
            
            # Check dimensions
            if width and height:
                try:
                    w = int(width)
                    h = int(height)
                    if w * h > 1000000:  # > 1 megapixel
                        large_images.append(f"{src[:50]} ({w}x{h})")
                except:
                    pass
            
            # Check format
            if src and not any(fmt in src.lower() for fmt in ['.webp', '.avif']):
                if any(fmt in src.lower() for fmt in ['.jpg', '.jpeg', '.png']):
                    non_optimized_format.append(src[:100])
        
        total_images = len(images)
        self.results['content_data']['total_images'] = total_images
        self.results['content_data']['images_missing_alt'] = len(missing_alt)
        
        # Report issues
        if missing_alt:
            self.results['critical_issues'].append({
                'category': 'Accessibility & SEO',
                'issue': f"{len(missing_alt)} images missing alt attribute",
                'severity': 'CRITICAL',
                'impact': 'Critical for accessibility and image SEO',
                'images': missing_alt[:10],
                'fix': '<img src="image.jpg" alt="Descriptive text about image content">',
                'recommendation': 'Add descriptive alt text to all images'
            })
        
        if empty_alt:
            self.results['high_priority'].append({
                'category': 'Accessibility & SEO',
                'issue': f"{len(empty_alt)} images with empty alt text",
                'severity': 'HIGH',
                'images': empty_alt[:10],
                'fix': 'Replace alt="" with descriptive text'
            })
        
        if non_optimized_format:
            self.results['medium_priority'].append({
                'category': 'Performance',
                'issue': f"{len(non_optimized_format)} images using non-optimized formats",
                'severity': 'MEDIUM',
                'recommendation': 'Convert to WebP or AVIF for better performance',
                'benefit': 'Can reduce file size by 25-50%'
            })
        
        if not missing_alt and not empty_alt:
            self.results['passed_checks'].append({
                'category': 'Accessibility',
                'check': 'Image Alt Text',
                'status': f'All {total_images} images have alt text'
            })
    
    def check_schema_markup(self):
        """Check for structured data / schema markup"""
        # JSON-LD
        json_ld = self.soup.find_all('script', type='application/ld+json')
        
        # Microdata
        microdata = self.soup.find_all(attrs={'itemtype': True})
        
        schemas_found = []
        
        if json_ld:
            for script in json_ld:
                try:
                    data = json.loads(script.string)
                    schema_type = data.get('@type', 'Unknown')
                    schemas_found.append(f"JSON-LD: {schema_type}")
                except:
                    pass
        
        if microdata:
            for item in microdata:
                itemtype = item.get('itemtype', '')
                schema_name = itemtype.split('/')[-1] if itemtype else 'Unknown'
                schemas_found.append(f"Microdata: {schema_name}")
        
        self.results['technical_data']['schemas'] = schemas_found
        
        if not json_ld and not microdata:
            self.results['medium_priority'].append({
                'category': 'Technical SEO',
                'issue': "No schema markup found",
                'severity': 'MEDIUM',
                'impact': 'Missing opportunity for rich snippets in search results',
                'recommendation': 'Add relevant schema markup (Organization, Article, Product, etc.)',
                'example': '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Your Company",
  "url": "https://yoursite.com"
}
</script>''',
                'tools': ['Google Schema Markup Generator', 'Schema.org documentation']
            })
        else:
            self.results['passed_checks'].append({
                'category': 'Technical SEO',
                'check': 'Schema Markup',
                'status': f'Found {len(schemas_found)} schemas',
                'schemas': schemas_found
            })
    
    def check_mobile_optimization(self):
        """Check mobile-friendly settings"""
        viewport = self.soup.find('meta', attrs={'name': 'viewport'})
        
        if not viewport:
            self.results['critical_issues'].append({
                'category': 'Mobile Optimization',
                'issue': "Missing viewport meta tag",
                'severity': 'CRITICAL',
                'impact': 'Page will not be mobile-friendly. Critical ranking factor.',
                'fix': '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                'how_to_fix': [
                    'Add viewport meta tag to <head>',
                    'Test on Google Mobile-Friendly Test',
                    'Ensure responsive design'
                ]
            })
        else:
            viewport_content = viewport.get('content', '')
            self.results['passed_checks'].append({
                'category': 'Mobile Optimization',
                'check': 'Viewport Meta Tag',
                'status': 'Present',
                'value': viewport_content
            })
            
            # Check viewport settings
            if 'width=device-width' not in viewport_content:
                self.results['high_priority'].append({
                    'category': 'Mobile Optimization',
                    'issue': "Viewport not set to device width",
                    'severity': 'HIGH',
                    'fix': '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
                })
        
        # Check for mobile-unfriendly elements
        flash = self.soup.find_all(['embed', 'object'], type='application/x-shockwave-flash')
        if flash:
            self.results['high_priority'].append({
                'category': 'Mobile Optimization',
                'issue': f"Flash content detected ({len(flash)} elements)",
                'severity': 'HIGH',
                'impact': 'Flash is not supported on mobile devices',
                'recommendation': 'Replace Flash with HTML5/CSS3'
            })
    
    def check_https_security(self):
        """Check HTTPS and security headers"""
        if not self.url.startswith('https://'):
            self.results['critical_issues'].append({
                'category': 'Security & Trust',
                'issue': "Site not using HTTPS",
                'severity': 'CRITICAL',
                'impact': 'Major ranking factor. Chrome marks HTTP as "Not Secure"',
                'how_to_fix': [
                    'Purchase SSL certificate',
                    'Install certificate on server',
                    'Update all internal links to https://',
                    'Set up 301 redirects from HTTP to HTTPS',
                    'Update robots.txt and sitemap'
                ],
                'cost': 'Free SSL available via Let\'s Encrypt'
            })
        else:
            self.results['passed_checks'].append({
                'category': 'Security',
                'check': 'HTTPS',
                'status': 'Enabled'
            })
        
        # Check security headers
        headers = self.results['technical_data'].get('headers', {})
        
        security_headers = {
            'Strict-Transport-Security': 'HSTS',
            'X-Content-Type-Options': 'MIME sniffing protection',
            'X-Frame-Options': 'Clickjacking protection',
            'X-XSS-Protection': 'XSS protection',
            'Content-Security-Policy': 'CSP'
        }
        
        missing_headers = []
        for header, description in security_headers.items():
            if header not in headers:
                missing_headers.append(f"{header} ({description})")
        
        if missing_headers:
            self.results['low_priority'].append({
                'category': 'Security & Trust',
                'issue': f"Missing security headers: {len(missing_headers)}",
                'severity': 'LOW',
                'headers': missing_headers,
                'recommendation': 'Add security headers to improve security posture'
            })
    
    def check_canonical_url(self):
        """Check canonical URL implementation"""
        canonical = self.soup.find('link', rel='canonical')
        
        if not canonical:
            self.results['high_priority'].append({
                'category': 'Technical SEO',
                'issue': "Missing canonical URL",
                'severity': 'HIGH',
                'impact': 'Risk of duplicate content issues',
                'fix': f'<link rel="canonical" href="{self.url}">',
                'recommendation': 'Add canonical tag to specify preferred URL version'
            })
        else:
            canonical_url = canonical.get('href', '')
            self.results['passed_checks'].append({
                'category': 'Technical SEO',
                'check': 'Canonical URL',
                'status': 'Present',
                'value': canonical_url
            })
            
            # Check if canonical points to different domain
            if canonical_url and urlparse(canonical_url).netloc != self.domain:
                self.results['high_priority'].append({
                    'category': 'Technical SEO',
                    'issue': "Canonical points to different domain",
                    'severity': 'HIGH',
                    'canonical': canonical_url,
                    'recommendation': 'Verify this is intentional (e.g., for syndicated content)'
                })
    
    def check_robots_meta(self):
        """Check robots meta tags"""
        robots_meta = self.soup.find('meta', attrs={'name': 'robots'})
        
        if robots_meta:
            content = robots_meta.get('content', '').lower()
            
            # Check for noindex
            if 'noindex' in content:
                self.results['critical_issues'].append({
                    'category': 'Technical SEO',
                    'issue': "Page is set to NOINDEX",
                    'severity': 'CRITICAL',
                    'current': f'<meta name="robots" content="{content}">',
                    'impact': 'Page will not be indexed by search engines',
                    'fix': 'Remove noindex directive or change to <meta name="robots" content="index, follow">'
                })
            
            # Check for nofollow
            if 'nofollow' in content:
                self.results['high_priority'].append({
                    'category': 'Technical SEO',
                    'issue': "Page is set to NOFOLLOW",
                    'severity': 'HIGH',
                    'impact': 'Search engines will not follow links on this page',
                    'recommendation': 'Remove nofollow unless intentional'
                })
        else:
            self.results['passed_checks'].append({
                'category': 'Technical SEO',
                'check': 'Robots Meta',
                'status': 'Not blocking (default index, follow)'
            })
    
    def analyze_content_quality(self):
        """Comprehensive content analysis"""
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
        
        # Word count
        words = text.split()
        word_count = len(words)
        
        # Sentence count
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len([s for s in sentences if s.strip()])
        
        # Average words per sentence
        avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
        
        # Paragraph count
        paragraphs = self.soup.find_all('p')
        paragraph_count = len(paragraphs)
        
        # Store content data
        self.results['content_data'].update({
            'word_count': word_count,
            'sentence_count': sentence_count,
            'paragraph_count': paragraph_count,
            'avg_words_per_sentence': round(avg_words_per_sentence, 1),
            'avg_words_per_paragraph': round(word_count / paragraph_count, 1) if paragraph_count > 0 else 0
        })
        
        # Word count analysis
        if word_count < 300:
            self.results['high_priority'].append({
                'category': 'Content Quality',
                'issue': f"Thin content ({word_count} words)",
                'severity': 'HIGH',
                'impact': 'Insufficient content for good rankings',
                'recommendation': f'Add {300 - word_count} more words. Target: 500-1000+ words',
                'suggestions': [
                    'Add detailed explanations',
                    'Include examples and case studies',
                    'Add FAQs',
                    'Include related topics',
                    'Add expert insights'
                ]
            })
        elif word_count >= 1000:
            self.results['passed_checks'].append({
                'category': 'Content Quality',
                'check': 'Word Count',
                'status': f'Excellent ({word_count} words)'
            })
        else:
            self.results['passed_checks'].append({
                'category': 'Content Quality',
                'check': 'Word Count',
                'status': f'Good ({word_count} words)'
            })
        
        # Readability check
        if avg_words_per_sentence > 25:
            self.results['medium_priority'].append({
                'category': 'Content Quality',
                'issue': f"Long sentences (avg {avg_words_per_sentence:.1f} words)",
                'severity': 'MEDIUM',
                'recommendation': 'Break long sentences into shorter ones. Aim for 15-20 words per sentence.',
                'benefit': 'Improves readability and user experience'
            })
        
        # Check for paragraphs
        if paragraph_count == 0:
            self.results['high_priority'].append({
                'category': 'Content Quality',
                'issue': "No paragraph tags found",
                'severity': 'HIGH',
                'recommendation': 'Structure content with <p> tags for better readability'
            })
        
        # Keyword density analysis (simple version)
        # Find most common words (excluding stop words)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'their', 'them'}
        
        clean_words = [word.lower() for word in words if len(word) > 3 and word.lower() not in stop_words and word.isalpha()]
        
        if clean_words:
            word_freq = Counter(clean_words)
            top_keywords = word_freq.most_common(10)
            
            self.results['content_data']['top_keywords'] = [
                {'keyword': word, 'count': count, 'density': f"{(count/word_count*100):.2f}%"}
                for word, count in top_keywords
            ]
    
    def check_internal_linking(self):
        """Analyze internal linking structure"""
        links = self.soup.find_all('a', href=True)
        
        internal_links = []
        external_links = []
        broken_links = []
        
        for link in links:
            href = link.get('href', '')
            anchor_text = link.get_text().strip()
            
            # Skip empty or javascript links
            if not href or href.startswith(('javascript:', 'mailto:', 'tel:', '#')):
                continue
            
            # Resolve relative URLs
            full_url = urljoin(self.url, href)
            parsed = urlparse(full_url)
            
            # Classify link
            if parsed.netloc == self.domain or not parsed.netloc:
                internal_links.append({
                    'url': full_url,
                    'anchor': anchor_text[:50] if anchor_text else '[No anchor text]'
                })
            else:
                external_links.append({
                    'url': full_url,
                    'anchor': anchor_text[:50] if anchor_text else '[No anchor text]',
                    'nofollow': 'nofollow' in link.get('rel', [])
                })
        
        self.results['content_data']['internal_links'] = len(internal_links)
        self.results['content_data']['external_links'] = len(external_links)
        
        # Check internal linking
        if len(internal_links) == 0:
            self.results['high_priority'].append({
                'category': 'Internal Linking',
                'issue': "No internal links found",
                'severity': 'HIGH',
                'impact': 'Missing opportunity to distribute link equity and improve site structure',
                'recommendation': 'Add 3-5 relevant internal links to related content',
                'benefit': 'Helps search engines understand site structure and improves user navigation'
            })
        elif len(internal_links) < 3:
            self.results['medium_priority'].append({
                'category': 'Internal Linking',
                'issue': f"Few internal links ({len(internal_links)})",
                'severity': 'MEDIUM',
                'recommendation': 'Add more internal links to related pages (aim for 3-5 per page)'
            })
        else:
            self.results['passed_checks'].append({
                'category': 'Internal Linking',
                'check': 'Internal Links',
                'status': f'{len(internal_links)} internal links found'
            })
        
        # Check for external links with follow
        external_follow = [link for link in external_links if not link['nofollow']]
        if external_follow:
            self.results['passed_checks'].append({
                'category': 'External Linking',
                'check': 'External Links',
                'status': f'{len(external_links)} external links ({len(external_follow)} follow)'
            })
    
    def check_open_graph(self):
        """Check Open Graph and social media tags"""
        og_tags = {
            'og:title': self.soup.find('meta', property='og:title'),
            'og:description': self.soup.find('meta', property='og:description'),
            'og:image': self.soup.find('meta', property='og:image'),
            'og:url': self.soup.find('meta', property='og:url'),
            'og:type': self.soup.find('meta', property='og:type'),
        }
        
        twitter_tags = {
            'twitter:card': self.soup.find('meta', attrs={'name': 'twitter:card'}),
            'twitter:title': self.soup.find('meta', attrs={'name': 'twitter:title'}),
            'twitter:description': self.soup.find('meta', attrs={'name': 'twitter:description'}),
            'twitter:image': self.soup.find('meta', attrs={'name': 'twitter:image'}),
        }
        
        missing_og = [tag for tag, elem in og_tags.items() if not elem]
        missing_twitter = [tag for tag, elem in twitter_tags.items() if not elem]
        
        if missing_og:
            self.results['medium_priority'].append({
                'category': 'Social Media',
                'issue': f"Missing Open Graph tags: {', '.join(missing_og)}",
                'severity': 'MEDIUM',
                'impact': 'Reduced control over how page appears when shared on Facebook, LinkedIn',
                'fix_example': '''<meta property="og:title" content="Your Page Title">
<meta property="og:description" content="Your page description">
<meta property="og:image" content="https://yoursite.com/image.jpg">
<meta property="og:url" content="https://yoursite.com/page">''',
                'recommendation': 'Add Open Graph tags for better social sharing'
            })
        else:
            self.results['passed_checks'].append({
                'category': 'Social Media',
                'check': 'Open Graph Tags',
                'status': 'All essential tags present'
            })
        
        if missing_twitter:
            self.results['low_priority'].append({
                'category': 'Social Media',
                'issue': f"Missing Twitter Card tags: {', '.join(missing_twitter)}",
                'severity': 'LOW',
                'recommendation': 'Add Twitter Card tags for optimized Twitter sharing'
            })
    
    def check_page_performance(self):
        """Analyze page performance metrics"""
        if not self.response:
            return
        
        # Load time
        load_time = self.results['technical_data']['response_time']
        
        # Page size
        page_size_bytes = len(self.response.content)
        page_size_kb = page_size_bytes / 1024
        page_size_mb = page_size_kb / 1024
        
        self.results['performance_data'].update({
            'load_time': round(load_time, 2),
            'page_size_kb': round(page_size_kb, 2),
            'page_size_mb': round(page_size_mb, 2)
        })
        
        # Check load time
        if load_time > 3:
            self.results['high_priority'].append({
                'category': 'Performance',
                'issue': f"Slow page load time ({load_time:.2f} seconds)",
                'severity': 'HIGH',
                'impact': 'Slow pages negatively impact rankings and user experience',
                'target': '< 3 seconds',
                'recommendations': [
                    'Compress images (use WebP)',
                    'Minify CSS and JavaScript',
                    'Enable browser caching',
                    'Use a CDN',
                    'Enable GZIP compression',
                    'Reduce server response time',
                    'Defer non-critical JavaScript'
                ],
                'tools': ['Google PageSpeed Insights', 'GTmetrix', 'WebPageTest']
            })
        elif load_time > 2:
            self.results['medium_priority'].append({
                'category': 'Performance',
                'issue': f"Page load time could be improved ({load_time:.2f} seconds)",
                'severity': 'MEDIUM',
                'target': '< 2 seconds for optimal experience'
            })
        else:
            self.results['passed_checks'].append({
                'category': 'Performance',
                'check': 'Page Load Time',
                'status': f'Excellent ({load_time:.2f}s)'
            })
        
        # Check page size
        if page_size_mb > 2:
            self.results['high_priority'].append({
                'category': 'Performance',
                'issue': f"Large page size ({page_size_mb:.2f} MB)",
                'severity': 'HIGH',
                'target': '< 2 MB',
                'recommendations': [
                    'Compress images',
                    'Remove unused CSS/JS',
                    'Lazy load images',
                    'Minify code'
                ]
            })
        elif page_size_kb > 1024:
            self.results['medium_priority'].append({
                'category': 'Performance',
                'issue': f"Page size could be optimized ({page_size_kb:.0f} KB)",
                'severity': 'MEDIUM',
                'target': '< 1 MB'
            })
        else:
            self.results['passed_checks'].append({
                'category': 'Performance',
                'check': 'Page Size',
                'status': f'Good ({page_size_kb:.0f} KB)'
            })
        
        # Check compression
        headers = self.results['technical_data']['headers']
        if 'Content-Encoding' not in headers:
            self.results['medium_priority'].append({
                'category': 'Performance',
                'issue': "GZIP compression not enabled",
                'severity': 'MEDIUM',
                'benefit': 'Can reduce page size by 50-70%',
                'recommendation': 'Enable GZIP compression on your server'
            })
    
    def check_redirects(self):
        """Check for redirects"""
        redirect_count = self.results['technical_data']['redirects']
        
        if redirect_count > 0:
            self.results['medium_priority'].append({
                'category': 'Technical SEO',
                'issue': f"{redirect_count} redirect(s) detected",
                'severity': 'MEDIUM',
                'impact': 'Redirects slow down page load and can dilute link equity',
                'recommendation': 'Minimize redirects. Use direct links when possible.'
            })
        else:
            self.results['passed_checks'].append({
                'category': 'Technical SEO',
                'check': 'Redirects',
                'status': 'No redirects (good)'
            })
    
    def generate_insights(self):
        """Generate AI-powered insights and recommendations"""
        insights = []
        
        # Overall health insight
        critical_count = len(self.results['critical_issues'])
        high_count = len(self.results['high_priority'])
        
        if critical_count > 0:
            insights.append({
                'type': 'critical',
                'title': '🚨 Critical Issues Require Immediate Attention',
                'message': f'Found {critical_count} critical issue(s) that are severely impacting your SEO performance. Address these first.',
                'action': 'Start with the Critical Issues tab'
            })
        
        if high_count > 3:
            insights.append({
                'type': 'warning',
                'title': '⚠️ Multiple High-Priority Issues Detected',
                'message': f'You have {high_count} high-priority issues. Fixing these will significantly improve your SEO.',
                'action': 'Review High Priority tab'
            })
        
        # Content insights
        word_count = self.results['content_data'].get('word_count', 0)
        if word_count < 300:
            insights.append({
                'type': 'suggestion',
                'title': '📝 Content Length Opportunity',
                'message': f'Your page has only {word_count} words. Pages with 1000+ words tend to rank better.',
                'action': 'Add comprehensive content covering user questions'
            })
        
        # Technical insights
        if not any('HTTPS' in str(check) for check in self.results['passed_checks']):
            insights.append({
                'type': 'critical',
                'title': '🔒 Security Alert',
                'message': 'Your site is not using HTTPS. This is a major ranking factor and security concern.',
                'action': 'Obtain and install SSL certificate immediately'
            })
        
        # Mobile insights
        if not any('Viewport' in str(check) for check in self.results['passed_checks']):
            insights.append({
                'type': 'critical',
                'title': '📱 Mobile Optimization Missing',
                'message': 'Page is not optimized for mobile devices. Mobile-first indexing makes this critical.',
                'action': 'Add viewport meta tag and ensure responsive design'
            })
        
        # Performance insights
        load_time = self.results['performance_data'].get('load_time', 0)
        if load_time > 3:
            insights.append({
                'type': 'warning',
                'title': '⚡ Performance Optimization Needed',
                'message': f'Page loads in {load_time:.1f}s. Users expect < 3 seconds. Slow sites lose visitors and rankings.',
                'action': 'Optimize images, enable caching, use CDN'
            })
        
        self.results['insights'] = insights
    
    def generate_action_plan(self):
        """Generate prioritized action plan"""
        action_plan = []
        
        # Critical issues first
        if self.results['critical_issues']:
            action_plan.append({
                'priority': 1,
                'phase': 'Immediate (This Week)',
                'title': '🔥 Fix Critical Issues',
                'tasks': [issue['issue'] for issue in self.results['critical_issues'][:5]],
                'impact': 'High',
                'effort': 'Medium',
                'roi': '⭐⭐⭐⭐⭐'
            })
        
        # High priority
        if self.results['high_priority']:
            action_plan.append({
                'priority': 2,
                'phase': 'Short Term (This Month)',
                'title': '⚠️ Address High Priority Items',
                'tasks': [issue['issue'] for issue in self.results['high_priority'][:5]],
                'impact': 'Medium-High',
                'effort': 'Medium',
                'roi': '⭐⭐⭐⭐'
            })
        
        # Medium priority
        if self.results['medium_priority']:
            action_plan.append({
                'priority': 3,
                'phase': 'Medium Term (Next 2-3 Months)',
                'title': '📋 Improve Medium Priority Areas',
                'tasks': [issue['issue'] for issue in self.results['medium_priority'][:5]],
                'impact': 'Medium',
                'effort': 'Low-Medium',
                'roi': '⭐⭐⭐'
            })
        
        # Content optimization
        action_plan.append({
            'priority': 4,
            'phase': 'Ongoing',
            'title': '✍️ Content Optimization',
            'tasks': [
                'Expand content to 1000+ words',
                'Add relevant keywords naturally',
                'Improve readability',
                'Add more internal links',
                'Update content regularly'
            ],
            'impact': 'High (Long-term)',
            'effort': 'High',
            'roi': '⭐⭐⭐⭐'
        })
        
        self.results['action_plan'] = action_plan
    
    def calculate_scores(self):
        """Calculate overall and category scores"""
        total_checks = (
            len(self.results['critical_issues']) +
            len(self.results['high_priority']) +
            len(self.results['medium_priority']) +
            len(self.results['low_priority']) +
            len(self.results['passed_checks'])
        )
        
        if total_checks > 0:
            # Weight different priorities
            passed_score = len(self.results['passed_checks']) * 1.0
            low_penalty = len(self.results['low_priority']) * 0.1
            medium_penalty = len(self.results['medium_priority']) * 0.3
            high_penalty = len(self.results['high_priority']) * 0.6
            critical_penalty = len(self.results['critical_issues']) * 1.0
            
            total_possible = total_checks
            total_achieved = passed_score - (low_penalty + medium_penalty + high_penalty + critical_penalty)
            
            score = max(0, int((total_achieved / total_possible) * 100))
            self.results['overall_score'] = score
        
        # Category scores
        categories = ['Technical SEO', 'Content Quality', 'Performance', 'Mobile Optimization', 'Security']
        
        for category in categories:
            category_passed = len([c for c in self.results['passed_checks'] if c.get('category') == category])
            category_issues = (
                len([i for i in self.results['critical_issues'] if i.get('category') == category]) +
                len([i for i in self.results['high_priority'] if i.get('category') == category]) +
                len([i for i in self.results['medium_priority'] if i.get('category') == category])
            )
            
            total = category_passed + category_issues
            if total > 0:
                self.results['category_scores'][category] = int((category_passed / total) * 100)
            else:
                self.results['category_scores'][category] = 100
    
    def run_comprehensive_audit(self):
        """Run all audit checks"""
        if not self.fetch_page():
            return self.results
        
        with st.spinner('🔍 Analyzing page structure...'):
            self.check_title_tag()
            self.check_meta_description()
            self.check_headings_structure()
            time.sleep(0.1)
        
        with st.spinner('🖼️ Checking images and media...'):
            self.check_images_optimization()
            time.sleep(0.1)
        
        with st.spinner('🔧 Performing technical checks...'):
            self.check_schema_markup()
            self.check_mobile_optimization()
            self.check_https_security()
            self.check_canonical_url()
            self.check_robots_meta()
            time.sleep(0.1)
        
        with st.spinner('📝 Analyzing content quality...'):
            self.analyze_content_quality()
            self.check_internal_linking()
            time.sleep(0.1)
        
        with st.spinner('🌐 Checking social and metadata...'):
            self.check_open_graph()
            time.sleep(0.1)
        
        with st.spinner('⚡ Measuring performance...'):
            self.check_page_performance()
            self.check_redirects()
            time.sleep(0.1)
        
        with st.spinner('🤖 Generating AI insights...'):
            self.generate_insights()
            self.generate_action_plan()
            self.calculate_scores()
        
        return self.results

# ==================== UI COMPONENTS ====================

def render_score_card(score):
    """Render main score card"""
    if score >= 80:
        score_class = "score-excellent"
        status = "EXCELLENT"
        emoji = "🎉"
        message = "Your SEO is in great shape!"
    elif score >= 60:
        score_class = "score-good"
        status = "GOOD"
        emoji = "👍"
        message = "Solid foundation, some improvements possible"
    elif score >= 40:
        score_class = "score-poor"
        status = "NEEDS WORK"
        emoji = "⚠️"
        message = "Several issues need attention"
    else:
        score_class = "score-poor"
        status = "CRITICAL"
        emoji = "🚨"
        message = "Immediate action required"
    
    st.markdown(f"""
    <div class="score-card {score_class}">
        <h1 style="margin: 0; font-size: 5rem;">{emoji}</h1>
        <h2 style="margin: 0.5rem 0; font-size: 3rem;">{score}/100</h2>
        <p style="margin: 0; font-size: 1.5rem; font-weight: bold;">{status}</p>
        <p style="margin: 0.5rem 0; font-size: 1rem; opacity: 0.9;">{message}</p>
    </div>
    """, unsafe_allow_html=True)

def render_category_scores(category_scores):
    """Render category breakdown"""
    st.markdown("### 📊 Category Breakdown")
    
    cols = st.columns(len(category_scores))
    
    for idx, (category, score) in enumerate(category_scores.items()):
        with cols[idx]:
            # Determine color
            if score >= 80:
                color = "#28a745"
            elif score >= 60:
                color = "#ffc107"
            else:
                color = "#dc3545"
            
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: white; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h3 style="margin: 0; color: {color}; font-size: 2rem;">{score}</h3>
                <p style="margin: 0.5rem 0; font-size: 0.9rem; color: #666;">{category}</p>
            </div>
            """, unsafe_allow_html=True)

def render_insights(insights):
    """Render AI insights"""
    st.markdown("### 🤖 AI-Powered Insights")
    
    for insight in insights:
        if insight['type'] == 'critical':
            icon = "🚨"
            color = "#dc3545"
        elif insight['type'] == 'warning':
            icon = "⚠️"
            color = "#ffc107"
        else:
            icon = "💡"
            color = "#17a2b8"
        
        st.markdown(f"""
        <div class="insight-box" style="border-color: {color};">
            <h4 style="margin: 0 0 0.5rem 0; color: {color};">{icon} {insight['title']}</h4>
            <p style="margin: 0 0 0.5rem 0;">{insight['message']}</p>
            <p style="margin: 0; font-weight: bold; color: {color};">→ {insight['action']}</p>
        </div>
        """, unsafe_allow_html=True)

def render_action_plan(action_plan):
    """Render prioritized action plan"""
    st.markdown("### 🎯 Your Prioritized Action Plan")
    
    for phase in action_plan:
        with st.expander(f"**{phase['phase']}** - {phase['title']}", expanded=(phase['priority'] == 1)):
            st.markdown(f"**Impact:** {phase['impact']} | **Effort:** {phase['effort']} | **ROI:** {phase['roi']}")
            st.markdown("**Tasks:**")
            for task in phase['tasks']:
                st.markdown(f"- {task}")

def render_issue_detailed(issue, key_prefix):
    """Render detailed issue with all information"""
    with st.expander(f"{issue['severity']}: {issue['issue']}", expanded=False):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"**📍 Category:** {issue.get('category', 'General')}")
            
            severity = issue['severity']
            if severity == 'CRITICAL':
                badge_class = 'priority-critical'
            elif severity == 'HIGH':
                badge_class = 'priority-high'
            elif severity == 'MEDIUM':
                badge_class = 'priority-medium'
            else:
                badge_class = 'priority-low'
            
            st.markdown(f'<span class="priority-badge {badge_class}">{severity} PRIORITY</span>', unsafe_allow_html=True)
            
            if issue.get('current'):
                st.markdown("**❌ Current:**")
                if isinstance(issue['current'], list):
                    for item in issue['current'][:3]:
                        st.code(str(item)[:200], language='html')
                else:
                    st.code(str(issue['current'])[:300], language='html')
        
        with col2:
            if issue.get('fix'):
                st.markdown("**✅ Fix:**")
                st.code(issue['fix'][:300], language='html')
                
                if st.button(f"📋 Copy Fix", key=f"{key_prefix}_copy_{hash(issue['issue'])}"):
                    st.success("✅ Copied to clipboard!")
        
        if issue.get('impact'):
            st.info(f"**⚡ Impact:** {issue['impact']}")
        
        if issue.get('recommendation'):
            st.markdown(f"**💡 Recommendation:** {issue['recommendation']}")
        
        if issue.get('how_to_fix'):
            st.markdown("**📋 How to Fix:**")
            for step in issue['how_to_fix']:
                st.markdown(f"- {step}")
        
        if issue.get('example'):
            st.markdown("**📝 Example:**")
            st.code(issue['example'], language='html')
        
        if issue.get('best_practices'):
            st.markdown("**✨ Best Practices:**")
            for practice in issue['best_practices']:
                st.markdown(f"- {practice}")

# ==================== MAIN APP ====================

def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 Advanced SEO Intelligence Platform</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.1rem;">Comprehensive SEO audit with AI-powered insights and actionable fixes</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚡ Features")
        st.success("""
        - **50+ SEO Checks**
        - **AI-Powered Insights**
        - **Priority-Based Fixes**
        - **Technical Audit**
        - **Content Analysis**
        - **Performance Metrics**
        - **Action Plan**
        - **Ready-to-Use Code**
        """)
        
        st.markdown("---")
        st.markdown("### 📚 What We Check")
        st.info("""
        **Technical SEO:**
        - Title & Meta tags
        - Headings structure
        - Schema markup
        - Canonical URLs
        - Robots directives
        
        **Content Quality:**
        - Word count
        - Readability
        - Keyword usage
        - Internal linking
        
        **Performance:**
        - Load time
        - Page size
        - Compression
        
        **Mobile & Security:**
        - Viewport config
        - HTTPS status
        - Security headers
        """)
        
        st.markdown("---")
        st.markdown("### 🎯 How to Use")
        st.markdown("""
        1. Enter URL
        2. Click Analyze
        3. Review score & insights
        4. Follow action plan
        5. Copy & implement fixes
        6. Re-audit to verify
        """)
    
    # Main input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        url_input = st.text_input(
            "🔍 Enter URL to Audit",
            placeholder="https://yourwebsite.com",
            help="Enter the full URL including https://"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_button = st.button("🚀 Run Complete Audit", type="primary", use_container_width=True)
    
    # Example URLs
    st.markdown("**Quick Test:**")
    example_cols = st.columns(4)
    with example_cols[0]:
        if st.button("🌍 Omo Valley", use_container_width=True):
            url_input = "https://omovalleytours.travel"
            analyze_button = True
    with example_cols[1]:
        if st.button("📰 BBC", use_container_width=True):
            url_input = "https://bbc.com"
            analyze_button = True
    with example_cols[2]:
        if st.button("🛍️ Amazon", use_container_width=True):
            url_input = "https://amazon.com"
            analyze_button = True
    with example_cols[3]:
        if st.button("🔍 Google", use_container_width=True):
            url_input = "https://google.com"
            analyze_button = True
    
    # Run audit
    if analyze_button and url_input:
        if not url_input.startswith(('http://', 'https://')):
            url_input = 'https://' + url_input
        
        # Create auditor and run
        auditor = AdvancedSEOAuditor(url_input)
        results = auditor.run_comprehensive_audit()
        
        st.markdown("---")
        st.markdown("## 📊 Audit Results")
        
        # Score card
        render_score_card(results['overall_score'])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🚨 Critical", len(results['critical_issues']), delta="Fix Now", delta_color="inverse")
        with col2:
            st.metric("⚠️ High Priority", len(results['high_priority']), delta="Important", delta_color="inverse")
        with col3:
            st.metric("📋 Medium", len(results['medium_priority']), delta="Soon")
        with col4:
            st.metric("✅ Passed", len(results['passed_checks']), delta="Good")
        
        st.markdown("---")
        
        # Category scores
        if results['category_scores']:
            render_category_scores(results['category_scores'])
            st.markdown("---")
        
        # AI Insights
        if results['insights']:
            render_insights(results['insights'])
            st.markdown("---")
        
        # Tabs for detailed results
        tabs = st.tabs([
            "🚨 Critical Issues",
            "⚠️ High Priority",
            "📋 Medium Priority",
            "💡 Low Priority",
            "✅ Passed Checks",
            "🎯 Action Plan",
            "📊 Data & Metrics",
            "📄 Export Report"
        ])
        
        # Critical Issues Tab
        with tabs[0]:
            if results['critical_issues']:
                st.error(f"**Found {len(results['critical_issues'])} critical issue(s). Fix these immediately!**")
                for idx, issue in enumerate(results['critical_issues']):
                    render_issue_detailed(issue, f"critical_{idx}")
            else:
                st.success("🎉 No critical issues found! Excellent!")
        
        # High Priority Tab
        with tabs[1]:
            if results['high_priority']:
                st.warning(f"**Found {len(results['high_priority'])} high priority issue(s).**")
                for idx, issue in enumerate(results['high_priority']):
                    render_issue_detailed(issue, f"high_{idx}")
            else:
                st.success("✅ No high priority issues!")
        
        # Medium Priority Tab
        with tabs[2]:
            if results['medium_priority']:
                st.info(f"**Found {len(results['medium_priority'])} medium priority issue(s).**")
                for idx, issue in enumerate(results['medium_priority']):
                    render_issue_detailed(issue, f"medium_{idx}")
            else:
                st.success("✅ No medium priority issues!")
        
        # Low Priority Tab
        with tabs[3]:
            if results['low_priority']:
                st.info(f"**Found {len(results['low_priority'])} low priority item(s).**")
                for idx, issue in enumerate(results['low_priority']):
                    render_issue_detailed(issue, f"low_{idx}")
            else:
                st.success("✅ No low priority issues!")
        
        # Passed Checks Tab
        with tabs[4]:
            st.success(f"**{len(results['passed_checks'])} checks passed!**")
            
            # Group by category
            categories = {}
            for check in results['passed_checks']:
                cat = check.get('category', 'General')
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(check)
            
            for category, checks in categories.items():
                with st.expander(f"✅ {category} ({len(checks)} passed)", expanded=False):
                    for check in checks:
                        st.markdown(f"- **{check['check']}**: {check['status']}")
                        if check.get('value'):
                            st.caption(f"  Value: {check['value'][:100]}")
        
        # Action Plan Tab
        with tabs[5]:
            if results['action_plan']:
                render_action_plan(results['action_plan'])
            else:
                st.info("Action plan will be generated based on issues found.")
        
        # Data & Metrics Tab
        with tabs[6]:
            st.markdown("### 📊 Technical Data")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Performance Metrics**")
                perf_data = results['performance_data']
                st.metric("Load Time", f"{perf_data.get('load_time', 0):.2f}s")
                st.metric("Page Size", f"{perf_data.get('page_size_kb', 0):.0f} KB")
                
                st.markdown("**Technical Info**")
                tech_data = results['technical_data']
                st.metric("Status Code", tech_data.get('status_code', 'N/A'))
                st.metric("Redirects", tech_data.get('redirects', 0))
            
            with col2:
                st.markdown("**Content Metrics**")
                content_data = results['content_data']
                st.metric("Word Count", content_data.get('word_count', 0))
                st.metric("Paragraphs", content_data.get('paragraph_count', 0))
                st.metric("Images", content_data.get('total_images', 0))
                st.metric("Internal Links", content_data.get('internal_links', 0))
            
            # Top Keywords
            if content_data.get('top_keywords'):
                st.markdown("### 🔑 Top Keywords Found")
                kw_df = pd.DataFrame(content_data['top_keywords'])
                st.dataframe(kw_df, use_container_width=True)
            
            # Schema Markup
            if results['technical_data'].get('schemas'):
                st.markdown("### 📋 Schema Markup Found")
                for schema in results['technical_data']['schemas']:
                    st.success(f"✅ {schema}")
        
        # Export Tab
        with tabs[7]:
            st.markdown("### 📥 Export Your Audit Report")
            
            # Create summary
            summary_data = {
                'URL': [results['url']],
                'Audit Date': [results['timestamp']],
                'Overall Score': [results['overall_score']],
                'Critical Issues': [len(results['critical_issues'])],
                'High Priority': [len(results['high_priority'])],
                'Medium Priority': [len(results['medium_priority'])],
                'Low Priority': [len(results['low_priority'])],
                'Passed Checks': [len(results['passed_checks'])],
                'Word Count': [results['content_data'].get('word_count', 0)],
                'Images': [results['content_data'].get('total_images', 0)],
                'Load Time (s)': [results['performance_data'].get('load_time', 0)],
                'Page Size (KB)': [results['performance_data'].get('page_size_kb', 0)]
            }
            
            df = pd.DataFrame(summary_data)
            
            st.dataframe(df, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV Summary",
                    data=csv,
                    file_name=f"seo_audit_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                # Create detailed report
                report = f"""
SEO AUDIT REPORT - ADVANCED ANALYSIS
{'='*80}

URL: {results['url']}
Audit Date: {results['timestamp']}
Overall Score: {results['overall_score']}/100

SUMMARY:
- Critical Issues: {len(results['critical_issues'])}
- High Priority: {len(results['high_priority'])}
- Medium Priority: {len(results['medium_priority'])}
- Low Priority: {len(results['low_priority'])}
- Passed Checks: {len(results['passed_checks'])}

CRITICAL ISSUES ({len(results['critical_issues'])}):
{chr(10).join([f"- {issue['issue']}" for issue in results['critical_issues']])}

HIGH PRIORITY ({len(results['high_priority'])}):
{chr(10).join([f"- {issue['issue']}" for issue in results['high_priority']])}

MEDIUM PRIORITY ({len(results['medium_priority'])}):
{chr(10).join([f"- {issue['issue']}" for issue in results['medium_priority']])}

CONTENT METRICS:
- Word Count: {results['content_data'].get('word_count', 0)}
- Paragraphs: {results['content_data'].get('paragraph_count', 0)}
- Images: {results['content_data'].get('total_images', 0)}
- Internal Links: {results['content_data'].get('internal_links', 0)}

PERFORMANCE:
- Load Time: {results['performance_data'].get('load_time', 0):.2f} seconds
- Page Size: {results['performance_data'].get('page_size_kb', 0):.0f} KB

ACTION PLAN:
{chr(10).join([f"{i+1}. {phase['title']} ({phase['phase']})" for i, phase in enumerate(results['action_plan'])])}

{'='*80}
Generated by Advanced SEO Intelligence Platform
                """
                
                st.download_button(
                    label="📄 Download Full Report",
                    data=report,
                    file_name=f"seo_audit_full_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    elif analyze_button:
        st.warning("⚠️ Please enter a URL to analyze")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p><strong>Advanced SEO Intelligence Platform MVP</strong></p>
        <p>Comprehensive auditing • AI-powered insights • Actionable fixes</p>
        <p style="font-size: 0.9rem; margin-top: 1rem;">
            Made with ❤️ using Streamlit | Version 2.0
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
