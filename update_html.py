import re

def update_html():
    filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\index.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We will replace the entire <section id="section-home">...</section>
    
    new_home_section = """
        <section id="section-home" class="app-section active">
            
            <!-- HERO SECTION -->
            <div class="saas-hero">
                <div class="saas-hero-content">
                    <div class="hero-badge">
                        <i class="fa-solid fa-sparkles"></i> Next-Gen Campus Placement & Career AI
                    </div>
                    <h1 class="hero-title">
                        Turn Your Resume Into <br/><span class="gradient-text">Real Opportunities</span>
                    </h1>
                    <p class="hero-desc">
                        Get AI-powered resume analysis, personalized career suggestions, company insights and placement-ready preparation — all in one place.
                    </p>
                    <div class="hero-cta-group">
                        <button class="btn btn-primary btn-lg" onclick="navigateTo('analyzer')">
                            <i class="fa-solid fa-upload"></i> Upload & Analyze Resume <i class="fa-solid fa-arrow-right ml-2"></i>
                        </button>
                        <button class="btn btn-outline btn-lg" onclick="navigateTo('mocktest')">
                            <i class="fa-solid fa-play"></i> See How It Works
                        </button>
                    </div>
                    <div class="hero-trust">
                        <div class="avatar-group">
                            <div class="avatar"></div>
                            <div class="avatar"></div>
                            <div class="avatar"></div>
                            <div class="avatar"></div>
                        </div>
                        <span class="text-muted text-sm">Trusted by 10,000+ students</span>
                    </div>
                </div>
                
                <div class="saas-hero-visual">
                    <!-- Dashboard Visual Cluster (CSS Only) -->
                    <div class="visual-card-main">
                        <div class="v-header">
                            <div>
                                <h4 style="margin:0; font-size: 1.1rem; color: var(--text-primary);">{{ user.name if user else 'Student Portal' }}</h4>
                                <span style="font-size: 0.8rem; color: var(--text-muted);">Computer Science Student</span>
                            </div>
                            <div class="v-avatar"><i class="fa-solid fa-user"></i></div>
                        </div>
                        <div class="v-skills mt-3">
                            <span class="v-badge blue">Java</span>
                            <span class="v-badge blue">Python</span>
                            <span class="v-badge blue">Web Development</span>
                            <span class="v-badge outline">AI/ML</span>
                        </div>
                        <div class="v-exp mt-3">
                            <h5 style="font-size: 0.85rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-plus" style="color: var(--primary);"></i> Experience / Projects</h5>
                            <div class="v-exp-item">
                                <i class="fa-solid fa-circle-check text-emerald"></i>
                                <div>
                                    <div style="font-size: 0.85rem; font-weight: 600;">Smart Vehicle Service App</div>
                                    <div style="font-size: 0.75rem; color: var(--text-muted);">Android Studio • Java</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="visual-card-floating top-right">
                        <div style="font-size: 0.8rem; font-weight: 600; text-align: center; margin-bottom: 0.5rem;">Resume Score</div>
                        <div class="v-score-circle">
                            <span style="font-size: 1.5rem; font-weight: 800; color: var(--text-primary);">82</span>
                        </div>
                        <div style="color: var(--accent-emerald); font-size: 0.8rem; font-weight: 600; text-align: center; margin-top: 0.5rem;">
                            <i class="fa-solid fa-sparkles"></i> Excellent
                        </div>
                    </div>
                    
                    <div class="visual-card-floating bottom-right">
                        <div style="font-size: 0.85rem; font-weight: 600; margin-bottom: 0.8rem;">Career Match</div>
                        <div class="v-match-row">
                            <span style="font-size: 0.75rem;">Software Developer</span>
                            <div class="v-bar-bg"><div class="v-bar-fill emerald" style="width: 92%;"></div></div>
                            <span style="font-size: 0.75rem; font-weight: 600;">92%</span>
                        </div>
                        <div class="v-match-row">
                            <span style="font-size: 0.75rem;">AI/ML Intern</span>
                            <div class="v-bar-bg"><div class="v-bar-fill purple" style="width: 85%;"></div></div>
                            <span style="font-size: 0.75rem; font-weight: 600;">85%</span>
                        </div>
                        <div class="v-match-row">
                            <span style="font-size: 0.75rem;">Web Developer</span>
                            <div class="v-bar-bg"><div class="v-bar-fill amber" style="width: 78%;"></div></div>
                            <span style="font-size: 0.75rem; font-weight: 600;">78%</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- FEATURE CARDS -->
            <div class="saas-features-grid mt-5">
                <div class="saas-feature-card" onclick="navigateTo('analyzer')">
                    <div class="sf-icon blue"><i class="fa-solid fa-file-lines"></i></div>
                    <div class="sf-content">
                        <h3>Resume Analysis</h3>
                        <p>Get detailed feedback, skill mapping and improvement suggestions.</p>
                    </div>
                    <div class="sf-arrow"><i class="fa-solid fa-arrow-right"></i></div>
                </div>
                
                <div class="saas-feature-card" onclick="navigateTo('analyzer')">
                    <div class="sf-icon orange"><i class="fa-solid fa-briefcase"></i></div>
                    <div class="sf-content">
                        <h3>Job Recommendations</h3>
                        <p>Find out which job roles you can apply for based on your resume score.</p>
                    </div>
                    <div class="sf-arrow"><i class="fa-solid fa-arrow-right"></i></div>
                </div>
                
                <div class="saas-feature-card" onclick="navigateTo('mocktest')">
                    <div class="sf-icon green"><i class="fa-solid fa-clipboard-question"></i></div>
                    <div class="sf-content">
                        <h3>Mock Tests</h3>
                        <p>Practice topic-wise MCQs from top companies with solutions.</p>
                    </div>
                    <div class="sf-arrow"><i class="fa-solid fa-arrow-right"></i></div>
                </div>
                
                <div class="saas-feature-card" onclick="navigateTo('prep')">
                    <div class="sf-icon purple"><i class="fa-solid fa-building"></i></div>
                    <div class="sf-content">
                        <h3>Company Insights</h3>
                        <p>Explore hiring trends, eligibility criteria and interview patterns.</p>
                    </div>
                    <div class="sf-arrow"><i class="fa-solid fa-arrow-right"></i></div>
                </div>
                
                <div class="saas-feature-card" onclick="navigateTo('alumni')">
                    <div class="sf-icon amber"><i class="fa-solid fa-users"></i></div>
                    <div class="sf-content">
                        <h3>Alumni Hub</h3>
                        <p>Learn from real alumni experiences and get placement tips.</p>
                    </div>
                    <div class="sf-arrow"><i class="fa-solid fa-arrow-right"></i></div>
                </div>
            </div>

            <!-- DASHBOARD SUMMARY SECTION -->
            <div class="saas-dashboard-summary mt-5">
                <div class="summary-welcome">
                    <div>
                        <span class="text-muted text-sm">Good Morning,</span>
                        <h2 style="font-size: 1.5rem; margin: 0.2rem 0; color: var(--text-primary);">{{ user.name if user else 'Student' }} 👋</h2>
                        <p style="font-size: 0.85rem; color: var(--text-secondary); margin: 0;">Let's prepare and get you closer to your dream career.</p>
                    </div>
                </div>
                
                <div class="summary-stats-grid">
                    <div class="summary-stat-card">
                        <div class="ss-icon blue"><i class="fa-solid fa-file-invoice"></i></div>
                        <div class="ss-info">
                            <div class="ss-num">3</div>
                            <div class="ss-label">Resumes Analyzed</div>
                        </div>
                    </div>
                    
                    <div class="summary-stat-card">
                        <div class="ss-icon green"><i class="fa-solid fa-chart-line"></i></div>
                        <div class="ss-info">
                            <div class="ss-num">5</div>
                            <div class="ss-label">Mock Tests Taken</div>
                        </div>
                    </div>
                    
                    <div class="summary-stat-card">
                        <div class="ss-icon purple"><i class="fa-solid fa-bullseye"></i></div>
                        <div class="ss-info">
                            <div class="ss-num">82%</div>
                            <div class="ss-label">Best Score</div>
                        </div>
                    </div>
                    
                    <div class="summary-stat-card">
                        <div class="ss-icon orange"><i class="fa-solid fa-bookmark"></i></div>
                        <div class="ss-info">
                            <div class="ss-num">12</div>
                            <div class="ss-label">Saved Job Roles</div>
                        </div>
                    </div>
                </div>
                
                <div class="summary-action-card">
                    <div class="sac-icon"><i class="fa-solid fa-clipboard-check"></i></div>
                    <div class="sac-content">
                        <h4 style="margin: 0; font-size: 0.9rem;">Your Next Step</h4>
                        <p style="margin: 0.2rem 0 0.8rem 0; font-size: 0.75rem; color: var(--text-muted);">Take a Mock Test on Data Structures to improve your score.</p>
                        <button class="btn btn-primary btn-sm" onclick="navigateTo('mocktest')">Start Practice <i class="fa-solid fa-arrow-right"></i></button>
                    </div>
                </div>
            </div>

        </section>
"""

    # We need to extract everything from <section id="section-home"... to the closing </section>
    pattern = re.compile(r'<section id="section-home" class="app-section active">.*?</section>', re.DOTALL)
    
    if pattern.search(content):
        content = pattern.sub(new_home_section, content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated section-home in index.html")
    else:
        print("Could not find section-home in index.html")

update_html()
