"""
Tamarind Bio API Client

A single-file client for interacting with the Tamarind Bio API.
Supports tool discovery, job submission (sync/async), and result management.

API Documentation: https://app.tamarind.bio/api-docs/
"""

import os
import time
import json
import zipfile
from pathlib import Path
from typing import Optional
from datetime import datetime

import requests
from dotenv import load_dotenv


class TamarindClient:
    """Client for the Tamarind Bio API."""
    
    BASE_URL = "https://app.tamarind.bio/api/"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Tamarind client.
        
        Args:
            api_key: Tamarind API key. If not provided, loads from TAMARIND_API_KEY env var.
        """
        # Load .env from current directory or tasks directory
        load_dotenv()
        load_dotenv(Path(__file__).parent / ".env")
        
        self.api_key = api_key or os.getenv("TAMARIND_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Set TAMARIND_API_KEY env var or pass api_key parameter. "
                "Copy tasks/env.example to tasks/.env and add your key."
            )
        
        self._headers = {"x-api-key": self.api_key}
        self._tools_cache: Optional[list] = None
    
    def _request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[dict] = None,
        json_data: Optional[dict] = None,
        files: Optional[dict] = None
    ) -> requests.Response:
        """Make an authenticated request to the API."""
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.request(
            method,
            url,
            headers=self._headers,
            params=params,
            json=json_data,
            files=files
        )
        return response
    
    # =========================================================================
    # Tool Discovery
    # =========================================================================
    
    def get_tools(self, refresh: bool = False) -> list[dict]:
        """
        Get list of available tools and their configurations.
        
        Args:
            refresh: If True, bypass cache and fetch fresh data.
            
        Returns:
            List of tool specifications with name, settings, description.
        """
        if self._tools_cache is not None and not refresh:
            return self._tools_cache
        
        response = self._request("GET", "tools")
        response.raise_for_status()
        self._tools_cache = response.json()
        return self._tools_cache
    
    def get_tool_spec(self, name: str) -> Optional[dict]:
        """
        Get specification for a specific tool by name.
        
        Args:
            name: Tool name (e.g., 'alphafold', 'esmfold', 'proteinmpnn')
            
        Returns:
            Tool specification dict or None if not found.
        """
        tools = self.get_tools()
        for tool in tools:
            if tool.get("name") == name:
                return tool
        return None
    
    def list_tool_names(self) -> list[str]:
        """Get list of all available tool names."""
        return [t.get("name") for t in self.get_tools() if t.get("name")]
    
    def search_tools(self, query: str) -> list[dict]:
        """
        Search tools by name or description.
        
        Args:
            query: Search string (case-insensitive)
            
        Returns:
            List of matching tool specifications.
        """
        query = query.lower()
        return [
            t for t in self.get_tools()
            if query in t.get("name", "").lower() 
            or query in t.get("description", "").lower()
            or query in t.get("displayName", "").lower()
        ]
    
    # =========================================================================
    # Job Submission
    # =========================================================================
    
    def submit_job_async(
        self, 
        tool: str, 
        settings: dict, 
        job_name: Optional[str] = None,
        job_email: Optional[str] = None
    ) -> dict:
        """
        Submit a job asynchronously (returns immediately with job info).
        
        Args:
            tool: Tool name (e.g., 'alphafold', 'esmfold')
            settings: Tool-specific settings dict
            job_name: Optional custom job name
            job_email: Optional email for notifications
            
        Returns:
            Dict with job metadata including jobName, status, etc.
        """
        if job_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            job_name = f"{tool}_{timestamp}"
        
        params = {
            "jobName": job_name,
            "type": tool,
            "settings": settings
        }
        if job_email:
            params["jobEmail"] = job_email
        
        response = self._request("POST", "submit-job", json_data=params)
        response.raise_for_status()
        
        # API returns plain text confirmation, not JSON
        response_text = response.text
        try:
            response_data = response.json()
        except (json.JSONDecodeError, ValueError):
            response_data = response_text
        
        return {
            "job_name": job_name,
            "tool": tool,
            "settings": settings,
            "response": response_data,
            "submitted_at": datetime.now().isoformat()
        }
    
    def submit_job_sync(
        self, 
        tool: str, 
        settings: dict, 
        job_name: Optional[str] = None,
        timeout: int = 600,
        poll_interval: int = 10
    ) -> dict:
        """
        Submit a job and wait for completion.
        
        Args:
            tool: Tool name
            settings: Tool-specific settings
            job_name: Optional custom job name
            timeout: Max seconds to wait for completion
            poll_interval: Seconds between status checks
            
        Returns:
            Dict with job info and final status.
            
        Raises:
            TimeoutError: If job doesn't complete within timeout.
        """
        job_info = self.submit_job_async(tool, settings, job_name)
        actual_job_name = job_info["job_name"]
        
        result = self.wait_for_job(actual_job_name, timeout, poll_interval)
        job_info["final_status"] = result
        return job_info
    
    def submit_batch(self, jobs: list[dict]) -> list[dict]:
        """
        Submit multiple jobs at once.
        
        Args:
            jobs: List of job dicts, each with 'tool', 'settings', optional 'job_name'
            
        Returns:
            List of job submission results.
        """
        response = self._request("POST", "submit-batch", json_data={"jobs": jobs})
        response.raise_for_status()
        return response.json()
    
    # =========================================================================
    # Job Management
    # =========================================================================
    
    def get_jobs(self) -> list[dict]:
        """
        Get list of all jobs in your account.
        
        Returns:
            List of job info dicts.
        """
        response = self._request("GET", "jobs")
        response.raise_for_status()
        data = response.json()
        # API returns {"jobs": [...], "startKey": ..., "statuses": ...}
        if isinstance(data, dict) and "jobs" in data:
            return data["jobs"]
        return data if isinstance(data, list) else []
    
    def get_job_status(self, job_name: str) -> Optional[dict]:
        """
        Get status of a specific job.
        
        Args:
            job_name: Name of the job
            
        Returns:
            Job status dict or None if not found.
        """
        jobs = self.get_jobs()
        for job in jobs:
            name = job.get("JobName") or job.get("jobName") or job.get("name")
            if name == job_name:
                return job
        return None
    
    def wait_for_job(
        self, 
        job_name: str, 
        timeout: int = 600, 
        poll_interval: int = 10
    ) -> dict:
        """
        Wait for a job to complete.
        
        Args:
            job_name: Name of the job
            timeout: Max seconds to wait
            poll_interval: Seconds between status checks
            
        Returns:
            Final job status dict.
            
        Raises:
            TimeoutError: If job doesn't complete within timeout.
            ValueError: If job not found.
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_job_status(job_name)
            
            if status is None:
                # Job might not appear immediately after submission
                time.sleep(poll_interval)
                continue
            
            # Handle both capitalized (API) and lowercase field names
            job_status = (status.get("JobStatus") or status.get("status") or "").lower()
            
            if job_status in ("complete", "completed", "done", "finished", "success"):
                return status
            elif job_status in ("failed", "error", "cancelled"):
                return status
            
            print(f"Job '{job_name}' status: {job_status}. Waiting...")
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Job '{job_name}' did not complete within {timeout} seconds")
    
    def delete_job(self, job_name: str) -> bool:
        """
        Delete a job and its associated data.
        
        Args:
            job_name: Name of the job to delete
            
        Returns:
            True if successful.
        """
        response = self._request("DELETE", "delete-job", json_data={"jobName": job_name})
        response.raise_for_status()
        return True
    
    # =========================================================================
    # Results
    # =========================================================================
    
    def download_results(
        self, 
        job_name: str, 
        output_dir: str = "./tmp",
        extract: bool = True
    ) -> Path:
        """
        Download job results to local directory.
        
        Args:
            job_name: Name of the job
            output_dir: Directory to save results (created if doesn't exist)
            extract: If True, extract zip contents
            
        Returns:
            Path to downloaded file or extracted directory.
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        params = {"jobName": job_name}
        response = self._request("POST", "result", json_data=params)
        response.raise_for_status()
        
        # Response contains a URL to download from
        download_url = response.text.replace('"', '')
        
        # Download the actual file
        download_response = requests.get(download_url)
        download_response.raise_for_status()
        
        # Save the zip file
        zip_path = output_path / f"{job_name}.zip"
        with open(zip_path, "wb") as f:
            f.write(download_response.content)
        
        if extract:
            extract_path = output_path / job_name
            extract_path.mkdir(exist_ok=True)
            
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(extract_path)
            
            # Remove zip after extraction
            zip_path.unlink()
            return extract_path
        
        return zip_path
    
    # =========================================================================
    # File Management
    # =========================================================================
    
    def upload_file(self, filepath: str) -> dict:
        """
        Upload a file to your Tamarind account.
        
        Args:
            filepath: Path to local file to upload
            
        Returns:
            Upload response with file info.
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        filename = filepath.name
        
        with open(filepath, "rb") as f:
            response = requests.put(
                f"{self.BASE_URL}upload/{filename}",
                headers=self._headers,
                data=f.read()
            )
        
        response.raise_for_status()
        return {"filename": filename, "response": response.text}
    
    def list_files(self) -> list[dict]:
        """
        List files in your Tamarind account.
        
        Returns:
            List of file info dicts.
        """
        response = self._request("GET", "files")
        response.raise_for_status()
        return response.json()
    
    def delete_file(self, filename: str) -> bool:
        """
        Delete a file from your account.
        
        Args:
            filename: Name of file to delete
            
        Returns:
            True if successful.
        """
        response = self._request("DELETE", "delete-file", json_data={"filename": filename})
        response.raise_for_status()
        return True
    
    # =========================================================================
    # Convenience Methods
    # =========================================================================
    
    def format_tool_info(self, tool: dict) -> str:
        """Format tool info as readable string."""
        lines = [
            f"Tool: {tool.get('displayName', tool.get('name'))}",
            f"  Name: {tool.get('name')}",
            f"  Description: {tool.get('description', 'N/A')}"
        ]
        
        if tool.get("github"):
            lines.append(f"  GitHub: {tool.get('github')}")
        if tool.get("paper"):
            lines.append(f"  Paper: {tool.get('paper')}")
        
        settings = tool.get("settings", [])
        if settings:
            lines.append("  Settings:")
            for s in settings:
                req = " (required)" if s.get("required") else ""
                desc = s.get("description", "")
                lines.append(f"    - {s.get('name')}{req}: {desc}")
        
        return "\n".join(lines)


