# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent
root@adelinamikki001:~/se-toolkit-lab-8/nanobot# uv run nanobot agent --logs --session cli:task1a-loop -c ./config.json -m "What is the agentic loop?"
Using config: /root/se-toolkit-lab-8/nanobot/config.json
2026-04-01 13:20:43.412 | INFO     | nanobot.agent.loop:_process_message:425 - Processing message from cli:user: What is the agentic loop?
⠹ nanobot is thinking...2026-04-01 13:20:43.742 | DEBUG    | nanobot.agent.memory:maybe_consolidate_by_tokens:323 - Token consolidation idle cli:task1a-loop: 4886/65536 via tiktoken

🐈 nanobot
The agentic loop is the fundamental reasoning cycle that autonomous AI agents use to accomplish tasks. It's a    
continuous feedback loop with these core stages:

Core Stages


 Stage     Description                                                         
 ───────────────────────────────────────────────────────────────────────────── 
 Perceive  Gather information (user input, environment, tool outputs, memory)  
 Reason    Analyze, plan, and decide on the next action
 Act       Execute the chosen action (call tools, modify files, send messages) 
 Observe   Process the outcome (results, errors, new state)
 Repeat    Loop back until the goal is achieved


Key Characteristics

 • Iterative — Breaks complex tasks into sequential steps
 • Adaptive — Adjusts plans based on real-time feedback
 • Autonomous — Can act without constant user guidance
 • Self-correcting — Can recover from errors and try alternative approaches

What Makes It "Agentic"

Unlike a standard chatbot that responds in a single turn, an agent using this loop can:
                                                                                                                 
 • Chain multiple tool calls together
 • Make decisions based on intermediate results
 • Persist context across actions
 • Complete multi-step workflows independently

This loop is the foundation of agentic AI systems—it's what enables an assistant like me to read files, run      
commands, search the web, and synthesize results all within a single request.

2026-04-01 13:20:59.171 | INFO     | nanobot.agent.loop:_process_message:479 - Response to cli:user: The **agentic loop** is the fundamental reasoning cycle that autonomous AI agents use to accomplish tasks. It's a contin...  
2026-04-01 13:20:59.180 | DEBUG    | nanobot.agent.memory:maybe_consolidate_by_tokens:323 - Token consolidation idle cli:task1a-loop: 5194/65536 via tiktoken

root@adelinamikki001:~/se-toolkit-lab-8/nanobot# uv run nanobot agent --logs --session cli:task1a-labs -c ./config.json -m "What labs are available in our LMS?" Using config: /root/se-toolkit-lab-8/nanobot/config.json 2026-03-31 22:56:44.610 | INFO | nanobot.agent.loop:_process_message:425 - Processing message from cli:user: What labs are available in our LMS? 🐈 nanobot I'll explore the workspace to find information about available labs in the LMS. 2026-03-31 22:56:49.240 | INFO | nanobot.agent.loop:_prepare_tools:253 - Tool call: list_dir({"path": "/root/se-toolkit-lab-8/nanobot/workspace"}) 2026-03-31 22:56:54.475 | INFO | nanobot.agent.loop:_prepare_tools:253 - Tool call: exec({"command": "find /root/se-toolkit-lab-8 -type d -name \"*lab*\" 2>/dev/null | head -20"}) 2026-03-31 22:57:04.159 | INFO | nanobot.agent.loop:_prepare_tools:253 - Tool call: list_dir({"path": "/root/se-toolkit-lab-8/lab"}) 2026-03-31 22:57:04.159 | INFO | nanobot.agent.loop:_prepare_tools:253 - Tool call: list_dir({"path": "/root/se-toolkit-lab-8/wiki"}) 2026-03-31 22:57:09.123 | INFO | nanobot.agent.loop:_prepare_tools:253 - Tool call: list_dir({"path": "/root/se-toolkit-lab-8/wiki/lab-1"}) 2026-03-31 22:57:09.124 | INFO | nanobot.agent.loop:_prepare_tools:253 - Tool call: read_file({"path": "/root/se-toolkit-lab-8/wiki/lab.md"}) 2026-03-31 22:57:11.294 | INFO | nanobot.agent.loop:_prepare_tools:253 - Tool call: exec({"command": "ls -la /root/se-toolkit-lab-8/wiki/ | grep -i lab"}) 2026-03-31 22:57:16.498 | INFO | nanobot.agent.loop:_prepare_tools:253 - Tool call: list_dir({"path": "/root/se-toolkit-lab-8/wiki/lab-1/docs"}) 2026-03-31 22:57:16.499 | INFO | nanobot.agent.loop:_prepare_tools:253 - Tool call: exec({"command": "find /root/se-toolkit-lab-8 -maxdepth 2 -type d -name \"lab*\" 2>/dev/null"}) 2026-03-31 22:57:27.899 | INFO | nanobot.agent.loop:_prepare_tools:253 - Tool call: read_file({"path": "/root/se-toolkit-lab-8/lab/tasks"}) 2026-03-31 22:57:27.899 | INFO | nanobot.agent.loop:_prepare_tools:253 - Tool call: exec({"command": "ls -la /root/se-toolkit-lab-8/lab/tasks/"}) 2026-03-31 22:57:30.243 | INFO | nanobot.agent.loop:_prepare_tools:253 - Tool call: exec({"command": "ls -la /root/se-toolkit-lab-8/lab/tasks/required/ /root/se-toolkit-lab-8/lab/tasks/optional/"}) 🐈 nanobot Based on my exploration of the workspace, here are the available labs in your LMS: Available Labs Lab 8 (Current) - se-toolkit-lab-8 • Location: /root/se-toolkit-lab-8/ • Wiki: /root/se-toolkit-lab-8/wiki/ • Tasks Directory: /root/se-toolkit-lab-8/lab/tasks/ Lab 8 Tasks: Required Tasks: • Task 1 • Task 2 • Task 3 • Task 4 • Task 5 Optional Tasks: • Task 1 Lab 1 (Reference) • Wiki: /root/se-toolkit-lab-8/wiki/lab-1/ • Contains documentation and diagrams for reference The current lab appears to be Lab 8 of a Software Engineering toolkit series. The lab focuses on hands-on tasks with both required and optional components. Would you like me to show you the details of any specific task? 2026-03-31 22:57:48.870 | INFO | nanobot.agent.loop:_process_message:479 - Response to cli:user: Based on my exploration of the workspace, here are the available labs in your LMS: ## Available Labs **Lab 8** (Curren... 2026-03-31 22:57:49.063 | DEBUG | nanobot.agent.memory:maybe_consolidate_by_tokens:323 - Token consolidation idle cli:task1a-labs: 8047/65536 via tiktoken

