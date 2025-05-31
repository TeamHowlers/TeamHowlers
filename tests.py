from flask_testing import TestCase
from app import app

class WeatherTestCase(TestCase):
    def create_app(self):
        return app

    def test_weather_endpoint(self):
        response = self.client.post('/weather')
        self.assert200(response)
        data = response.get_json()
        self.assertEqual(len(data), 3)
        for item in data:
            self.assertIn('city', item)
            self.assertIn('temperature', item)
            self.assertIn('humidity', item)
            self.assertIn('pressure', item)

if __name__ == '__main__':
    unittest.main()