#!/usr/bin/env python3
"""
SEO Audit Tool - Streamlit Web App
Professional SEO analysis with beautiful UI
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
</style>
""", unsafe_allow_html=True)

class SEOAuditor:
    def __init__(self, url):
        self.url = url
        self.domain = urlparse(url).netloc
        self.soup = None
        self.response = None
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
            self.soup = BeautifulSoup(self.response.content, 'html.parser')
            return True
        except Exception as e:
            st.error(f"❌ Failed to fetch page: {str(e)}")
            return False
    
    def check_title_tag(self):
        """Check title tag optimization"""
        title = self.soup.find('title')
        
        if not title:
            self.results['issues'].append("Missing <title> tag")
            return
        
        title_text = title.get_text().strip()
        title_length = len(title_text)
        
        if not title_text:
            self.results['issues'].append("Empty <title> tag")
        elif title_length < 30:
            self.results['warnings'].append(f"Title too short ({title_length} chars). Recommended: 50-60")
        elif title_length > 60:
            self.results['warnings'].append(f"Title too long ({title_length} chars). May be truncated")
        else:
            self.results['passed'].append(f"Title length optimal ({title_length} chars): {title_text}")
    
    def check_meta_description(self):
        """Check meta description"""
        meta_desc = self.soup.find('meta', attrs={'name': 'description'})
        
        if not meta_desc:
            self.results['issues'].append("Missing meta description")
            return
        
        desc_text = meta_desc.get('content', '').strip()
        desc_length = len(desc_text)
        
        if not desc_text:
            self.results['issues'].append("Empty meta description")
        elif desc_length < 120:
            self.results['warnings'].append(f"Meta description too short ({desc_length} chars). Recommended: 150-160")
        elif desc_length > 160:
            self.results['warnings'].append(f"Meta description too long ({desc_length} chars)")
        else:
            self.results['passed'].append(f"Meta description optimal ({desc_length} chars)")
    
    def check_headings(self):
        """Analyze heading structure"""
        h1_tags = self.soup.find_all('h1')
        
        if not h1_tags:
            self.results['issues'].append("Missing H1 tag")
        elif len(h1_tags) > 1:
            self.results['warnings'].append(f"Multiple H1 tags found ({len(h1_tags)}). Recommended: 1 per page")
        else:
            h1_text = h1_tags[0].get_text().strip()
            self.results['passed'].append(f"H1 tag found: {h1_text}")
        
        headings = []
        for i in range(1, 7):
            tags = self.soup.find_all(f'h{i}')
            if tags:
                headings.append(f"H{i}: {len(tags)}")
        
        if headings:
            self.results['passed'].append(f"Heading structure: {', '.join(headings)}")
    
    def check_images(self):
        """Check image optimization"""
        images = self.soup.find_all('img')
        
        if not images:
            self.results['warnings'].append("No images found on page")
            return
        
        missing_alt = []
        empty_alt = []
        
        for img in images:
            src = img.get('src', '')
            alt = img.get('alt')
            
            if alt is None:
                missing_alt.append(src)
            elif not alt.strip():
                empty_alt.append(src)
        
        total_images = len(images)
        self.results['passed'].append(f"Total images found: {total_images}")
        
        if missing_alt:
            self.results['issues'].append(f"{len(missing_alt)} image(s) missing alt attribute")
        
        if empty_alt:
            self.results['warnings'].append(f"{len(empty_alt)} image(s) with empty alt text")
        
        if not missing_alt and not empty_alt:
            self.results['passed'].append("All images have alt attributes")
    
    def check_links(self):
        """Analyze internal and external links"""
        links = self.soup.find_all('a', href=True)
        
        internal_links = []
        external_links = []
        
        for link in links:
            href = link.get('href', '')
            
            if href.startswith('#') or href.startswith('javascript:'):
                continue
            
            full_url = urljoin(self.url, href)
            parsed = urlparse(full_url)
            
            if parsed.netloc == self.domain or not parsed.netloc:
                internal_links.append(full_url)
            else:
                external_links.append(full_url)
        
        self.results['passed'].append(f"Total links: {len(links)}")
        self.results['passed'].append(f"Internal links: {len(internal_links)}")
        self.results['passed'].append(f"External links: {len(external_links)}")
        
        if len(links) > 100:
            self.results['warnings'].append(f"High number of links ({len(links)}). May dilute link equity")
    
    def check_content(self):
        """Analyze page content"""
        for script in self.soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        text = self.soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        word_count = len(text.split())
        
        self.results['passed'].append(f"Word count: {word_count}")
        
        if word_count < 300:
            self.results['warnings'].append(f"Low word count ({word_count}). Recommended: 300+")
        elif word_count > 2500:
            self.results['warnings'].append(f"Very high word count ({word_count}). Consider breaking into multiple pages")
    
    def check_https(self):
        """Check HTTPS/SSL"""
        if self.url.startswith('https://'):
            self.results['passed'].append("Using HTTPS")
        else:
            self.results['issues'].append("Page not using HTTPS")
    
    def check_page_speed(self):
        """Check basic page load metrics"""
        if self.response:
            load_time = self.response.elapsed.total_seconds()
            page_size = len(self.response.content) / 1024
            
            self.results['passed'].append(f"Page load time: {load_time:.2f} seconds")
            self.results['passed'].append(f"Page size: {page_size:.2f} KB")
            
            if load_time > 3:
                self.results['warnings'].append(f"Slow page load time ({load_time:.2f}s). Recommended: < 3s")
            
            if page_size > 1024:
                self.results['warnings'].append(f"Large page size ({page_size:.2f} KB). Consider optimization")
    
    def check_mobile_viewport(self):
        """Check mobile viewport meta tag"""
        viewport = self.soup.find('meta', attrs={'name': 'viewport'})
        if not viewport:
            self.results['issues'].append("Missing viewport meta tag for mobile")
        else:
            self.results['passed'].append("Viewport meta tag found")
    
    def check_open_graph(self):
        """Check Open Graph tags"""
        og_tags = {
            'og:title': self.soup.find('meta', property='og:title'),
            'og:description': self.soup.find('meta', property='og:description'),
            'og:image': self.soup.find('meta', property='og:image'),
        }
        
        missing_og = [tag for tag, elem in og_tags.items() if not elem]
        
        if missing_og:
            self.results['warnings'].append(f"Missing Open Graph tags: {', '.join(missing_og)}")
        else:
            self.results['passed'].append("All essential Open Graph tags present")
    
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

