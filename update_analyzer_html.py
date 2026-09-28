import re

html_filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\index.html'

with open(html_filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_html = """
        <section id="section-analyzer" class="app-section">
            
            <!-- ANALYZER HERO SECTION -->
            <div class="analyzer-hero">
                <div class="analyzer-hero-left">
                    <div class="a-badge">
                        <i class="fa-solid fa-sparkles"></i> AI-Powered Resume Analysis
                    </div>
                    <h2 class="a-title">AI Resume PDF Analyzer &<br><span class="gradient-text">45-Company Matcher</span></h2>
                    <p class="a-desc">
                        Upload your resume PDF to extract skills, evaluate ATS readiness, and compare directly against 45 company hiring requirements and candidate cohort benchmarks.
                    </p>
                </div>
                <div class="analyzer-hero-right">
                    <!-- Floating Dashboard Cards (CSS Only) -->
                    <div class="a-float-card ats-card">
                        <div style="font-size: 0.8rem; font-weight: 600; text-align: center; margin-bottom: 0.8rem; color: var(--text-primary);">ATS Score</div>
                        <div class="v-score-circle large" style="margin: 0 auto; width: 80px; height: 80px; border: 4px solid var(--accent-emerald);">
                            <span style="font-size: 1.8rem; font-weight: 800; color: var(--text-primary);">82</span>
                        </div>
                        <div style="color: var(--accent-emerald); font-size: 0.85rem; font-weight: 700; text-align: center; margin-top: 0.8rem;">
                            <i class="fa-solid fa-arrow-trend-up"></i> Good Match
                        </div>
                    </div>
                    <div class="a-float-card company-card">
                        <div class="c-match-row">
                            <div class="c-icon" style="color: #EF4444; background: rgba(239,68,68,0.1);">T</div>
                            <div class="c-info">
                                <span class="c-name">TCS</span>
                                <span class="c-score">92% Match</span>
                            </div>
                        </div>
                        <div class="c-match-row">
                            <div class="c-icon" style="color: #3B82F6; background: rgba(59,130,246,0.1);">I</div>
                            <div class="c-info">
                                <span class="c-name">Infosys</span>
                                <span class="c-score">86% Match</span>
                            </div>
                        </div>
                        <div class="c-match-row">
                            <div class="c-icon" style="color: #F59E0B; background: rgba(245,158,11,0.1);">A</div>
                            <div class="c-info">
                                <span class="c-name">Amazon</span>
                                <span class="c-score">78% Match</span>
                            </div>
                        </div>
                        <div class="c-match-row">
                            <div class="c-icon" style="color: #10B981; background: rgba(16,185,129,0.1);">G</div>
                            <div class="c-info">
                                <span class="c-name">Google</span>
                                <span class="c-score">74% Match</span>
                            </div>
                        </div>
                        <div class="c-match-row">
                            <div class="c-icon" style="color: #8B5CF6; background: rgba(139,92,246,0.1);">M</div>
                            <div class="c-info">
                                <span class="c-name">Microsoft</span>
                                <span class="c-score">71% Match</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- UPLOAD & INFO SECTION -->
            <div class="analyzer-main-grid">
                
                <!-- MAIN RESUME UPLOAD CARD -->
                <div class="upload-panel">
                    <div class="upload-chips">
                        <div class="u-chip red"><i class="fa-solid fa-file-pdf"></i> PDF Upload</div>
                        <div class="u-chip green"><i class="fa-solid fa-shield-halved"></i> Malware Protection (DOCX Blocked)</div>
                        <div class="u-chip blue"><i class="fa-solid fa-magnifying-glass-chart"></i> AI Resume Verifier Active</div>
                        <div class="u-chip purple"><i class="fa-solid fa-file-circle-check"></i> PDF Only Accepted</div>
                    </div>
                    
                    <div class="upload-dropzone" id="drop-zone" onclick="document.getElementById('resume-file-input').click()">
                        <input type="file" id="resume-file-input" accept=".pdf,application/pdf" style="display:none" onchange="handleFileSelected(event)">
                        <div class="dz-icon"><i class="fa-solid fa-cloud-arrow-up"></i></div>
                        <h3 class="dz-title">Drag & Drop your Resume PDF here</h3>
                        <p class="dz-sub">or <span class="dz-link">click to browse from your computer</span></p>
                        <p class="dz-meta">Standard PDF resume format supported (up to 16MB) | .docx & Word files are blocked</p>
                        <div id="selected-file-info" class="selected-file-info" style="display:none;"></div>
                    </div>
                    
                    <div class="upload-actions">
                        <div class="sample-loader-dropdown">
                            <button class="btn btn-outline" onclick="toggleSampleMenu()">
                                <i class="fa-solid fa-file-lines"></i> Load Sample PDF Resume
                            </button>
                            <div class="dropdown-menu" id="sample-menu">
                                <div class="dropdown-item" onclick="loadSampleResume('fullstack')">
                                    <i class="fa-solid fa-layer-group"></i> Full Stack Developer (React / Node)
                                </div>
                                <div class="dropdown-item" onclick="loadSampleResume('aiml')">
                                    <i class="fa-solid fa-brain"></i> AI / ML &amp; Data Science
                                </div>
                                <div class="dropdown-item" onclick="loadSampleResume('fresher_dsa')">
                                    <i class="fa-solid fa-code"></i> Fresher SDE (DSA &amp; C++/Java)
                                </div>
                            </div>
                        </div>
                        
                        <button class="btn btn-primary btn-gradient" id="btn-analyze-resume" onclick="submitResumeAnalysis()">
                            <i class="fa-solid fa-wand-magic-sparkles"></i> Analyze Resume PDF & Match 45 Recruiters <i class="fa-solid fa-arrow-right"></i>
                        </button>
                    </div>
                </div>
                
                <!-- RIGHT-SIDE INFORMATION CARD -->
                <div class="info-panel">
                    <h3 class="info-title">What You'll Get</h3>
                    <div class="info-row">
                        <div class="info-icon blue"><i class="fa-solid fa-chart-column"></i></div>
                        <div class="info-text">
                            <h4>Detailed Resume Analysis</h4>
                            <p>ATS score, skill mapping, formatting gaps & improvement tips.</p>
                        </div>
                    </div>
                    <div class="info-row">
                        <div class="info-icon green"><i class="fa-solid fa-building"></i></div>
                        <div class="info-text">
                            <h4>Company Match (45 Recruiters)</h4>
                            <p>See which companies you can apply to based on your profile.</p>
                        </div>
                    </div>
                    <div class="info-row">
                        <div class="info-icon purple"><i class="fa-solid fa-bullseye"></i></div>
                        <div class="info-text">
                            <h4>Skill & Keyword Insights</h4>
                            <p>Find missing skills and get AI-powered suggestions.</p>
                        </div>
                    </div>
                    <div class="info-row">
                        <div class="info-icon orange"><i class="fa-solid fa-lightbulb"></i></div>
                        <div class="info-text">
                            <h4>Actionable Recommendations</h4>
                            <p>Get a personalized roadmap to improve your chances.</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- BOTTOM STATISTICS -->
            <div class="stats-row">
                <div class="stat-card">
                    <div class="stat-icon blue"><i class="fa-solid fa-city"></i></div>
                    <div class="stat-content">
                        <h3>45</h3>
                        <p><strong>Companies Analyzed</strong><br>TCS, Infosys, Amazon, Google & more</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon green"><i class="fa-solid fa-user-check"></i></div>
                    <div class="stat-content">
                        <h3>98%</h3>
                        <p><strong>ATS Compatibility Check</strong><br>Industry-standard evaluation</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon purple"><i class="fa-solid fa-chart-line"></i></div>
                    <div class="stat-content">
                        <h3>Personalized Matches</h3>
                        <p><strong>Company-wise fitment</strong><br>Find your best opportunities</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon orange"><i class="fa-solid fa-file-contract"></i></div>
                    <div class="stat-content">
                        <h3>Improvement Tips</h3>
                        <p><strong>Get actionable suggestions</strong><br>Boost your resume score</p>
                    </div>
                </div>
            </div>

"""

pattern = re.compile(r'<section id="section-analyzer" class="app-section">.*?<!-- Analysis Loading Indicator -->', re.DOTALL)
if pattern.search(content):
    content = pattern.sub(new_html + '            <!-- Analysis Loading Indicator -->', content)
    with open(html_filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced analyzer section in index.html")
else:
    print("Could not find section-analyzer regex match.")
