// --- Safe JSON Fetch Wrapper ---
async function safeJsonFetch(response) {
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
        return await response.json();
    } else {
        const text = await response.text();
        console.error("Non-JSON response received:", text.substring(0, 200));
        throw new Error("Server returned an invalid or HTML response. (Possible Network/Server Error)");
    }
}

/**
 * AI Career Companion - Alumni Experience Portal & Leaderboard (Module 4)
 * Modern Olympic Podium & Leaderboard UI per high-fidelity design specifications.
 */

let alumniSearchTimeout = null;
let currentMetricTab = 'experience';
let currentTimeFilter = 'all';
let currentAlumniPage = 1;
const ITEMS_PER_PAGE = 5;

// Base rich performers dataset accurately matching college alumni
const BASE_MOCK_PERFORMERS = [
    {
        id: 1,
        student_name: 'Priya Patel',
        company: 'Google',
        role: 'Software Development Engineer (SDE-1)',
        package_lpa: 35.00,
        batch_year: '2024',
        offer_type: 'On-Campus Placement',
        difficulty: 'Hard',
        email: 'priya.patel@gmail.com',
        avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=256&q=80',
        initials: 'PP',
        xp: '2,569 XP',
        xp_num: 2569,
        badges: 15,
        problems: { easy: 724, medium: 512, hard: 233, total: 1469 },
        achievements_icons: ['<i class="fa-solid fa-trophy text-amber"></i>', '<i class="fa-solid fa-medal text-blue"></i>'],
        achievements_count: 5,
        rounds: [
            { round_name: 'Round 1: Online Coding Assessment', details: 'Solved 2 LeetCode Medium/Hard algorithmic challenges on Graph Traversal and Dynamic Programming with optimal time/space complexity.' },
            { round_name: 'Round 2: Technical Interview 1', details: 'In-depth problem solving on Binary Trees, Maximum Path Sum, and Trie prefix search implementation with live test-case dry running.' },
            { round_name: 'Round 3: Technical Interview 2', details: 'Distributed Systems and Concurrency: Design a resilient cache invalidation pipeline and discuss thread contention with lock-free structures.' },
            { round_name: 'Round 4: Googleyness & Leadership', details: 'Scenario-based behavioral questions on handling ambiguity, cross-team conflict resolution, and commitment to open engineering practices.' }
        ],
        preparation_tips: 'Solved 450+ LeetCode problems with special emphasis on Dynamic Programming, Graphs, and Trees. Practiced writing clean code on Google Docs without IDE auto-complete.',
        advice_to_juniors: 'Never jump straight into writing code. Explain your brute force first, discuss trade-offs, and verify edge cases out loud before typing.'
    },
    {
        id: 2,
        student_name: 'Aarav Sharma',
        company: 'Amazon',
        role: 'Software Development Engineer (SDE-1)',
        package_lpa: 28.50,
        batch_year: '2024',
        offer_type: 'On-Campus Placement',
        difficulty: 'Hard',
        email: 'aarav.sharma@amazon.com',
        avatar: 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=256&q=80',
        initials: 'AS',
        xp: '1,840 XP',
        xp_num: 1840,
        badges: 12,
        problems: { easy: 610, medium: 430, hard: 409, total: 1449 },
        achievements_icons: ['<i class="fa-solid fa-trophy text-blue"></i>', '<i class="fa-solid fa-medal text-silver"></i>'],
        achievements_count: 4,
        rounds: [
            { round_name: 'Round 1: Online Assessment (OA2)', details: 'Two algorithmic coding problems on Monotonic Stack and Sliding Window, followed by Amazon Work Style behavioral simulation.' },
            { round_name: 'Round 2: Technical Round 1', details: 'Data Structures and Algorithms: Solved Top-K Frequent Elements using Min-Heap and discussed complexity optimizations.' },
            { round_name: 'Round 3: Technical Round 2', details: 'Object-Oriented Design & LLD: Designed an extensible Parking Lot system using Factory and Strategy design patterns with database schemas.' },
            { round_name: 'Round 4: Bar Raiser Interview', details: 'Rigorous evaluation across Amazon 16 Leadership Principles using the STAR format, plus past production project architecture breakdown.' }
        ],
        preparation_tips: 'Thoroughly prepared 2-3 detailed stories for each of Amazon 16 Leadership Principles using the STAR method, and mastered the Blind 75 LeetCode list.',
        advice_to_juniors: 'Customer obsession and ownership are real culture pillars at Amazon. Tie every technical trade-off back to how it impacts end-user experience.'
    },
    {
        id: 3,
        student_name: 'Sneha Kulkarni',
        company: 'Microsoft',
        role: 'Software Engineer',
        package_lpa: 32.00,
        batch_year: '2024',
        offer_type: 'On-Campus Placement',
        difficulty: 'Hard',
        email: 'sneha.kulkarni@gmail.com',
        avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=256&q=80',
        initials: 'SK',
        xp: '1,620 XP',
        xp_num: 1620,
        badges: 10,
        problems: { easy: 430, medium: 380, hard: 225, total: 1035 },
        achievements_icons: ['<i class="fa-solid fa-trophy text-amber"></i>', '<i class="fa-solid fa-gem text-emerald"></i>'],
        achievements_count: 3,
        rounds: [
            { round_name: 'Round 1: Operating Systems & DSA', details: 'Process scheduling algorithms, LRU Cache, and semaphore deadlock prevention.' },
            { round_name: 'Round 2: High Level Architecture', details: 'Distributed key-value store with consistent hashing and partition tolerance.' }
        ],
        preparation_tips: 'Master OS concurrency, virtual memory paging, and cloud microservices.',
        advice_to_juniors: 'Know your operating systems and computer network fundamentals inside out.'
    },
    {
        id: 4,
        student_name: 'Karan Mehta',
        company: 'General',
        role: 'Senior Software Engineer',
        package_lpa: 14.00,
        batch_year: '2023',
        offer_type: 'On-Campus Placement',
        difficulty: 'Medium',
        email: 'karan.mehta@gmail.com',
        avatar: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=256&q=80',
        initials: 'KM',
        xp: '1,120 XP',
        xp_num: 1120,
        badges: 8,
        problems: { easy: 390, medium: 280, hard: 205, total: 875 },
        achievements_icons: ['<i class="fa-solid fa-trophy text-amber"></i>', '<i class="fa-solid fa-award text-blue"></i>'],
        achievements_count: 2,
        rounds: [
            { round_name: 'Round 1: Core Python & Backend Architecture', details: 'FastAPI async generators, SQL connection pooling.' },
            { round_name: 'Round 2: Fullstack Integration & Debugging', details: 'Live debugging of race condition in database transactions.' }
        ],
        preparation_tips: 'Deep dive into Python GIL, database indexing, and REST architectural constraints.',
        advice_to_juniors: 'Understand how memory and databases actually work underneath high-level libraries.'
    },
    {
        id: 5,
        student_name: 'Ananya Joshi',
        company: 'Infosys',
        role: 'Specialist Programmer (SP)',
        package_lpa: 10.50,
        batch_year: '2024',
        offer_type: 'On-Campus Placement',
        difficulty: 'Hard',
        email: 'ananya.joshi@gmail.com',
        avatar: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=256&q=80',
        initials: 'AJ',
        xp: '980 XP',
        xp_num: 980,
        badges: 7,
        problems: { easy: 310, medium: 230, hard: 170, total: 710 },
        achievements_icons: ['<i class="fa-solid fa-award text-purple"></i>'],
        achievements_count: 2,
        rounds: [
            { round_name: 'Round 1: HackWithInfy Finalist Round', details: 'Advanced DP and Fenwick tree problem.' },
            { round_name: 'Round 2: Technical Interview', details: 'Java JVM internals, garbage collection tuning, and SQL join algorithms.' }
        ],
        preparation_tips: 'Master Java collection internals, JVM memory model, and SQL join indexes.',
        advice_to_juniors: 'Participate actively in coding contests like HackWithInfy, CodeChef, and LeetCode Biweekly.'
    },
    {
        id: 6,
        student_name: 'Rohan Deshmukh',
        company: 'TCS',
        role: 'TCS Digital Developer',
        package_lpa: 9.00,
        batch_year: '2023',
        offer_type: 'On-Campus Placement',
        difficulty: 'Medium',
        email: 'rohan.deshmukh@gmail.com',
        avatar: 'https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?auto=format&fit=crop&w=256&q=80',
        initials: 'RD',
        xp: '820 XP',
        xp_num: 820,
        badges: 6,
        problems: { easy: 290, medium: 210, hard: 140, total: 640 },
        achievements_icons: ['<i class="fa-solid fa-medal text-blue"></i>'],
        achievements_count: 1,
        rounds: [
            { round_name: 'Round 1: TCS National Qualifier Test (NQT)', details: 'Advanced aptitude, logic puzzles, and two medium DSA questions.' },
            { round_name: 'Round 2: Technical + Managerial Interview', details: 'OOP principles in Java, SQL subqueries, and software engineering life cycle.' }
        ],
        preparation_tips: 'Strengthen quantitative aptitude alongside Java/Python coding fundamentals.',
        advice_to_juniors: 'Dont neglect aptitude and communication skills; they open the door to technical rounds.'
    },
    {
        id: 7,
        student_name: 'Rahul Verma',
        company: 'Accenture',
        role: 'Advanced App Engineering Analyst',
        package_lpa: 6.50,
        batch_year: '2024',
        offer_type: 'On-Campus Placement',
        difficulty: 'Easy',
        email: 'rahul.verma@accenture.com',
        avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=256&q=80',
        initials: 'RV',
        xp: '680 XP',
        xp_num: 680,
        badges: 5,
        problems: { easy: 260, medium: 190, hard: 130, total: 580 },
        achievements_icons: ['<i class="fa-solid fa-award text-amber"></i>'],
        achievements_count: 1,
        rounds: [
            { round_name: 'Round 1: Cognitive & Technical Assessment', details: 'Pseudocode analysis, cloud computing fundamentals, and network basics.' },
            { round_name: 'Round 2: HR + Technical Discussion', details: 'Projects walk-through, database normalization, and behavioral questions.' }
        ],
        preparation_tips: 'Revise DBMS normalization, SDLC agile methodology, and basic data structures.',
        advice_to_juniors: 'Be completely honest on your resume; every project you list will be tested in depth.'
    },
    {
        id: 8,
        student_name: 'Meera Nair',
        company: 'Wipro',
        role: 'Project Engineer (Turbo)',
        package_lpa: 6.50,
        batch_year: '2024',
        offer_type: 'On-Campus Placement',
        difficulty: 'Medium',
        email: 'meera.nair@wipro.com',
        avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=256&q=80',
        initials: 'MN',
        xp: '590 XP',
        xp_num: 590,
        badges: 4,
        problems: { easy: 240, medium: 170, hard: 100, total: 510 },
        achievements_icons: ['<i class="fa-solid fa-award text-blue"></i>'],
        achievements_count: 1,
        rounds: [
            { round_name: 'Round 1: Elite National Talent Hunt', details: 'Quantitative, logical, and hands-on programming problems.' },
            { round_name: 'Round 2: Turbo Upgrade Coding Challenge', details: 'Trees, recursion, and greedy algorithms.' }
        ],
        preparation_tips: 'Solved practice tests on HackerRank and thoroughly reviewed OS paging and database indexing.',
        advice_to_juniors: 'Take the Turbo upgrade test seriously—it elevates the standard offer to a premium technology role.'
    }
];

