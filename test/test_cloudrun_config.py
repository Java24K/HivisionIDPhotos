from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class CloudRunConfigTest(unittest.TestCase):
    def test_dockerfile_starts_fastapi_api_on_cloud_run_port(self):
        dockerfile = (PROJECT_ROOT / "Dockerfile").read_text()

        self.assertIn("EXPOSE 8080", dockerfile)
        self.assertNotIn("app.py", dockerfile)
        self.assertIn("deploy_api.py", dockerfile)

    def test_deploy_api_uses_cloud_run_port_and_has_health_endpoint(self):
        deploy_api = (PROJECT_ROOT / "deploy_api.py").read_text()

        self.assertIn('os.environ.get("PORT"', deploy_api)
        self.assertIn('uvicorn.run(app, host="0.0.0.0", port=port)', deploy_api)
        self.assertIn('@app.get("/healthz")', deploy_api)

    def test_dockerignore_excludes_local_only_build_context(self):
        dockerignore = (PROJECT_ROOT / ".dockerignore").read_text()

        self.assertIn(".venv", dockerignore)
        self.assertIn(".git", dockerignore)
        self.assertIn("__pycache__", dockerignore)
        self.assertNotIn("hivision/creator/weights", dockerignore)


if __name__ == "__main__":
    unittest.main()
