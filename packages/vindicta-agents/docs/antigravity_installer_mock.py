import shutil
import yaml
from pathlib import Path


class Installer:
    def __init__(self, target_repo: Path, library_path: Path):
        self.target_repo = target_repo
        self.library_path = library_path
        self.agent_dir = target_repo / "agents"
        self.workflow_dir = target_repo / ".agent" / "workflows"

    def init_repo(self):
        """Initialize the target repository for antigravity."""
        self.workflow_dir.mkdir(parents=True, exist_ok=True)
        self.agent_dir.mkdir(parents=True, exist_ok=True)
        print(f"Initialized {self.target_repo}")

    def install_agent(self, agent_id: str):
        """Install an agent and its workflows."""
        agent_src = self.library_path / "agents" / agent_id
        if not agent_src.exists():
            raise ValueError(f"Agent '{agent_id}' not found in library.")

        # Load metadata
        metadata_path = agent_src / "metadata.yaml"
        with open(metadata_path, "r") as f:
            metadata = yaml.safe_load(f)

        # Copy AGENT.md
        dest_agent_dir = self.agent_dir / agent_id
        dest_agent_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(agent_src / "AGENT.md", dest_agent_dir / "AGENT.md")

        # Copy workflows
        for wf in metadata.get("workflows", []):
            self.install_workflow(wf)

        print(f"Successfully installed agent '{agent_id}' and associated workflows.")

    def install_workflow(self, workflow_id: str):
        """Install a single workflow file."""
        wf_filename = f"{workflow_id}.md"
        src_path = self.library_path / "workflows" / wf_filename
        dest_path = self.workflow_dir / wf_filename

        if src_path.exists():
            shutil.copy(src_path, dest_path)
            print(f"  - Installed workflow: {workflow_id}")
        else:
            print(f"  - Warning: Workflow '{workflow_id}' not found in library.")
