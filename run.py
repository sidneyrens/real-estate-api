import os
import sys
import unittest
from app import create_app

app, api = create_app()

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test_loader = unittest.TestLoader()
        test_suite = test_loader.discover('tests', pattern='test_*.py')
        test_runner = unittest.TextTestRunner(verbosity=2)
        test_runner.run(test_suite)
    else:
        app.run(debug=app.config['DEBUG'], host='localhost', port=5001)