![Agent output](screenshots/1.png)

## Task 1B — Agent with LMS tools
root@adelinamikki001:~/se-toolkit-lab-8/nanobot# NANOBOT_LMS_BACKEND_URL=http://localhost:42002 \
NANOBOT_LMS_API_KEY=key8 \
uv run nanobot agent -c ./config.json -m "What labs are available?"
Using config: /root/se-toolkit-lab-8/nanobot/config.json

🐈 nanobot
Here are the available labs:


 ID  Title                                                  
 ───────────────────────────────────────────────────────────
 1   Lab 01 – Products, Architecture & Roles
 2   Lab 02 — Run, Fix, and Deploy a Backend Service
 3   Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4   Lab 04 — Testing, Front-end, and AI Agents
 5   Lab 05 — Data Pipeline and Analytics Dashboard
 6   Lab 06 — Build Your Own Agent
 7   Lab 07 — Build a Client with an AI Coding Agent
 8   lab-08


Would you like more details about any specific lab?

root@adelinamikki001:~/se-toolkit-lab-8/nanobot# uv run nanobot agent -c ./config.json -m "Is the LMS backend healthy?"
Using config: /root/se-toolkit-lab-8/nanobot/config.json

🐈 nanobot
Let me check if the LMS backend is responding by querying for labs:

🐈 nanobot
Yes, the LMS backend appears to be healthy!                                                                      
                                                                                                                 
I can see that the LMS backend is running:                                                                       
                                                                                                                 
 • uvicorn is running the lms_backend.main:app application (PID 1693588)                                         
                                                                                                                 
The backend service is up and responding, which is why I was able to retrieve the list of labs earlier. The LMS  
MCP tools are working correctly.

 ![Agent output](screenshots/1b.png)

## Task 1C — Skill prompt
root@adelinamikki001:~/se-toolkit-lab-8/nanobot# uv run nanobot agent --logs --session cli:task1c -c ./config.json -m "Show me the scores"
Using config: /root/se-toolkit-lab-8/nanobot/config.json
2026-04-01 13:37:07.698 | INFO     | nanobot.agent.loop:_process_message:425 - Processing message from cli:user: Show me the scores
⠙ nanobot is thinking...2026-04-01 13:37:07.897 | DEBUG    | nanobot.agent.memory:maybe_consolidate_by_tokens:323 - Token consolidation idle cli:task1c: 8751/65536 via tiktoken
                                                                                                                 
