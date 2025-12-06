"""
Test execution report generator for OCR API tests.
Generates a summary of test results including statistics and recommendations.
"""

import json
from datetime import datetime
from pathlib import Path


class TestReport:
    """Generate detailed test reports"""

    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
            },
            "by_category": {
                "extraction": {"passed": 0, "failed": 0, "total": 0},
                "verification": {"passed": 0, "failed": 0, "total": 0},
                "edge_cases": {"passed": 0, "failed": 0, "total": 0},
            },
            "images": {
                "1.png": {"passed": 0, "failed": 0, "details": []},
                "2.png": {"passed": 0, "failed": 0, "details": []},
                "3.png": {"passed": 0, "failed": 0, "details": []},
            },
            "recommendations": [],
        }

    def add_test_result(self, test_name, status, message=""):
        """Add a test result"""
        category = self._get_category(test_name)
        image = self._get_image(test_name)

        self.results["tests"]["total"] += 1
        if status == "passed":
            self.results["tests"]["passed"] += 1
            if category:
                self.results["by_category"][category]["passed"] += 1
                self.results["by_category"][category]["total"] += 1
            if image:
                self.results["images"][image]["passed"] += 1
        elif status == "failed":
            self.results["tests"]["failed"] += 1
            if category:
                self.results["by_category"][category]["failed"] += 1
                self.results["by_category"][category]["total"] += 1
            if image:
                self.results["images"][image]["failed"] += 1
                self.results["images"][image]["details"].append(
                    {"test": test_name, "error": message}
                )
        elif status == "skipped":
            self.results["tests"]["skipped"] += 1

    def generate_recommendations(self):
        """Generate recommendations based on results"""
        recommendations = []

        # Check if all tests passed
        if self.results["tests"]["failed"] == 0:
            recommendations.append("✅ All tests passed! API is performing well.")
            return recommendations

        # Check extraction issues
        extraction_stats = self.results["by_category"]["extraction"]
        if extraction_stats["failed"] > 0:
            recommendations.append(
                f"⚠️  Extraction: {extraction_stats['failed']}/{extraction_stats['total']} tests failed. "
                "Consider reviewing expected output values or model training data."
            )

        # Check verification issues
        verification_stats = self.results["by_category"]["verification"]
        if verification_stats["failed"] > 0:
            recommendations.append(
                f"⚠️  Verification: {verification_stats['failed']}/{verification_stats['total']} tests failed. "
                "Check field similarity matching and verification logic."
            )

        # Check specific image issues
        for image_name, image_results in self.results["images"].items():
            total = image_results["passed"] + image_results["failed"]
            if total > 0 and image_results["failed"] > 0:
                fail_rate = (image_results["failed"] / total) * 100
                recommendations.append(
                    f"⚠️  Image {image_name}: {fail_rate:.0f}% failure rate. "
                    "May need retraining or expected value adjustment."
                )

        return recommendations

    def generate_html_report(self, filepath="test_report.html"):
        """Generate HTML test report"""
        self.results["recommendations"] = self.generate_recommendations()

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>OCR API Test Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #333;
                    border-bottom: 3px solid #4CAF50;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #555;
                    margin-top: 30px;
                }}
                .stats {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin: 20px 0;
                }}
                .stat-box {{
                    padding: 15px;
                    border-radius: 5px;
                    text-align: center;
                    color: white;
                    font-weight: bold;
                }}
                .passed {{ background-color: #4CAF50; }}
                .failed {{ background-color: #f44336; }}
                .skipped {{ background-color: #ff9800; }}
                .total {{ background-color: #2196F3; }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #f2f2f2;
                    font-weight: bold;
                }}
                .recommendation {{
                    padding: 12px;
                    margin: 10px 0;
                    border-left: 4px solid #ff9800;
                    background-color: #fff3e0;
                    border-radius: 4px;
                }}
                .timestamp {{
                    color: #666;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🧪 OCR API Test Report</h1>
                <p class="timestamp">Generated: {self.results['timestamp']}</p>

                <h2>📊 Overall Statistics</h2>
                <div class="stats">
                    <div class="stat-box total">
                        <div>Total Tests</div>
                        <div style="font-size: 2em;">{self.results['tests']['total']}</div>
                    </div>
                    <div class="stat-box passed">
                        <div>Passed</div>
                        <div style="font-size: 2em;">{self.results['tests']['passed']}</div>
                    </div>
                    <div class="stat-box failed">
                        <div>Failed</div>
                        <div style="font-size: 2em;">{self.results['tests']['failed']}</div>
                    </div>
                    <div class="stat-box skipped">
                        <div>Skipped</div>
                        <div style="font-size: 2em;">{self.results['tests']['skipped']}</div>
                    </div>
                </div>

                <h2>📁 Results by Image</h2>
                <table>
                    <tr>
                        <th>Image</th>
                        <th>Passed</th>
                        <th>Failed</th>
                        <th>Success Rate</th>
                    </tr>
        """

        for image_name, image_results in self.results["images"].items():
            total = image_results["passed"] + image_results["failed"]
            success_rate = (
                f"{(image_results['passed'] / total * 100):.0f}%"
                if total > 0
                else "N/A"
            )
            html_content += f"""
                    <tr>
                        <td>{image_name}</td>
                        <td style="color: #4CAF50;">{image_results['passed']}</td>
                        <td style="color: #f44336;">{image_results['failed']}</td>
                        <td>{success_rate}</td>
                    </tr>
            """

        html_content += """
                </table>

                <h2>🔍 Results by Category</h2>
                <table>
                    <tr>
                        <th>Category</th>
                        <th>Passed</th>
                        <th>Failed</th>
                        <th>Total</th>
                    </tr>
        """

        for category, stats in self.results["by_category"].items():
            html_content += f"""
                    <tr>
                        <td>{category.title()}</td>
                        <td style="color: #4CAF50;">{stats['passed']}</td>
                        <td style="color: #f44336;">{stats['failed']}</td>
                        <td>{stats['total']}</td>
                    </tr>
            """

        html_content += """
                </table>
        """

        if self.results["recommendations"]:
            html_content += "<h2>💡 Recommendations</h2>"
            for rec in self.results["recommendations"]:
                html_content += f'<div class="recommendation">{rec}</div>'

        html_content += """
            </div>
        </body>
        </html>
        """

        with open(filepath, "w") as f:
            f.write(html_content)

        print(f"✅ Report generated: {filepath}")
        return filepath

    def generate_json_report(self, filepath="test_report.json"):
        """Generate JSON test report"""
        self.results["recommendations"] = self.generate_recommendations()

        with open(filepath, "w") as f:
            json.dump(self.results, f, indent=2)

        print(f"✅ Report generated: {filepath}")
        return filepath

    def print_summary(self):
        """Print test summary to console"""
        self.results["recommendations"] = self.generate_recommendations()

        print("\n" + "=" * 70)
        print("OCR API TEST SUMMARY")
        print("=" * 70)

        print(f"\n📊 Overall Results:")
        print(f"  Total:   {self.results['tests']['total']} tests")
        print(f"  ✅ Passed:  {self.results['tests']['passed']}")
        print(f"  ❌ Failed:  {self.results['tests']['failed']}")
        print(f"  ⏭️  Skipped: {self.results['tests']['skipped']}")

        print(f"\n📁 Results by Image:")
        for image_name, image_results in self.results["images"].items():
            total = image_results["passed"] + image_results["failed"]
            if total > 0:
                success_rate = (image_results["passed"] / total * 100)
                print(f"  {image_name:10} ✅ {image_results['passed']} / ❌ {image_results['failed']} ({success_rate:.0f}%)")

        print(f"\n🔍 Results by Category:")
        for category, stats in self.results["by_category"].items():
            if stats["total"] > 0:
                pass_rate = (stats["passed"] / stats["total"] * 100)
                print(f"  {category.title():15} ✅ {stats['passed']} / ❌ {stats['failed']} ({pass_rate:.0f}%)")

        if self.results["recommendations"]:
            print(f"\n💡 Recommendations:")
            for i, rec in enumerate(self.results["recommendations"], 1):
                print(f"  {i}. {rec}")

        print("\n" + "=" * 70)


# Pytest hook for generating report
def pytest_sessionfinish(session, exitstatus):
    """Called after test session"""
    report = TestReport()

    # Parse results (simplified - would need actual implementation)
    print("\n✅ Test session completed!")