let allEnrichedAlumni = [...BASE_MOCK_PERFORMERS];

async function fetchAlumniExperiences() {
    try {
        const res = await fetch('/api/alumni/experiences');
        const data = await safeJsonFetch(res);

        if (data.success && Array.isArray(data.experiences) && data.experiences.length > 0) {
            const dbRecords = data.experiences.map((e, idx) => {
                const cleanName = e.student_name || 'Alumni Senior';
                const existing = BASE_MOCK_PERFORMERS.find(p => p.id === e.id || p.student_name.toLowerCase() === cleanName.toLowerCase());
                if (existing) {
                    return {
                        ...existing,
                        ...e,
                        problems: existing.problems,
                        xp: existing.xp,
                        xp_num: existing.xp_num,
                        badges: existing.badges,
                        achievements_icons: existing.achievements_icons,
                        achievements_count: existing.achievements_count,
                        avatar: existing.avatar,
                        initials: existing.initials
                    };
                }
                const parts = cleanName.trim().split(' ');
                const inits = parts.length >= 2 ? (parts[0][0] + parts[1][0]).toUpperCase() : cleanName.slice(0, 2).toUpperCase();
                const pkg = parseFloat(e.package_lpa) || 12.0;
                const calculatedXp = Math.round(pkg * 60) + (100 - idx * 10);
                
                return {
                    id: e.id,
                    student_name: cleanName,
                    company: e.company || 'Top Recruiter',
                    role: e.role || 'Software Engineer',
                    package_lpa: pkg,
                    batch_year: e.batch_year || '2024',
                    offer_type: e.offer_type || 'On-Campus Placement',
                    difficulty: e.difficulty || 'Medium',
                    email: e.email || `${cleanName.toLowerCase().replace(/\s+/g, '.')}@gmail.com`,
                    avatar: `https://images.unsplash.com/photo-${1500000000000 + (idx * 1111111)}?auto=format&fit=crop&w=256&q=80`,
                    initials: inits,
                    xp: `${calculatedXp.toLocaleString()} XP`,
                    xp_num: calculatedXp,
                    badges: Math.max(3, Math.round(pkg / 3)),
                    problems: {
                        easy: Math.round(calculatedXp * 0.45),
                        medium: Math.round(calculatedXp * 0.35),
                        hard: Math.round(calculatedXp * 0.20),
                        total: calculatedXp
                    },
                    achievements_icons: ['<i class="fa-solid fa-award text-blue"></i>'],
                    achievements_count: 1,
                    rounds: e.rounds || [],
                    preparation_tips: e.preparation_tips || 'Systematic problem solving and core computer science fundamentals.',
                    advice_to_juniors: e.advice_to_juniors || 'Focus on consistent practice and clear communication.'
                };
            });

            // Combine prioritizing baseline alumni list
            const combinedMap = new Map();
            BASE_MOCK_PERFORMERS.forEach(item => combinedMap.set(item.id, item));
            dbRecords.forEach(item => {
                const existingKey = Array.from(combinedMap.entries()).find(([_, v]) => v.student_name.toLowerCase() === item.student_name.toLowerCase());
                if (existingKey) {
                    combinedMap.set(existingKey[0], { ...existingKey[1], ...item });
                } else {
                    combinedMap.set(item.id, item);
                }
            });
            allEnrichedAlumni = Array.from(combinedMap.values());
        }
    } catch (err) {
        console.warn('Using baseline alumni performers data:', err);
    }

    if (!window.AppState) window.AppState = {};
    window.AppState.allAlumniExperiences = allEnrichedAlumni;

    updatePodiumDisplay();
    renderAlumniLeaderboard();
}

