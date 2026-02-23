#!/usr/bin/env python3
"""
SEO Audit Tool - Streamlit Web App with Actionable Fixes
Professional SEO analysis with code snippets and quick fixes
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd
from collections import Counter
import time
from datetime import datetime
import warnings
import html
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="SEO Audit Tool",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
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
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .issue-critical {
        color: #dc3545;
        font-weight: bold;
    }
    .issue-warning {
        color: #ffc107;
        font-weight: bold;
    }
    .issue-passed {
        color: #28a745;
        font-weight: bold;
    }
    .code-snippet {
        background: #f4f4f4;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        font-family: monospace;
        font-size: 0.9rem;
        margin: 0.5rem 0;
        border-radius: 4px;
        overflow-x: auto;
    }
    .fix-snippet {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        font-family: monospace;
        font-size: 0.9rem;
        margin: 0.5rem 0;
        border-radius: 4px;
        overflow-x: auto;
    }
    .location-badge {
        background: #007bff;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.85rem;
        display: inline-block;
        margin: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

class SEOAuditor:
    def __init__(self, url):
        self.url = url
        self.domain = urlparse(url).netloc
        self.soup = None
        self.response = None
        self.html_content = ""
        self.results = {
            'url': url,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'score': 0,
            'issues': [],
            'warnings': [],
            'passed': []
        }
        
    def fetch_page(self):
        """Fetch the webpage"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            self.response = requests.get(self.url, headers=headers, timeout=10, verify=False)
            self.html_content = self.response.text
            self.soup = BeautifulSoup(self.response.content, 'html.parser')
            return True
        except Exception as e:
            st.error(f"❌ Failed to fetch page: {str(e)}")
            return False
    
    def get_html_snippet(self, element, context_lines=2):
        """Get HTML snippet with context"""
        if not element:
            return None
        
        # Get the element as string
        element_html = str(element)
        # Truncate if too long
        if len(element_html) > 500:
            element_html = element_html[:500] + "..."
        return element_html
    
    def find_in_source(self, search_text):
        """Find line number in source"""
        lines = self.html_content.split('\n')
        for i, line in enumerate(lines, 1):
            if search_text in line:
                return i
        return None
    
    def check_title_tag(self):
        """Check title tag optimization"""
        title = self.soup.find('title')
        
        if not title:
            self.results['issues'].append({
                'type': 'critical',
                'message': "Missing <title> tag",
                'location': '<head>',
                'current': None,
                'fix': '<title>Your Page Title Here - Brand Name</title>',
                'recommendation': 'Add a descriptive title tag in the <head> section. Keep it between 50-60 characters.',
                'example': '<title>Omo Valley Cultural Tours - Experience Ethiopia | Your Brand</title>',
                'priority': 'HIGH',
                'impact': 'Critical for SEO - Title tags are one of the most important on-page SEO elements'
            })
            return
        
        title_text = title.get_text().strip()
        title_length = len(title_text)
        line_number = self.find_in_source('<title>')
        
        if not title_text:
            self.results['issues'].append({
                'type': 'critical',
                'message': "Empty <title> tag",
                'location': f'<head> (Line {line_number})' if line_number else '<head>',
                'current': '<title></title>',
                'fix': '<title>Your Page Title Here - Brand Name</title>',
                'recommendation': 'Add descriptive text to your title tag',
                'priority': 'HIGH'
            })
        elif title_length < 30:
            self.results['warnings'].append({
                'type': 'warning',
                'message': f"Title too short ({title_length} characters)",
                'location': f'<head> (Line {line_number})' if line_number else '<head>',
                'current': f'<title>{title_text}</title>',
                'fix': f'<title>{title_text} - Add More Descriptive Keywords Here</title>',
                'recommendation': 'Extend your title to 50-60 characters for better SEO. Include primary keywords.',
                'example': 'If current is "Tours", make it "Omo Valley Cultural Tours - Experience Ethiopia"',
                'priority': 'MEDIUM'
            })
        elif title_length > 60:
            suggested_title = title_text[:57] + "..."
            self.results['warnings'].append({
                'type': 'warning',
                'message': f"Title too long ({title_length} characters). May be truncated in search results",
                'location': f'<head> (Line {line_number})' if line_number else '<head>',
                'current': f'<title>{title_text}</title>',
                'fix': f'<title>{suggested_title}</title>',
                'recommendation': 'Shorten your title to 50-60 characters. Google typically displays the first 50-60 characters.',
                'priority': 'MEDIUM'
            })
        else:
            self.results['passed'].append({
                'type': 'passed',
                'message': f"Title length optimal ({title_length} characters)",
                'details': title_text,
                'location': f'Line {line_number}' if line_number else 'N/A'
            })
    
    def check_meta_description(self):
        """Check meta description"""
        meta_desc = self.soup.find('meta', attrs={'name': 'description'})
        
        if not meta_desc:
            self.results['issues'].append({
                'type': 'critical',
                'message': "Missing meta description",
                'location': '<head>',
                'current': None,
                'fix': '<meta name="description" content="Write a compelling description of your page here (150-160 characters)">',
                'recommendation': 'Add a meta description tag in the <head> section. This appears in search results and influences click-through rates.',
                'example': '<meta name="description" content="Explore authentic Omo Valley cultural tours. Experience traditional tribes, local customs, and breathtaking landscapes in Southern Ethiopia. Book your adventure today!">',
                'priority': 'HIGH',
                'impact': 'High - Meta descriptions directly impact click-through rates from search results'
            })
            return
        
        desc_text = meta_desc.get('content', '').strip()
        desc_length = len(desc_text)
        meta_html = str(meta_desc)
        line_number = self.find_in_source('meta name="description"')
        
        if not desc_text:
            self.results['issues'].append({
                'type': 'critical',
                'message': "Empty meta description",
                'location': f'<head> (Line {line_number})' if line_number else '<head>',
                'current': meta_html,
                'fix': '<meta name="description" content="Write your compelling description here">',
                'recommendation': 'Add descriptive content that summarizes the page',
                'priority': 'HIGH'
            })
        elif desc_length < 120:
            self.results['warnings'].append({
                'type': 'warning',
                'message': f"Meta description too short ({desc_length} characters)",
                'location': f'<head> (Line {line_number})' if line_number else '<head>',
                'current': meta_html,
                'fix': f'<meta name="description" content="{desc_text} [Add 30-40 more characters with relevant keywords and call-to-action]">',
                'recommendation': f'Expand to 150-160 characters (currently {desc_length}). Add more descriptive text and a call-to-action.',
                'priority': 'MEDIUM'
            })
        elif desc_length > 160:
            truncated = desc_text[:157] + "..."
            self.results['warnings'].append({
                'type': 'warning',
                'message': f"Meta description too long ({desc_length} characters)",
                'location': f'<head> (Line {line_number})' if line_number else '<head>',
                'current': meta_html,
                'fix': f'<meta name="description" content="{truncated}">',
                'recommendation': f'Shorten to 150-160 characters (currently {desc_length}). Google truncates longer descriptions.',
                'priority': 'MEDIUM'
            })
        else:
            self.results['passed'].append({
                'type': 'passed',
                'message': f"Meta description optimal ({desc_length} characters)",
                'details': desc_text[:100] + "..." if len(desc_text) > 100 else desc_text,
                'location': f'Line {line_number}' if line_number else 'N/A'
            })
    
    def check_headings(self):
        """Analyze heading structure"""
        h1_tags = self.soup.find_all('h1')
        
        if not h1_tags:
            self.results['issues'].append({
                'type': 'critical',
                'message': "Missing H1 tag",
                'location': '<body>',
                'current': None,
                'fix': '<h1>Your Main Page Heading Here</h1>',
                'recommendation': 'Add ONE H1 tag that describes the main topic of the page. Place it near the top of your content.',
                'example': '<h1>Omo Valley Cultural Tours - Authentic Ethiopian Experiences</h1>',
                'priority': 'HIGH',
                'impact': 'Critical - H1 tags help search engines understand the main topic of your page'
            })
        elif len(h1_tags) > 1:
            h1_list = []
            for i, h1 in enumerate(h1_tags, 1):
                h1_text = h1.get_text().strip()[:50]
                h1_html = self.get_html_snippet(h1)
                line_number = self.find_in_source(h1_text[:20]) if h1_text else None
                h1_list.append({
                    'number': i,
                    'text': h1_text,
                    'html': h1_html,
                    'line': line_number
                })
            
            self.results['warnings'].append({
                'type': 'warning',
                'message': f"Multiple H1 tags found ({len(h1_tags)})",
                'location': 'Throughout page',
                'current': h1_list,
                'fix': 'Keep only ONE H1 tag. Change others to H2, H3, etc.',
                'recommendation': f'You have {len(h1_tags)} H1 tags. Best practice is to have only ONE H1 per page. Convert the extra H1s to H2 or H3 tags.',
                'example': 'Change <h1>Secondary Heading</h1> to <h2>Secondary Heading</h2>',
                'priority': 'MEDIUM'
            })
        else:
            h1_text = h1_tags[0].get_text().strip()
            line_number = self.find_in_source(h1_text[:20]) if h1_text else None
            self.results['passed'].append({
                'type': 'passed',
                'message': f"H1 tag found: {h1_text[:50]}",
                'details': h1_text,
                'location': f'Line {line_number}' if line_number else 'N/A'
            })
        
        # Check heading hierarchy
        headings = []
        for i in range(1, 7):
            tags = self.soup.find_all(f'h{i}')
            if tags:
                headings.append(f"H{i}: {len(tags)}")
        
        if headings:
            self.results['passed'].append({
                'type': 'passed',
                'message': f"Heading structure: {', '.join(headings)}",
                'details': ', '.join(headings)
            })
    
    def check_images(self):
        """Check image optimization"""
        images = self.soup.find_all('img')
        
        if not images:
            self.results['warnings'].append({
                'type': 'warning',
                'message': "No images found on page",
                'recommendation': 'Consider adding relevant images to improve user engagement',
                'priority': 'LOW'
            })
            return
        
        missing_alt = []
        empty_alt = []
        
        for img in images:
            src = img.get('src', '')[:100]
            alt = img.get('alt')
            img_html = self.get_html_snippet(img)
            
            if alt is None:
                missing_alt.append({
                    'src': src,
                    'html': img_html,
                    'fix': str(img).replace('>', ' alt="Descriptive text here">')
                })
            elif not alt.strip():
                empty_alt.append({
                    'src': src,
                    'html': img_html,
                    'fix': str(img).replace('alt=""', 'alt="Descriptive text here"')
                })
        
        total_images = len(images)
        self.results['passed'].append({
            'type': 'passed',
            'message': f"Total images found: {total_images}",
            'details': f"{total_images} images"
        })
        
        if missing_alt:
            self.results['issues'].append({
                'type': 'critical',
                'message': f"{len(missing_alt)} image(s) missing alt attribute",
                'location': 'Throughout page',
                'images': missing_alt,
                'recommendation': 'Add descriptive alt text to all images for accessibility and SEO',
                'example': '<img src="tour.jpg" alt="Omo Valley cultural tour group visiting local village">',
                'priority': 'HIGH',
                'impact': 'Required for accessibility and helps search engines understand image content'
            })
        
        if empty_alt:
            self.results['warnings'].append({
                'type': 'warning',
                'message': f"{len(empty_alt)} image(s) with empty alt text",
                'location': 'Throughout page',
                'images': empty_alt,
                'recommendation': 'Replace empty alt="" with descriptive text',
                'priority': 'MEDIUM'
            })
        
        if not missing_alt and not empty_alt:
            self.results['passed'].append({
                'type': 'passed',
                'message': "All images have alt attributes",
                'details': f"All {total_images} images properly tagged"
            })
    
    def check_links(self):
        """Analyze internal and external links"""
        links = self.soup.find_all('a', href=True)
        
        internal_links = []
        external_links = []
        broken_links = []
        
        for link in links:
            href = link.get('href', '')
            link_text = link.get_text().strip()[:50]
            
            if href.startswith('#') or href.startswith('javascript:'):
                continue
            
            full_url = urljoin(self.url, href)
            parsed = urlparse(full_url)
            
            if parsed.netloc == self.domain or not parsed.netloc:
                internal_links.append(full_url)
            else:
                external_links.append(full_url)
                
            # Check for suspicious links
            if not href or href == '#':
                broken_links.append({
                    'text': link_text,
                    'html': str(link)[:100],
                    'issue': 'Empty or invalid href'
                })
        
        self.results['passed'].append({
            'type': 'passed',
            'message': f"Total links: {len(links)}",
            'details': f"{len(links)} total links"
        })
        self.results['passed'].append({
            'type': 'passed',
            'message': f"Internal links: {len(internal_links)}",
            'details': f"{len(internal_links)} internal links"
        })
        self.results['passed'].append({
            'type': 'passed',
            'message': f"External links: {len(external_links)}",
            'details': f"{len(external_links)} external links"
        })
        
        if len(links) > 100:
            self.results['warnings'].append({
                'type': 'warning',
                'message': f"High number of links ({len(links)})",
                'recommendation': 'Consider reducing the number of links. Too many links can dilute link equity and overwhelm users.',
                'priority': 'LOW'
            })
        
        if broken_links:
            self.results['warnings'].append({
                'type': 'warning',
                'message': f"{len(broken_links)} link(s) with issues",
                'links': broken_links,
                'recommendation': 'Fix or remove links with empty or invalid href attributes',
                'priority': 'MEDIUM'
            })
    
    def check_content(self):
        """Analyze page content"""
        # Remove script and style elements
        for script in self.soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        text = self.soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        word_count = len(text.split())
        
        self.results['passed'].append({
            'type': 'passed',
            'message': f"Word count: {word_count}",
            'details': f"{word_count} words"
        })
        
        if word_count < 300:
            self.results['warnings'].append({
                'type': 'warning',
                'message': f"Low word count ({word_count} words)",
                'recommendation': f'Add more content. Recommended: 300+ words (currently {word_count}). More content helps search engines understand your page topic.',
                'suggestion': 'Add detailed descriptions, benefits, features, FAQs, or customer testimonials',
                'priority': 'MEDIUM',
                'target': '500-1000 words for optimal SEO'
            })
        elif word_count > 2500:
            self.results['warnings'].append({
                'type': 'warning',
                'message': f"Very high word count ({word_count} words)",
                'recommendation': 'Consider breaking content into multiple pages or sections for better user experience',
                'priority': 'LOW'
            })
    
    def check_https(self):
        """Check HTTPS/SSL"""
        if self.url.startswith('https://'):
            self.results['passed'].append({
                'type': 'passed',
                'message': "Using HTTPS",
                'details': "Secure connection (SSL/TLS)"
            })
        else:
            self.results['issues'].append({
                'type': 'critical',
                'message': "Page not using HTTPS",
                'current': 'http://',
                'fix': 'https://',
                'recommendation': 'Enable HTTPS for your website. This is critical for security and SEO.',
                'steps': [
                    '1. Obtain SSL certificate from your hosting provider',
                    '2. Install certificate on your server',
                    '3. Update all internal links to use https://',
                    '4. Set up 301 redirects from HTTP to HTTPS'
                ],
                'priority': 'CRITICAL',
                'impact': 'Google prioritizes HTTPS sites. Chrome marks HTTP sites as "Not Secure"'
            })
    
    def check_page_speed(self):
        """Check basic page load metrics"""
        if self.response:
            load_time = self.response.elapsed.total_seconds()
            page_size = len(self.response.content) / 1024
            
            self.results['passed'].append({
                'type': 'passed',
                'message': f"Page load time: {load_time:.2f} seconds",
                'details': f"{load_time:.2f}s"
            })
            self.results['passed'].append({
                'type': 'passed',
                'message': f"Page size: {page_size:.2f} KB",
                'details': f"{page_size:.2f} KB"
            })
            
            if load_time > 3:
                self.results['warnings'].append({
                    'type': 'warning',
                    'message': f"Slow page load time ({load_time:.2f} seconds)",
                    'recommendation': 'Optimize page speed to under 3 seconds',
                    'suggestions': [
                        'Compress images (use WebP format)',
                        'Minify CSS and JavaScript',
                        'Enable browser caching',
                        'Use a CDN (Content Delivery Network)',
                        'Reduce server response time'
                    ],
                    'priority': 'HIGH',
                    'tools': ['Google PageSpeed Insights', 'GTmetrix', 'WebPageTest.org']
                })
            
            if page_size > 1024:
                self.results['warnings'].append({
                    'type': 'warning',
                    'message': f"Large page size ({page_size:.2f} KB)",
                    'recommendation': 'Reduce page size to improve load times',
                    'suggestions': [
                        'Compress images',
                        'Minify CSS/JS files',
                        'Remove unused code',
                        'Lazy load images'
                    ],
                    'priority': 'MEDIUM'
                })
    
    def check_mobile_viewport(self):
        """Check mobile viewport meta tag"""
        viewport = self.soup.find('meta', attrs={'name': 'viewport'})
        if not viewport:
            self.results['issues'].append({
                'type': 'critical',
                'message': "Missing viewport meta tag for mobile",
                'location': '<head>',
                'current': None,
                'fix': '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                'recommendation': 'Add viewport meta tag for mobile responsiveness',
                'priority': 'HIGH',
                'impact': 'Required for mobile-friendly designation in Google'
            })
        else:
            viewport_content = viewport.get('content', '')
            self.results['passed'].append({
                'type': 'passed',
                'message': "Viewport meta tag found",
                'details': viewport_content
            })
    
    def check_open_graph(self):
        """Check Open Graph tags"""
        og_tags = {
            'og:title': self.soup.find('meta', property='og:title'),
            'og:description': self.soup.find('meta', property='og:description'),
            'og:image': self.soup.find('meta', property='og:image'),
        }
        
        missing_og = [tag for tag, elem in og_tags.items() if not elem]
        
        if missing_og:
            self.results['warnings'].append({
                'type': 'warning',
                'message': f"Missing Open Graph tags: {', '.join(missing_og)}",
                'location': '<head>',
                'fix_example': '''<meta property="og:title" content="Your Page Title">
<meta property="og:description" content="Your page description">
<meta property="og:image" content="https://yoursite.com/image.jpg">
<meta property="og:url" content="https://yoursite.com/page">''',
                'recommendation': 'Add Open Graph tags for better social media sharing',
                'priority': 'LOW',
                'benefit': 'Controls how your page appears when shared on Facebook, LinkedIn, etc.'
            })
        else:
            self.results['passed'].append({
                'type': 'passed',
                'message': "All essential Open Graph tags present",
                'details': "og:title, og:description, og:image"
            })
    
    def run_audit(self):
        """Run complete SEO audit"""
        if not self.fetch_page():
            return self.results
        
        # Run all checks
        self.check_title_tag()
        self.check_meta_description()
        self.check_headings()
        self.check_images()
        self.check_links()
        self.check_content()
        self.check_https()
        self.check_page_speed()
        self.check_mobile_viewport()
        self.check_open_graph()
        
        # Calculate score
        total_checks = len(self.results['passed']) + len(self.results['warnings']) + len(self.results['issues'])
        if total_checks > 0:
            score = int((len(self.results['passed']) / total_checks) * 100)
            self.results['score'] = score
        
        return self.results

