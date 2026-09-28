import re

html_filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\index.html'

with open(html_filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_html = """
        <section id="section-alumni" class="app-section">
            
            <!-- ALUMNI HERO SECTION -->
            <div class="hof-hero">
                <div class="hof-hero-left">
                    <div class="h-badge">
                        <i class="fa-solid fa-trophy"></i> Hall of Fame
                    </div>
                    <h2 class="h-title">Best Scorers' <span class="gradient-text">Challenge Tests</span></h2>
                    <p class="h-desc">
                        Solve curated mock test sets cleared with perfect 100% scores by our top placed alumni seniors.
                    </p>
                </div>
                <div class="hof-hero-right">
                    <!-- Premium UI Achievement Composition (No Images) -->
                    <div class="h-achievement-wrapper">
                        <!-- Glow effect behind -->
                        <div class="h-glow"></div>
                        
                        <div class="h-main-award">
                            <div class="h-award-icon">
                                <i class="fa-solid fa-trophy"></i>
                            </div>
                            <h3>HALL OF FAME</h3>
                            <div class="h-award-score">100%</div>
                        </div>
                        
                        <!-- Floating Badges -->
                        <div class="h-float-badge b-top">
                            <i class="fa-solid fa-star"></i> Top Performer
                        </div>
                        <div class="h-float-badge b-bottom">
                            <i class="fa-solid fa-briefcase"></i> Placement Challenge
                        </div>
                    </div>
                </div>
            </div>

            <!-- MAIN HALL OF FAME CONTAINER -->
            <div class="hof-main-container">
                
                <div class="hof-header">
                    <div class="hof-header-left">
                        <div class="hof-icon"><i class="fa-solid fa-trophy"></i></div>
                        <div>
                            <h3 class="hof-title">Top Performers (Hall of Fame)</h3>
                            <p class="hof-sub">Learn from the best. Solve their exact test sets and challenge yourself.</p>
                        </div>
                    </div>
                    <div class="hof-header-right">
                        <button class="btn btn-outline" onclick="fetchAlumniExperiences()">
                            <i class="fa-solid fa-chart-simple"></i> View All Alumni <i class="fa-solid fa-arrow-right" style="margin-left: 0.5rem;"></i>
                        </button>
                    </div>
                </div>
                
                <!-- Filter bar (hidden behind a collapse/button or styled neatly) -->
                <div class="hof-filters">
                    <div class="h-search-wrap">
                        <i class="fa-solid fa-magnifying-glass"></i>
                        <input type="text" id="alumni-search-input" placeholder="Search by name, company, role..." oninput="debounceAlumniSearch()">
                    </div>
                    <select id="alumni-company-filter" class="h-select" onchange="fetchAlumniExperiences()">
                        <option value="all">All Companies</option>
                        <option value="Amazon">Amazon</option>
                        <option value="Google">Google</option>
                        <option value="TCS">TCS</option>
                        <option value="Infosys">Infosys</option>
                    </select>
                    <select id="alumni-difficulty-filter" class="h-select" onchange="fetchAlumniExperiences()">
                        <option value="all">All Difficulties</option>
                        <option value="Hard">High Bar (Hard)</option>
                        <option value="Medium">Standard (Medium)</option>
                        <option value="Easy">Foundation (Easy)</option>
                    </select>
                </div>

                <!-- Alumni Grid -->
                <div class="hof-grid" id="alumni-feed-container">
                    <!-- Javascript will inject the cards here -->
                </div>
                
            </div>
        </section>
"""

# Replace `<section id="section-alumni" class="app-section">` down to the next section or `</section>`
pattern = re.compile(r'<section id="section-alumni" class="app-section">.*?</section>', re.DOTALL)
if pattern.search(content):
    content = pattern.sub(new_html, content)
    with open(html_filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced section-alumni HTML in index.html")
else:
    print("Regex failed to find alumni block.")