function updatePodiumDisplay() {
    // Sort by XP descending so top 3 are reliably displayed on the podium
    const sortedPodium = [...allEnrichedAlumni].sort((a, b) => (b.xp_num || 0) - (a.xp_num || 0));

    if (sortedPodium.length >= 3) {
        const top1 = sortedPodium[0];
        const top2 = sortedPodium[1];
        const top3 = sortedPodium[2];

        // Update Rank 1 (Center)
        const name1 = document.getElementById('podium-name-1');
        const comp1 = document.getElementById('podium-comp-1');
        const prob1 = document.getElementById('podium-prob-1');
        const img1 = document.getElementById('podium-img-1');
        const init1 = document.getElementById('podium-init-1');
        if (name1) name1.innerText = top1.student_name;
        if (comp1) comp1.innerText = top1.company;
        if (prob1) prob1.innerText = `${(top1.problems?.total || top1.xp_num || 2569).toLocaleString()} Problems`;
        if (img1 && top1.avatar) {
            img1.src = top1.avatar;
            img1.alt = top1.student_name;
        }
        if (init1) init1.innerText = top1.initials || 'PP';

        // Update Rank 2 (Left)
        const name2 = document.getElementById('podium-name-2');
        const comp2 = document.getElementById('podium-comp-2');
        const prob2 = document.getElementById('podium-prob-2');
        const img2 = document.getElementById('podium-img-2');
        const init2 = document.getElementById('podium-init-2');
        if (name2) name2.innerText = top2.student_name;
        if (comp2) comp2.innerText = top2.company;
        if (prob2) prob2.innerText = `${(top2.problems?.total || top2.xp_num || 1840).toLocaleString()} Problems`;
        if (img2 && top2.avatar) {
            img2.src = top2.avatar;
            img2.alt = top2.student_name;
        }
        if (init2) init2.innerText = top2.initials || 'AS';

        // Update Rank 3 (Right)
        const name3 = document.getElementById('podium-name-3');
        const comp3 = document.getElementById('podium-comp-3');
        const prob3 = document.getElementById('podium-prob-3');
        const img3 = document.getElementById('podium-img-3');
        const init3 = document.getElementById('podium-init-3');
        if (name3) name3.innerText = top3.student_name;
        if (comp3) comp3.innerText = top3.company;
        if (prob3) prob3.innerText = `${(top3.problems?.total || top3.xp_num || 1620).toLocaleString()} Problems`;
        if (img3 && top3.avatar) {
            img3.src = top3.avatar;
            img3.alt = top3.student_name;
        }
        if (init3) init3.innerText = top3.initials || 'SK';
    }

    const countEl = document.getElementById('total-alumni-count');
    if (countEl) {
        countEl.innerText = `${Math.max(200, allEnrichedAlumni.length)}+`;
    }
}

