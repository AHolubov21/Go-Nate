# NATHAN Project Documentation

**Description**

NATHAN is a system that helps DevOps engineers solve problems that arise in IT infrastructure. NATHAN uses a Slack bot to monitor alerts, Ollama (+llama2 7b) to generate prompts, and a runbook (a separate document) to determine the actions that need to be taken to resolve the problem.

**Benefits**

- **Local operation:** Ollama works completely locally, which ensures the security of working with confidential information.
- **Increased productivity:** NATHAN allows DevOps engineers to solve problems faster, which leads to increased IT infrastructure performance.
- **Reduced costs:** NATHAN can help reduce IT support costs by automating routine tasks.
- **Improved security:** NATHAN can improve IT infrastructure security by automating incident response processes.

**Components:**

- **Slack bot:**
    - Receives alerts from Slack.
    - Filters alerts by priority.
    - Passes alerts to Ollama.
- **Ollama (+llama2 7b):**
    - Generates prompts based on the alert text and information from the runbook.
    - Sends prompts to the Slack bot.
- **Runbook:**
    - Contains instructions for solving problems.
    - Stored separately from the NATHAN system.
- **Database:**
    - Stores information about alerts and system configuration.
    - Used to filter alerts and generate reports.
- **Web server:**
    - Provides an interface for managing the NATHAN system.
    - Used to configure alerts, configure Ollama, and manage runbooks.
- **AWS:**
    - NATHAN can be deployed on AWS.
    - The following AWS components are used:
        - EC2: virtual machines for the Slack bot, Ollama, and web server.
        - RDS: MySQL database.
        - S3: storage for runbooks.
        - Lambda: function for automatically updating runbooks.

**Component interaction:**

1. The Slack bot receives an alert from Slack.
2. The Slack bot filters the alert by priority.
3. The Slack bot passes the alert to Ollama.
4. Ollama generates prompts based on the alert text and information from the runbook.
5. Ollama sends prompts to the Slack bot.
6. The Slack bot posts prompts to the Slack channel.
7. The DevOps engineer resolves the problem using the information in the runbook.

**Limitations:**

- NATHAN may not have prompts for all types of alerts.
- **Accuracy sensitivity:**
    - The accuracy of Ollama prompts depends on the quality of the runbook and the content of the alert.
    - Inaccurate or incomplete runbooks can lead to inaccurate prompts.