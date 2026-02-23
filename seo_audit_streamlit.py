#!/usr/bin/env python3
"""
WordPress SEO Audit Tool - Practical Edition
Complete source URL listings for every issue - Perfect for WordPress sites
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
import io
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="WordPress SEO Audit Tool",
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
    .url-list {
        background: #f8f9fa;
        padding: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 0.5rem 0;
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.85rem;
    }
    .fix-badge {
        background: #28a745;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        display: inline-block;
    }
    .wp-badge {
        background: #21759b;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        display: inline-block;
        margin: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

class WordPressSEOAuditor:
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
            'issues': [],
            'passed_checks': [],
            'wordpress_detected': False,
            'wordpress_version': None,
            'wordpress_plugins': [],
            'wordpress_theme': None,
            # Detailed listings for WordPress fixes
            'images_missing_alt': [],
            'images_empty_alt': [],
            'images_no_title': [],
            'images_large_size': [],
            'images_non_webp': [],
            'broken_links': [],
            'internal_links_list': [],
            'external_links_list': [],
            'h1_tags_list': [],
            'all_headings': [],
            'pages_to_noindex': [],
            'missing_schema_opportunities': [],
            'slow_resources': []
        }
        
    def fetch_page(self):
        """Fetch webpage"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            self.response = requests.get(self.url, headers=headers, timeout=15, verify=False, allow_redirects=True)
            self.html_content = self.response.text
            self.soup = BeautifulSoup(self.response.content, 'html.parser')
            
            return True
        except Exception as e:
            st.error(f"❌ Failed to fetch page: {str(e)}")
            return False
    
    def detect_wordpress(self):
        """Detect if site is WordPress and get version"""
        # Check for WordPress generator meta tag
        generator = self.soup.find('meta', attrs={'name': 'generator'})
        if generator:
            content = generator.get('content', '')
            if 'WordPress' in content:
                self.results['wordpress_detected'] = True
                # Extract version
                version_match = re.search(r'WordPress ([\d.]+)', content)
                if version_match:
                    self.results['wordpress_version'] = version_match.group(1)
        
        # Check for wp-content in HTML
        if 'wp-content' in self.html_content or 'wp-includes' in self.html_content:
            self.results['wordpress_detected'] = True
        
        # Detect theme
        theme_match = re.search(r'/wp-content/themes/([^/]+)/', self.html_content)
        if theme_match:
            self.results['wordpress_theme'] = theme_match.group(1)
        
        # Detect common plugins
        plugin_patterns = [
            r'/wp-content/plugins/([^/]+)/',
            r'wp-content/plugins/([^/\'"]+)'
        ]
        
        plugins = set()
        for pattern in plugin_patterns:
            matches = re.findall(pattern, self.html_content)
            plugins.update(matches)
        
        self.results['wordpress_plugins'] = list(plugins)[:20]  # Limit to 20
    
    def check_images_detailed(self):
        """Comprehensive image check with full URLs"""
        images = self.soup.find_all('img')
        
        if not images:
            return
        
        for img in images:
            src = img.get('src', '')
            if not src:
                continue
            
            # Make absolute URL
            full_url = urljoin(self.url, src)
            
            alt = img.get('alt')
            title = img.get('title')
            width = img.get('width')
            height = img.get('height')
            
            # Get parent context (for WordPress, often in <figure> or <div>)
            parent = img.parent
            parent_class = parent.get('class', []) if parent else []
            parent_id = parent.get('id', '') if parent else ''
            
            # Check alt text
            if alt is None:
                self.results['images_missing_alt'].append({
                    'url': full_url,
                    'html': str(img)[:200],
                    'parent_class': ' '.join(parent_class) if parent_class else 'none',
                    'parent_id': parent_id,
                    'location': f"Check WordPress Media Library or post content"
                })
            elif not alt.strip():
                self.results['images_empty_alt'].append({
                    'url': full_url,
                    'current_alt': '',
                    'html': str(img)[:200]
                })
            
            # Check title
            if not title:
                self.results['images_no_title'].append({
                    'url': full_url,
                    'has_alt': bool(alt and alt.strip())
                })
            
            # Check size
            if width and height:
                try:
                    w = int(width)
                    h = int(height)
                    if w > 2000 or h > 2000:
                        self.results['images_large_size'].append({
                            'url': full_url,
                            'width': w,
                            'height': h,
                            'recommendation': f'Resize to max 1920x1920 or use WordPress responsive images'
                        })
                except:
                    pass
            
            # Check format
            file_ext = full_url.lower().split('?')[0].split('.')[-1]
            if file_ext in ['jpg', 'jpeg', 'png'] and 'webp' not in full_url.lower():
                self.results['images_non_webp'].append({
                    'url': full_url,
                    'current_format': file_ext,
                    'recommendation': 'Convert to WebP using plugin like "WebP Converter for Media"'
                })
        
        # Create issues based on findings
        if self.results['images_missing_alt']:
            self.results['issues'].append({
                'severity': 'CRITICAL',
                'category': 'Images & Media',
                'issue': f"{len(self.results['images_missing_alt'])} images missing alt text",
                'count': len(self.results['images_missing_alt']),
                'wordpress_fix': [
                    '1. Go to WordPress Media Library',
                    '2. Click on each image',
                    '3. Add descriptive "Alternative Text"',
                    '4. Or use plugin: "Auto Image Alt Text"'
                ],
                'bulk_fix': 'Use SEO plugin like Rank Math or Yoast to find and fix all at once',
                'details_key': 'images_missing_alt'
            })
        
        if self.results['images_non_webp']:
            self.results['issues'].append({
                'severity': 'MEDIUM',
                'category': 'Performance',
                'issue': f"{len(self.results['images_non_webp'])} images not using WebP format",
                'count': len(self.results['images_non_webp']),
                'wordpress_fix': [
                    'Install plugin: "WebP Converter for Media"',
                    'Or "Imagify" or "ShortPixel"',
                    'Enable automatic WebP conversion',
                    'Regenerate thumbnails'
                ],
                'benefit': 'Can reduce image size by 25-35%',
                'details_key': 'images_non_webp'
            })
        
        if self.results['images_large_size']:
            self.results['issues'].append({
                'severity': 'HIGH',
                'category': 'Performance',
                'issue': f"{len(self.results['images_large_size'])} oversized images detected",
                'count': len(self.results['images_large_size']),
                'wordpress_fix': [
                    'Install plugin: "Regenerate Thumbnails"',
                    'Or manually resize in WordPress Media Library',
                    'Set max image dimensions in Settings > Media'
                ],
                'details_key': 'images_large_size'
            })
    
    def check_links_detailed(self):
        """Detailed link analysis with full URLs"""
        links = self.soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href', '').strip()
            anchor_text = link.get_text().strip()
            rel = link.get('rel', [])
            
            if not href:
                self.results['broken_links'].append({
                    'type': 'Empty href',
                    'url': '',
                    'anchor_text': anchor_text or '[No anchor text]',
                    'html': str(link)[:150],
                    'fix': 'Remove this link or add proper URL'
                })
                continue
            
            # Skip anchors and javascript
            if href.startswith('#') or href.startswith('javascript:') or href.startswith('mailto:') or href.startswith('tel:'):
                continue
            
            # Make absolute URL
            full_url = urljoin(self.url, href)
            parsed = urlparse(full_url)
            
            # Classify as internal or external
            is_internal = parsed.netloc == self.domain or not parsed.netloc
            
            link_data = {
                'url': full_url,
                'anchor_text': anchor_text[:100] if anchor_text else '[No anchor text]',
                'nofollow': 'nofollow' in rel,
                'target': link.get('target', '_self'),
                'location_in_page': self.get_link_location(link)
            }
            
            if is_internal:
                self.results['internal_links_list'].append(link_data)
            else:
                self.results['external_links_list'].append(link_data)
            
            # Check for broken patterns
            if href == '#' or href == '/' or href == '':
                self.results['broken_links'].append({
                    'type': 'Invalid link',
                    'url': href,
                    'anchor_text': anchor_text,
                    'fix': 'Update or remove this link in WordPress editor'
                })
        
        # Create issues
        if self.results['broken_links']:
            self.results['issues'].append({
                'severity': 'HIGH',
                'category': 'Links',
                'issue': f"{len(self.results['broken_links'])} broken or empty links found",
                'count': len(self.results['broken_links']),
                'wordpress_fix': [
                    'Install plugin: "Broken Link Checker"',
                    'It will automatically find and notify you of broken links',
                    'Or manually search and fix in WordPress editor'
                ],
                'details_key': 'broken_links'
            })
        
        if len(self.results['internal_links_list']) < 3:
            self.results['issues'].append({
                'severity': 'MEDIUM',
                'category': 'Internal Linking',
                'issue': f"Only {len(self.results['internal_links_list'])} internal links found",
                'wordpress_fix': [
                    'Add 3-5 internal links to related posts/pages',
                    'Use WordPress "Insert link" button in editor',
                    'Or use plugin: "Internal Link Juicer" for automatic linking'
                ],
                'benefit': 'Improves SEO and helps visitors navigate your site'
            })
    
    def get_link_location(self, link):
        """Determine where in the page the link is"""
        parent = link.parent
        locations = []
        
        # Check parents
        for _ in range(5):  # Check up to 5 levels
            if not parent:
                break
            
            if parent.name == 'nav':
                return 'Navigation Menu'
            elif parent.name == 'header':
                return 'Header'
            elif parent.name == 'footer':
                return 'Footer'
            elif parent.name == 'aside':
                return 'Sidebar'
            elif parent.name == 'article' or parent.name == 'main':
                return 'Main Content'
            
            # Check for common WordPress classes
            classes = parent.get('class', [])
            if any('menu' in c for c in classes):
                return 'Menu'
            if any('widget' in c for c in classes):
                return 'Widget'
            if any('footer' in c for c in classes):
                return 'Footer'
            
            parent = parent.parent
        
        return 'Content Area'
    
    def check_headings_detailed(self):
        """Detailed heading analysis"""
        for i in range(1, 7):
            tags = self.soup.find_all(f'h{i}')
            for tag in tags:
                text = tag.get_text().strip()
                self.results['all_headings'].append({
                    'level': f'H{i}',
                    'text': text,
                    'length': len(text),
                    'parent_class': ' '.join(tag.parent.get('class', [])) if tag.parent else '',
                    'html': str(tag)[:200]
                })
        
        # Check H1 specifically
        h1_tags = self.soup.find_all('h1')
        
        for h1 in h1_tags:
            self.results['h1_tags_list'].append({
                'text': h1.get_text().strip(),
                'html': str(h1)[:200]
            })
        
        if not h1_tags:
            self.results['issues'].append({
                'severity': 'CRITICAL',
                'category': 'Content Structure',
                'issue': "Missing H1 heading",
                'wordpress_fix': [
                    'Edit your page/post in WordPress',
                    'Make sure your main title uses "Heading 1" format',
                    'In Block Editor: Select title block → Set to H1',
                    'In Classic Editor: Select text → Choose "Heading 1" from dropdown'
                ],
                'seo_impact': 'H1 tells search engines the main topic of your page'
            })
        elif len(h1_tags) > 1:
            self.results['issues'].append({
                'severity': 'HIGH',
                'category': 'Content Structure',
                'issue': f"Multiple H1 headings found ({len(h1_tags)})",
                'count': len(h1_tags),
                'wordpress_fix': [
                    'Keep only ONE H1 per page (usually your main title)',
                    'Change other H1s to H2 or H3',
                    'In WordPress editor: Select heading → Change format'
                ],
                'details_key': 'h1_tags_list'
            })
    
    def check_meta_tags(self):
        """Check meta tags with WordPress-specific advice"""
        title = self.soup.find('title')
        meta_desc = self.soup.find('meta', attrs={'name': 'description'})
        
        if not title or not title.get_text().strip():
            self.results['issues'].append({
                'severity': 'CRITICAL',
                'category': 'Meta Tags',
                'issue': "Missing or empty title tag",
                'wordpress_fix': [
                    'Install SEO plugin: Rank Math, Yoast SEO, or All in One SEO',
                    'Edit page/post → Scroll to SEO section',
                    'Fill in "SEO Title" field',
                    'Keep it 50-60 characters'
                ],
                'plugin_recommendation': 'Rank Math (Free) - Most comprehensive',
                'current': str(title) if title else 'None'
            })
        else:
            title_text = title.get_text().strip()
            title_length = len(title_text)
            
            if title_length < 30 or title_length > 60:
                self.results['issues'].append({
                    'severity': 'MEDIUM',
                    'category': 'Meta Tags',
                    'issue': f"Title length not optimal ({title_length} characters)",
                    'current_title': title_text,
                    'target': '50-60 characters',
                    'wordpress_fix': [
                        'Edit page in WordPress',
                        'Update SEO Title in your SEO plugin',
                        f'Current: {title_length} chars, Target: 50-60 chars'
                    ]
                })
        
        if not meta_desc:
            self.results['issues'].append({
                'severity': 'CRITICAL',
                'category': 'Meta Tags',
                'issue': "Missing meta description",
                'wordpress_fix': [
                    'Install SEO plugin (Rank Math/Yoast)',
                    'Edit page/post',
                    'Fill in "Meta Description" field',
                    'Keep it 150-160 characters',
                    'Include primary keyword and call-to-action'
                ],
                'example': 'Discover authentic Omo Valley tours. Experience Ethiopian culture with expert guides. Book your adventure today!'
            })
        else:
            desc_text = meta_desc.get('content', '').strip()
            desc_length = len(desc_text)
            
            if desc_length < 120 or desc_length > 160:
                self.results['issues'].append({
                    'severity': 'MEDIUM',
                    'category': 'Meta Tags',
                    'issue': f"Meta description length not optimal ({desc_length} characters)",
                    'current_description': desc_text,
                    'target': '150-160 characters',
                    'wordpress_fix': [
                        'Edit in SEO plugin',
                        f'Adjust from {desc_length} to 150-160 characters'
                    ]
                })
    
    def check_wordpress_specific(self):
        """WordPress-specific SEO checks"""
        
        # Check for SEO plugins
        seo_plugins = []
        common_seo_plugins = {
            'wordpress-seo': 'Yoast SEO',
            'all-in-one-seo-pack': 'All in One SEO',
            'seo-by-rank-math': 'Rank Math',
            'wp-seopress': 'SEOPress'
        }
        
        for plugin_slug, plugin_name in common_seo_plugins.items():
            if plugin_slug in ' '.join(self.results['wordpress_plugins']):
                seo_plugins.append(plugin_name)
        
        if not seo_plugins:
            self.results['issues'].append({
                'severity': 'HIGH',
                'category': 'WordPress Setup',
                'issue': "No SEO plugin detected",
                'wordpress_fix': [
                    'Install one of these SEO plugins:',
                    '• Rank Math (Recommended - Free & comprehensive)',
                    '• Yoast SEO (Popular - Freemium)',
                    '• All in One SEO (User-friendly)',
                    '',
                    'How to install:',
                    '1. Go to Plugins → Add New',
                    '2. Search for "Rank Math"',
                    '3. Click Install → Activate',
                    '4. Follow setup wizard'
                ],
                'benefit': 'SEO plugins help optimize every page automatically'
            })
        
        # Check for caching
        caching_plugins = ['wp-rocket', 'w3-total-cache', 'wp-super-cache', 'wp-fastest-cache', 'litespeed-cache']
        has_caching = any(plugin in ' '.join(self.results['wordpress_plugins']) for plugin in caching_plugins)
        
        if not has_caching:
            self.results['issues'].append({
                'severity': 'MEDIUM',
                'category': 'WordPress Performance',
                'issue': "No caching plugin detected",
                'wordpress_fix': [
                    'Install a caching plugin:',
                    '• WP Rocket (Premium - Best performance)',
                    '• LiteSpeed Cache (Free - If using LiteSpeed server)',
                    '• W3 Total Cache (Free)',
                    '',
                    'Installation:',
                    'Plugins → Add New → Search → Install → Activate'
                ],
                'benefit': 'Caching can improve page speed by 50-70%'
            })
        
        # Check for image optimization plugins
        image_plugins = ['ewww-image-optimizer', 'shortpixel', 'imagify', 'smush', 'webp-converter']
        has_image_optimizer = any(plugin in ' '.join(self.results['wordpress_plugins']) for plugin in image_plugins)
        
        if not has_image_optimizer and len(self.results['images_non_webp']) > 0:
            self.results['issues'].append({
                'severity': 'MEDIUM',
                'category': 'WordPress Performance',
                'issue': "No image optimization plugin detected",
                'wordpress_fix': [
                    'Install image optimization plugin:',
                    '• WebP Converter for Media (Free - WebP conversion)',
                    '• ShortPixel (Freemium - Compression + WebP)',
                    '• Imagify (Freemium - Auto optimization)',
                    '',
                    'After installing:',
                    '1. Configure settings',
                    '2. Bulk optimize existing images',
                    '3. Enable auto-optimization for new uploads'
                ]
            })
    
    def check_performance(self):
        """Performance checks"""
        if self.response:
            load_time = self.response.elapsed.total_seconds()
            page_size = len(self.response.content) / 1024  # KB
            
            if load_time > 3:
                self.results['issues'].append({
                    'severity': 'HIGH',
                    'category': 'Performance',
                    'issue': f"Slow page load time ({load_time:.2f} seconds)",
                    'current': f'{load_time:.2f}s',
                    'target': '< 3 seconds',
                    'wordpress_fix': [
                        '1. Install WP Rocket or LiteSpeed Cache',
                        '2. Optimize images (use WebP Converter)',
                        '3. Minify CSS/JS (in cache plugin settings)',
                        '4. Enable lazy loading for images',
                        '5. Use a CDN like Cloudflare (free)',
                        '6. Remove unused plugins',
                        '7. Use lightweight theme',
                        '8. Upgrade hosting if needed'
                    ],
                    'test_tools': [
                        'GTmetrix.com - Detailed performance report',
                        'PageSpeed Insights - Google recommendations',
                        'Pingdom - Speed test from multiple locations'
                    ]
                })
            
            if page_size > 1024:  # > 1MB
                self.results['issues'].append({
                    'severity': 'MEDIUM',
                    'category': 'Performance',
                    'issue': f"Large page size ({page_size:.0f} KB)",
                    'current': f'{page_size:.0f} KB',
                    'target': '< 1 MB',
                    'wordpress_fix': [
                        '1. Compress images before uploading',
                        '2. Use image optimization plugin',
                        '3. Lazy load images',
                        '4. Minify CSS/JavaScript',
                        '5. Remove unused plugins/themes'
                    ]
                })
    
    def check_mobile_optimization(self):
        """Mobile optimization check"""
        viewport = self.soup.find('meta', attrs={'name': 'viewport'})
        
        if not viewport:
            self.results['issues'].append({
                'severity': 'CRITICAL',
                'category': 'Mobile',
                'issue': "Missing viewport meta tag",
                'wordpress_fix': [
                    'Most WordPress themes include this automatically',
                    'If missing:',
                    '1. Switch to a modern, responsive theme',
                    '2. Or add to theme header.php:',
                    '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                    '',
                    'Recommended themes:',
                    '• Astra (Free, fast, SEO-friendly)',
                    '• GeneratePress (Lightweight)',
                    '• Kadence (Modern, feature-rich)'
                ],
                'impact': 'Without this, your site won\'t be mobile-friendly (major ranking factor)'
            })
    
    def check_https(self):
        """HTTPS check"""
        if not self.url.startswith('https://'):
            self.results['issues'].append({
                'severity': 'CRITICAL',
                'category': 'Security',
                'issue': "Site not using HTTPS",
                'wordpress_fix': [
                    '1. Get free SSL certificate:',
                    '   • Contact your hosting provider (usually free)',
                    '   • Most hosts: cPanel → SSL/TLS → Install Let\'s Encrypt',
                    '',
                    '2. Force HTTPS in WordPress:',
                    '   • Install plugin: "Really Simple SSL"',
                    '   • Activate it',
                    '   • It handles everything automatically',
                    '',
                    '3. Update WordPress settings:',
                    '   • Settings → General',
                    '   • Change URLs from http:// to https://',
                    '   • Save',
                    '',
                    '4. Update .htaccess to redirect HTTP to HTTPS'
                ],
                'impact': 'Google prioritizes HTTPS sites. Chrome shows HTTP as "Not Secure"',
                'cost': 'Free with most hosting providers'
            })
    
    def generate_wordpress_action_plan(self):
        """Generate WordPress-specific action plan"""
        action_plan = []
        
        # Group by priority
        critical = [i for i in self.results['issues'] if i['severity'] == 'CRITICAL']
        high = [i for i in self.results['issues'] if i['severity'] == 'HIGH']
        medium = [i for i in self.results['issues'] if i['severity'] == 'MEDIUM']
        
        if critical:
            action_plan.append({
                'phase': 'URGENT - Do Today',
                'priority': 'CRITICAL',
                'tasks': critical,
                'estimated_time': f'{len(critical) * 15} minutes'
            })
        
        if high:
            action_plan.append({
                'phase': 'This Week',
                'priority': 'HIGH',
                'tasks': high,
                'estimated_time': f'{len(high) * 20} minutes'
            })
        
        if medium:
            action_plan.append({
                'phase': 'This Month',
                'priority': 'MEDIUM',
                'tasks': medium,
                'estimated_time': f'{len(medium) * 30} minutes'
            })
        
        return action_plan
    
    def calculate_score(self):
        """Calculate SEO score"""
        total_issues = len(self.results['issues'])
        critical = len([i for i in self.results['issues'] if i['severity'] == 'CRITICAL'])
        high = len([i for i in self.results['issues'] if i['severity'] == 'HIGH'])
        medium = len([i for i in self.results['issues'] if i['severity'] == 'MEDIUM'])
        
        # Weighted scoring
        penalty = (critical * 15) + (high * 10) + (medium * 5)
        score = max(0, 100 - penalty)
        
        self.results['overall_score'] = score
    
    def run_audit(self):
        """Run complete WordPress SEO audit"""
        if not self.fetch_page():
            return self.results
        
        with st.spinner('🔍 Detecting WordPress...'):
            self.detect_wordpress()
            time.sleep(0.1)
        
        with st.spinner('📝 Checking meta tags...'):
            self.check_meta_tags()
            time.sleep(0.1)
        
        with st.spinner('📋 Analyzing headings...'):
            self.check_headings_detailed()
            time.sleep(0.1)
        
        with st.spinner('🖼️ Scanning all images...'):
            self.check_images_detailed()
            time.sleep(0.1)
        
        with st.spinner('🔗 Checking all links...'):
            self.check_links_detailed()
            time.sleep(0.1)
        
        with st.spinner('🔧 WordPress-specific checks...'):
            self.check_wordpress_specific()
            time.sleep(0.1)
        
        with st.spinner('⚡ Performance analysis...'):
            self.check_performance()
            time.sleep(0.1)
        
        with st.spinner('📱 Mobile optimization...'):
            self.check_mobile_optimization()
            time.sleep(0.1)
        
        with st.spinner('🔒 Security checks...'):
            self.check_https()
            time.sleep(0.1)
        
        with st.spinner('📊 Calculating score...'):
            self.calculate_score()
        
        return self.results

