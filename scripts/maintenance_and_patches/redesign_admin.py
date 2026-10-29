import os

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\admin.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find where the modals start.
# Usually `<div class="modal-backdrop"` or similar.
modal_start_idx = content.find('<!-- ========================================== -->\n    <!-- MODALS')
if modal_start_idx == -1:
    modal_start_idx = content.find('<div class="modal-backdrop"')

modals_and_scripts = content[modal_start_idx:]

# New HTML structure
new_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Career Companion - Admin Console</title>
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- FontAwesome for fallback -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <link rel="stylesheet" href="/static/css/style.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        /* ADMIN DASHBOARD SPECIFIC STYLES */
        :root {
            --admin-bg: #F8FAFC;
            --admin-sidebar-width: 260px;
            --admin-nav-height: 70px;
            --admin-primary: #3B82F6;
            --admin-purple: #8B5CF6;
            --admin-border: #E2E8F0;
            --admin-text-main: #0F172A;
            --admin-text-muted: #64748B;
        }

        body {
            background-color: var(--admin-bg);
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
            color: var(--admin-text-main);
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }

        /* Top Navbar */
        .admin-top-nav {
            height: var(--admin-nav-height);
            background: white;
            border-bottom: 1px solid var(--admin-border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 1.5rem;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 100;
        }

        .admin-nav-left {
            display: flex;
            align-items: center;
            gap: 1rem;
            width: var(--admin-sidebar-width);
        }

        .admin-brand {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            text-decoration: none;
        }

        .admin-brand img {
            width: 36px;
            height: 36px;
            border-radius: 8px;
        }

        .admin-brand-text {
            display: flex;
            flex-direction: column;
        }

        .admin-brand-title {
            font-size: 1rem;
            font-weight: 700;
            color: var(--admin-text-main);
            line-height: 1.2;
        }

        .admin-brand-sub {
            font-size: 0.75rem;
            color: var(--admin-text-muted);
            font-weight: 500;
        }

        .admin-nav-center {
            display: flex;
            gap: 0.5rem;
        }

        .admin-nav-link {
            padding: 0.5rem 1rem;
            border-radius: 20px;
            text-decoration: none;
            color: var(--admin-text-muted);
            font-size: 0.875rem;
            font-weight: 500;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .admin-nav-link:hover {
            color: var(--admin-text-main);
            background: #F1F5F9;
        }

        .admin-nav-link.active {
            background: linear-gradient(135deg, var(--admin-primary), var(--admin-purple));
            color: white;
            box-shadow: 0 4px 6px -1px rgba(59,130,246,0.2);
        }

        .admin-nav-right {
            display: flex;
            align-items: center;
            gap: 1.25rem;
        }

        .admin-nav-icon {
            color: var(--admin-text-muted);
            cursor: pointer;
            position: relative;
        }

        .admin-nav-icon-badge {
            position: absolute;
            top: -4px;
            right: -4px;
            background: #EF4444;
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }

        .admin-user-profile {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            cursor: pointer;
        }

        .admin-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--admin-purple), var(--admin-primary));
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: 600;
        }

        /* App Layout */
        .admin-app-layout {
            display: flex;
            margin-top: var(--admin-nav-height);
            flex: 1;
        }

        /* Sidebar */
        .admin-sidebar {
            width: var(--admin-sidebar-width);
            background: transparent;
            padding: 1.5rem 1rem;
            position: fixed;
            top: var(--admin-nav-height);
            bottom: 0;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }

        .admin-sidebar-nav {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
            flex: 1;
        }

        .admin-sidebar-link {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem 1rem;
            border-radius: 12px;
            color: var(--admin-text-muted);
            text-decoration: none;
            font-size: 0.875rem;
            font-weight: 500;
            transition: all 0.2s;
        }

        .admin-sidebar-link:hover {
            background: white;
            color: var(--admin-text-main);
        }

        .admin-sidebar-link.active {
            background: #EFF6FF;
            color: var(--admin-primary);
            font-weight: 600;
        }

        .admin-sidebar-link i, .admin-sidebar-link svg {
            width: 18px;
            height: 18px;
        }

        .admin-sidebar-promo {
            background: white;
            border-radius: 16px;
            padding: 1.25rem;
            border: 1px solid var(--admin-border);
            text-align: center;
            margin-top: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
        }

        .admin-promo-icon {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: #EFF6FF;
            color: var(--admin-primary);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1rem;
        }

        .admin-promo-title {
            font-size: 0.875rem;
            font-weight: 700;
            color: var(--admin-text-main);
            margin-bottom: 0.25rem;
        }

        .admin-promo-desc {
            font-size: 0.75rem;
            color: var(--admin-text-muted);
            margin-bottom: 1rem;
            line-height: 1.4;
        }

        .admin-promo-btn {
            background: #F8FAFC;
            color: var(--admin-primary);
            border: 1px solid #E2E8F0;
            border-radius: 20px;
            padding: 0.4rem 1rem;
            font-size: 0.75rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            text-decoration: none;
        }

        .admin-promo-btn:hover {
            background: white;
            border-color: var(--admin-primary);
        }

        /* Main Content */
        .admin-main-content {
            margin-left: var(--admin-sidebar-width);
            padding: 2rem;
            flex: 1;
            max-width: calc(100vw - var(--admin-sidebar-width));
        }

        /* Hero */
        .admin-hero {
            background: white;
            border-radius: 24px;
            padding: 2rem;
            border: 1px solid var(--admin-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.02);
            position: relative;
            overflow: hidden;
        }

        .admin-hero::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 50%;
            height: 100%;
            background: radial-gradient(circle at top right, rgba(59,130,246,0.05), transparent 70%);
            pointer-events: none;
        }

        .admin-hero-left {
            max-width: 60%;
            z-index: 1;
        }

        .admin-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: #F8FAFC;
            border: 1px solid var(--admin-border);
            padding: 0.35rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--admin-text-muted);
            margin-bottom: 1rem;
        }

        .admin-hero-title {
            font-size: 2.25rem;
            font-weight: 800;
            color: var(--admin-text-main);
            line-height: 1.2;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }

        .admin-hero-title span {
            background: linear-gradient(135deg, var(--admin-primary), var(--admin-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .admin-hero-desc {
            font-size: 1rem;
            color: var(--admin-text-muted);
            line-height: 1.5;
        }

        .admin-hero-right {
            display: flex;
            gap: 1rem;
            z-index: 1;
            position: relative;
        }

        .admin-mini-chart-card {
            background: white;
            border: 1px solid var(--admin-border);
            border-radius: 16px;
            padding: 1rem;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);
            width: 140px;
        }
        
        .admin-mini-chart-title {
            font-size: 0.7rem;
            font-weight: 600;
            color: var(--admin-text-muted);
            margin-bottom: 0.5rem;
        }
        
        .css-chart-bar-container {
            display: flex;
            align-items: flex-end;
            gap: 4px;
            height: 40px;
            margin-top: 10px;
        }
        .css-bar {
            flex: 1;
            background: linear-gradient(to top, rgba(59,130,246,0.2), rgba(59,130,246,0.8));
            border-radius: 2px 2px 0 0;
        }

        /* Metric Cards */
        .admin-metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .admin-metric-card {
            background: white;
            border-radius: 20px;
            padding: 1.5rem;
            border: 1px solid var(--admin-border);
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
            transition: transform 0.2s;
        }

        .admin-metric-card:hover {
            transform: translateY(-2px);
        }

        .am-icon {
            width: 48px;
            height: 48px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        .am-icon.blue { background: #EFF6FF; color: var(--admin-primary); }
        .am-icon.purple { background: #F5F3FF; color: var(--admin-purple); }
        .am-icon.green { background: #F0FDF4; color: #10B981; }
        .am-icon.orange { background: #FFF7ED; color: #F97316; }

        .am-content {
            flex: 1;
        }

        .am-title {
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--admin-text-muted);
            margin-bottom: 0.25rem;
        }

        .am-value {
            font-size: 1.75rem;
            font-weight: 800;
            color: var(--admin-text-main);
            line-height: 1.1;
            margin-bottom: 0.25rem;
        }

        .am-trend {
            font-size: 0.75rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }
        .am-trend.positive { color: #10B981; }
        .am-trend.neutral { color: var(--admin-text-muted); }

        /* Management Panel */
        .admin-panel-container {
            background: white;
            border-radius: 24px;
            border: 1px solid var(--admin-border);
            box-shadow: 0 4px 20px rgba(0,0,0,0.02);
            overflow: hidden;
            margin-bottom: 2rem;
        }

        .admin-panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.5rem 2rem;
            border-bottom: 1px solid var(--admin-border);
        }

        .admin-tabs {
            display: flex;
            gap: 0.5rem;
        }

        .admin-tab {
            padding: 0.6rem 1.25rem;
            border-radius: 20px;
            font-size: 0.875rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            border: 1px solid transparent;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .admin-tab.active {
            background: linear-gradient(135deg, var(--admin-primary), var(--admin-purple));
            color: white;
            box-shadow: 0 4px 6px -1px rgba(59,130,246,0.2);
        }

        .admin-tab:not(.active) {
            background: #F8FAFC;
            color: var(--admin-text-muted);
            border-color: var(--admin-border);
        }
        .admin-tab:not(.active):hover {
            color: var(--admin-text-main);
            background: #F1F5F9;
        }

        .admin-btn-primary {
            background: linear-gradient(135deg, var(--admin-primary), var(--admin-purple));
            color: white;
            border: none;
            padding: 0.6rem 1.25rem;
            border-radius: 20px;
            font-size: 0.875rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            box-shadow: 0 4px 6px -1px rgba(59,130,246,0.2);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .admin-btn-primary:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 8px -1px rgba(59,130,246,0.3);
        }

        /* Filter Bar */
        .admin-filter-bar {
            padding: 1.25rem 2rem;
            display: flex;
            gap: 1rem;
            align-items: center;
            border-bottom: 1px solid var(--admin-border);
            background: #FAFAFA;
        }

        .admin-search-wrapper {
            flex: 1;
            position: relative;
        }
        .admin-search-wrapper i {
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            color: #94A3B8;
        }
        .admin-search-input {
            width: 100%;
            padding: 0.6rem 1rem 0.6rem 2.5rem;
            border: 1px solid var(--admin-border);
            border-radius: 20px;
            font-size: 0.875rem;
            outline: none;
            transition: border-color 0.2s;
            font-family: 'Inter', sans-serif;
        }
        .admin-search-input:focus {
            border-color: var(--admin-primary);
        }

        .admin-select {
            padding: 0.6rem 2rem 0.6rem 1rem;
            border: 1px solid var(--admin-border);
            border-radius: 20px;
            font-size: 0.875rem;
            color: var(--admin-text-main);
            background: white;
            outline: none;
            cursor: pointer;
            font-weight: 500;
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2364748b' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 0.75rem center;
        }

        .admin-btn-outline {
            background: white;
            border: 1px solid var(--admin-border);
            padding: 0.6rem 1rem;
            border-radius: 20px;
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--admin-text-main);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: background 0.2s;
        }
        .admin-btn-outline:hover {
            background: #F1F5F9;
        }

        /* Table */
        .admin-table-wrapper {
            overflow-x: auto;
        }

        .admin-table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }

        .admin-table th {
            padding: 1rem 1.5rem;
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--admin-text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 1px solid var(--admin-border);
            background: white;
            white-space: nowrap;
        }

        .admin-table td {
            padding: 1.25rem 1.5rem;
            font-size: 0.875rem;
            border-bottom: 1px solid var(--admin-border);
            vertical-align: middle;
        }

        .admin-table tr:hover {
            background: #FAFAFA;
        }

        /* Checkbox */
        .admin-checkbox {
            width: 16px;
            height: 16px;
            border-radius: 4px;
            border: 1px solid #CBD5E1;
            cursor: pointer;
            accent-color: var(--admin-primary);
        }

        /* Student Cell */
        .student-cell {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .student-avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: #EFF6FF;
            color: var(--admin-primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.875rem;
        }

        .student-info {
            display: flex;
            flex-direction: column;
        }

        .student-name {
            font-weight: 600;
            color: var(--admin-text-main);
        }

        .student-email {
            font-size: 0.75rem;
            color: var(--admin-text-muted);
        }

        /* Badges */
        .ats-badge {
            display: inline-block;
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.75rem;
        }
        .ats-badge.high { background: #F0FDF4; color: #10B981; }
        .ats-badge.med { background: #FFF7ED; color: #F97316; }
        .ats-badge.low { background: #FEF2F2; color: #EF4444; }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.25rem 0.6rem;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
        }
        .status-badge::before {
            content: '';
            width: 6px;
            height: 6px;
            border-radius: 50%;
        }
        
        .status-badge.ready { background: #F0FDF4; color: #10B981; }
        .status-badge.ready::before { background: #10B981; }

        .status-badge.progress { background: #FFF7ED; color: #F97316; }
        .status-badge.progress::before { background: #F97316; }

        .status-badge.improve { background: #FEF2F2; color: #EF4444; }
        .status-badge.improve::before { background: #EF4444; }

        .status-badge.not-started { background: #F1F5F9; color: #64748B; }
        .status-badge.not-started::before { background: #64748B; }

        /* Placement Badge */
        .placement-badge {
            display: inline-block;
            padding: 0.35rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            border: 1px solid transparent;
        }
        .placement-badge.placed { background: white; border-color: #10B981; color: #10B981; }
        .placement-badge.interviewing { background: white; border-color: var(--admin-primary); color: var(--admin-primary); }
        .placement-badge.not-placed { background: white; border-color: var(--admin-border); color: var(--admin-text-muted); }

        /* Actions */
        .action-group {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .btn-action-promote {
            background: #F0FDF4;
            color: #10B981;
            border: none;
            padding: 0.35rem 0.75rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.35rem;
            transition: background 0.2s;
        }
        .btn-action-promote:hover { background: #DCFCE7; }

        .btn-action-icon {
            width: 28px;
            height: 28px;
            border-radius: 8px;
            border: 1px solid var(--admin-border);
            background: white;
            color: var(--admin-text-muted);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s;
        }
        .btn-action-icon:hover {
            background: #F1F5F9;
            color: var(--admin-text-main);
        }
        .btn-action-icon.delete:hover {
            background: #FEF2F2;
            color: #EF4444;
            border-color: #FECACA;
        }

        /* Pagination */
        .admin-pagination {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.25rem 2rem;
            background: white;
        }
        .pagination-info {
            font-size: 0.875rem;
            color: var(--admin-text-muted);
        }
        .pagination-controls {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .page-btn {
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            border: 1px solid var(--admin-border);
            background: white;
            color: var(--admin-text-muted);
            cursor: pointer;
            font-weight: 600;
            font-size: 0.875rem;
        }
        .page-btn.active {
            background: var(--admin-primary);
            color: white;
            border-color: var(--admin-primary);
        }
        .page-btn:hover:not(.active) {
            background: #F1F5F9;
        }

        @media (max-width: 1024px) {
            .admin-sidebar { width: 80px; padding: 1.5rem 0.5rem; }
            .admin-sidebar-link span { display: none; }
            .admin-sidebar-promo { display: none; }
            .admin-main-content { margin-left: 80px; max-width: calc(100vw - 80px); }
            .admin-nav-left { width: 80px; }
            .admin-brand-text { display: none; }
            .admin-hero { flex-direction: column; gap: 1.5rem; align-items: flex-start; }
            .admin-hero-left { max-width: 100%; }
            .admin-metrics-grid { grid-template-columns: repeat(2, 1fr); }
            .admin-nav-center { display: none; }
        }

        @media (max-width: 768px) {
            .admin-sidebar { display: none; }
            .admin-main-content { margin-left: 0; max-width: 100vw; padding: 1rem; }
            .admin-metrics-grid { grid-template-columns: 1fr; }
            .admin-filter-bar { flex-direction: column; align-items: flex-start; }
            .admin-select { width: 100%; }
            .admin-search-wrapper { width: 100%; }
            .admin-table { display: none; }
            /* Add mobile cards logic if needed */
        }
    </style>
</head>
<body>

    <!-- TOP NAVIGATION -->
    <header class="admin-top-nav">
        <div class="admin-nav-left">
            <a href="/" class="admin-brand">
                <img src="/static/images/logo.png" alt="Logo">
                <div class="admin-brand-text">
                    <span class="admin-brand-title">AI Career Companion</span>
                    <span class="admin-brand-sub">Admin Console</span>
                </div>
            </a>
        </div>
        <div class="admin-nav-center">
            <a href="#" class="admin-nav-link active"><i data-lucide="layout-dashboard"></i> Cohort Management</a>
            <a href="#" class="admin-nav-link" onclick="document.getElementById('tab-alumni').click()"><i data-lucide="users"></i> Alumni Records</a>
            <a href="#" class="admin-nav-link"><i data-lucide="bar-chart-3"></i> Placement Analytics</a>
            <a href="#" class="admin-nav-link"><i data-lucide="message-square"></i> Messages</a>
            <a href="#" class="admin-nav-link"><i data-lucide="settings"></i> Settings</a>
        </div>
        <div class="admin-nav-right">
            <div class="admin-nav-icon">
                <i data-lucide="bell"></i>
                <div class="admin-nav-icon-badge"></div>
            </div>
            <div class="admin-user-profile" onclick="adminLogout()">
                <div class="admin-avatar">PM</div>
                <span style="font-size:0.875rem; font-weight:600; color:var(--admin-text-main);">Panth Mistry <i data-lucide="chevron-down" style="width:14px; height:14px; vertical-align:middle;"></i></span>
            </div>
        </div>
    </header>

    <div class="admin-app-layout">
        <!-- SIDEBAR -->
        <aside class="admin-sidebar">
            <nav class="admin-sidebar-nav">
                <a href="#" class="admin-sidebar-link active"><i data-lucide="graduation-cap"></i> <span>Cohort & Placement</span></a>
                <a href="#" class="admin-sidebar-link"><i data-lucide="briefcase"></i> <span>Alumni Records</span></a>
                <a href="#" class="admin-sidebar-link"><i data-lucide="bar-chart-3"></i> <span>Placement Analytics</span></a>
                <a href="#" class="admin-sidebar-link"><i data-lucide="users"></i> <span>Mentor Management</span></a>
                <a href="#" class="admin-sidebar-link"><i data-lucide="message-square"></i> <span>Messages</span></a>
                <a href="#" class="admin-sidebar-link"><i data-lucide="book-open"></i> <span>Resources</span></a>
                <a href="#" class="admin-sidebar-link"><i data-lucide="settings"></i> <span>Platform Settings</span></a>
            </nav>

            <div class="admin-sidebar-promo">
                <div class="admin-promo-icon">
                    <i data-lucide="users"></i>
                </div>
                <h4 class="admin-promo-title">Build a stronger alumni network</h4>
                <p class="admin-promo-desc">Connect, guide and help more students get placed.</p>
                <a href="javascript:openCreateAlumniLoginModal()" class="admin-promo-btn">Invite Alumni <i data-lucide="arrow-right" style="width:14px; height:14px;"></i></a>
            </div>
        </aside>

        <!-- MAIN CONTENT -->
        <main class="admin-main-content">
            
            <!-- HERO -->
            <div class="admin-hero">
                <div class="admin-hero-left">
                    <div class="admin-badge">
                        <i data-lucide="settings" style="width:14px;height:14px;"></i> Master Administration Console
                    </div>
                    <h1 class="admin-hero-title">Cohort & <span>Placement Management</span></h1>
                    <p class="admin-hero-desc">Manage student cohorts, track real-time placement progress, and supervise alumni records & verified mentors.</p>
                </div>
                <div class="admin-hero-right">
                    <div class="admin-mini-chart-card">
                        <div class="admin-mini-chart-title">Placement Growth</div>
                        <div class="css-chart-bar-container">
                            <div class="css-bar" style="height: 30%;"></div>
                            <div class="css-bar" style="height: 50%;"></div>
                            <div class="css-bar" style="height: 40%;"></div>
                            <div class="css-bar" style="height: 70%;"></div>
                            <div class="css-bar" style="height: 90%;"></div>
                        </div>
                    </div>
                    <div class="admin-mini-chart-card" style="display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center;">
                        <div class="admin-mini-chart-title" style="margin-bottom:0.75rem;">ATS Readiness</div>
                        <div style="width:60px; height:60px; border-radius:50%; border: 6px solid #EFF6FF; border-top-color: var(--admin-primary); display:flex; align-items:center; justify-content:center; font-weight:800; font-size:1rem; color:var(--admin-primary);">
                            75%
                        </div>
                    </div>
                </div>
            </div>

            <!-- METRICS -->
            <div class="admin-metrics-grid">
                <div class="admin-metric-card">
                    <div class="am-icon blue"><i data-lucide="users"></i></div>
                    <div class="am-content">
                        <div class="am-title">Total Cohort Students</div>
                        <div class="am-value" id="admin-stat-students">--</div>
                        <div class="am-trend positive"><i data-lucide="trending-up" style="width:12px;height:12px;"></i> +0%</div>
                    </div>
                </div>
                <div class="admin-metric-card">
                    <div class="am-icon purple"><i data-lucide="briefcase"></i></div>
                    <div class="am-content">
                        <div class="am-title">Successfully Placed</div>
                        <div class="am-value" id="admin-stat-placed">--</div>
                        <div class="am-trend positive"><i data-lucide="trending-up" style="width:12px;height:12px;"></i> +0%</div>
                    </div>
                </div>
                <div class="admin-metric-card">
                    <div class="am-icon green"><i data-lucide="file-text"></i></div>
                    <div class="am-content">
                        <div class="am-title">Average ATS Score</div>
                        <div class="am-value" id="admin-stat-ats">--</div>
                        <div class="am-trend positive"><i data-lucide="trending-up" style="width:12px;height:12px;"></i> +0%</div>
                    </div>
                </div>
                <div class="admin-metric-card">
                    <div class="am-icon orange"><i data-lucide="users"></i></div>
                    <div class="am-content">
                        <div class="am-title">Alumni Mentors</div>
                        <div class="am-value" id="admin-stat-mentors">--</div>
                        <div class="am-trend positive"><i data-lucide="trending-up" style="width:12px;height:12px;"></i> +0%</div>
                    </div>
                </div>
            </div>

            <!-- MANAGEMENT PANEL -->
            <div class="admin-panel-container">
                <div class="admin-panel-header">
                    <div class="admin-tabs">
                        <button class="admin-tab active" id="tab-students" onclick="switchAdminTab('students')">
                            <i data-lucide="graduation-cap"></i> Student Cohort & Progress
                        </button>
                        <button class="admin-tab" id="tab-alumni" onclick="switchAdminTab('alumni')">
                            <i data-lucide="users"></i> Manage Alumni Records
                        </button>
                    </div>
                    <button class="admin-btn-primary" onclick="openCreateStudentLoginModal()" id="btn-add-student">
                        <i data-lucide="plus"></i> Add Ongoing Student
                    </button>
                </div>

                <div class="admin-filter-bar">
                    <div class="admin-search-wrapper">
                        <i data-lucide="search"></i>
                        <input type="text" class="admin-search-input" id="admin-search" placeholder="Search student name, roll no, or email..." oninput="filterAdminTable()">
                    </div>
                    <select class="admin-select" id="admin-filter-branch" onchange="filterAdminTable()">
                        <option value="all">All Branches</option>
                        <option value="Computer Science">Computer Science</option>
                        <option value="IT">IT</option>
                        <option value="Electronics">Electronics</option>
                        <option value="Mechanical">Mechanical</option>
                    </select>
                    <select class="admin-select" id="admin-filter-status" onchange="filterAdminTable()">
                        <option value="all">All Placement Status</option>
                        <option value="Placed">Placed</option>
                        <option value="Interviewing">Interviewing</option>
                        <option value="Not Placed">Not Placed</option>
                    </select>
                    <select class="admin-select" id="admin-filter-readiness" onchange="filterAdminTable()">
                        <option value="all">All Readiness</option>
                        <option value="Ready">Ready</option>
                        <option value="In Progress">In Progress</option>
                        <option value="Needs Improvement">Needs Improvement</option>
                    </select>
                    <button class="admin-btn-outline" onclick="resetAdminFilters()">
                        <i data-lucide="rotate-ccw"></i> Reset Filters
                    </button>
                </div>

                <!-- Student Table -->
                <div class="admin-table-wrapper" id="students-view">
                    <table class="admin-table">
                        <thead>
                            <tr>
                                <th style="width: 40px;"><input type="checkbox" class="admin-checkbox"></th>
                                <th>STUDENT & EMAIL</th>
                                <th>ROLL NO.</th>
                                <th>BRANCH / BATCH</th>
                                <th>ATS SCORE <i data-lucide="chevron-down" style="width:12px;height:12px;display:inline;"></i></th>
                                <th>READINESS</th>
                                <th>PRACTICE TESTS</th>
                                <th>PLACEMENT STATUS</th>
                                <th>ACTIONS</th>
                            </tr>
                        </thead>
                        <tbody id="admin-student-tbody">
                            <!-- Populated by JS -->
                        </tbody>
                    </table>
                </div>

                <!-- Alumni Table (Hidden by default) -->
                <div class="admin-table-wrapper" id="alumni-view" style="display:none;">
                    <table class="admin-table">
                        <thead>
                            <tr>
                                <th>ALUMNI MENTOR</th>
                                <th>ROLL / BATCH</th>
                                <th>COMPANY & ROLE</th>
                                <th>PACKAGE</th>
                                <th>OFFER TYPE</th>
                                <th>ACTIONS</th>
                            </tr>
                        </thead>
                        <tbody id="admin-alumni-tbody">
                            <!-- Populated by JS -->
                        </tbody>
                    </table>
                </div>

                <!-- Pagination -->
                <div class="admin-pagination">
                    <div class="pagination-info">Showing <span id="pagination-count">0</span> records</div>
                    <div class="pagination-controls">
                        <button class="page-btn"><i data-lucide="chevron-left"></i></button>
                        <button class="page-btn active">1</button>
                        <button class="page-btn"><i data-lucide="chevron-right"></i></button>
                    </div>
                </div>

            </div>
        </main>
    </div>

    <!-- Scripts and Modals injection point -->
"""

# append modals_and_scripts and closing tags
new_html += modals_and_scripts

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Redesigned admin.html")
