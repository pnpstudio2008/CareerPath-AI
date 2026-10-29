/**
 * ==============================================================================
 * AI CAREER COMPANION - GOOGLE APPS SCRIPT WEBHOOK (Code.gs)
 * ==============================================================================
 * 
 * Purpose: Receives student & alumni data from the Admin Portal and automatically
 * appends the records into a Google Sheet with 17 formatted columns.
 * 
 * ------------------------------------------------------------------------------
 * HOW TO DEPLOY IN GOOGLE APPS SCRIPT:
 * 1. Open Google Sheets -> Extensions -> Apps Script.
 * 2. Paste this entire Code.gs content into the editor.
 * 3. Click "Deploy" (top-right) -> "New deployment".
 * 4. Select type: "Web app".
 * 5. Configuration:
 *    - Description: "AI Career Companion Student & Alumni Sync"
 *    - Execute as: "Me" (your Google account)
 *    - Who has access: "Anyone" (allows webhook from web client/server)
 * 6. Click "Deploy", copy the Web App URL (ends in /exec), and paste it into
 *    the GOOGLE_SCRIPT_WEBHOOK_URL constant in static/js/admin_panel.js.
 * ==============================================================================
 */

// Define the exact 17 column headers as requested
const SHEET_HEADERS = [
  "Student ID",
  "Student Type",
  "Full Name",
  "Contact Phone",
  "Email (Gmail)",
  "Enrollment / Alumni User ID",
  "Department / Branch",
  "CSE/IT Section",
  "Graduation Batch",
  "Target Company / Career Track",
  "Placed Company",
  "Role / Designation",
  "Offered Package (₹ LPA)",
  "Login Password",
  "2FA Security Key",
  "Account Status",
  "Created Date"
];

/**
 * Handles incoming POST requests from the Admin Portal.
 */
