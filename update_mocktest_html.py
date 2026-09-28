import re

html_filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\index.html'

with open(html_filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_html = """
        <section id="section-mocktest" class="app-section">
            
            <!-- HERO SECTION -->
            <div class="mocktest-hero">
                <div class="mocktest-hero-left">
                    <div class="m-badge">
                        <i class="fa-solid fa-bolt"></i> Practice Smarter, Get Hired Faster
                    </div>
                    <h2 class="m-title">Adaptive Skill & Certification<br><span class="gradient-text">Mock Test</span></h2>
                    <p class="m-desc">
                        Real-time online technical assessments dynamically created from your resume skills, certifications, and live industry question feeds.
                    </p>
                </div>
                <div class="mocktest-hero-right">
                    <!-- Abstract UI Composition -->
                    <div class="m-abstract-card">
                        <div class="m-abs-header"><i class="fa-solid fa-brain"></i> AI Assessment</div>
                        <div class="m-abs-body">
                            <div class="m-abs-line"></div>
                            <div class="m-abs-line short"></div>
                            <div class="m-abs-line"></div>
                            <div class="m-abs-line shorter"></div>
                        </div>
                        <div class="m-abs-footer">
                            <span class="m-abs-tag">12 Questions</span>
                            <span class="m-abs-tag outline">Adaptive</span>
                        </div>
                    </div>
                    
                    <div class="m-float-card fc-1">
                        <i class="fa-solid fa-code text-blue"></i> Real Questions
                    </div>
                    <div class="m-float-card fc-2">
                        <i class="fa-solid fa-robot text-purple"></i> AI Personalized
                    </div>
                    <div class="m-float-card fc-3">
                        <i class="fa-solid fa-chart-pie text-orange"></i> Detailed Feedback
                    </div>
                </div>
            </div>

            <!-- MAIN CONFIGURATION CARD -->
            <div id="mocktest-config-wrapper" class="mocktest-main-card">
                <div class="m-card-header">
                    <div class="m-header-left">
                        <div class="m-header-icon"><i class="fa-solid fa-sliders"></i></div>
                        <div>
                            <h3 class="m-header-title">Test Configuration</h3>
                            <p class="m-header-sub">Customize your mock test or let AI analyze your resume and create the perfect test for you.</p>
                        </div>
                    </div>
                    <div class="m-header-right">
                        <i class="fa-solid fa-sparkles"></i>
                        <div>
                            <strong>Powered by AI</strong>
                            <span>Questions tailored to your resume skills & latest industry patterns</span>
                        </div>
                    </div>
                </div>

                <div class="m-config-grid">
                    <!-- LEFT COLUMN -->
                    <div class="m-config-left">
                        <!-- STEP 1 -->
                        <div class="m-step-group">
                            <div class="m-step-header">
                                <span class="m-step-number">1</span>
                                <div>
                                    <h4>Target Skills / Technologies</h4>
                                    <p>Select the skills you want to be tested on (auto-detected from your resume)</p>
                                </div>
                            </div>
                            <div class="m-step-content" id="mocktest-tags-container">
                                <!-- Tags injected by JS -->
                            </div>
                            <!-- JS Will inject Add Custom Skill button here if needed -->
                        </div>

                        <!-- STEP 3 (Upload Resume) -->
                        <div class="m-step-group mt-5">
                            <div class="m-step-header">
                                <span class="m-step-number">3</span>
                                <div>
                                    <h4>Upload Resume (Optional)</h4>
                                    <p>Upload your resume to get more personalized and relevant questions</p>
                                </div>
                            </div>
                            <div class="m-step-content">
                                <div class="m-mini-upload" onclick="navigateTo('analyzer')">
                                    <div class="m-mini-upload-left">
                                        <div class="m-mini-icon"><i class="fa-solid fa-cloud-arrow-up"></i></div>
                                        <div>
                                            <strong>Drag & drop your resume PDF here</strong>
                                            <span>or click to browse</span>
                                        </div>
                                    </div>
                                    <button class="btn btn-outline btn-sm"><i class="fa-solid fa-rotate"></i> Re-scan / Update Resume</button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- RIGHT COLUMN -->
                    <div class="m-config-right">
                        <!-- STEP 2 -->
                        <div class="m-step-group">
                            <div class="m-step-header">
                                <span class="m-step-number">2</span>
                                <div>
                                    <h4>Test Settings</h4>
                                    <p>Configure your mock test parameters</p>
                                </div>
                            </div>
                            <div class="m-step-content m-settings-list">
                                <div class="m-setting-item">
                                    <label><i class="fa-solid fa-list-ol"></i> Number of Questions</label>
                                    <select id="mocktest-count-select" class="form-select m-select">
                                        <option value="10">10 Questions (Quick 10-Minute Assessment)</option>
                                        <option value="12" selected>12 Questions (Standard 12-Minute Mock)</option>
                                        <option value="15">15 Questions (Full Comprehensive Mock)</option>
                                    </select>
                                </div>
                                <div class="m-setting-item">
                                    <label><i class="fa-solid fa-gauge-high"></i> Difficulty Level</label>
                                    <select id="mocktest-difficulty-select" class="form-select m-select">
                                        <option value="all" selected>Adaptive / Mixed (All Levels)</option>
                                        <option value="Easy">Foundation / Easy</option>
                                        <option value="Medium">Interview Standard (Medium)</option>
                                        <option value="Hard">Advanced / High Bar (Hard)</option>
                                    </select>
                                </div>
                                <div class="m-setting-item">
                                    <label><i class="fa-solid fa-briefcase"></i> Target Career Track</label>
                                    <select id="mocktest-role-select" class="form-select m-select">
                                        <option value="Software Engineer" selected>Software Development Engineer (SDE)</option>
                                        <option value="Full Stack Developer">Full Stack Web Developer</option>
                                        <option value="Backend Developer">Backend Engineer (Python / Java / Node)</option>
                                        <option value="AI / ML Engineer">AI / ML & Data Science</option>
                                        <option value="Cloud & DevOps">Cloud & DevOps Engineer</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        <!-- CTA -->
                        <button class="m-btn-start" id="btn-start-mocktest" onclick="generateAndStartMockTest()">
                            <i class="fa-solid fa-play"></i> Start Mock Test (10-15 Questions) <i class="fa-solid fa-arrow-right" style="margin-left: auto;"></i>
                        </button>
                    </div>
                </div>
            </div>

            <!-- BOTTOM FEATURE CARDS -->
            <div class="m-features-row">
                <div class="m-feature-card">
                    <div class="m-feat-icon green"><i class="fa-solid fa-brain"></i></div>
                    <div class="m-feat-text">
                        <h4>AI-Powered Questions</h4>
                        <p>Based on your resume & latest trends</p>
                    </div>
                </div>
                <div class="m-feature-card">
                    <div class="m-feat-icon blue"><i class="fa-solid fa-layer-group"></i></div>
                    <div class="m-feat-text">
                        <h4>Multiple Difficulty Levels</h4>
                        <p>Easy, Medium, Hard & Adaptive</p>
                    </div>
                </div>
                <div class="m-feature-card">
                    <div class="m-feat-icon orange"><i class="fa-solid fa-building"></i></div>
                    <div class="m-feat-text">
                        <h4>Industry Relevant</h4>
                        <p>Questions from top companies</p>
                    </div>
                </div>
                <div class="m-feature-card">
                    <div class="m-feat-icon purple"><i class="fa-solid fa-chart-column"></i></div>
                    <div class="m-feat-text">
                        <h4>Detailed Performance Report</h4>
                        <p>Know your strengths & weak areas</p>
                    </div>
                </div>
            </div>

            <!-- 2. Loading State (Preserved) -->
"""

# Replace the content safely
# We need to find `<section id="section-mocktest" class="app-section">` down to `<!-- 2. Loading State -->`
pattern = re.compile(r'<section id="section-mocktest" class="app-section">.*?<!-- 2. Loading State -->', re.DOTALL)
if pattern.search(content):
    content = pattern.sub(new_html, content)
    with open(html_filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced section-mocktest HTML in index.html")
else:
    # Maybe it uses `<!-- 2. Loading State -->`? Let's check string.
    print("Regex failed to find mocktest block.")
