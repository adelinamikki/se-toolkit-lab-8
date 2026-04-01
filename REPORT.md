# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent
$ uv run nanobot agent -m "What is the agentic loop?"
                                                                                                    
The agentic loop is the fundamental cycle that an AI agent follows to accomplish tasks autonomously. It typically
consists of these core stages:

 1 Perceive — Gather information about the current state (user input, environment, tool outputs, memory)
 2 Reason — Analyze the situation, plan next steps, and decide what action to take
 3 Act — Execute the chosen action (call a tool, send a message, modify a file, etc.)
 4 Observe — Receive feedback from the action (success, error, output data)
 5 Repeat — Loop back to reason with the new information until the task is complete


 ┌─────────────┐
 │   Perceive  │
 └──────┬──────┘
        ↓
 ┌─────────────┐
 │    Reason   │
 └──────┬──────┘
        ↓
 ┌─────────────┐
 │     Act     │
 └──────┬──────┘
        ↓
 ┌─────────────┐
 │   Observe   │
 └──────┬──────┘
        ↓
     (loop)


This loop enables agents to:

 • Break complex tasks into steps
 • Adapt based on feedback
 • Recover from errors
 • Maintain context across multiple actions
                                                                                                                 
In my case, each time you send a message, I go through this loop: I perceive your request, reason about what     
tools or actions are needed, act by calling tools if necessary, observe the results, and continue until I can    
provide a complete response.

Based on my exploration of the workspace, here are the available labs in your LMS:

Available Labs

Lab 8 (Current) - se-toolkit-lab-8

 • Location: /root/se-toolkit-lab-8/
 • Wiki: /root/se-toolkit-lab-8/wiki/
 • Tasks Directory: /root/se-toolkit-lab-8/lab/tasks/
 • Tasks Directory: /root/se-toolkit-lab-8/lab/tasks/

Lab 8 Tasks:

Required Tasks:

 • Task 1
 • Task 2
 • Task 3

 • Task 1
 • Task 2
 • Task 3
 • Task 1
 • Task 2
 • Task 3
 • Task 2
 • Task 3
 • Task 4
 • Task 3
 • Task 4
 • Task 4
 • Task 5
 • Task 5

Optional Tasks:
Optional Tasks:

 • Task 1
 • Task 1


Lab 1 (Reference)

 • Wiki: /root/se-toolkit-lab-8/wiki/lab-1/
 • Contains documentation and diagrams for reference

The current lab appears to be Lab 8 of a Software Engineering toolkit series. The lab focuses on hands-on tasks  
with both required and optional components. Would you like me to show you the details of any specific task?      
![Agent output](screenshots/1.png)

## Task 1B — Agent with LMS tools
$ uv run nanobot agent -m "What labs are available in our LMS?"
Here are the available labs:


 ID  Title                                                  
 ───────────────────────────────────────────────────────────
 1   - lab-01 — Lab 01 – Products, Architecture & Roles
 2   - lab-02 — Lab 02 — Run, Fix, and Deploy a Backend Service
 3   - lab-03 — Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4   - lab-04 — Lab 04 — Testing, Front-end, and AI Agents
 5   - lab-05 — Lab 05 — Data Pipeline and Analytics Dashboard
 6   - lab-06 — Lab 06 — Build Your Own Agent
 7   - lab-07 — Lab 07 — Build a Client with an AI Coding Agent
 8   - lab-08s


Would you like more details about any specific lab?
 ![Agent output](screenshots/1b.png)

## Task 1C — Skill prompt
$ uv run nanobot agent -m "Show me the scores"
Here's a summary of the scores and completion rates:

Completion Rates by Lab


 Lab     Completion Rate  Passed  Total 
 ────────────────────────────────────── 
 Lab 01  100.0%           258     258   
 Lab 02  89.1%            131     147   
 Lab 03  89.1%            156     175   
 Lab 04  97.2%            239     246   
 Lab 05  98.8%            247     250   
 Lab 06  98.4%            242     246   
 Lab 07  99.6%            238     239   
 Lab 08  0.0%             0       0     

                                                                                                                 
Key Observations

 • Highest completion: Lab 01 (100%), Lab 07 (99.6%), Lab 05 (98.8%)
 • Lowest completion: Lab 02 & Lab 03 (both 89.1%)
 • Lab 08: Not yet started (0 students)

Average Score Highlights

 • Highest avg scores: Lab setup (84.2), Plan and Scaffold (76.7), Documentation Agent (73.9)
 • Lowest avg scores: Plan skill development (16.7), Make your VM a proxy (0.0), CI/CD tasks (~33-44%)

Would you like to see top learners, group performance, or submission timelines for any specific lab?
![Agent output](screenshots/1cc.png)

## Task 2A — Deployed agent



## Task 2B — Web client



## Task 3A — Structured logging



## Task 3B — Traces



## Task 3C — Observability MCP tools



## Task 4A — Multi-step investigation



## Task 4B — Proactive health check



## Task 4C — Bug fix and recovery