🐈 nanobot
Let me get the individual learner scores:
2026-04-01 13:37:16.780 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: mcp_lms_lms_learner_scores({"lab": "lab-01"})
2026-04-01 13:37:16.781 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: mcp_lms_lms_learner_scores({"lab": "lab-02"})
2026-04-01 13:37:16.781 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: mcp_lms_lms_learner_scores({"lab": "lab-03"})
2026-04-01 13:37:16.781 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: mcp_lms_lms_learner_scores({"lab": "lab-04"})
2026-04-01 13:37:16.781 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: mcp_lms_lms_learner_scores({"lab": "lab-05"})
2026-04-01 13:37:16.781 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: mcp_lms_lms_learner_scores({"lab": "lab-06"})
2026-04-01 13:37:16.781 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: mcp_lms_lms_learner_scores({"lab": "lab-07"})
2026-04-01 13:37:39.836 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: mcp_lms_lms_group_performance({"lab": "lab-01"})
2026-04-01 13:37:39.837 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: mcp_lms_lms_group_performance({"lab": "lab-02"})
2026-04-01 13:37:39.837 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: mcp_lms_lms_group_performance({"lab": "lab-03"})
2026-04-01 13:37:39.837 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: mcp_lms_lms_group_performance({"lab": "lab-04"})
2026-04-01 13:37:39.837 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: mcp_lms_lms_group_performance({"lab": "lab-05"})
2026-04-01 13:37:39.837 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: mcp_lms_lms_group_performance({"lab": "lab-06"})
2026-04-01 13:37:39.837 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: mcp_lms_lms_group_performance({"lab": "lab-07"})
2026-04-01 13:37:46.047 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: read_file({"path": "/root/se-toolkit-lab-8/nanobot/workspace/skills/lms/SKILL.md"})
                                                                                                                 
🐈 nanobot
I've already shown you the available score data from the LMS. Here's what I can provide with the available tools:

Summary of Scores Already Shown:

Completion Rates


 Lab     Rate    Passed/Total 
 ──────────────────────────── 
 Lab 01  100.0%  258/258      
 Lab 02  89.1%   131/147      
 Lab 03  89.1%   156/175      
 Lab 04  97.2%   239/246      
 Lab 05  98.8%   247/250      
 Lab 06  98.4%   242/246      
 Lab 07  99.6%   238/239      
 Lab 08  0.0%    0/0


Average Task Scores (already provided in detail above)

The LMS tools available (mcp_lms_labs, mcp_lms_pass_rates, mcp_lms_completion_rate) don't include individual     
learner scores or group performance breakdowns.

What specific score information are you looking for? For example:

 • A specific lab's task scores?
 • Comparison between labs?
 • A particular format or visualization?
 • Something else I haven't shown yet?

2026-04-01 13:37:54.665 | INFO     | nanobot.agent.loop:_process_message:479 - Response to cli:user: I've already shown you the available score data from the LMS. Here's what I can provide with the available tools:

## Su...
2026-04-01 13:37:54.677 | DEBUG    | nanobot.agent.memory:maybe_consolidate_by_tokens:323 - Token consolidation idle cli:task1c: 11209/65536 via tiktoken
![Agent output](screenshots/1cc.png)

## Task 2A — Deployed agent

Nanobot gateway startup logs:

```
nanobot-1  | Using config: /app/nanobot/config.resolved.json
nanobot-1  | 🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
nanobot-1  | ✓ Channels enabled: webchat
nanobot-1  | ✓ Heartbeat: every 1800s
nanobot-1  | MCP server 'lms': connected, 9 tools registered
nanobot-1  | MCP server 'webchat': connected, 1 tools registered
nanobot-1  | Agent loop started
```

All containers running:
```
se-toolkit-lab-8-backend-1          Up 11 seconds
se-toolkit-lab-8-caddy-1            Up 10 seconds    0.0.0.0:42002->80/tcp
se-toolkit-lab-8-nanobot-1          Up 11 seconds
se-toolkit-lab-8-qwen-code-api-1    Up 16 seconds (healthy)
se-toolkit-lab-8-postgres-1         Up 17 seconds (healthy)
se-toolkit-lab-8-client-web-flutter-1  Up
se-toolkit-lab-8-client-web-react-1    Up
```

## Task 2B — Web client

**Flutter web client** — `http://localhost:42002/flutter/` serves real content, `main.dart.js` present.

**WebSocket test** — `ws://localhost:42002/ws/chat?access_key=adelinamikki`:

Request: `{"type":"message","content":"What labs are available?"}`

Response:
```json
{"type":"text","content":"Currently, there are **no labs available** in the LMS. The backend is healthy, but the item count is 0 — meaning no labs have been loaded or created yet.\n\nWould you like me to trigger a sync pipeline to see if that pulls in any lab data?","format":"markdown"}
```

The full chain works: Flutter → Caddy → WebSocket → nanobot gateway → LMS MCP → agent responds through WebSocket without errors.

## Task 3A — Structured logging



## Task 3B — Traces



## Task 3C — Observability MCP tools



## Task 4A — Multi-step investigation



## Task 4B — Proactive health check



## Task 4C — Bug fix and recovery