def render_issue_with_fix(issue, index):
    """Render an issue with code snippets and fixes"""
    with st.expander(f"❌ {issue['message']}", expanded=True):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**📍 Location:**")
            st.markdown(f"<span class='location-badge'>{issue.get('location', 'Unknown')}</span>", unsafe_allow_html=True)
            
            if issue.get('current'):
                st.markdown("**❌ Current Code:**")
                if isinstance(issue['current'], list):
                    for item in issue['current']:
                        st.code(item.get('html', item.get('text', '')), language='html')
                        if item.get('line'):
                            st.caption(f"Line {item['line']}")
                else:
                    st.code(issue['current'], language='html')
        
        with col2:
            if issue.get('fix'):
                st.markdown("**✅ Recommended Fix:**")
                st.code(issue['fix'], language='html')
                
                # Copy button
                if st.button(f"📋 Copy Fix", key=f"copy_fix_{index}"):
                    st.success("✅ Copied! Paste this into your HTML")
        
        st.markdown("**💡 How to Fix:**")
        st.info(issue.get('recommendation', 'Fix this issue'))
        
        if issue.get('example'):
            st.markdown("**📝 Example:**")
            st.code(issue['example'], language='html')
        
        if issue.get('steps'):
            st.markdown("**📋 Steps:**")
            for step in issue['steps']:
                st.markdown(f"- {step}")
        
        if issue.get('impact'):
            st.warning(f"**⚡ Impact:** {issue['impact']}")
        
        # Priority badge
        priority = issue.get('priority', 'MEDIUM')
        if priority == 'CRITICAL' or priority == 'HIGH':
            st.error(f"🔥 Priority: {priority}")
        elif priority == 'MEDIUM':
            st.warning(f"⚠️ Priority: {priority}")
        else:
            st.info(f"ℹ️ Priority: {priority}")
        
        # Images specific
        if issue.get('images'):
            st.markdown("**🖼️ Images needing alt text:**")
            for img_issue in issue['images'][:5]:  # Show first 5
                with st.container():
                    st.markdown(f"**Image:** `{img_issue['src']}`")
                    col_a, col_b = st.columns([1, 1])
                    with col_a:
                        st.code(img_issue['html'][:200], language='html')
                    with col_b:
                        st.code(img_issue['fix'][:200], language='html')
            if len(issue['images']) > 5:
                st.caption(f"...and {len(issue['images']) - 5} more images")