# Streamlit UI
def main():
    # Header
    st.markdown('<h1 class="main-header">🔍 SEO On-Page Audit Tool</h1>', unsafe_allow_html=True)
    st.markdown("### Professional SEO analysis similar to SEMrush & Ahrefs")
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/667eea/ffffff?text=SEO+Audit+Pro", use_container_width=True)
        st.markdown("---")
        st.markdown("### About")
        st.info("""
        This tool analyzes your webpage for:
        - Meta tags optimization
        - Heading structure
        - Image optimization
        - Content quality
        - Technical SEO
        - Mobile friendliness
        - And more!
        """)
        
        st.markdown("---")
        st.markdown("### Quick Tips")
        st.success("""
        **SEO Best Practices:**
        - Title: 50-60 chars
        - Description: 150-160 chars
        - 1 H1 per page
        - Alt text on images
        - 300+ words content
        - HTTPS enabled
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
        analyze_button = st.button("🚀 Analyze", type="primary", use_container_width=True)
    
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
        with st.spinner('🔍 Analyzing webpage... Please wait...'):
            auditor = SEOAuditor(url_input)
            results = auditor.run_audit()
        
        # Display results
        st.markdown("---")
        st.markdown("## 📊 Audit Results")
        
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
        tab1, tab2, tab3, tab4 = st.tabs(["🚨 Critical Issues", "⚠️ Warnings", "✅ Passed Checks", "📄 Export"])
        
        with tab1:
            if results['issues']:
                st.markdown("### Critical Issues to Fix Immediately")
                for issue in results['issues']:
                    st.markdown(f"""
                    <div class="metric-card">
                        <span class="issue-critical">❌ {issue}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("🎉 No critical issues found! Great job!")
        
        with tab2:
            if results['warnings']:
                st.markdown("### Warnings - Recommended Improvements")
                for warning in results['warnings']:
                    st.markdown(f"""
                    <div class="metric-card">
                        <span class="issue-warning">⚠️ {warning}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ No warnings! Your SEO is well optimized!")
        
        with tab3:
            if results['passed']:
                st.markdown("### What's Working Well")
                for passed in results['passed']:
                    st.markdown(f"""
                    <div class="metric-card">
                        <span class="issue-passed">✅ {passed}</span>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab4:
            st.markdown("### Export Results")
            
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
                # Create detailed report
                report = f"""
SEO AUDIT REPORT
================
URL: {results['url']}
Date: {results['timestamp']}
Score: {results['score']}/100

CRITICAL ISSUES ({len(results['issues'])}):
{chr(10).join(['- ' + issue for issue in results['issues']])}

WARNINGS ({len(results['warnings'])}):
{chr(10).join(['- ' + warning for warning in results['warnings']])}

PASSED CHECKS ({len(results['passed'])}):
{chr(10).join(['- ' + passed for passed in results['passed']])}
                """
                
                st.download_button(
                    label="📄 Download Report",
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
        <p><strong>SEO Audit Tool</strong> | Professional on-page SEO analysis</p>
        <p>Made with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
