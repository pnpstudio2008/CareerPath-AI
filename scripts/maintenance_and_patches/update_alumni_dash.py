import re

html_filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\alumni_profile.html'

with open(html_filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_html = """
    <!-- Main Content Container -->
    <main class="container alumni-main-container" style="max-width: 1300px; margin: 0 auto; padding: 2rem 1.5rem;">
        
        <!-- NEW PREMIUM ALUMNI HERO -->
        <div class="alumni-premium-hero">
            <div class="ap-hero-bg"></div>
            <div class="ap-hero-content">
                <div class="ap-profile-main">
                    <div class="ap-avatar">{{ alumni.initials or alumni.name[:2].upper() }}</div>
                    <div class="ap-profile-info">
                        <div class="ap-name-row">
                            <h1 class="ap-name">{{ alumni.name }}</h1>
                            <span class="ap-verified-badge"><i class="fa-solid fa-certificate"></i> Verified Alumni Mentor</span>
                        </div>
                        <div class="ap-chips-row">
                            <span class="ap-chip"><i class="fa-solid fa-id-card text-blue"></i> Roll No: {{ alumni.roll_no }}</span>
                            <span class="ap-chip"><i class="fa-solid fa-building text-purple"></i> {{ alumni.company }}</span>
                            <span class="ap-chip"><i class="fa-solid fa-briefcase text-blue"></i> {{ alumni.role }}</span>
                            <span class="ap-chip"><i class="fa-solid fa-indian-rupee-sign text-emerald"></i> ₹{{ alumni.package_lpa }} LPA</span>
                            <span class="ap-chip"><i class="fa-solid fa-calendar text-orange"></i> Class of {{ alumni.batch_year }}</span>
                        </div>
                        <div class="ap-actions-row">
                            <a href="https://www.linkedin.com/search/results/all/?keywords={{ alumni.name|urlencode }}%20{{ alumni.company|urlencode }}" target="_blank" class="ap-btn-primary">
                                <i class="fa-brands fa-linkedin"></i> My LinkedIn Profile
                            </a>
                            <a href="/?view=platform#alumni" class="ap-btn-secondary">
                                <i class="fa-solid fa-book-open"></i> Published Story
                            </a>
                        </div>
                    </div>
                </div>
                <div class="ap-quote-card">
                    <i class="fa-solid fa-quote-left ap-quote-icon"></i>
                    <p class="ap-quote-text">Helping juniors grow, because someone once helped me.</p>
                    <span class="ap-quote-label"><i class="fa-solid fa-star"></i> Give Back • Guide • Grow</span>
                </div>
            </div>
        </div>

        <!-- NEW METRICS ROW -->
        <div class="ap-metrics-grid">
            <!-- Mail Inquiries -->
            <div class="ap-metric-card">
                <div class="ap-metric-header">
                    <div class="ap-m-icon" style="background:#FEE2E2; color:#EF4444;"><i class="fa-brands fa-google"></i></div>
                    <span class="ap-m-label">Mail / Gmail Inquiries</span>
                    <i class="fa-solid fa-chevron-right ap-m-arrow"></i>
                </div>
                <div class="ap-metric-body">
                    <h2 class="ap-m-value">{{ metrics.gmail_inquiries }}</h2>
                    <span class="ap-m-trend neutral"><i class="fa-solid fa-arrow-right"></i> —</span>
                    <div class="ap-sparkline red"></div>
                </div>
            </div>

            <!-- LinkedIn -->
            <div class="ap-metric-card">
                <div class="ap-metric-header">
                    <div class="ap-m-icon" style="background:#DBEAFE; color:#3B82F6;"><i class="fa-brands fa-linkedin"></i></div>
                    <span class="ap-m-label">LinkedIn Approaches</span>
                    <i class="fa-solid fa-chevron-right ap-m-arrow"></i>
                </div>
                <div class="ap-metric-body">
                    <h2 class="ap-m-value">{{ metrics.linkedin_approaches }}</h2>
                    <span class="ap-m-trend neutral"><i class="fa-solid fa-arrow-right"></i> —</span>
                    <div class="ap-sparkline blue"></div>
                </div>
            </div>

            <!-- Juniors Assisted -->
            <div class="ap-metric-card">
                <div class="ap-metric-header">
                    <div class="ap-m-icon" style="background:#D1FAE5; color:#10B981;"><i class="fa-solid fa-users"></i></div>
                    <span class="ap-m-label">Total Juniors Assisted</span>
                    <i class="fa-solid fa-chevron-right ap-m-arrow"></i>
                </div>
                <div class="ap-metric-body">
                    <h2 class="ap-m-value">{{ metrics.total_approached }}</h2>
                    <span class="ap-m-trend neutral"><i class="fa-solid fa-arrow-right"></i> —</span>
                    <div class="ap-sparkline green"></div>
                </div>
            </div>

            <!-- Helpful Votes -->
            <div class="ap-metric-card">
                <div class="ap-metric-header">
                    <div class="ap-m-icon" style="background:#F3E8FF; color:#8B5CF6;"><i class="fa-solid fa-heart"></i></div>
                    <span class="ap-m-label">Helpful Story Votes</span>
                    <i class="fa-solid fa-chevron-right ap-m-arrow"></i>
                </div>
                <div class="ap-metric-body">
                    <h2 class="ap-m-value">{{ metrics.story_upvotes }}</h2>
                    <span class="ap-m-trend neutral"><i class="fa-solid fa-arrow-right"></i> —</span>
                    <div class="ap-sparkline purple"></div>
                </div>
            </div>
        </div>

        <!-- MAIN DASHBOARD GRID (3-Column) -->
        <div class="ap-dashboard-grid">
            <!-- Left: Senior Profile -->
            <div class="ap-panel ap-profile-panel">
                <div class="ap-panel-header">
                    <div class="ap-panel-title">
                        <i class="fa-solid fa-user text-primary"></i> Senior Profile & Career Record
                    </div>
                    <div class="ap-panel-actions">
                        <span class="ap-verified-badge small">Verified Alumni <i class="fa-solid fa-check"></i></span>
                        <button class="ap-btn-edit" onclick="openProfileEditModal()"><i class="fa-solid fa-pen"></i> Edit</button>
                    </div>
                </div>
                <div class="ap-profile-table">
                    <div class="ap-row"><div class="ap-label"><i class="fa-solid fa-user"></i> Full Name</div><div class="ap-val">{{ alumni.name }}</div></div>
                    <div class="ap-row"><div class="ap-label"><i class="fa-solid fa-id-card"></i> Alumni User ID</div><div class="ap-val">{{ alumni.roll_no }}</div></div>
                    <div class="ap-row"><div class="ap-label"><i class="fa-solid fa-envelope"></i> Email Address</div><div class="ap-val">{{ alumni.email }}</div></div>
                    <div class="ap-row"><div class="ap-label"><i class="fa-solid fa-building-columns"></i> Department</div><div class="ap-val">{{ alumni.branch }}</div></div>
                    <div class="ap-row"><div class="ap-label"><i class="fa-solid fa-briefcase"></i> Current Role</div><div class="ap-val">{{ alumni.role }}</div></div>
                    <div class="ap-row"><div class="ap-label"><i class="fa-solid fa-building"></i> Current Company</div><div class="ap-val"><strong>{{ alumni.company }}</strong></div></div>
                </div>
            </div>

            <!-- Center: Outreach Channels -->
            <div class="ap-panel ap-chart-panel">
                <div class="ap-panel-header">
                    <div class="ap-panel-title"><i class="fa-solid fa-chart-pie text-primary"></i> Outreach Channels</div>
                </div>
                <div class="ap-donut-container">
                    <svg viewBox="0 0 36 36" class="ap-donut-svg">
                        <!-- Conic chart will be rendered by CSS or JS, fallback to simple SVG rings -->
                        <path class="ap-donut-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                        <!-- dynamic portions set via inline styles later -->
                        <path class="ap-donut-segment red" stroke-dasharray="{{ metrics.channel_ratio.gmail_pct }}, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                        <path class="ap-donut-segment blue" stroke-dasharray="{{ metrics.channel_ratio.linkedin_pct }}, 100" stroke-dashoffset="-{{ metrics.channel_ratio.gmail_pct }}" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                    </svg>
                    <div class="ap-donut-center">
                        <strong>{{ metrics.total_approached }}</strong>
                        <span>Total<br>Approaches</span>
                    </div>
                </div>
                <div class="ap-chart-legend">
                    <div class="ap-legend-item"><div class="ap-dot red"></div> Gmail <span>{{ metrics.gmail_inquiries }} ({{ metrics.channel_ratio.gmail_pct }}%)</span></div>
                    <div class="ap-legend-item"><div class="ap-dot blue"></div> LinkedIn <span>{{ metrics.linkedin_approaches }} ({{ metrics.channel_ratio.linkedin_pct }}%)</span></div>
                </div>
                <p class="ap-chart-sub">Distribution of student approaches via Mail vs LinkedIn.</p>
            </div>

            <!-- Right: Recent Activity -->
            <div class="ap-panel ap-activity-panel">
                <div class="ap-panel-header">
                    <div class="ap-panel-title"><i class="fa-solid fa-clock text-primary"></i> Recent Activity</div>
                    <i class="fa-solid fa-chevron-right ap-icon-btn"></i>
                </div>
                <div class="ap-activity-feed">
                    {% if metrics.inquiries|length == 0 %}
                    <div class="ap-activity-empty">
                        <i class="fa-solid fa-inbox"></i>
                        <span>No recent activity</span>
                        <small>Your alumni activity will appear here.</small>
                    </div>
                    {% else %}
                        {% for inq in metrics.inquiries[:4] %}
                        <div class="ap-activity-item">
                            {% if inq.channel == 'gmail' %}
                            <div class="ap-act-icon red"><i class="fa-brands fa-google"></i></div>
                            {% else %}
                            <div class="ap-act-icon blue"><i class="fa-brands fa-linkedin"></i></div>
                            {% endif %}
                            <div class="ap-act-info">
                                <strong>New {{ inq.channel }} inquiry</strong>
                                <span>{{ inq.student_name }}</span>
                            </div>
                        </div>
                        {% endfor %}
                    {% endif %}
                </div>
            </div>
        </div>

        <!-- EXISTING TABLES (Preserved Functionality) -->
        <div class="portal-grid-2" style="margin-top: 2rem;">
            <!-- Left Column: Junior Student Inquiries & Mentorship Inbox -->
            <div style="display:flex; flex-direction:column; gap:1.5rem;">
                <!-- Card: Junior Student Inquiries & Mentorship Inbox -->
                <div class="card ap-panel">
                    <div class="card-header-flex mb-3">
                        <div>
                            <h3 style="margin-bottom:0.25rem;"><i class="fa-solid fa-inbox text-primary"></i> Junior Student Mentorship Requests</h3>
                            <p class="text-muted" style="font-size:0.85rem; margin:0;">Students who approached via Gmail and LinkedIn for guidance.</p>
                        </div>
                        <span class="badge badge-purple">{{ metrics.inquiries|length }} Total Requests</span>
                    </div>

                    <!-- Filter Tabs -->
                    <div class="inquiry-filter-tabs">
                        <button class="inquiry-filter-btn active" onclick="filterInquiries('all', this)">All</button>
                        <button class="inquiry-filter-btn" onclick="filterInquiries('gmail', this)"><i class="fa-brands fa-google text-danger"></i> Gmail</button>
                        <button class="inquiry-filter-btn" onclick="filterInquiries('linkedin', this)"><i class="fa-brands fa-linkedin text-info"></i> LinkedIn</button>
                        <button class="inquiry-filter-btn" onclick="filterInquiries('Pending', this)"><i class="fa-solid fa-clock text-warning"></i> Pending</button>
                        <button class="inquiry-filter-btn" onclick="filterInquiries('Replied', this)"><i class="fa-solid fa-check text-info"></i> Replied</button>
                    </div>

                    <!-- Table -->
                    <div class="data-table-container">
                        <table class="inquiry-table">
                            <thead>
                                <tr>
                                    <th>Student</th>
                                    <th>Channel</th>
                                    <th>Target Role</th>
                                    <th>Query Topic</th>
                                    <th>Status</th>
                                    <th style="text-align:right;">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for inq in metrics.inquiries %}
                                <tr class="inquiry-row" data-channel="{{ inq.channel }}" data-status="{{ inq.status }}">
                                    <td>
                                        <strong>{{ inq.student_name }}</strong>
                                        <div class="text-muted" style="font-size:0.75rem;">{{ inq.student_branch }} ('{{ inq.student_batch[-2:] }}')</div>
                                    </td>
                                    <td>
                                        {% if inq.channel == 'gmail' %}
                                        <span class="badge" style="background:rgba(234,67,53,0.12); color:#EA4335; border:1px solid rgba(234,67,53,0.3); font-size:0.75rem;"><i class="fa-brands fa-google"></i> Gmail</span>
                                        {% else %}
                                        <span class="badge" style="background:rgba(10,102,194,0.12); color:#0A66C2; border:1px solid rgba(10,102,194,0.3); font-size:0.75rem;"><i class="fa-brands fa-linkedin"></i> LinkedIn</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        <span style="font-size:0.82rem; font-weight:600; color:var(--primary);">{{ inq.target_company }}</span>
                                    </td>
                                    <td style="max-width:260px;">
                                        <div style="font-size:0.82rem; color:var(--text-secondary); line-height:1.35;">{{ inq.query_topic }}</div>
                                    </td>
                                    <td>
                                        {% if inq.status == 'Pending' %}
                                        <span class="badge badge-warning" id="status-tag-{{ inq.id }}"><i class="fa-solid fa-clock"></i> Pending</span>
                                        {% elif inq.status == 'Replied' %}
                                        <span class="badge badge-info" id="status-tag-{{ inq.id }}"><i class="fa-solid fa-check"></i> Replied</span>
                                        {% else %}
                                        <span class="badge badge-success" id="status-tag-{{ inq.id }}"><i class="fa-solid fa-circle-check"></i> Done</span>
                                        {% endif %}
                                    </td>
                                    <td style="text-align:right; white-space:nowrap;">
                                        {% if inq.channel == 'gmail' %}
                                        <a href="mailto:{{ inq.student_email }}?subject=Placement Guidance - {{ inq.target_company }}&body=Hi {{ inq.student_name }},%0D%0A%0D%0ARegarding your mentorship inquiry on {{ inq.query_topic }}..." class="btn btn-sm btn-primary" style="padding:0.25rem 0.55rem; font-size:0.76rem;" onclick="markReplied({{ inq.id }})">
                                            <i class="fa-brands fa-google"></i> Reply
                                        </a>
                                        {% else %}
                                        <a href="https://www.linkedin.com/search/results/all/?keywords={{ inq.student_name }}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-linkedin-action" style="padding:0.25rem 0.55rem; font-size:0.76rem;" onclick="markReplied({{ inq.id }})">
                                            <i class="fa-brands fa-linkedin"></i> Connect
                                        </a>
                                        {% endif %}
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Right Column: Contributed Questions & Fast Actions -->
            <div style="display:flex; flex-direction:column; gap:1.5rem;">
                
                <!-- Card: Placement Test Questions Contributed -->
                <div class="card ap-panel">
                    <div class="card-header-flex mb-3">
                        <div>
                            <h3 style="margin-bottom:0.25rem;"><i class="fa-solid fa-code-branch text-primary"></i> Contributed Questions</h3>
                            <p class="text-muted" style="font-size:0.85rem; margin:0;">Share technical MCQs.</p>
                        </div>
                        <button class="btn btn-primary btn-sm" onclick="openContributeQuestionModal()">
                            <i class="fa-solid fa-plus"></i> Add
                        </button>
                    </div>

                    <div class="data-table-container">
                        <table class="inquiry-table" style="min-width: 100%;">
                            <thead>
                                <tr>
                                    <th>Subject</th>
                                    <th>Question</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody id="alumni-questions-tbody">
                                <tr><td colspan="3" class="text-center p-3 text-muted"><div class="spinner"></div> Loading contributed questions...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Card: Fast Action Shortcuts -->
                <div class="card ap-panel">
                    <h3 style="margin-bottom:1.25rem;"><i class="fa-solid fa-rocket text-warning"></i> Fast Actions</h3>
                    <div style="display:flex; flex-direction:column; gap:1rem;">
                        <a href="/?view=platform#alumni" class="quick-action-card">
                            <div class="action-icon" style="background:#8B5CF6;"><i class="fa-solid fa-users-viewfinder"></i></div>
                            <div>
                                <strong style="display:block; font-size:0.95rem;">Alumni Placement Hub</strong>
                                <span class="text-muted" style="font-size:0.8rem;">Browse placement stories & archives.</span>
                            </div>
                        </a>
                        <a href="/?view=platform#analyzer" class="quick-action-card">
                            <div class="action-icon bg-primary"><i class="fa-solid fa-file-arrow-up"></i></div>
                            <div>
                                <strong style="display:block; font-size:0.95rem;">Resume ATS Benchmark</strong>
                                <span class="text-muted" style="font-size:0.8rem;">Evaluate resumes against standards.</span>
                            </div>
                        </a>
                    </div>
                </div>

            </div>
        </div>
    </main>

    <!-- Placeholder Modal for Profile Edit -->
    <div class="modal-backdrop" id="edit-profile-modal-backdrop" onclick="closeProfileEditModal(event)">
        <div class="modal-content" style="max-width: 500px;">
            <button class="modal-close-btn" onclick="closeProfileEditModal(event)">&times;</button>
            <h2 style="font-size:1.5rem; margin-bottom:1rem;"><i class="fa-solid fa-pen text-primary"></i> Edit Profile</h2>
            <p class="text-muted mb-4">Profile editing functionality is connected to your university SSO. Contact administration to update core details.</p>
            <button class="btn btn-outline w-100" onclick="closeProfileEditModal(event, true)">Close</button>
        </div>
    </div>
"""

# Replace `<main class="container alumni-main-container"...` down to `<!-- Contribute Question Modal -->`
pattern = re.compile(r'<!-- Main Content Container -->\s*<main class="container alumni-main-container".*?</main>', re.DOTALL)
if pattern.search(content):
    content = pattern.sub(new_html, content)
    
    # Also inject a tiny script for the edit modal
    script_inject = """
        function openProfileEditModal() {
            const modal = document.getElementById('edit-profile-modal-backdrop');
            if(modal) modal.classList.add('active');
        }
        function closeProfileEditModal(event, force=false) {
            if(force || event.target === document.getElementById('edit-profile-modal-backdrop') || event.target.classList.contains('modal-close-btn')) {
                document.getElementById('edit-profile-modal-backdrop').classList.remove('active');
            }
        }
    """
    content = content.replace('// ALUMNI CONTRIBUTED QUESTIONS HANDLERS', script_inject + '\n        // ALUMNI CONTRIBUTED QUESTIONS HANDLERS')
    
    with open(html_filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced main container in alumni_profile.html")
else:
    print("Regex failed to find main content block.")
