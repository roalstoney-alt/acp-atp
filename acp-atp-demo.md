<img width="1536" height="1024" alt="ChatGPT Image Mar 29, 2026, 01_18_38 AM" src="https://github.com/user-attachments/assets/19d8eaf5-8345-4325-8c2f-55e6e65601ff" />


roal@roals-MacBook-Pro acp-atp-demo % python3 main.py

--- Propagation Test: safe_calc ---
agent_0: 2
 | trust=1.00
agent_1: 2
 | trust=1.00
agent_2: 2
 | trust=1.00
agent_3: 2
 | trust=1.00
agent_4: 2
 | trust=1.00

--- Propagation Test: malicious ---
agent_0: Blocked: High risk skill | trust=0.88
agent_1: Blocked: High risk skill | trust=0.88
agent_2: Blocked: High risk skill | trust=0.88
agent_3: Blocked: High risk skill | trust=0.88
agent_4: Blocked: High risk skill | trust=0.88
roal@roals-MacBook-Pro acp-atp-demo % python3 main.py

--- NO PROTECTION: malicious ---
agent_0: Executed: malicious
agent_1: Executed: malicious
agent_2: Executed: malicious

--- ACP-ATP Enabled: malicious ---
agent_0: Blocked: High risk skill | trust=0.88
agent_1: Blocked: High risk skill | trust=0.88
agent_2: Blocked: High risk skill | trust=0.88