function openAlumniDetailByRank(rankNumber) {
    const sortedPodium = [...allEnrichedAlumni].sort((a, b) => (b.xp_num || 0) - (a.xp_num || 0));
    if (sortedPodium && sortedPodium[rankNumber - 1]) {
        openAlumniDetail(sortedPodium[rankNumber - 1].id);
    }
}

function switchAlumniMetric(metric) {
    currentMetricTab = metric;
    currentAlumniPage = 1;

    document.querySelectorAll('.alumni-tab-btn').forEach(btn => btn.classList.remove('active'));
    const activeBtn = document.getElementById(`tab-${metric}`);
    if (activeBtn) activeBtn.classList.add('active');

    renderAlumniLeaderboard();
}

function filterAlumniTimeRange(rangeVal) {
    currentTimeFilter = rangeVal;
    currentAlumniPage = 1;
    renderAlumniLeaderboard();
}

function debounceAlumniSearch() {
    if (alumniSearchTimeout) clearTimeout(alumniSearchTimeout);
    alumniSearchTimeout = setTimeout(() => {
        currentAlumniPage = 1;
        renderAlumniLeaderboard();
    }, 250);
}

function renderAlumniLeaderboard() {
    const tbody = document.getElementById('alumni-feed-container');
    if (!tbody) return;

    let records = [...allEnrichedAlumni];
    const query = document.getElementById('alumni-search-input')?.value.trim().toLowerCase() || '';

    // Search Filter by student name, company, or role
    if (query) {
        records = records.filter(r => 
            (r.student_name && r.student_name.toLowerCase().includes(query)) ||
            (r.company && r.company.toLowerCase().includes(query)) ||
            (r.role && r.role.toLowerCase().includes(query))
        );
    }

    // Time / Category Filter
    if (currentTimeFilter === 'top_packages') {
        records.sort((a, b) => (parseFloat(b.package_lpa) || 0) - (parseFloat(a.package_lpa) || 0));
    } else if (currentTimeFilter === 'year') {
        records = records.filter(r => String(r.batch_year) === '2024' || String(r.batch_year) === '2023');
    }

    // Sort by selected tab metric
    if (currentMetricTab === 'experience') {
        records.sort((a, b) => (b.xp_num || 0) - (a.xp_num || 0));
    } else if (currentMetricTab === 'badges') {
        records.sort((a, b) => (b.badges || 0) - (a.badges || 0));
    } else if (currentMetricTab === 'problems') {
        records.sort((a, b) => ((b.problems?.total || 0) - (a.problems?.total || 0)));
    } else if (currentMetricTab === 'achievements') {
        records.sort((a, b) => (b.achievements_count || 0) - (a.achievements_count || 0));
    }

    if (records.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center p-5" style="background:#FFFFFF; border-radius:14px;">
                    <div style="width:64px; height:64px; border-radius:50%; background:#EFF6FF; color:#2563EB; display:flex; align-items:center; justify-content:center; font-size:1.8rem; margin:0 auto 1rem;">
                        <i class="fa-solid fa-user-graduate"></i>
                    </div>
                    <h4 style="font-weight:700; color:#0F172A; margin-bottom:0.25rem;">No Alumni Records Found</h4>
                    <p style="font-size:0.88rem; color:#64748B;">No performers matched your search criteria. Try a different keyword.</p>
                </td>
            </tr>
        `;
        renderPagination(0);
        return;
    }

    // Pagination slice
    const totalPages = Math.ceil(records.length / ITEMS_PER_PAGE);
    if (currentAlumniPage > totalPages) currentAlumniPage = totalPages;
    const startIndex = (currentAlumniPage - 1) * ITEMS_PER_PAGE;
    const paginatedRecords = records.slice(startIndex, startIndex + ITEMS_PER_PAGE);

    tbody.innerHTML = paginatedRecords.map((item, idx) => {
        const actualRank = startIndex + idx + 1;
        let rankBadgeHtml = '';
        let rowClass = 'rank-row-other';

        if (actualRank === 1) {
            rankBadgeHtml = `<span class="rank-badge badge-gold" title="Rank 1 - Gold"><i class="fa-solid fa-medal"></i></span>`;
            rowClass = 'rank-row-1';
        } else if (actualRank === 2) {
            rankBadgeHtml = `<span class="rank-badge badge-silver" title="Rank 2 - Silver"><i class="fa-solid fa-medal"></i></span>`;
            rowClass = 'rank-row-2';
        } else if (actualRank === 3) {
            rankBadgeHtml = `<span class="rank-badge badge-bronze" title="Rank 3 - Bronze"><i class="fa-solid fa-medal"></i></span>`;
            rowClass = 'rank-row-3';
        } else {
            rankBadgeHtml = `<span class="rank-badge badge-neutral">${actualRank}</span>`;
            rowClass = 'rank-row-other';
        }

        const achievementsList = (item.achievements_icons || ['<i class="fa-solid fa-trophy text-amber"></i>']).join(' ');

        return `
            <tr class="alumni-row ${rowClass}" onclick="openAlumniDetail(${item.id})">
                <td style="text-align: center;">${rankBadgeHtml}</td>
                <td>
                    <div class="user-cell">
                        <div class="user-avatar-wrap">
                            <img src="${item.avatar}" alt="${item.student_name}" class="user-avatar-img" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                            <div class="user-avatar-initials" style="display:none;">${item.initials || 'AL'}</div>
                        </div>
                        <div class="user-meta">
                            <span class="user-full-name">${item.student_name}</span>
                            <span class="user-company-name">${item.company}</span>
                        </div>
                    </div>
                </td>
                <td class="td-xp">
                    <strong>${item.xp || (item.xp_num ? item.xp_num.toLocaleString() + ' XP' : '850 XP')}</strong>
                </td>
                <td class="td-badges">
                    <span>${item.badges || 5}</span>
                </td>
                <td>
                    <div class="problems-tags-row">
                        <span class="prob-tag tag-easy">Easy ${item.problems?.easy || 320}</span>
                        <span class="prob-tag tag-med">Medium ${item.problems?.medium || 210}</span>
                        <span class="prob-tag tag-hard">Hard ${item.problems?.hard || 140}</span>
                    </div>
                </td>
                <td>
                    <div class="achievements-row">
                        ${achievementsList}
                        <span class="achieve-pill">+${item.achievements_count || 1}</span>
                    </div>
                </td>
                <td style="text-align: right;">
                    <button type="button" class="btn-view-profile" onclick="event.stopPropagation(); openAlumniDetail(${item.id})">
                        View Profile
                    </button>
                </td>
            </tr>
        `;
    }).join('');

    renderPagination(totalPages);
}

function renderPagination(totalPages) {
    const container = document.getElementById('alumni-pagination-container');
    if (!container) return;

    if (totalPages <= 1) {
        container.innerHTML = '';
        return;
    }

    let html = `
        <button type="button" class="pg-btn" ${currentAlumniPage === 1 ? 'disabled' : ''} onclick="changeAlumniPage(${currentAlumniPage - 1})" aria-label="Previous Page">
            <i class="fa-solid fa-chevron-left"></i>
        </button>
    `;

    for (let p = 1; p <= totalPages; p++) {
        if (totalPages > 6 && p > 3 && p < totalPages - 1 && Math.abs(p - currentAlumniPage) > 1) {
            if (p === 4) html += `<span class="pg-ellipsis">...</span>`;
            continue;
        }
        html += `
            <button type="button" class="pg-btn ${p === currentAlumniPage ? 'active' : ''}" onclick="changeAlumniPage(${p})">
                ${p}
            </button>
        `;
    }

    html += `
        <button type="button" class="pg-btn" ${currentAlumniPage === totalPages ? 'disabled' : ''} onclick="changeAlumniPage(${currentAlumniPage + 1})" aria-label="Next Page">
            <i class="fa-solid fa-chevron-right"></i>
        </button>
    `;

    container.innerHTML = html;
}

function changeAlumniPage(page) {
    currentAlumniPage = page;
    renderAlumniLeaderboard();
}

function getInitials(name) {
    if (!name) return 'AL';
    const parts = name.trim().split(' ');
    if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase();
    return name.slice(0, 2).toUpperCase();
}

// Wrapper function for starting the challenge test
window.startAlumniChallenge = function(company, role) {
    if (typeof navigateTo === 'function') navigateTo('mocktest');
    
    const roleSelect = document.getElementById('mocktest-role-select');
    if (roleSelect && role) {
        for (let i = 0; i < roleSelect.options.length; i++) {
            if (roleSelect.options[i].text.toLowerCase().includes(role.toLowerCase())) {
                roleSelect.selectedIndex = i;
                break;
            }
        }
    }
    
    if (typeof mockActiveSkills !== 'undefined') {
        mockActiveSkills = ['DSA', 'System Design', 'OOP', 'Database'];
        if (typeof updateMockSkillsPreview === 'function') updateMockSkillsPreview();
    }
    
    setTimeout(() => {
        if (typeof generateAndStartMockTest === 'function') {
            generateAndStartMockTest();
        }
    }, 500);
};

function openAlumniDetail(expId) {
    const experiences = window.AppState?.allAlumniExperiences || allEnrichedAlumni;
    const exp = experiences.find(e => String(e.id) === String(expId));
    if (!exp) return;

    const modal = document.getElementById('alumni-detail-modal');
    const avatarEl = document.getElementById('alumni-detail-avatar');
    const nameEl = document.getElementById('alumni-detail-name');
    const statusEl = document.getElementById('alumni-detail-status');
    const subtitleEl = document.getElementById('alumni-detail-subtitle');
    const bodyEl = document.getElementById('alumni-detail-body');
    const upvoteCountEl = document.getElementById('alumni-detail-upvote-count');
    const upvoteBtnEl = document.getElementById('alumni-detail-upvote-btn');
    const gmailBtnEl = document.getElementById('alumni-detail-gmail-btn');

    if (!modal) return;

    const initials = exp.initials || getInitials(exp.student_name);
    const difficultyColor = exp.difficulty === 'Hard' ? 'badge-danger' : exp.difficulty === 'Medium' ? 'badge-warning' : 'badge-success';
    const seniorEmail = exp.email || `${exp.student_name.toLowerCase().replace(/\\s+/g, '.')}@gmail.com`;

    if (avatarEl) avatarEl.innerText = initials;
    if (nameEl) nameEl.innerText = exp.student_name;
    if (statusEl) {
        statusEl.innerText = exp.status || 'Selected';
        statusEl.className = 'badge badge-success';
    }
    if (subtitleEl) {
        subtitleEl.innerText = `Batch of ${exp.batch_year} • ${exp.offer_type || 'On-Campus Placement'}`;
    }

    let roundsHtml = '';
    if (exp.rounds && exp.rounds.length > 0) {
        roundsHtml = `
            <div class="alumni-section-title"><i class="fa-solid fa-list-ol"></i> Round-by-Round Interview Breakdown:</div>
            <ul class="rounds-timeline-list">
                ${exp.rounds.map(r => `
                    <li class="round-timeline-step">
                        <div class="round-name">${r.round_name || 'Interview Round'}</div>
                        <div class="round-desc">${r.details || ''}</div>
                    </li>
                `).join('')}
            </ul>
        `;
    }

    const safeCompany = (exp.company || '').replace(/'/g, "\\'");
    const safeRole = (exp.role || '').replace(/'/g, "\\'");

    bodyEl.innerHTML = `
        <div class="alumni-badges-row mb-3">
            <span class="badge badge-primary"><i class="fa-solid fa-building"></i> ${exp.company}</span>
            <span class="badge badge-outline"><i class="fa-solid fa-user-tie"></i> ${exp.role}</span>
            <span class="ctc-badge">₹${exp.package_lpa} LPA Package</span>
            <span class="badge ${difficultyColor}">${exp.difficulty} Interview</span>
        </div>

        <div class="alumni-email-tag mb-3" style="display:inline-flex;">
            <i class="fa-solid fa-envelope"></i> ${seniorEmail}
        </div>

        ${roundsHtml}

        <div class="alumni-section-title mt-3"><i class="fa-solid fa-book-bookmark"></i> Preparation Strategy & Resources:</div>
        <p style="font-size:0.92rem; color:var(--text-secondary); line-height:1.6;">${exp.preparation_tips || 'Consistent practice on Core CS and coding challenges.'}</p>

        ${exp.advice_to_juniors ? `
            <div class="alumni-section-title mt-3"><i class="fa-solid fa-comment-dots"></i> Advice to Junior Students:</div>
            <div class="alumni-quote" style="font-size:0.95rem; line-height:1.5;">"${exp.advice_to_juniors}"</div>
        ` : ''}

        <div style="margin-top:1.5rem; padding-top:1.25rem; border-top:1px solid #E2E8F0; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
            <button type="button" class="btn btn-primary" onclick="closeAlumniDetailModal(); startAlumniChallenge('${safeCompany}', '${safeRole}')">
                <i class="fa-solid fa-play"></i> Solve Their Exact Test
            </button>
            <span style="font-size:0.85rem; color:#64748B;"><i class="fa-solid fa-bolt text-amber"></i> Cleared with 100% Score</span>
        </div>
    `;

    if (upvoteCountEl) upvoteCountEl.innerText = exp.upvotes || 0;
    if (upvoteBtnEl) {
        upvoteBtnEl.onclick = () => upvoteExperience(exp.id, upvoteBtnEl);
        upvoteBtnEl.disabled = false;
        upvoteBtnEl.style.color = 'var(--text-primary)';
    }

    const linkedinBtnEl = document.getElementById('alumni-detail-linkedin-btn');
    if (linkedinBtnEl) {
        linkedinBtnEl.href = `https://www.linkedin.com/search/results/all/?keywords=${encodeURIComponent(exp.student_name + ' ' + exp.company)}`;
        linkedinBtnEl.onclick = () => trackLinkedInOutreach(encodeURIComponent(exp.student_name), encodeURIComponent(exp.company), encodeURIComponent(seniorEmail));
    }

    if (gmailBtnEl) {
        gmailBtnEl.onclick = () => contactSeniorViaGmail(
            encodeURIComponent(seniorEmail),
            encodeURIComponent(exp.student_name),
            encodeURIComponent(exp.company),
            encodeURIComponent(exp.role)
        );
    }

    modal.classList.add('active');
}