function doPost(e) {
  try {
    const lock = LockService.getScriptLock();
    lock.waitLock(30000); // 30s lock to prevent concurrency conflicts

    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let sheet = ss.getSheetByName("Student & Alumni Records");
    
    // Create sheet if it does not exist
    if (!sheet) {
      sheet = ss.insertSheet("Student & Alumni Records");
    }

    // Ensure header row is set up
    setupSheetHeaders(sheet);

    // Parse incoming payload (supports JSON or URL-encoded form)
    let data = {};
    if (e.postData && e.postData.contents) {
      try {
        data = JSON.parse(e.postData.contents);
      } catch (parseErr) {
        data = e.parameter || {};
      }
    } else if (e.parameter) {
      data = e.parameter;
    }

    // Format current timestamp if not provided
    const currentDate = data.created_date || Utilities.formatDate(new Date(), "Asia/Kolkata", "dd/MM/yyyy HH:mm:ss");

    // Extract exact values mapped to the 17 column format
    const rowValues = [
      data.student_id || data.id || "N/A",
      data.student_type || (data.alumni_id ? "Alumni Student" : "Ongoing Student"),
      data.full_name || data.name || "Anonymous",
      data.contact_phone || data.phone || "N/A",
      data.email || "N/A",
      data.enrollment_alumni_id || data.roll_no || data.alumni_id || data.enrollment_no || "N/A",
      data.department_branch || data.department || data.branch || "Computer Science & Engineering",
      data.section || data.cse_it_section || "N/A",
      data.graduation_batch || data.batch_year || data.batch || "2025",
      data.target_company || data.career_track || "General / Tech",
      data.placed_company || data.company || "Not Placed",
      data.role_designation || data.role || (data.student_type === "Alumni Student" ? "Software Engineer" : "Student / Aspirant"),
      data.offered_package_lpa !== undefined ? data.offered_package_lpa : (data.package_lpa || 0),
      data.login_password || data.password || "N/A",
      data.security_key_2fa || data.alumni_id || data.roll_no || "N/A",
      data.account_status || (data.student_type === "Alumni Student" ? "Verified Alumni Mentor" : "Active (Ongoing)"),
      currentDate
    ];

    // Append the row to Google Sheet
    sheet.appendRow(rowValues);
    const lastRow = sheet.getLastRow();

    // Format new row cells
    const rowRange = sheet.getRange(lastRow, 1, 1, SHEET_HEADERS.length);
    rowRange.setVerticalAlignment("middle");
    rowRange.setFontFamily("Roboto");
    rowRange.setFontSize(10);

    // Apply color badge to Student Type column (Column B)
    const typeCell = sheet.getRange(lastRow, 2);
    if (String(rowValues[1]).includes("Alumni")) {
      typeCell.setFontColor("#15803d"); // Dark green for Alumni
      typeCell.setFontWeight("bold");
    } else {
      typeCell.setFontColor("#4338ca"); // Indigo for Ongoing Student
      typeCell.setFontWeight("bold");
    }

    lock.releaseLock();

    // ----------------------------------------------------------------------
    // AUTOMATIC WELCOME EMAIL DISPATCH (From: pnp.studio2008@gmail.com)
    // ----------------------------------------------------------------------
    sendWelcomeEmail(data);

    return ContentService.createTextOutput(JSON.stringify({
      status: "success",
      message: "Student / Alumni record successfully appended to Google Sheet and welcome credentials email sent.",
      row: lastRow,
      name: rowValues[2],
      type: rowValues[1],
      email: rowValues[4]
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Sends a welcome notification email with login credentials directly from pnp.studio2008@gmail.com.
 * Message: "This is your account created by admin of CareerPathAI. Use this account to find flaws
 * in your resume and build up your skills."
 */
function sendWelcomeEmail(data) {
  const recipientEmail = (data.email || "").trim();
  if (!recipientEmail || recipientEmail === "N/A" || !recipientEmail.includes("@")) {
    console.log("Skipping email: No valid recipient email provided.");
    return;
  }

  const studentName = data.full_name || data.name || "Student";
  const studentType = data.student_type || (data.alumni_id ? "Alumni Student" : "Ongoing Student");
  const userId = data.enrollment_alumni_id || data.roll_no || data.alumni_id || data.enrollment_no || "N/A";
  const password = data.login_password || data.password || "N/A";
  const secKey = data.security_key_2fa || data.alumni_id || data.roll_no || "N/A";
  const branch = data.department_branch || data.department || data.branch || "Computer Science & Engineering";
  const batch = data.graduation_batch || data.batch_year || "2025";
  const portalUrl = data.portal_url || "http://127.0.0.1:5000/student/login";

  const subject = `Welcome to CareerPathAI - Your ${studentType} Portal Account is Ready!`;

  const htmlBody = `
  <!DOCTYPE html>
  <html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
  </head>
  <body style="font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color:#f1f5f9; margin:0; padding:24px 12px; color:#1e293b;">
    <div style="max-width:600px; margin:0 auto; background:#ffffff; border-radius:16px; overflow:hidden; box-shadow:0 10px 25px rgba(0,0,0,0.06); border:1px solid #e2e8f0;">
      
      <!-- Header Banner -->
      <div style="background:linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%); padding:32px 24px; text-align:center; color:#ffffff;">
        <h1 style="margin:0; font-size:26px; font-weight:800; letter-spacing:-0.5px;">CareerPathAI</h1>
        <p style="margin:8px 0 0; opacity:0.92; font-size:14px; font-weight:500;">AI-Powered Placement & Career Skill Acceleration Portal</p>
      </div>

      <!-- Main Body -->
      <div style="padding:32px 28px;">
        <p style="font-size:16px; line-height:1.6; color:#334155; margin:0 0 18px 0;">
          Hi <strong>${studentName}</strong>,
        </p>
        
        <!-- Primary Admin Statement -->
        <div style="background:#eef2ff; border-left:4px solid #4f46e5; border-radius:8px; padding:18px 20px; margin:20px 0; font-size:15px; line-height:1.6; color:#1e1b4b;">
          🎯 <strong>This is your account created by the admin of CareerPathAI.</strong><br>
          Use this account to <strong>find flaws in your resume</strong>, evaluate your ATS score against top hiring benchmarks, and <strong>build up your technical and interview skills</strong>!
        </div>

        <!-- Credentials Card -->
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:12px; padding:22px; margin:24px 0;">
          <div style="font-size:14px; font-weight:800; color:#4f46e5; margin-bottom:16px; text-transform:uppercase; letter-spacing:0.75px;">
            🔐 Your Account Login Details
          </div>
          
          <table style="width:100%; border-collapse:collapse; font-size:14px;">
            <tr>
              <td style="padding:8px 0; color:#64748b; font-weight:600; width:45%;">Account Type:</td>
              <td style="padding:8px 0; color:#4f46e5; font-weight:800;">${studentType}</td>
            </tr>
            <tr style="border-top:1px dashed #e2e8f0;">
              <td style="padding:8px 0; color:#64748b; font-weight:600;">Enrollment / User ID:</td>
              <td style="padding:8px 0; color:#0f172a; font-weight:800; font-family:'Consolas', monospace; font-size:15px;">${userId}</td>
            </tr>
            <tr style="border-top:1px dashed #e2e8f0;">
              <td style="padding:8px 0; color:#64748b; font-weight:600;">Login Password:</td>
              <td style="padding:8px 0; color:#0f172a; font-weight:800; font-family:'Consolas', monospace; font-size:15px;">${password}</td>
            </tr>
            <tr style="border-top:1px dashed #e2e8f0;">
              <td style="padding:8px 0; color:#64748b; font-weight:600;">2FA Security Key:</td>
              <td style="padding:8px 0; color:#0f172a; font-weight:800; font-family:'Consolas', monospace; font-size:15px;">${secKey}</td>
            </tr>
            <tr style="border-top:1px dashed #e2e8f0;">
              <td style="padding:8px 0; color:#64748b; font-weight:600;">Department & Batch:</td>
              <td style="padding:8px 0; color:#0f172a; font-weight:600;">${branch} (Class of ${batch})</td>
            </tr>
          </table>
        </div>

        <!-- Key Portal Capabilities -->
        <div style="margin:24px 0;">
          <p style="font-size:14px; font-weight:700; color:#334155; margin:0 0 10px 0;">
            🚀 Recommended Next Steps on CareerPathAI:
          </p>
          <ul style="margin:0; padding-left:20px; font-size:13.5px; line-height:1.7; color:#475569;">
            <li><strong>Analyze Resume ATS Score:</strong> Upload your latest resume to discover missing skills, formatting gaps, and actionable recommendations.</li>
            <li><strong>Practice Technical Quizzes:</strong> Solve curated MCQs on DSA, Web Technologies, Database Systems, and Core Engineering subjects.</li>
            <li><strong>Alumni Placement Hub:</strong> Explore interview rounds from seniors placed at top tier tech enterprises.</li>
          </ul>
        </div>

        <!-- CTA Button -->
        <div style="text-align:center; margin:32px 0 16px 0;">
          <a href="${portalUrl}" style="display:inline-block; background:#4f46e5; color:#ffffff; padding:14px 34px; font-weight:800; font-size:15px; text-decoration:none; border-radius:10px; box-shadow:0 4px 14px rgba(79,70,229,0.4);" target="_blank">
            👉 Access Your Student Portal Account
          </a>
        </div>
      </div>

      <!-- Footer -->
      <div style="background:#f8fafc; padding:20px; text-align:center; font-size:12px; color:#94a3b8; border-top:1px solid #e2e8f0;">
        <p style="margin:0 0 6px 0;">Sent on behalf of <strong>CareerPathAI Administration</strong> &bull; Sender: <strong>pnp.studio2008@gmail.com</strong></p>
        <p style="margin:0;">Please keep your credentials confidential. For assistance, contact your department placement coordinator.</p>
      </div>
    </div>
  </body>
  </html>
  `;

  try {
    MailApp.sendEmail({
      to: recipientEmail,
      subject: subject,
      htmlBody: htmlBody,
      name: "CareerPathAI Admin"
    });
    console.log("Welcome notification email sent from pnp.studio2008@gmail.com to " + recipientEmail);
  } catch (err) {
    console.warn("Could not dispatch email: " + err.toString());
  }
}

/**
 * Handles GET requests to verify webhook status.
 */
function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({
    status: "active",
    message: "AI Career Companion Google Apps Script Webhook is live and ready to receive student & alumni records.",
    headers: SHEET_HEADERS
  })).setMimeType(ContentService.MimeType.JSON);
}

/**
 * Helper function to configure professional headers, colors, and formatting on the sheet.
 */
function setupSheetHeaders(sheet) {
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(SHEET_HEADERS);
    
    // Style header row
    const headerRange = sheet.getRange(1, 1, 1, SHEET_HEADERS.length);
    headerRange.setBackground("#4F46E5"); // Indigo theme matching the portal
    headerRange.setFontColor("#FFFFFF");
    headerRange.setFontWeight("bold");
    headerRange.setFontFamily("Roboto");
    headerRange.setFontSize(11);
    headerRange.setHorizontalAlignment("center");
    headerRange.setVerticalAlignment("middle");
    
    sheet.setRowHeight(1, 35);
    sheet.setFrozenRows(1);

    // Auto-resize columns for readability
    for (let i = 1; i <= SHEET_HEADERS.length; i++) {
      sheet.autoResizeColumn(i);
      sheet.setColumnWidth(i, Math.max(sheet.getColumnWidth(i) + 20, 140));
    }
  }
}
