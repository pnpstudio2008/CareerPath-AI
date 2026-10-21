import unittest
from app import app

class TestAdminSessionAndNavigation(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_admin_navigation_preserves_session(self):
        """Verify that an admin stays logged in across all admin sections and favicon/404s."""
        # 1. Establish an active admin session
        with self.app.session_transaction() as sess:
            sess['admin_logged_in'] = True
            sess['admin_user'] = 'Prof. Riya Modi'
            sess['faculty_name'] = 'Prof. Riya Modi'

        # 2. Check /favicon.ico (must NOT 404 and must NOT wipe session)
        fav_res = self.app.get('/favicon.ico')
        self.assertEqual(fav_res.status_code, 200)

        # Verify session is still intact after favicon
        with self.app.session_transaction() as sess:
            self.assertTrue(sess.get('admin_logged_in'))

        # 3. Navigate to Cohort Management (/admin)
        res = self.app.get('/admin')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Cohort Management', res.data)

        # 4. Navigate to Alumni Records (/admin/alumni)
        res = self.app.get('/admin/alumni')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Alumni Records', res.data)

        # 5. Navigate to Placement Analytics (/admin/analytics)
        res = self.app.get('/admin/analytics')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Placement Analytics', res.data)

        # 6. Navigate to Faculty Profile (/faculty/profile)
        res = self.app.get('/faculty/profile')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Prof. Riya Modi', res.data)

        # 7. Navigate to Settings (/admin/settings)
        res = self.app.get('/admin/settings')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Settings', res.data)

        # 8. Check 404 handling when logged in as admin -> should safely redirect to /admin, NOT /student/login
        res_404 = self.app.get('/some/nonexistent/page')
        self.assertEqual(res_404.status_code, 302)
        self.assertEqual(res_404.headers['Location'], '/admin')

        # 9. Verify session is still active after 404 redirect
        with self.app.session_transaction() as sess:
            self.assertTrue(sess.get('admin_logged_in'))

        # 10. Check GET /student/login while admin is logged in -> should redirect to /admin without wiping session
        res_login = self.app.get('/student/login')
        self.assertEqual(res_login.status_code, 302)
        self.assertEqual(res_login.headers['Location'], '/admin')

        # Verify session is STILL intact
        with self.app.session_transaction() as sess:
            self.assertTrue(sess.get('admin_logged_in'))

        print("[OK] TestAdminSessionAndNavigation passed successfully!")

if __name__ == '__main__':
    unittest.main()