def render_warning_with_fix(warning, index):
    """Render a warning with fix suggestions"""
    with st.expander(f"⚠️ {warning['message']}", expanded=False):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if warning.get('location'):
                st.markdown("**📍 Location:**")
                st.markdown(f"<span class='location-badge'>{warning['location']}</span>", unsafe_allow_html=True)
            
            if warning.get('current'):
                st.markdown("**⚠️ Current:**")
                if isinstance(warning['current'], list):
                    for item in warning['current']:
                        st.code(item.get('html', item.get('text', ''))[:200], language='html')
                else:
                    st.code(warning['current'][:200], language='html')
        
        with col2:
            if warning.get('fix'):
                st.markdown("**✅ Suggested Fix:**")
                st.code(warning['fix'][:200], language='html')
        
        st.markdown("**💡 Recommendation:**")
        st.info(warning.get('recommendation', 'Improve this'))
        
        if warning.get('suggestions'):
            st.markdown("**📝 Suggestions:**")
            for suggestion in warning['suggestions']:
                st.markdown(f"- {suggestion}")
        
        if warning.get('example'):
            st.markdown("**📝 Example:**")
            st.code(warning['example'], language='html')
        
        if warning.get('priority'):
            priority = warning['priority']
            if priority == 'HIGH':
                st.warning(f"⚠️ Priority: {priority}")
            else:
                st.info(f"ℹ️ Priority: {priority}")