function closeAlumniDetailModal(e) {
    if (e && e.target && e.target !== e.currentTarget && !e.target.classList.contains('modal-close')) {
        return;
    }
    const modal = document.getElementById('alumni-detail-modal');
    if (modal) modal.classList.remove('active');
}

// Close on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const modal = document.getElementById('alumni-detail-modal');
        if (modal && modal.classList.contains('active')) {
            modal.classList.remove('active');
        }
    }
});

function contactSeniorViaGmail(email, name, company, role) {
    const decodedEmail = decodeURIComponent(email || 'alumni.contact@gmail.com');
    const decodedName = decodeURIComponent(name || 'Senior');
    const decodedCompany = decodeURIComponent(company || 'Target Company');
    const decodedRole = decodeURIComponent(role || 'Software Engineer');

    const subject = `Placement Guidance Request - ${decodedCompany} (${decodedRole})`;
    const body = `Hi ${decodedName},

I hope this email finds you well!

I came across your placement experience for ${decodedCompany} (${decodedRole}) on the AI Career Companion portal. Your journey and preparation tips were very inspiring.

As a junior student preparing for upcoming campus recruitment drives, I would love to connect with you to ask a few quick questions regarding preparation resources, coding rounds, and interview tips.

Thank you so much for taking out time to guide juniors!

Best regards,
[Your Name]
[Your Branch & College]`;

    const gmailUrl = `https://mail.google.com/mail/?view=cm&fs=1&to=${encodeURIComponent(decodedEmail)}&su=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;

    fetch('/api/alumni/track-outreach', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            alumni_id: decodedEmail,
            alumni_email: decodedEmail,
            alumni_name: decodedName,
            channel: 'gmail',
            student_name: window.AppState?.currentUser?.name || 'Junior Student',
            student_email: window.AppState?.currentUser?.email || 'student@itm.ac.in',
            target_company: decodedCompany,
            query_topic: `Mentorship request for ${decodedCompany} (${decodedRole})`
        })
    }).catch(e => console.log('Track outreach:', e));

    window.open(gmailUrl, '_blank', 'noopener,noreferrer');
    showToast(`Redirecting to Gmail to contact ${decodedName}...`, 'info');
}

function trackLinkedInOutreach(seniorName, company, seniorEmail) {
    const decodedName = decodeURIComponent(seniorName || 'Senior');
    const decodedCompany = decodeURIComponent(company || 'Company');
    const decodedEmail = decodeURIComponent(seniorEmail || '');

    fetch('/api/alumni/track-outreach', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            alumni_id: decodedEmail || decodedName,
            alumni_email: decodedEmail,
            alumni_name: decodedName,
            channel: 'linkedin',
            student_name: window.AppState?.currentUser?.name || 'Junior Student',
            student_email: window.AppState?.currentUser?.email || 'student@itm.ac.in',
            target_company: decodedCompany || 'Company',
            query_topic: `LinkedIn networking & profile connection for ${decodedCompany}`
        })
    }).catch(e => console.log('Track linkedin outreach:', e));
}

async function upvoteExperience(expId, btn) {
    try {
        const res = await fetch(`/api/alumni/upvote/${expId}`, { method: 'POST' });
        const data = await safeJsonFetch(res);
        if (data.success) {
            const countEl = (btn && (btn.querySelector('#alumni-detail-upvote-count') || btn.querySelector('.upvote-count') || btn.querySelector('span'))) || document.getElementById('alumni-detail-upvote-count');
            if (countEl) {
                const currentVal = parseInt(countEl.innerText) || 0;
                countEl.innerText = (data.upvotes !== undefined) ? data.upvotes : (currentVal + 1);
            }
            if (btn) {
                btn.style.color = '#ef4444';
                btn.classList.add('upvoted');
                btn.disabled = true;
            }
            showToast('❤️ Thank you! Your upvote has been recorded.', 'success');
        } else {
            showToast(data.error || 'Failed to record upvote.', 'error');
        }
    } catch (err) {
        showToast('Upvote failed: ' + err.message, 'error');
    }
}