# ==================== UI FUNCTIONS ====================

def render_wordpress_info(results):
    """Render WordPress detection info"""
    if results['wordpress_detected']:
        st.success("✅ WordPress Site Detected!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            version = results.get('wordpress_version', 'Unknown')
            st.metric("WordPress Version", version)
        
        with col2:
            theme = results.get('wordpress_theme', 'Unknown')
            st.metric("Active Theme", theme)
        
        with col3:
            plugin_count = len(results.get('wordpress_plugins', []))
            st.metric("Plugins Detected", plugin_count)
        
        if results.get('wordpress_plugins'):
            with st.expander("🔌 Detected Plugins"):
                plugins = results['wordpress_plugins']
                for i in range(0, len(plugins), 3):
                    cols = st.columns(3)
                    for j, col in enumerate(cols):
                        if i + j < len(plugins):
                            col.markdown(f"• {plugins[i + j]}")
    else:
        st.info("ℹ️ Not a WordPress site (or WordPress is hidden)")

def render_detailed_issues(results):
    """Render issues with full source URLs"""
    
    for issue in results['issues']:
        severity = issue['severity']
        
        # Color coding
        if severity == 'CRITICAL':
            badge_color = "🔴"
            expander_open = True
        elif severity == 'HIGH':
            badge_color = "🟠"
            expander_open = False
        elif severity == 'MEDIUM':
            badge_color = "🟡"
            expander_open = False
        else:
            badge_color = "🔵"
            expander_open = False
        
        with st.expander(f"{badge_color} {severity}: {issue['issue']}", expanded=expander_open):
            
            # WordPress Fix Instructions
            if issue.get('wordpress_fix'):
                st.markdown("### 🔧 How to Fix in WordPress:")
                for step in issue['wordpress_fix']:
                    if step.startswith('•'):
                        st.markdown(f"  {step}")
                    else:
                        st.markdown(step)
            
            # Show detailed listings with URLs
            if issue.get('details_key'):
                key = issue['details_key']
                items = results.get(key, [])
                
                if items:
                    st.markdown(f"### 📋 Complete List ({len(items)} items):")
                    
                    # Create DataFrame for download
                    if key == 'images_missing_alt':
                        st.markdown("**All images missing alt text:**")
                        df_data = []
                        for idx, img in enumerate(items, 1):
                            st.markdown(f"""
                            **{idx}. Image URL:**
                            ```
                            {img['url']}
                            ```
                            - Location: {img['location']}
                            - Parent class: {img['parent_class']}
                            """)
                            df_data.append({
                                'Image URL': img['url'],
                                'Location': img['location'],
                                'Parent Class': img['parent_class'],
                                'Fix': 'Add alt text in WordPress Media Library'
                            })
                        
                        # Download button
                        if df_data:
                            df = pd.DataFrame(df_data)
                            csv = df.to_csv(index=False)
                            st.download_button(
                                "📥 Download Full List (CSV)",
                                csv,
                                f"images_missing_alt_{datetime.now().strftime('%Y%m%d')}.csv",
                                "text/csv",
                                key=f"download_{key}"
                            )
                    
                    elif key == 'images_non_webp':
                        st.markdown("**Images to convert to WebP:**")
                        df_data = []
                        for idx, img in enumerate(items[:20], 1):  # Show first 20
                            st.markdown(f"{idx}. `{img['url']}`")
                            df_data.append({
                                'Image URL': img['url'],
                                'Current Format': img['current_format'],
                                'Recommendation': img['recommendation']
                            })
                        
                        if len(items) > 20:
                            st.info(f"Showing first 20 of {len(items)} images. Download CSV for complete list.")
                        
                        df = pd.DataFrame(df_data)
                        csv = df.to_csv(index=False)
                        st.download_button(
                            "📥 Download Full List (CSV)",
                            csv,
                            f"images_to_convert_{datetime.now().strftime('%Y%m%d')}.csv",
                            "text/csv",
                            key=f"download_{key}"
                        )
                    
                    elif key == 'images_large_size':
                        st.markdown("**Oversized images to optimize:**")
                        df_data = []
                        for idx, img in enumerate(items, 1):
                            st.markdown(f"{idx}. `{img['url']}` - Size: {img['width']}x{img['height']}px")
                            df_data.append({
                                'Image URL': img['url'],
                                'Width': img['width'],
                                'Height': img['height'],
                                'Recommendation': img['recommendation']
                            })
                        
                        df = pd.DataFrame(df_data)
                        csv = df.to_csv(index=False)
                        st.download_button(
                            "📥 Download List (CSV)",
                            csv,
                            f"large_images_{datetime.now().strftime('%Y%m%d')}.csv",
                            "text/csv",
                            key=f"download_{key}"
                        )
                    
                    elif key == 'broken_links':
                        st.markdown("**Broken or invalid links:**")
                        df_data = []
                        for idx, link in enumerate(items, 1):
                            st.markdown(f"""
                            **{idx}. Issue:** {link['type']}
                            - Anchor text: "{link['anchor_text']}"
                            - Fix: {link['fix']}
                            ```html
                            {link.get('html', '')}
                            ```
                            """)
                            df_data.append({
                                'Issue': link['type'],
                                'URL': link['url'],
                                'Anchor Text': link['anchor_text'],
                                'Fix': link['fix']
                            })
                        
                        df = pd.DataFrame(df_data)
                        csv = df.to_csv(index=False)
                        st.download_button(
                            "📥 Download Broken Links (CSV)",
                            csv,
                            f"broken_links_{datetime.now().strftime('%Y%m%d')}.csv",
                            "text/csv",
                            key=f"download_{key}"
                        )
                    
                    elif key == 'h1_tags_list':
                        st.markdown("**All H1 tags found:**")
                        for idx, h1 in enumerate(items, 1):
                            st.markdown(f"{idx}. \"{h1['text']}\"")
                            st.code(h1['html'], language='html')
                        
                        st.markdown("**Fix:** Keep only ONE H1. Change others to H2 or H3 in WordPress editor.")
            
            # Plugin recommendations
            if issue.get('plugin_recommendation'):
                st.success(f"💡 Recommended Plugin: {issue['plugin_recommendation']}")
            
            # Benefit
            if issue.get('benefit'):
                st.info(f"✨ Benefit: {issue['benefit']}")
            
            # SEO Impact
            if issue.get('seo_impact'):
                st.warning(f"⚠️ SEO Impact: {issue['seo_impact']}")

def render_all_links(results):
    """Render complete link inventory"""
    st.markdown("### 🔗 Complete Link Inventory")
    
    tab1, tab2 = st.tabs(["Internal Links", "External Links"])
    
    with tab1:
        internal = results.get('internal_links_list', [])
        if internal:
            st.markdown(f"**Found {len(internal)} internal links:**")
            
            df_data = []
            for idx, link in enumerate(internal, 1):
                df_data.append({
                    'No.': idx,
                    'URL': link['url'],
                    'Anchor Text': link['anchor_text'],
                    'Location': link['location_in_page'],
                    'NoFollow': 'Yes' if link['nofollow'] else 'No'
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download Internal Links (CSV)",
                csv,
                f"internal_links_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )
        else:
            st.warning("No internal links found - Add links to related posts/pages!")
    
    with tab2:
        external = results.get('external_links_list', [])
        if external:
            st.markdown(f"**Found {len(external)} external links:**")
            
            df_data = []
            for idx, link in enumerate(external, 1):
                df_data.append({
                    'No.': idx,
                    'URL': link['url'],
                    'Anchor Text': link['anchor_text'],
                    'NoFollow': 'Yes' if link['nofollow'] else 'No',
                    'Opens In': 'New Tab' if link['target'] == '_blank' else 'Same Tab'
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download External Links (CSV)",
                csv,
                f"external_links_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )
        else:
            st.info("No external links found")

def render_all_headings(results):
    """Render complete heading structure"""
    st.markdown("### 📋 Complete Heading Structure")
    
    headings = results.get('all_headings', [])
    
    if headings:
        df_data = []
        for heading in headings:
            df_data.append({
                'Level': heading['level'],
                'Text': heading['text'],
                'Length': heading['length'],
                'Parent Class': heading['parent_class']
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        # Visual hierarchy
        st.markdown("**Hierarchy Visualization:**")
        for heading in headings:
            indent = "  " * (int(heading['level'][1]) - 1)
            st.markdown(f"{indent}**{heading['level']}:** {heading['text'][:80]}")
        
        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Download Heading Structure (CSV)",
            csv,
            f"headings_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    else:
        st.warning("No headings found on page")

def render_action_plan(action_plan):
    """Render WordPress action plan"""
    st.markdown("## 🎯 Your WordPress SEO Action Plan")
    
    for phase in action_plan:
        priority = phase['priority']
        
        if priority == 'CRITICAL':
            color = "#dc3545"
            icon = "🔴"
        elif priority == 'HIGH':
            color = "#fd7e14"
            icon = "🟠"
        else:
            color = "#ffc107"
            icon = "🟡"
        
        st.markdown(f"### {icon} {phase['phase']}")
        st.markdown(f"*Estimated time: {phase['estimated_time']}*")
        
        for idx, task in enumerate(phase['tasks'], 1):
            with st.expander(f"{idx}. {task['issue']}", expanded=False):
                st.markdown(f"**Category:** {task['category']}")
                
                if task.get('wordpress_fix'):
                    st.markdown("**WordPress Fix Steps:**")
                    for step in task['wordpress_fix']:
                        st.markdown(step)
                
                if task.get('benefit'):
                    st.success(f"**Benefit:** {task['benefit']}")

# ==================== MAIN APP ====================

def main():
    st.markdown('<h1 class="main-header">🔍 WordPress SEO Audit Tool</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.1rem;">Complete source URL listings • WordPress-specific fixes • Ready for implementation</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 WordPress Optimized")
        st.success("""
        **Perfect for:**
        - WordPress site owners
        - Bloggers
        - Agencies
        - Freelancers
        - WooCommerce stores
        
        **Provides:**
        - Full image URLs
        - All broken links
        - Plugin recommendations
        - Step-by-step fixes
        - Downloadable lists
        """)
        
        st.markdown("---")
        st.markdown("### 📥 What You Get")
        st.info("""
        1. **Complete Image List**
           - All images missing alt text
           - Full URLs
           - Download as CSV
        
        2. **All Links Inventory**
           - Internal links
           - External links
           - Broken links
           - Download lists
        
        3. **WordPress Fixes**
           - Exact plugin names
           - Menu locations
           - Settings to change
        
        4. **Action Plan**
           - Priority order
           - Time estimates
           - Step-by-step guide
        """)
    
    # Main input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        url_input = st.text_input(
            "Enter your WordPress site URL:",
            placeholder="https://yourwordpresssite.com",
            help="Enter your WordPress website URL"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_button = st.button("🚀 Audit Site", type="primary", use_container_width=True)
    
    # Run audit
    if analyze_button and url_input:
        if not url_input.startswith(('http://', 'https://')):
            url_input = 'https://' + url_input
        
        auditor = WordPressSEOAuditor(url_input)
        results = auditor.run_audit()
        
        st.markdown("---")
        
        # WordPress Detection
        render_wordpress_info(results)
        
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
        
        # Issue count
        critical = len([i for i in results['issues'] if i['severity'] == 'CRITICAL'])
        high = len([i for i in results['issues'] if i['severity'] == 'HIGH'])
        medium = len([i for i in results['issues'] if i['severity'] == 'MEDIUM'])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("🔴 Critical", critical, "Fix ASAP")
        col2.metric("🟠 High Priority", high, "This Week")
        col3.metric("🟡 Medium", medium, "This Month")
        
        st.markdown("---")
        
        # Tabs
        tabs = st.tabs([
            "🚨 Issues & Fixes",
            "🎯 Action Plan",
            "🖼️ All Images",
            "🔗 All Links",
            "📋 Headings",
            "📥 Download Reports"
        ])
        
        with tabs[0]:
            if results['issues']:
                render_detailed_issues(results)
            else:
                st.success("🎉 No issues found! Your WordPress site SEO is excellent!")
        
        with tabs[1]:
            action_plan = auditor.generate_wordpress_action_plan()
            if action_plan:
                render_action_plan(action_plan)
            else:
                st.success("✅ No action needed!")
        
        with tabs[2]:
            st.markdown("## 🖼️ Complete Image Analysis")
            
            total_images = (
                len(results['images_missing_alt']) +
                len(results['images_empty_alt']) +
                len(results['images_no_title']) +
                len(results['images_large_size']) +
                len(results['images_non_webp'])
            )
            
            if total_images > 0:
                st.info(f"Found image optimization opportunities:")
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Missing Alt", len(results['images_missing_alt']))
                col2.metric("Large Size", len(results['images_large_size']))
                col3.metric("Need WebP", len(results['images_non_webp']))
                
                # Show lists
                if results['images_missing_alt']:
                    with st.expander(f"📋 Images Missing Alt Text ({len(results['images_missing_alt'])})", expanded=True):
                        df_data = []
                        for img in results['images_missing_alt']:
                            st.markdown(f"**URL:** `{img['url']}`")
                            st.caption(f"Location: {img['location']}")
                            df_data.append({
                                'Image URL': img['url'],
                                'Location': img['location'],
                                'Fix': 'Add in WP Media Library'
                            })
                        
                        df = pd.DataFrame(df_data)
                        csv = df.to_csv(index=False)
                        st.download_button(
                            "📥 Download List",
                            csv,
                            f"images_missing_alt_{datetime.now().strftime('%Y%m%d')}.csv",
                            "text/csv"
                        )
            else:
                st.success("✅ All images are optimized!")
        
        with tabs[3]:
            render_all_links(results)
        
        with tabs[4]:
            render_all_headings(results)
        
        with tabs[5]:
            st.markdown("## 📥 Download Complete Reports")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Summary report
                summary_text = f"""
WORDPRESS SEO AUDIT REPORT
========================

Site: {results['url']}
Date: {results['timestamp']}
Score: {results['overall_score']}/100

WordPress Info:
- Detected: {'Yes' if results['wordpress_detected'] else 'No'}
- Version: {results.get('wordpress_version', 'Unknown')}
- Theme: {results.get('wordpress_theme', 'Unknown')}
- Plugins: {len(results.get('wordpress_plugins', []))}

Issues Found:
- Critical: {critical}
- High: {high}
- Medium: {medium}

Image Issues:
- Missing alt text: {len(results['images_missing_alt'])}
- Need WebP: {len(results['images_non_webp'])}
- Oversized: {len(results['images_large_size'])}

Links:
- Internal: {len(results['internal_links_list'])}
- External: {len(results['external_links_list'])}
- Broken: {len(results['broken_links'])}

Priority Actions:
{chr(10).join([f"- {issue['issue']}" for issue in results['issues'][:10]])}
"""
                
                st.download_button(
                    "📄 Download Summary Report",
                    summary_text,
                    f"wordpress_seo_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                    "text/plain",
                    use_container_width=True
                )
            
            with col2:
                # Create master spreadsheet
                st.download_button(
                    "📊 Download Master Spreadsheet",
                    "Complete audit data available in individual tabs above",
                    f"wordpress_seo_audit_{datetime.now().strftime('%Y%m%d')}.txt",
                    "text/plain",
                    use_container_width=True,
                    disabled=True,
                    help="Download individual CSVs from each tab above"
                )
    
    elif analyze_button:
        st.warning("⚠️ Please enter a URL")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p><strong>WordPress SEO Audit Tool</strong> - Complete source listings for practical fixes</p>
        <p>Made for WordPress site owners • Download all lists • Implement immediately</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