# Streamlit UI
def main():
    # Header
    st.markdown('<h1 class="main-header">🔍 SEO On-Page Audit Tool</h1>', unsafe_allow_html=True)
    st.markdown("### Professional SEO analysis with actionable fixes and code snippets")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### About")
        st.info("""
        This tool analyzes your webpage and provides:
        - **Specific code snippets** showing issues
        - **Ready-to-use fixes** you can copy/paste
        - **Line numbers** for easy location
        - **Before/After examples**
        - **Priority levels** for each issue
        """)
        
        st.markdown("---")
        st.markdown("### SEO Best Practices")
        st.success("""
        **Quick Reference:**
        - Title: 50-60 chars
        - Description: 150-160 chars
        - 1 H1 per page
        - Alt text on all images
        - 300+ words content
        - HTTPS enabled
        - Mobile viewport tag
        """)
        
        st.markdown("---")
        st.markdown("### 🎯 How to Use")
        st.markdown("""
        1. Enter your URL
        2. Click **Analyze**
        3. Review issues with **red ❌**
        4. **Copy the fix code**
        5. **Paste into your HTML**
        6. Re-audit to verify!
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        url_input = st.text_input(
            "Enter URL to audit:",
            placeholder="https://example.com",
            help="Enter the full URL including https://"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_button = st.button("🚀 Analyze & Get Fixes", type="primary", use_container_width=True)
    
    # Sample URLs
    st.markdown("**Try these examples:**")
    example_cols = st.columns(3)
    with example_cols[0]:
        if st.button("🌍 Omo Valley Tours", use_container_width=True):
            url_input = "https://omovalleytours.travel"
            analyze_button = True
    with example_cols[1]:
        if st.button("📰 BBC News", use_container_width=True):
            url_input = "https://bbc.com"
            analyze_button = True
    with example_cols[2]:
        if st.button("🛍️ Amazon", use_container_width=True):
            url_input = "https://amazon.com"
            analyze_button = True
    
    # Run audit
    if analyze_button and url_input:
        # Add https:// if missing
        if not url_input.startswith(('http://', 'https://')):
            url_input = 'https://' + url_input
        
        # Progress
        with st.spinner('🔍 Analyzing webpage and preparing fixes... Please wait...'):
            auditor = SEOAuditor(url_input)
            results = auditor.run_audit()
        
        # Display results
        st.markdown("---")
        st.markdown("## 📊 Audit Results with Actionable Fixes")
        
        # Score card
        score = results['score']
        if score >= 80:
            score_class = "score-excellent"
            score_status = "✅ EXCELLENT"
            score_emoji = "🎉"
        elif score >= 60:
            score_class = "score-good"
            score_status = "⚠️ GOOD"
            score_emoji = "👍"
        else:
            score_class = "score-poor"
            score_status = "❌ NEEDS IMPROVEMENT"
            score_emoji = "⚠️"
        
        st.markdown(f"""
        <div class="score-card {score_class}">
            <h1 style="margin: 0; font-size: 4rem;">{score_emoji}</h1>
            <h2 style="margin: 0.5rem 0;">SEO Score: {score}/100</h2>
            <p style="margin: 0; font-size: 1.5rem;">{score_status}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="✅ Passed Checks",
                value=len(results['passed']),
                delta="Good"
            )
        
        with col2:
            st.metric(
                label="⚠️ Warnings",
                value=len(results['warnings']),
                delta="Review"
            )
        
        with col3:
            st.metric(
                label="❌ Critical Issues",
                value=len(results['issues']),
                delta="Fix Now"
            )
        
        st.markdown("---")
        
        # Tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs(["🚨 Critical Issues (Fix First!)", "⚠️ Warnings", "✅ Passed Checks", "📄 Export"])
        
        with tab1:
            if results['issues']:
                st.markdown("### ❌ Critical Issues - Fix These First!")
                st.markdown("Click each issue to see the **current code** and **ready-to-use fix**:")
                for i, issue in enumerate(results['issues']):
                    render_issue_with_fix(issue, i)
            else:
                st.success("🎉 No critical issues found! Great job!")
        
        with tab2:
            if results['warnings']:
                st.markdown("### ⚠️ Warnings - Recommended Improvements")
                st.markdown("Click to see suggestions and fixes:")
                for i, warning in enumerate(results['warnings']):
                    render_warning_with_fix(warning, i)
            else:
                st.success("✅ No warnings! Your SEO is well optimized!")
        
        with tab3:
            if results['passed']:
                st.markdown("### ✅ What's Working Well")
                for passed in results['passed']:
                    st.success(f"✅ {passed['message']}")
                    if passed.get('details'):
                        st.caption(f"Details: {passed['details']}")
        
        with tab4:
            st.markdown("### 📥 Export Results")
            
            # Create DataFrame
            export_data = {
                'URL': [results['url']],
                'Score': [results['score']],
                'Critical Issues': [len(results['issues'])],
                'Warnings': [len(results['warnings'])],
                'Passed': [len(results['passed'])],
                'Timestamp': [results['timestamp']]
            }
            df = pd.DataFrame(export_data)
            
            # Display table
            st.dataframe(df, use_container_width=True)
            
            # Download buttons
            col1, col2 = st.columns(2)
            
            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"seo_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                # Create detailed report with fixes
                report = f"""SEO AUDIT REPORT WITH FIXES
================
URL: {results['url']}
Date: {results['timestamp']}
Score: {results['score']}/100

CRITICAL ISSUES ({len(results['issues'])}):
{chr(10).join(['- ' + issue['message'] for issue in results['issues']])}

WARNINGS ({len(results['warnings'])}):
{chr(10).join(['- ' + warning['message'] for warning in results['warnings']])}

PASSED CHECKS ({len(results['passed'])}):
{chr(10).join(['- ' + passed['message'] for passed in results['passed']])}

DETAILED FIXES:
{chr(10).join([f"{i+1}. {issue['message']}{chr(10)}   Fix: {issue.get('fix', 'See report')}{chr(10)}" for i, issue in enumerate(results['issues'])])}
                """
                
                st.download_button(
                    label="📄 Download Full Report",
                    data=report,
                    file_name=f"seo_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    elif analyze_button:
        st.warning("⚠️ Please enter a URL to analyze")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p><strong>SEO Audit Tool with Actionable Fixes</strong> | Copy, paste, and fix immediately!</p>
        <p>Made with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