# =============================================================================
# CLI Entry Point
# =============================================================================

def main():
    """CLI entry point for the Tamarind client."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Tamarind Bio API Client")
    parser.add_argument("--api-key", help="API key (or set TAMARIND_API_KEY env var)")
    parser.add_argument("--list-tools", action="store_true", help="List available tools")
    parser.add_argument("--search", help="Search tools by name/description")
    parser.add_argument("--tool-info", help="Get info for specific tool")
    parser.add_argument("--list-jobs", action="store_true", help="List your jobs")
    parser.add_argument("--list-files", action="store_true", help="List your files")
    parser.add_argument("--test-alphafold", action="store_true", help="Run test AlphaFold job")
    parser.add_argument("--test-esmfold", action="store_true", help="Run test ESMFold job (faster)")
    
    args = parser.parse_args()
    
    # Initialize client
    try:
        client = TamarindClient(api_key=args.api_key)
        print("Tamarind client initialized successfully!\n")
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    
    # List tools
    if args.list_tools:
        print("Available tools:")
        print("-" * 50)
        for name in client.list_tool_names():
            print(f"  - {name}")
        print(f"\nTotal: {len(client.list_tool_names())} tools")
    
    # Search tools
    if args.search:
        results = client.search_tools(args.search)
        print(f"Search results for '{args.search}':")
        print("-" * 50)
        for tool in results:
            print(client.format_tool_info(tool))
            print()
    
    # Tool info
    if args.tool_info:
        tool = client.get_tool_spec(args.tool_info)
        if tool:
            print(client.format_tool_info(tool))
        else:
            print(f"Tool '{args.tool_info}' not found")
    
    # List jobs
    if args.list_jobs:
        jobs = client.get_jobs()
        print("Your jobs:")
        print("-" * 50)
        for job in jobs[:20]:  # Show first 20
            name = job.get("JobName") or job.get("jobName") or job.get("name")
            status = job.get("JobStatus") or job.get("status")
            job_type = job.get("Type") or job.get("type", "")
            print(f"  - {name} ({job_type}): {status}")
        if len(jobs) > 20:
            print(f"  ... and {len(jobs) - 20} more")
    
    # List files
    if args.list_files:
        files = client.list_files()
        print("Your files:")
        print("-" * 50)
        for f in files:
            print(f"  - {f}")
    
    # Test ESMFold (faster than AlphaFold)
    if args.test_esmfold:
        print("Running ESMFold test job...")
        print("-" * 50)
        
        # Short test sequence (insulin B chain fragment)
        test_sequence = "FVNQHLCGSHLVEALYLVCGERGFFYTPKA"
        
        print(f"Sequence: {test_sequence}")
        print(f"Length: {len(test_sequence)} residues")
        print()
        
        # Submit async
        job = client.submit_job_async(
            tool="esmfold",
            settings={"sequence": test_sequence}
        )
        print(f"Submitted job: {job['job_name']}")
        print(f"Response: {job['response']}")
        print()
        print("Job submitted! Check status with --list-jobs")
        print(f"Download results when complete: client.download_results('{job['job_name']}')")
    
    # Test AlphaFold
    if args.test_alphafold:
        print("Running AlphaFold test job...")
        print("-" * 50)
        
        # Very short test sequence
        test_sequence = "MALKSLVLLSLLVLVLLLVRVQPSLGKETAAAKFERQHMDSSTSAASSSNYCNQMMKSRNLTKDRCKPVNTFVHESLADVQAVCSQKNVACKNGQTNCYQSYSTMSITDCRETGSSKYPNCAYKTTQANKHIIVACEGNPYVPVHFDASV"
        
        print(f"Sequence: {test_sequence[:50]}...")
        print(f"Length: {len(test_sequence)} residues")
        print()
        
        job = client.submit_job_async(
            tool="alphafold",
            settings={
                "sequence": test_sequence,
                "numModels": "1",
                "numRecycles": 3
            }
        )
        print(f"Submitted job: {job['job_name']}")
        print(f"Response: {job['response']}")
        print()
        print("Job submitted! AlphaFold jobs can take 10-30+ minutes.")
        print(f"Check status with --list-jobs")
    
    # Default: show usage if no args
    if not any([args.list_tools, args.search, args.tool_info, args.list_jobs, 
                args.list_files, args.test_alphafold, args.test_esmfold]):
        print("Quick usage examples:")
        print("-" * 50)
        print("  tamarind --list-tools")
        print("  tamarind --tool-info alphafold")
        print("  tamarind --list-jobs")
        print("  tamarind --test-esmfold")
        print()
        print("Programmatic usage:")
        print("-" * 50)
        print("""
from tamarind_client import TamarindClient

client = TamarindClient()

# List tools
tools = client.list_tool_names()
print(f"Available: {len(tools)} tools")

# Get tool spec
spec = client.get_tool_spec("esmfold")
print(client.format_tool_info(spec))

# Submit async job
job = client.submit_job_async("esmfold", {"sequence": "MKTLLIAAAG..."})
print(f"Job name: {job['job_name']}")

# Submit sync job (waits for completion)
result = client.submit_job_sync("esmfold", {"sequence": "MKTLLIAAAG..."}, timeout=300)

# Download results
path = client.download_results("job_name", output_dir="./results")
print(f"Downloaded to: {path}")
""")


if __name__ == "__main__":
    main()
