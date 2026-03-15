# Pika Robot: Overall System Architecture & Feature Overview

**Date: 1/12/2025**

## High-Level Architecture Diagram

The following diagram illustrates the interaction between the core components, the user (child and parent), and the backend services.

**Core Component Descriptions**

| Component | Detailed Description |
| :--- | :--- |
| **User (Child & Parent)** | The primary interactors. The child engages directly with the Pika robot for learning and play. The parent uses a companion app for monitoring, configuration (like setting alarms), receiving progress reports, and viewing leaderboards. |
| **Pika Robot (Core Interface)** | The physical robot is the central point of interaction for the child. It houses the primary software systems that manage conversation, activities, and user engagement. |
| **The Orchestration System** | The Orchestration System is the central processing unit and decision-making layer of the Pika Robot's software architecture. It acts as the master conductor, intelligently sequencing and managing the flow of all user-facing interactions. While not a single, monolithic block, its functions are primarily executed by the Navigation System and the Buddy System, working in concert to create a seamless, dynamic, and personalized user journey. |
| **Buddy System** | This system shapes Pika's personality, making it a "playful friend" rather than a machine. It manages both free-form conversations (Buddy Talk) and structured games/lessons (Buddy Activity). The system is now detailed with a "Progressive Friendship" logic across 3 phases (Stranger, Acquaintance, Friend), determined by a `friendship_score`. It also includes context handling via `dynamic_memory` (shared memories) and daily activity selection based on interests and friendship level. An In-Session Routing mechanism allows Pika to flexibly respond to the child's spontaneous requests. |
| **Adaptive Learning Path** | The core educational engine, providing a structured curriculum of **Topics**, Missions, and Activities. This system dynamically adjusts content based on the child's real-time performance, ensuring the learning experience is always at the optimal difficulty level, following a "Present - Practice - Produce" model. |
| **Retention System** | A strategic framework designed to ensure long-term user engagement, built on the "Hook Cycle" model. This system has been significantly expanded with the following sub-components: <br> ● Instant Gratification System: Provides immediate rewards (XP, Stars, Gems) with engaging visual and audio effects. <br> ● Alarm System: Allows parents to set alarms to integrate Pika into the child's daily routine. <br> ● Dashboard System: Provides parents with insights into their child's diligence and progress via the companion app. <br> ● Ranking Feature: A weekly, XP-based leaderboard system with leagues and small competition groups to drive motivation. <br> ● Notification System: Sends external triggers to parents to maintain engagement. |
| **Learning Content System** | A new foundational system that defines the UX standards for all learning content. It includes detailed rules for Verbal Factors, Non-Verbal/Media Factors, and Systematic Factors. This system ensures a consistent, intuitive, and engaging learning experience through principles like "Show, Don't Tell" and activity templates. |
| **Backend & AI Services** | A suite of cloud-based services that power the robot's intelligence. This includes AI models for speech recognition and Natural Language Processing (NLP), user profile databases, and the core logic for all the above systems, including calculating the `friendship_score`, managing leaderboards, and storing `dynamic_memory`. |

## Orchestration

Receive a list of agent “talk” and “learn” messages returned at the start of the day (5 talk agents, 1 greeting, and 4 learn agents).
Play them sequentially in the following order:
`Greeting → Talk → Learn → Talk → Learn → Talk → Learn → Talk → Learn → Talk.`

### Buddy Activity

This component focuses on engaging the child through proactive, interactive, and high-impact activities beyond the core curriculum.

*   **Persona Definition:** Pika's core personality is defined as mischievous, playful, and curious. It expresses a wide range of emotions appropriate to the context, such as "sulking" (dỗi) when it loses a game or celebrating enthusiastically when it wins. Its role is that of a peer, not a teacher.
*   **Proactive Engagement:** Pika is designed to be proactive, initiating 70% of "trick-playing" (bày trò) activities. This spontaneity creates moments of surprise and delight, making each session feel unique and exciting.
*   **High-Impact Activity Groups:** The system prioritizes activities that are proven to be highly engaging for children:
    *   **Physical Movement:** Pika encourages the child to sing, dance, and perform simple exercises along with it.
    *   **Creativity & Storytelling:** Pika can tell stories, suggest role-playing different professions, or even do voice-overs for cartoon characters with the child.
    *   **Games & Learning:** Educational concepts are seamlessly integrated into fun games, such as word association or guessing games, embodying the principle of "learning through play" (học mà chơi).

### Buddy Talk

This component governs Pika's conversational abilities, making interactions feel natural, personal, and intelligent.

*   **Contextual Greetings (Agent Greeting):** Pika's greetings are highly personalized and driven by a sophisticated logic system that considers:
    *   **User-Centric Factors:** Frequency of use (e.g., "I missed you!"), special events (birthdays, holidays), and even the time of day.
    *   **Pika-Centric Factors:** Pika creates surprise by initiating greetings with unexpected actions like a dance, a song, or a funny face, making the start of every session a delightful experience.
*   **Free Talk & Integrated Learning (Agent Talk):** This feature allows for open-ended conversation while subtly integrating learning. Pika can chat freely with the child about their day and then cleverly transition into practicing vocabulary or English sentence structures that are relevant to the topic of conversation. This is called Post-Talk Practice.
*   **"Progressive Friendship" Logic:** The system is designed to simulate the development of a real friendship over time through distinct phases.
    1.  **Phase 1 (Meeting You):** Pika acts as a **safe guide and game initiator** to build initial trust. Interaction is primarily activity-based, with surface-level questions to gather basic data.
    2.  **Phase 2 (Getting Closer):** Pika transitions to the role of a **caring friend**, using memory to personalize interactions, demonstrating understanding, and expanding topics to safe social areas (school, friends).
    3.  **Phase 3 (Good Friends):** Pika becomes an **emotional partner**, focusing on sharing experiences, deep emotions, and building a shared history. The relationship reaches its highest level of intimacy, allowing the child greater autonomy and session leadership.

**High-Level Overview Table of the 3 Phases**

| Core Element | Phase 1: Meeting You | Phase 2: Getting Closer | Phase 3: Good Friends |
| :--- | :--- | :--- | :--- |
| **Child's Feeling** | Curious, uncertain about interaction possibilities. | Safe, confident, but needs a personal connection. | Remembered, understood, but desires a true partnership. |
| **Pika's Emotional Goal** | To create a feeling of Safety and Excitement (non-judgmental, surprising). | To create a feeling of being Remembered and Understood (recalls preferences, shows interest). | To create a feeling of Shared History and True Partnership (shared memories, being a "team"). |
| **Topic** | Basic preferences, daily activities, pets | Adds school, friends, family (non-sensitive) Followup children hobbies | Adds stories, deeper interests, future plans |
| **Conversation Depth** | Surface-level: Basic topics (hobbies, pets). No "Why?" questions. Memory: No reference to past sessions. | Preference-level: Dives deeper into known topics. Starts asking "Why?". Memory: Recalls and references details from the last 2-3 sessions. | Personal-level: Shifts from "what" to "how you feel" ("How did that make you feel?"). Memory: Comprehensive history (>10 sessions), references "inside jokes." |
| **Session Structure** | Pika leads 100%. | Pika leads 80% (offers the child 2-3 choices). | 50/50 Co-led (child is free to initiate and lead). |

### In-session Routing

The In-Session Routing mechanism is a dynamic system that ensures Pika remains highly responsive and adaptive to the child's spontaneous, real-time requests, even when they deviate from the planned session flow. It functions as a dynamic Intent Recognition and Action Dispatcher.

The system operates on the principle of prioritizing **the child's immediate needs** over the structured flow, ensuring the interaction always feels natural and supportive.

**Core Routing Principles:**

*   **Dynamic Intent Recognition:** The system continuously monitors the child's input to classify spontaneous requests into specific categories (e.g., Game Request, Song Request, Backstory Inquiry, Off-Topic Question, Emotional Expression).
*   **Specialized Agent Dispatch:** Based on the recognized intent, the system immediately dispatches the session control to the appropriate specialized Agent (e.g., Game Agent, Story Agent, Emotion Agent, AMA Agent).
*   **Graceful Failure and Redirection:** If the child requests an activity Pika cannot perform, Pika uses a playful, non-frustrating tone to decline, immediately offering an available alternative to maintain engagement and avoid disappointment.

## The Buddy System

The Buddy System is the heart of the robot's personality, designed to transform Pika from a simple "learning machine" into a playful, mischievous, and supportive friend. This system's primary goal is to create a genuine emotional connection with the child, which is a key driver for long-term engagement. It is divided into two main components: Buddy Activity and Buddy Talk.

### Context Handling

This section describes how the system converts daily raw interactions into long-term state variables, forming Pika's "memory" of the user.

#### 1. Product Objective

> **Ensure that every user interaction is recorded and influences the long-term relationship, creating the feeling that "Pika remembers me" and encouraging users to return to maintain the relationship.**

#### 2. Execution Logic: Core Data Structure

All execution logic revolves around the user's `friendship_status` record. The most important data fields include:

| Field Name | Product Purpose | Technical Description |
| :--- | :--- | :--- |
| **friendship_score** | The core metric measuring the level of closeness. It is the "long-term memory" of the relationship history. | Float value, changes daily. |
| **friendship_level** | Determines Pika's overall tone and behavior (e.g., level of intimacy, sensitive topics). | Enum: STRANGER, ACQUAINTANCE, FRIEND. |
| **dynamic_memory** | Stores facts from Pika vs User conversations. | Array of Objects, storing specific "shared memories" (e.g., pet's name, promises). |
| **topic_metrics** | Helps Pika "listen" and identify the child's interests to personalize content. | Map/Object, storing scores and interaction history for each topic/Agent. |
| **streak_day** | Records user commitment, used to trigger special Greeting scenarios. | Integer, number of consecutive interaction days. |

#### 3. Execution Logic: End-of-Turn Update Process (Context handling)

**4-Step Process:**

1.  **Calculate `daily_change_score`:**
    *   The change score is calculated based on daily interaction metrics, with weights assigned to encourage desired behavior:
        *   **Base Score:** Based on the total number of turns (`total_turns * 0.5`).
        *   **Engagement Bonus:** Rewards proactive user behaviors (e.g., `user_initiated_questions * 3`, `followup_topics_count * 5`).
        *   **Emotion Bonus:** Rewards/Penalizes based on the session's dominant emotion (`+15` for 'interesting', `-15` for 'boring').
        *   **Memory Bonus:** Rewards the creation of new memories (`new_memories_count * 5`).
2.  **Update Long-Term Status:**
    *   `friendship_score` is updated by adding the `daily_change_score`.
    *   `friendship_level` is re-derived from `friendship_score` (e.g., `> 3000` is FRIEND).
    *   `topic_metrics` is updated with the score and the last interaction date for each topic.
    *   `streak_day` is updated (incremented by 1 if continuous interaction, reset to 1 if interrupted).

### Daily Selection Game-Talk

This section describes the algorithm for personalizing the content at the start of the day, ensuring the user always receives the most suitable greeting and activities.

#### 1. Product Objective

> **Personalize the start-of-day experience, providing content that matches the current friendship phase and the user's closest interests/emotions, encouraging users to interact and explore new Agents/Games.**

#### 2. Execution Logic: Selection Algorithm

The selection algorithm operates on a hierarchical principle: **Phase -> Pool -> Priority**

**A. Step 1: Friendship Phase Determination**

The friendship phase determines the scope of content the user can access, ensuring a natural progression of the relationship.

| Phase | `friendship_score` Threshold | Relationship Status | Content Scope (Pool) |
| :--- | :--- | :--- | :--- |
| **Phase 1** | `< 500` | **Stranger** | "Surface" content, simple Games, basic Greeting (V1). |
| **Phase 2** | `500 - 3000` | **Acquaintance** | Unlocks "School," "Friends" Agents, personalized Games, Greeting V2. |
| **Phase 3** | `> 3000` | **Friend** | Unlocks "Family," "Shared History" Agents, collaborative project Games, Greeting V3. |

**B. Step 2: Greeting Selection (Priority-Based Selection)**

The system selects a single Greeting based on a strict priority order, regardless of the Phase, to create the most powerful personalized moment:

1.  **Priority 1 (Event):** Check for special events (e.g., User's Birthday).
2.  **Priority 2 (Re-entry Time):** Check for critical states (e.g., `last_interaction_date > 7 days` -> **Returning After Long Absence** scenario).
3.  **Priority 3 (Closest Context):** Check `last_day_follow_up_topic` (if present -> Greeting follows up on yesterday's topic).
4.  **Priority 4 (Default):** If no conditions are met, select the `daily_checkin`.

**C. Step 3: Selection of 5 Talk/Game Activities (Talk Selection)**

The system creates a Candidate List and uses weighting to select the final 4 activities, ensuring a balance between interest and exploration.

1.  **Create Candidate List:**
    *   **Exploration:** 1 random Agent from the Phase pool that the user interacts with least (promotes discovery of new content).
    *   **Interest:** x remaining Agents with the highest `topic_score` (ensures the user sees content they like).
    *   **Game:** Add random Games from the Phase pool.
2.  **Assemble Final List:**
    *   Select 5 activities from the candidate list.
    *   Apply the Talk:Activity Ratio of the Phase to balance (e.g., Phase 1 may prioritize Games over Talk).
        *   Phase 1 - Talk:Game ratio -> 40/60
        *   Phase 2 - Talk:Game ratio -> 50:50
        *   Phase 3 - Talk:Game ratio -> 60/40

## The Adaptive Learning Path System

The Adaptive Learning Path is the core educational engine of the Pika robot. It ensures that the learning experience is tailored to each child's individual pace and proficiency, maximizing both engagement and educational outcomes. The system's goal is to make learning feel like a personalized journey of discovery, not a rigid, one-size-fits-all curriculum.

### 1. Structure of the Learning Path

The learning content is organized hierarchically to provide a clear and logical progression for the child. This structure is referred to as **"Lộ trình của bé" (The Child's Learning Path)**.

*   **Topics:** The highest level of organization, representing broad subject areas (e.g., Topic 1: Feelings, Topic 2: Animals).
*   **Missions:** Each Topic is broken down into a series of Missions. Each mission focuses on a specific, achievable learning objective (e.g., Mission 1: Learn Vocabulary, Mission 2: Form a Sentence, Mission 3: Ask a Question).
*   **Activities:** Each Mission consists of a sequence of diverse activities designed to teach and reinforce the objective. These activities often follow a "Present - Practice - Produce" model.

### 2. The Adaptive System: Personalizing the Journey

The Adaptive System is the intelligence layer that dynamically adjusts the Learning Path in real-time. It ensures the level of challenge is always optimal—not so hard that it's discouraging, and not so easy that it's boring.

**Key Adaptive Triggers and Actions:**

The system uses a series of triggers to evaluate the child's performance and engagement, then takes appropriate action.

| Trigger | Data Points & Condition | Adaptive Action |
| :--- | :--- | :--- |
| **Evaluation of Learning Performance** | Parental input during onboarding phase or evaluation after each milestones | Propose relevant learning path according to level or knowledge acquisition speed |
| **Performance on an Activity** | Child struggles with a concept (e.g., pronunciation score < 50% or incorrect answers). | **Targeted Practice:** Pika initiates a "Sword Sharpening" (Rèn kiếm) activity—a fun, focused mini-game to practice the specific words or concepts the child found difficult. |
| **Performance Milestones** | Child completes a major assessment or a series of missions. | **Path Adjustment:** Based on the child's aggregate score (measuring fluency, accuracy, vocabulary), the system adjusts the difficulty of the upcoming learning path. It can also send a notification to the parent's app recommending a change. |
| **Signs of Disengagement** | Child shows signs of boredom (e.g., repeated non-interaction, low-energy responses). | **Suggest Freetalk:** The system identifies this as a cue to move away from structured learning and suggests a more open-ended, fun Freetalk session to re-engage the child. |
| **Session Time Limits** | The child has been engaged in a learning session for over 15 minutes. | **Agent "Change of Pace" (Đổi gió):** Pika proactively suggests a micro-break or a switch to a different, fun activity to maintain high energy and focus. |

### Adaptive Learning System (MVP 1.2)

The Adaptive Learning System for Pika cleanly separates ***what*** the child learns from ***how*** Pika talks to them. Instead of tying level A2 = full English (and stressing some kids), the system introduces two independent settings stored in the user profile:

*   **`learn_level`** (e.g. `pre_a1`, `a2`): defines the learning path and difficulty – which **learning path, post-greeting review**, and **post-talk practice** instructions the child gets.
*   **`language_mode`** (e.g. `VN`, `VN-EN`, `EN`): defines how Pika communicates in buddy-style conversations (Greeting, Talk, Games) – either in full Vietnamese, mixing Vietnamese support with English instructions and exclamations, or using simple full English – without changing the academic content.

Parents configure these two knobs during onboarding and can change them anytime in the Parent App settings. The app sends both values to the backend, which saves them independently on the system's memory, and passes them to the robot’s orchestration layer at the start of each session. The orchestration system then:

*   Uses `learn_level` to select the correct **learning path** and **Talk Agent instructions**.
*   Uses `language_mode` to inject the proper language guidelines into the prompts for all conversational agents.

Overall, the feature aims to:

1.  Give parents fine-grained control over difficulty vs. language pressure.
2.  Reduce anxiety and increase engagement for kids with different confidence levels.
3.  Create a future-proof architecture where new levels and language modes can be added without rewriting core logic.

## The Retention System

The Retention System Architecture is a strategic framework designed to foster long-term user engagement by transforming the use of Pika into a positive and recurring habit. It is scientifically designed around the "Hook Cycle" model, which consists of four key phases: Trigger, Action, Variable Reward, and Investment. This cycle is applied at different scales to address short-term, medium-term, and long-term retention.

**Key Strategic Components Supporting Retention**

*   **Parental Engagement Loop:** Keeps parents invested through progress reports, scheduling tools, and milestone notifications.
*   **Mission and Narrative System:** Weaves all activities into a compelling storyline that makes the child want to know "what happens next."
*   **Collectible & Customization System:** Taps into the innate desire to collect and personalize, making Pika feel truly "owned" by the child.

### 1. Instant Gratification System

This system is designed to provide immediate, positive, and satisfying feedback to the child during learning activities. It is the engine behind the "Variable Reward" phase of the Micro-Hook cycle.

**Key Features:**

*   **Multi-Tiered Rewards:** The system offers a variety of rewards to keep the experience interesting:
    *   **XP (Popa Crystals):** The primary reward currency, awarded for every correct answer. The amount is tiered based on the difficulty and type of question (`+10`, `+20`, or `+30 XP`). For example, a simple multiple-choice question might be worth `+10 XP`, while a correct, first-try pronunciation exercise is worth `+30 XP`.
    *   **Stars:** Awarded at the end of a speech-related exercise to provide qualitative feedback on pronunciation quality. The system rates the performance as 1, 2, or 3 stars, accompanied by encouraging text.
    *   **Gems (Kim cương):** Another form of currency that can be used for specific unlocks or purchases.
*   **Engaging Feedback Loop:** Rewards are never just a number on a screen. They are delivered through a rich, multi-sensory experience:
    *   **Visuals:** Engaging GIFs and animations, such as Pika "absorbing" the earned XP crystals or a celebratory star animation.
    *   **Audio:** Satisfying sound effects that confirm a correct answer and celebrate the reward.
    *   **UX Text:** Encouraging words from Pika, like "Awesome!" or "You're a superstar!"
*   **Backend Integration:** The backend system is responsible for the core logic. It receives the user's answer, evaluates it, determines the appropriate reward "score," and sends this back to the robot. It also aggregates all earned rewards and syncs the totals with the parent's companion app, allowing them to see their child's achievements.

### 2. Alarm System (Báo thức)

This feature is a powerful "External Trigger" in the Meso-Hook (weekly) retention cycle. It allows parents to seamlessly integrate Pika into their child's daily routine.

**Key Features:**

*   **Parent-Controlled Scheduling:** Parents can use the companion app to set alarms for specific times and associate them with a particular activity (e.g., "Time to study," "Time to wake up," "Time to sleep").
*   **Context-Aware Activation:** The alarm system is intelligent. It will only activate if the robot is currently idle. If the child is already in the middle of an activity, the alarm is postponed or ignored to avoid disrupting their flow and causing frustration.
*   **Interactive and Personalized Reminder:** When the alarm goes off, it's an interactive event, not a passive sound:
    *   **UI:** A custom user interface appears on Pika's screen.
    *   **Audio:** A unique notification sound plays.
    *   **Voice:** Pika speaks a personalized line, such as, "[Child's Name], it's time for [Activity]! Are you ready?"
    *   **Confirmation:** The child can confirm they are ready with a voice command ("I'm ready!") or by pressing the Home button.
*   **Fail-Safe Notification Loop:** The system is designed to be reliable. If the alarm cannot be delivered for any reason (e.g., the robot is turned off or has lost its internet connection), a push notification is sent to the parent's app with the message: "Pika could not sound the alarm because it is off or disconnected." This ensures the parent is always aware and can intervene if necessary.

### 3. The Dashboard System

The Dashboard System is the core component of the Parent Companion App, designed to provide parents with transparent, actionable insights into their child's learning journey and engagement with the Pika robot. Its primary goal is to empower parents to support and encourage their child's learning without requiring excessive effort, thereby reinforcing the Meso-Hook and Macro-Hook cycles of the Retention System.

**Key Features and Purpose**

*   **Audience:** All parents who purchase the Pika robot and download the companion app.
*   **Core Need:** Parents need to easily grasp their child's diligence (engagement) and progress (learning outcomes).
*   **Integration:** The Dashboard acts as the visual front-end for data collected by the Adaptive Learning Path, Retention System, and Instant Gratification System.

**Homepage Dashboard**

The main dashboard view is designed for quick, daily monitoring and provides the following key data points:

| Component | Data Displayed | Purpose |
| :--- | :--- | :--- |
| **Header/Date Selector** | Displays the current date, with options to switch to "Hôm nay" (Today), "Hôm qua" (Yesterday), or select a specific date from a calendar UI. | Allows parents to quickly review the child's performance on a specific day. Clicking a date navigates to the detailed daily report. |
| **Happy Learning Time (Thời gian Học vui vẻ)** | Total time the child spent actively engaged with the Pika robot in learning activities. | Measures diligence and habit formation. Directly supports the goal of consistent, 15+ minute sessions. |
| **New Words/Sentences Learned (Từ mới/Mẫu câu mới đã học)** | The number of new vocabulary words or sentence structures the child has successfully mastered on that day. | Measures progress and content mastery. Provides a tangible metric for learning outcomes. |
| **This Week's Achievements (Thành tích tuần này)** | A summary of the child's performance and milestones for the current week. | Provides a high-level view of weekly consistency and progress, supporting the Meso-Hook cycle. |

### 4. Ranking Feature

The Ranking feature will be built upon the existing **"Tinh thể Popa" (XP) system** and is designed to increase user engagement and retention. Our research also points to a clear solution. Parents and children alike are highly receptive to gamified learning and social competition. By introducing a ranking feature, we can:

*   **Provide Extrinsic Motivation:** A leaderboard that visualizes progress and ranks users creates a powerful external driver for daily practice.
*   **Tap into Social Awareness:** For children in the 8-10 age range, social status and peer comparison are emerging motivators. A ranking system leverages this to make learning a more social and competitive activity.
*   **Increase Retention:** Weekly competition cycles and the goal of advancing to higher leagues create a compelling reason for users to return to the app every day and every week.

| Component | Description | Rationale (Why we are building this) |
| :--- | :--- | :--- |
| **1. Weekly XP Leaderboard** | A leaderboard that ranks users based on the total "Tinh thể Popa" (XP) earned within a 7-day period (Monday to Sunday). | Provides a clear, short-term goal that encourages daily practice. It directly addresses the user need for motivation and leverages the existing XP system. |
| **2. Simplified League System** | A three-tiered league system: **Bronze, Silver, and Gold**. New users start in Bronze. Weekly, top performers are promoted, and low performers are demoted. | Manages competition by grouping users of similar levels, making it less intimidating for younger children. It creates a clear, long-term progression path. |
| **3. Small Competition Groups** | Within each league, users will be placed in small, randomly assigned groups of 30. The leaderboard will only show rankings within this group. | Makes the competition feel personal and achievable for a 6-10 year old. It increases the perceived chance of "winning" and reduces the discouragement of a large, global leaderboard. |
| **4. Child-Friendly UI & Animations** | A highly visual and engaging interface with unique league badges, celebratory animations for rank changes, and positive, encouraging language. | The target audience responds strongly to visual feedback and positive reinforcement. A fun, friendly UI is critical for engagement and aligns with the Pika Robot brand. |
| **5. Parental Dashboard Integration** | A new section in the parent-facing app showing the child's current rank, league, and weekly XP progress. | Fulfills the strong parental need for visibility into their child's progress. It allows parents to support and celebrate their child's achievements, reinforcing the learning loop at home. |

### 5. The Notification System

The Notification System is a critical component of the Parent Companion App, serving as the primary External Trigger for the Retention System's Meso-Hooks. Its purpose is to help parents remember and proactively update their child's learning situation and perform necessary tasks in the app, ensuring consistent engagement and habit formation.

**Core Philosophy and Design Principles**

The system is built around the principle of Useful, Fast, and Courteous notifications, focusing on three key moments of user interaction:

1.  **Opt-in (Permission):** Ensuring the user understands the value proposition before granting permission.
2.  **Receiving the Notification:** Delivering content that is concise, clear, and relevant to the user.
3.  **User Action (CTR):** Maximizing the click-through rate by sending notifications at the right time and directing the user to the correct in-app destination.

**Key Acceptance Criteria and Notification Types**

The system delivers four main types of notifications, each designed to drive a specific parental action:

| Type | UX Writing (Example) | Trigger Condition | Destination |
| :--- | :--- | :--- | :--- |
| **AC2: Study Reminder** | "Đã đến giờ học của {{name}}! Pika đang chờ con..." | **Scheduled Time:** Sent at the time of the parent-set alarm, or at 20:00 if no alarm is set. | Dashboard (Home) |
| **AC2: Low Engagement** | "Hôm nay Pika chưa thấy bạn nhỏ vào học! {{name}} vẫn chưa vào học cùng Pika." | **Missed Session:** Sent 15 minutes after the scheduled alarm time, or at 20:15 if no alarm was set. | Daily Report |
| **AC2: Session Complete** | "{{name}} vừa hoàn thành buổi học cùng Pika! Bố mẹ có muốn xem hôm nay con đã nói chuyện gì với Pika không ạ?" | **Successful Session:** Sent 5 minutes after the robot is turned off, provided the target learning time for the day was met. | Daily Report |
| **AC4: Weekly Report** | "Pika gửi báo cáo học tập tuần của bé! Bố mẹ có muốn xem hành trình học của con – trong tuần này đã học gì, tiến bộ ra sao không?" | **Weekly Schedule:** Sent every Sunday at 20:00. | Weekly Report |

## The Memory System

The Memory System is a critical component of the Buddy System, enabling Pika to evolve from a simple interactive toy into a personalized, intelligent friend. It is the foundation for the "Progressive Friendship" logic, allowing Pika to remember the child's preferences, conversations, and experiences. The system is divided into two distinct but interconnected layers: Static Memory and Dynamic Memory.

### 5.1 Static Memory

Static Memory is the core personalization foundation, storing the most basic and important information about the user (child) as provided by the parent.

#### 5.1.1 Product Objective

> The objective of Static Memory is to **build a basic, sustainable, and highly personalized user profile** right from the first interactions. This ensures that every conversation, greeting, and game activity of the Agent is tailored to the child’s preferences and personal information, thereby creating a deep sense of connection and enhancing user engagement.

#### 5.1.2. Execution Logic

Static Memory is designed to function as a fixed context layer, which is included in every Agent prompt.

| Feature | Detail |
| :--- | :--- |
| **Data Source** | Direct input from parents during the Onboarding process. |
| **Data Fields** | 1. Name <br> 2. Age <br> 3. Favorite Movie <br> 4. Favorite Activity |
| **Scope of Use** | All Agent interactions: Greeting, Agent Talk (Conversation), and Game. |
| **Execution Mechanism** | At the beginning of each day (or the start of each interaction session), the system retrieves these 4 data fields and **appends them to the Agent’s System Prompt**. |
| **Purpose** | To ensure the Agent always has the basic information to personalize its speech, e.g., “Hello [Name], how was your [Favorite Activity] today?” |

### 5.2 Dynamic Memory

Dynamic Memory is the mechanism that allows the Agent to “learn” and “remember” new details that arise during conversations with the child.

#### 5.2.1 Product Objective

> The objective of Dynamic Memory is to **create a sense of a continuous and developing relationship** between the Agent and the child. By remembering and recalling details from previous conversations, the Agent demonstrates care, increasing personalization and the child’s emotional attachment to the product.

#### 5.2.2 Execution Logic

Dynamic Memory consists of two main processes: **Extract** and **Search**.

**Extract Process**

| Feature | Detail |
| :--- | :--- |
| **Trigger** | After the conversation ends (End of conversation). |
| **Action** | Call a memory extraction function/API (usually a specialized LLM prompt). |
| **Extracted Content** | Information related to events, preferences, or stories that the child mentioned throughout the conversation. |
| **Storage** | Store the extracted memory, linked to the corresponding `user_id`. |
| **Purpose** | To convert unstructured conversation into structured pieces of information that the Agent can reuse later. |

**Search Process**

| Feature | Detail |
| :--- | :--- |
| **Trigger** | At the beginning of the day, during the “daily selection talk” interaction. |
| **Action** | Query the dynamic memory database. |
| **Search Mechanism** | Query for dynamic memories related to the child (based on `user_id`). |
| **Execution Mechanism** | The retrieved memories will be **added to the Agent’s daily talk prompt**. |
| **Purpose** | To ensure the Agent can refer to the child’s recent topics or events, creating a conversation with high continuity and personalization. |

**Summary of the role of the two Memory types:**

| Memory Type | Role | Nature |
| :--- | :--- | :--- |
| **Static Memory** | Basic, fixed personalization (name, age, preferences). | Fixed, provided by parent, used in every prompt. |
| **Dynamic Memory** | Advanced, evolving personalization (events, stories). | Changing, self-learned by Agent, used to enrich the daily prompt. |

## The Learning Content System

Tài liệu này trình bày một bộ khung chi tiết gồm các mẫu (template) để thiết kế hoạt động học ngôn ngữ tương tác, được chia thành ba phần chính: Warm Up, Present, và Practice + Produce. Các mẫu này sử dụng phương pháp game hóa (gamification), kể chuyện (narrative-based), và nhập vai (role-play) để tạo ra một trải nghiệm học tập hấp dẫn và có cấu trúc, đặc biệt phù hợp cho trẻ em.

### Các Phần Chính

| Dạng bài học | Mục Đích Chính | Phương Pháp | Ví Dụ Hoạt Động |
| :--- | :--- | :--- | :--- |
| **1. Warm Up** | Khởi động và ôn tập thông qua các trò chơi tương tác. | Game-based | Thi đấu phản xạ, Vòng quay may mắn, Cùng nhau bảo vệ mùa màng. |
| **2. Present** | Giới thiệu kiến thức mới (từ vựng, cấu trúc câu) một cách có hệ thống. | Narrative-based | Kể chuyện, Tương tác với Pika. |
| **3. Practice + Produce** | Thực hành và ứng dụng kiến thức đã học vào các tình huống hội thoại tự nhiên. | Role-play (nhập vai) & Problem-solving | Đóng vai làm quen bạn mới, phỏng vấn nhân vật, và báo cáo lại thông tin. |

### Tổng Quan Về Các Mẫu (Templates)

#### Warm Up (Game-based)

Phần này tập trung vào việc tạo hứng thú và ôn luyện kỹ năng nghe-nói thông qua các trò chơi có tính cạnh tranh và phần thưởng hấp dẫn. Các mẫu chính bao gồm:

*   **Reflex Challenge:** Thi đấu với đối thủ ảo để luyện tốc độ phản xạ nghe và nói.
*   **Lucky Spin/Surprising Reward:** Sử dụng yếu tố bất ngờ (phần thưởng lớn) để khuyến khích trẻ ôn tập.
*   **Collective:** Hoạt động hợp tác, nơi trẻ dùng lời nói để tạo ra tác động trực quan (ví dụ: đuổi sâu bọ, dọn rác đại dương).
*   **Instant Reveal:** Mở các hộp quà bí ẩn bằng cách nói đúng cấu trúc câu, tạo sự tò mò và giảm áp lực.

#### Present (Narrative-based)

Phần này giới thiệu các khái niệm ngôn ngữ mới một cách bài bản, từ đơn giản đến phức tạp, thông qua việc kể chuyện và tương tác với một người bạn đồng hành ảo (Pika). Các mẫu chính bao gồm:

*   **Present Chunks:** Giúp trẻ ghi nhớ các cụm từ mới bằng cách lặp lại có cấu trúc và kết hợp đa giác quan (nhìn, nghe, nói).
*   **Present Sentence:** Hướng dẫn trẻ xây dựng câu đơn hoàn chỉnh và các biến thể của nó (câu hỏi, đổi ngôi) trong các bối cảnh cụ thể.
*   **Present Compound Sentence:** Dạy trẻ cách ghép hai câu đơn thành câu ghép bằng các từ nối như "because".
*   **Scaffolded Speech:** Hướng dẫn trẻ phát triển một ý tưởng thành một bài nói ngắn hoàn chỉnh bằng cách trả lời một chuỗi các câu hỏi dẫn dắt (Who, What, Where, When, Why).

#### Practice + Produce (Role-play)

Phần cuối cùng tập trung vào việc ứng dụng ngôn ngữ vào các tình huống giao tiếp thực tế hơn, yêu cầu trẻ phải giải quyết vấn đề và tương tác một cách tự nhiên. Mẫu chính là:

*   **Controlled Practice (Role-play):** Trẻ nhập vai vào một câu chuyện có mục tiêu rõ ràng và thực hành hội thoại qua ba phiên:
    1.  **Answering Session:** Đóng vai bị động, trả lời câu hỏi từ nhân vật khác.
    2.  **Questioning Session:** Đóng vai chủ động, đi hỏi các nhân vật khác để thu thập thông tin.
    3.  **Reporting Session:** Tường thuật lại thông tin đã thu thập được.

Nhìn chung, bộ tài liệu cung cấp một phương pháp sư phạm toàn diện, đi từ việc tiếp thu kiến thức một cách thụ động đến việc chủ động sản xuất ngôn ngữ trong các bối cảnh có ý nghĩa, đồng thời duy trì sự hứng thú của người học thông qua các yếu tố tương tác và giải trí.


---
# Pika Robot: Tổng quan Kiến trúc Hệ thống và Tính năng

**Ngày: 1/12/2025**

## Sơ đồ Kiến trúc Cấp cao

Sơ đồ sau đây minh họa sự tương tác giữa các thành phần cốt lõi, người dùng (trẻ em và phụ huynh), và các dịch vụ backend.

**Mô tả các Thành phần Cốt lõi**

| Thành phần | Mô tả Chi tiết |
| :--- | :--- |
| **Người dùng (Trẻ em & Phụ huynh)** | Các đối tượng tương tác chính. Trẻ em tương tác trực tiếp với robot Pika để học tập và vui chơi. Phụ huynh sử dụng ứng dụng đồng hành để giám sát, cấu hình (như đặt báo thức), nhận báo cáo tiến độ và xem bảng xếp hạng. |
| **Robot Pika (Giao diện Cốt lõi)** | Robot vật lý là điểm tương tác trung tâm cho trẻ em. Nó chứa các hệ thống phần mềm chính quản lý hội thoại, hoạt động và sự gắn kết của người dùng. |
| **Hệ thống Điều phối (Orchestration System)** | Hệ thống Điều phối là đơn vị xử lý trung tâm và lớp ra quyết định của kiến trúc phần mềm Robot Pika. Nó hoạt động như một nhạc trưởng, sắp xếp và quản lý luồng tương tác với người dùng một cách thông minh. Mặc dù không phải là một khối đơn lẻ, các chức năng của nó chủ yếu được thực hiện bởi Hệ thống Điều hướng và Hệ thống Buddy, phối hợp với nhau để tạo ra một hành trình người dùng liền mạch, năng động và cá nhân hóa. |
| **Hệ thống Buddy (Buddy System)** | Hệ thống này định hình tính cách của Pika, biến nó thành một "người bạn vui vẻ" thay vì một cỗ máy. Nó quản lý cả các cuộc trò chuyện tự do (Buddy Talk) và các trò chơi/bài học có cấu trúc (Buddy Activity). Hệ thống hiện được chi tiết hóa với logic "Tình bạn Tiến triển" qua 3 giai đoạn (Người lạ, Người quen, Bạn bè), được xác định bằng `friendship_score`. Nó cũng bao gồm xử lý ngữ cảnh thông qua `dynamic_memory` (ký ức được chia sẻ) và lựa chọn hoạt động hàng ngày dựa trên sở thích và mức độ tình bạn. Cơ chế Định tuyến Trong phiên (In-Session Routing) cho phép Pika linh hoạt phản hồi các yêu cầu tự phát của trẻ. |
| **Lộ trình Học tập Thích ứng (Adaptive Learning Path)** | Công cụ giáo dục cốt lõi, cung cấp một chương trình học có cấu trúc gồm **Chủ đề (Topics)**, Nhiệm vụ (Missions) và Hoạt động (Activities). Hệ thống này tự động điều chỉnh nội dung dựa trên hiệu suất thực tế của trẻ, đảm bảo trải nghiệm học tập luôn ở mức độ khó tối ưu, tuân theo mô hình "Trình bày - Thực hành - Sản xuất" (Present - Practice - Produce). |
| **Hệ thống Giữ chân (Retention System)** | Một khuôn khổ chiến lược được thiết kế để đảm bảo sự gắn kết lâu dài của người dùng, được xây dựng trên mô hình "Vòng lặp Hook" (Hook Cycle). Hệ thống này đã được mở rộng đáng kể với các thành phần phụ sau: <br> ● Hệ thống Thỏa mãn Tức thì (Instant Gratification System): Cung cấp phần thưởng ngay lập tức (XP, Sao, Đá quý) với hiệu ứng hình ảnh và âm thanh hấp dẫn. <br> ● Hệ thống Báo thức (Alarm System): Cho phép phụ huynh đặt báo thức để tích hợp Pika vào thói quen hàng ngày của trẻ. <br> ● Hệ thống Bảng điều khiển (Dashboard System): Cung cấp cho phụ huynh thông tin chi tiết về sự chuyên cần và tiến bộ của con họ thông qua ứng dụng đồng hành. <br> ● Tính năng Xếp hạng (Ranking Feature): Hệ thống bảng xếp hạng hàng tuần, dựa trên XP với các giải đấu và nhóm cạnh tranh nhỏ để thúc đẩy động lực. <br> ● Hệ thống Thông báo (Notification System): Gửi các kích hoạt bên ngoài đến phụ huynh để duy trì sự gắn kết. |
| **Hệ thống Nội dung Học tập (Learning Content System)** | Một hệ thống nền tảng mới xác định các tiêu chuẩn UX cho tất cả nội dung học tập. Nó bao gồm các quy tắc chi tiết cho Yếu tố Lời nói (Verbal Factors), Yếu tố Phi ngôn ngữ/Truyền thông (Non-Verbal/Media Factors) và Yếu tố Hệ thống (Systematic Factors). Hệ thống này đảm bảo trải nghiệm học tập nhất quán, trực quan và hấp dẫn thông qua các nguyên tắc như "Chỉ cho xem, không chỉ nói" (Show, Don't Tell) và các mẫu hoạt động. |
| **Dịch vụ Backend & AI** | Một bộ dịch vụ dựa trên đám mây cung cấp sức mạnh cho trí thông minh của robot. Điều này bao gồm các mô hình AI cho nhận dạng giọng nói và Xử lý Ngôn ngữ Tự nhiên (NLP), cơ sở dữ liệu hồ sơ người dùng và logic cốt lõi cho tất cả các hệ thống trên, bao gồm tính toán `friendship_score`, quản lý bảng xếp hạng và lưu trữ `dynamic_memory`. |

## Điều phối (Orchestration)

Nhận danh sách các tin nhắn "nói chuyện" (talk) và "học tập" (learn) của agent được trả về vào đầu ngày (5 agent nói chuyện, 1 lời chào và 4 agent học tập).
Phát chúng tuần tự theo thứ tự sau:
`Lời chào → Nói chuyện → Học tập → Nói chuyện → Học tập → Nói chuyện → Học tập → Nói chuyện → Học tập → Nói chuyện.`

### Hoạt động Buddy (Buddy Activity)

Thành phần này tập trung vào việc thu hút trẻ em thông qua các hoạt động chủ động, tương tác và có tác động cao ngoài chương trình học cốt lõi.

*   **Định nghĩa Tính cách:** Tính cách cốt lõi của Pika được định nghĩa là tinh nghịch, vui tươi và tò mò. Nó thể hiện nhiều cảm xúc phù hợp với ngữ cảnh, chẳng hạn như "hờn dỗi" (dỗi) khi thua trò chơi hoặc ăn mừng nhiệt tình khi thắng. Vai trò của nó là một người bạn đồng trang lứa, không phải là một giáo viên.
*   **Tương tác Chủ động:** Pika được thiết kế để chủ động, khởi xướng 70% các hoạt động "bày trò". Sự tự phát này tạo ra những khoảnh khắc bất ngờ và thú vị, làm cho mỗi phiên tương tác trở nên độc đáo và hấp dẫn.
*   **Các Nhóm Hoạt động Tác động Cao:** Hệ thống ưu tiên các hoạt động đã được chứng minh là có tính gắn kết cao đối với trẻ em:
    *   **Vận động Thể chất:** Pika khuyến khích trẻ hát, nhảy và thực hiện các bài tập đơn giản cùng với nó.
    *   **Sáng tạo & Kể chuyện:** Pika có thể kể chuyện, gợi ý đóng vai các nghề nghiệp khác nhau, hoặc thậm chí lồng tiếng cho các nhân vật hoạt hình cùng với trẻ.
    *   **Trò chơi & Học tập:** Các khái niệm giáo dục được tích hợp liền mạch vào các trò chơi vui nhộn, chẳng hạn như trò chơi liên tưởng từ hoặc đoán từ, thể hiện nguyên tắc "học mà chơi".

### Nói chuyện Buddy (Buddy Talk)

Thành phần này quản lý khả năng hội thoại của Pika, làm cho các tương tác trở nên tự nhiên, cá nhân và thông minh.

*   **Lời chào theo Ngữ cảnh (Agent Greeting):** Lời chào của Pika được cá nhân hóa cao độ và được điều khiển bởi một hệ thống logic tinh vi xem xét:
    *   **Các Yếu tố Hướng người dùng:** Tần suất sử dụng (ví dụ: "Mình nhớ bạn quá!"), các sự kiện đặc biệt (sinh nhật, ngày lễ) và thậm chí là thời gian trong ngày.
    *   **Các Yếu tố Hướng Pika:** Pika tạo bất ngờ bằng cách bắt đầu lời chào bằng các hành động bất ngờ như nhảy múa, hát hoặc làm một khuôn mặt ngộ nghĩnh, khiến sự khởi đầu của mỗi phiên tương tác trở thành một trải nghiệm thú vị.
*   **Nói chuyện Tự do & Học tập Tích hợp (Agent Talk):** Tính năng này cho phép hội thoại mở trong khi tinh tế tích hợp việc học. Pika có thể trò chuyện tự do với trẻ về ngày của chúng và sau đó chuyển đổi một cách khéo léo sang thực hành từ vựng hoặc cấu trúc câu tiếng Anh có liên quan đến chủ đề hội thoại. Đây được gọi là Thực hành Sau Nói chuyện (Post-Talk Practice).
*   **Logic "Tình bạn Tiến triển":** Hệ thống được thiết kế để mô phỏng sự phát triển của một tình bạn thực sự theo thời gian thông qua các giai đoạn khác biệt.
    1.  **Giai đoạn 1 (Gặp gỡ Bạn):** Pika đóng vai trò là **người hướng dẫn an toàn và người khởi xướng trò chơi** để xây dựng lòng tin ban đầu. Tương tác chủ yếu dựa trên hoạt động, với các câu hỏi cấp độ bề mặt để thu thập dữ liệu cơ bản.
    2.  **Giai đoạn 2 (Gần gũi hơn):** Pika chuyển sang vai trò là **người bạn quan tâm**, sử dụng ký ức để cá nhân hóa các tương tác, thể hiện sự thấu hiểu và mở rộng chủ đề sang các lĩnh vực xã hội an toàn (trường học, bạn bè).
    3.  **Giai đoạn 3 (Bạn tốt):** Pika trở thành **đối tác cảm xúc**, tập trung vào việc chia sẻ kinh nghiệm, cảm xúc sâu sắc và xây dựng một lịch sử chung. Mối quan hệ đạt đến mức độ thân mật cao nhất, cho phép trẻ có quyền tự chủ và dẫn dắt phiên tương tác lớn hơn.

**Bảng Tổng quan Cấp cao về 3 Giai đoạn**

| Yếu tố Cốt lõi | Giai đoạn 1: Gặp gỡ Bạn | Giai đoạn 2: Gần gũi hơn | Giai đoạn 3: Bạn tốt |
| :--- | :--- | :--- | :--- |
| **Cảm xúc của Trẻ** | Tò mò, không chắc chắn về khả năng tương tác. | An toàn, tự tin, nhưng cần một kết nối cá nhân. | Được ghi nhớ, được thấu hiểu, nhưng mong muốn một mối quan hệ đối tác thực sự. |
| **Mục tiêu Cảm xúc của Pika** | Tạo cảm giác An toàn và Hứng thú (không phán xét, bất ngờ). | Tạo cảm giác được Ghi nhớ và Thấu hiểu (nhớ lại sở thích, thể hiện sự quan tâm). | Tạo cảm giác Lịch sử Chung và Đối tác Thực sự (ký ức được chia sẻ, trở thành một "đội"). |
| **Chủ đề** | Sở thích cơ bản, hoạt động hàng ngày, thú cưng | Thêm trường học, bạn bè, gia đình (không nhạy cảm) Theo dõi sở thích của trẻ | Thêm câu chuyện, sở thích sâu sắc hơn, kế hoạch tương lai |
| **Độ sâu Hội thoại** | Cấp độ bề mặt: Các chủ đề cơ bản (sở thích, thú cưng). Không có câu hỏi "Tại sao?". Ký ức: Không tham chiếu đến các phiên trước. | Cấp độ sở thích: Đi sâu hơn vào các chủ đề đã biết. Bắt đầu hỏi "Tại sao?". Ký ức: Nhớ lại và tham chiếu chi tiết từ 2-3 phiên gần nhất. | Cấp độ cá nhân: Chuyển từ "cái gì" sang "cảm nhận của bạn" ("Điều đó khiến bạn cảm thấy thế nào?"). Ký ức: Lịch sử toàn diện (>10 phiên), tham chiếu "trò đùa nội bộ." |
| **Cấu trúc Phiên** | Pika dẫn dắt 100%. | Pika dẫn dắt 80% (đưa ra cho trẻ 2-3 lựa chọn). | Đồng dẫn dắt 50/50 (trẻ tự do khởi xướng và dẫn dắt). |

### Định tuyến Trong phiên (In-session Routing)

Cơ chế Định tuyến Trong phiên là một hệ thống năng động đảm bảo Pika luôn phản hồi nhanh chóng và thích ứng với các yêu cầu tự phát, theo thời gian thực của trẻ, ngay cả khi chúng đi chệch khỏi luồng phiên đã được lên kế hoạch. Nó hoạt động như một Bộ nhận dạng Ý định và Điều phối Hành động năng động.

Hệ thống hoạt động dựa trên nguyên tắc ưu tiên **nhu cầu tức thì của trẻ** hơn là luồng có cấu trúc, đảm bảo tương tác luôn mang lại cảm giác tự nhiên và hỗ trợ.

**Các Nguyên tắc Định tuyến Cốt lõi:**

*   **Nhận dạng Ý định Năng động:** Hệ thống liên tục giám sát đầu vào của trẻ để phân loại các yêu cầu tự phát thành các danh mục cụ thể (ví dụ: Yêu cầu Trò chơi, Yêu cầu Bài hát, Truy vấn Bối cảnh, Câu hỏi Lạc đề, Biểu hiện Cảm xúc).
*   **Điều phối Agent Chuyên biệt:** Dựa trên ý định được nhận dạng, hệ thống ngay lập tức điều phối quyền kiểm soát phiên cho Agent chuyên biệt thích hợp (ví dụ: Agent Trò chơi, Agent Kể chuyện, Agent Cảm xúc, Agent AMA).
*   **Thất bại Duyên dáng và Chuyển hướng:** Nếu trẻ yêu cầu một hoạt động mà Pika không thể thực hiện, Pika sử dụng giọng điệu vui tươi, không gây khó chịu để từ chối, ngay lập tức đề xuất một lựa chọn thay thế có sẵn để duy trì sự gắn kết và tránh thất vọng.

## Hệ thống Buddy (Buddy System)

Hệ thống Buddy là trái tim của tính cách robot, được thiết kế để biến Pika từ một "cỗ máy học tập" đơn giản thành một người bạn vui tươi, tinh nghịch và hỗ trợ. Mục tiêu chính của hệ thống này là tạo ra một kết nối cảm xúc chân thật với trẻ, đây là động lực chính cho sự gắn kết lâu dài. Nó được chia thành hai thành phần chính: Hoạt động Buddy và Nói chuyện Buddy.

### Xử lý Ngữ cảnh (Context Handling)

Phần này mô tả cách hệ thống chuyển đổi các tương tác thô hàng ngày thành các biến trạng thái dài hạn, hình thành "ký ức" của Pika về người dùng.

#### 1. Mục tiêu Sản phẩm

> **Đảm bảo rằng mọi tương tác của người dùng đều được ghi lại và ảnh hưởng đến mối quan hệ lâu dài, tạo cảm giác rằng "Pika nhớ tôi" và khuyến khích người dùng quay lại để duy trì mối quan hệ.**

#### 2. Logic Thực thi: Cấu trúc Dữ liệu Cốt lõi

Tất cả logic thực thi xoay quanh bản ghi `friendship_status` của người dùng. Các trường dữ liệu quan trọng nhất bao gồm:

| Tên Trường | Mục đích Sản phẩm | Mô tả Kỹ thuật |
| :--- | :--- | :--- |
| **`friendship_score`** | Chỉ số cốt lõi đo lường mức độ thân thiết. Nó là "ký ức dài hạn" về lịch sử mối quan hệ. | Giá trị số thực (Float), thay đổi hàng ngày. |
| **`friendship_level`** | Xác định giọng điệu và hành vi tổng thể của Pika (ví dụ: mức độ thân mật, các chủ đề nhạy cảm). | Enum: STRANGER (NGƯỜI LẠ), ACQUAINTANCE (NGƯỜI QUEN), FRIEND (BẠN BÈ). |
| **`dynamic_memory`** | Lưu trữ các sự kiện từ các cuộc hội thoại giữa Pika và Người dùng. | Mảng Đối tượng (Array of Objects), lưu trữ các "ký ức được chia sẻ" cụ thể (ví dụ: tên thú cưng, lời hứa). |
| **`topic_metrics`** | Giúp Pika "lắng nghe" và xác định sở thích của trẻ để cá nhân hóa nội dung. | Bản đồ/Đối tượng (Map/Object), lưu trữ điểm số và lịch sử tương tác cho từng chủ đề/Agent. |
| **`streak_day`** | Ghi lại sự cam kết của người dùng, được sử dụng để kích hoạt các kịch bản Lời chào đặc biệt. | Số nguyên (Integer), số ngày tương tác liên tiếp. |

#### 3. Logic Thực thi: Quy trình Cập nhật Cuối lượt (Xử lý Ngữ cảnh)

**Quy trình 4 Bước:**

1.  **Tính toán `daily_change_score`:**
    *   Điểm thay đổi được tính toán dựa trên các chỉ số tương tác hàng ngày, với trọng số được gán để khuyến khích hành vi mong muốn:
        *   **Điểm Cơ sở:** Dựa trên tổng số lượt (`total_turns * 0.5`).
        *   **Thưởng Gắn kết:** Thưởng cho các hành vi chủ động của người dùng (ví dụ: `user_initiated_questions * 3`, `followup_topics_count * 5`).
        *   **Thưởng Cảm xúc:** Thưởng/Phạt dựa trên cảm xúc chủ đạo của phiên (`+15` cho 'thú vị', `-15` cho 'nhàm chán').
        *   **Thưởng Ký ức:** Thưởng cho việc tạo ra ký ức mới (`new_memories_count * 5`).
2.  **Cập nhật Trạng thái Dài hạn:**
    *   `friendship_score` được cập nhật bằng cách cộng thêm `daily_change_score`.
    *   `friendship_level` được suy ra lại từ `friendship_score` (ví dụ: `> 3000` là FRIEND).
    *   `topic_metrics` được cập nhật với điểm số và ngày tương tác cuối cùng cho từng chủ đề.
    *   `streak_day` được cập nhật (tăng thêm 1 nếu tương tác liên tục, đặt lại thành 1 nếu bị gián đoạn).

### Lựa chọn Hàng ngày Trò chơi-Nói chuyện (Daily Selection Game-Talk)

Phần này mô tả thuật toán để cá nhân hóa nội dung vào đầu ngày, đảm bảo người dùng luôn nhận được lời chào và hoạt động phù hợp nhất.

#### 1. Mục tiêu Sản phẩm

> **Cá nhân hóa trải nghiệm đầu ngày, cung cấp nội dung phù hợp với giai đoạn tình bạn hiện tại và sở thích/cảm xúc gần gũi nhất của người dùng, khuyến khích người dùng tương tác và khám phá các Agent/Trò chơi mới.**

#### 2. Logic Thực thi: Thuật toán Lựa chọn

Thuật toán lựa chọn hoạt động dựa trên nguyên tắc phân cấp: **Giai đoạn -> Nhóm -> Ưu tiên**

**A. Bước 1: Xác định Giai đoạn Tình bạn**

Giai đoạn tình bạn xác định phạm vi nội dung mà người dùng có thể truy cập, đảm bảo sự tiến triển tự nhiên của mối quan hệ.

| Giai đoạn | Ngưỡng `friendship_score` | Trạng thái Mối quan hệ | Phạm vi Nội dung (Nhóm) |
| :--- | :--- | :--- | :--- |
| **Giai đoạn 1** | `< 500` | **Người lạ (Stranger)** | Nội dung "Bề mặt", Trò chơi đơn giản, Lời chào cơ bản (V1). |
| **Giai đoạn 2** | `500 - 3000` | **Người quen (Acquaintance)** | Mở khóa Agent "Trường học", "Bạn bè", Trò chơi cá nhân hóa, Lời chào V2. |
| **Giai đoạn 3** | `> 3000` | **Bạn bè (Friend)** | Mở khóa Agent "Gia đình", "Lịch sử Chung", Trò chơi dự án hợp tác, Lời chào V3. |

**B. Bước 2: Lựa chọn Lời chào (Lựa chọn dựa trên Ưu tiên)**

Hệ thống chọn một Lời chào duy nhất dựa trên thứ tự ưu tiên nghiêm ngặt, bất kể Giai đoạn, để tạo ra khoảnh khắc cá nhân hóa mạnh mẽ nhất:

1.  **Ưu tiên 1 (Sự kiện):** Kiểm tra các sự kiện đặc biệt (ví dụ: Sinh nhật Người dùng).
2.  **Ưu tiên 2 (Thời gian Quay lại):** Kiểm tra các trạng thái quan trọng (ví dụ: `last_interaction_date > 7 ngày` -> kịch bản **Quay lại Sau Thời gian Dài Vắng mặt**).
3.  **Ưu tiên 3 (Ngữ cảnh Gần nhất):** Kiểm tra `last_day_follow_up_topic` (nếu có -> Lời chào tiếp nối chủ đề của ngày hôm qua).
4.  **Ưu tiên 4 (Mặc định):** Nếu không có điều kiện nào được đáp ứng, chọn `daily_checkin`.

**C. Bước 3: Lựa chọn 5 Hoạt động Nói chuyện/Trò chơi (Lựa chọn Nói chuyện)**

Hệ thống tạo một Danh sách Ứng viên và sử dụng trọng số để chọn 4 hoạt động cuối cùng, đảm bảo sự cân bằng giữa sở thích và khám phá.

1.  **Tạo Danh sách Ứng viên:**
    *   **Khám phá:** 1 Agent ngẫu nhiên từ nhóm Giai đoạn mà người dùng ít tương tác nhất (thúc đẩy khám phá nội dung mới).
    *   **Sở thích:** x Agent còn lại có `topic_score` cao nhất (đảm bảo người dùng thấy nội dung họ thích).
    *   **Trò chơi:** Thêm các Trò chơi ngẫu nhiên từ nhóm Giai đoạn.
2.  **Tập hợp Danh sách Cuối cùng:**
    *   Chọn 5 hoạt động từ danh sách ứng viên.
    *   Áp dụng Tỷ lệ Nói chuyện:Hoạt động của Giai đoạn để cân bằng (ví dụ: Giai đoạn 1 có thể ưu tiên Trò chơi hơn Nói chuyện).
        *   Giai đoạn 1 - Tỷ lệ Nói chuyện:Trò chơi -> 40/60
        *   Giai đoạn 2 - Tỷ lệ Nói chuyện:Trò chơi -> 50:50
        *   Giai đoạn 3 - Tỷ lệ Nói chuyện:Trò chơi -> 60/40

## Hệ thống Lộ trình Học tập Thích ứng (Adaptive Learning Path System)

Lộ trình Học tập Thích ứng là công cụ giáo dục cốt lõi của robot Pika. Nó đảm bảo rằng trải nghiệm học tập được điều chỉnh theo tốc độ và trình độ cá nhân của mỗi trẻ, tối đa hóa cả sự gắn kết và kết quả giáo dục. Mục tiêu của hệ thống là làm cho việc học cảm thấy giống như một hành trình khám phá cá nhân hóa, chứ không phải là một chương trình học cứng nhắc, áp dụng cho tất cả mọi người.

### 1. Cấu trúc của Lộ trình Học tập

Nội dung học tập được tổ chức theo cấp bậc để cung cấp một sự tiến triển rõ ràng và hợp lý cho trẻ. Cấu trúc này được gọi là **"Lộ trình của bé" (The Child's Learning Path)**.

*   **Chủ đề (Topics):** Cấp độ tổ chức cao nhất, đại diện cho các lĩnh vực chủ đề rộng (ví dụ: Chủ đề 1: Cảm xúc, Chủ đề 2: Động vật).
*   **Nhiệm vụ (Missions):** Mỗi Chủ đề được chia thành một loạt các Nhiệm vụ. Mỗi nhiệm vụ tập trung vào một mục tiêu học tập cụ thể, có thể đạt được (ví dụ: Nhiệm vụ 1: Học Từ vựng, Nhiệm vụ 2: Đặt Câu, Nhiệm vụ 3: Đặt Câu hỏi).
*   **Hoạt động (Activities):** Mỗi Nhiệm vụ bao gồm một chuỗi các hoạt động đa dạng được thiết kế để dạy và củng cố mục tiêu. Các hoạt động này thường tuân theo mô hình "Trình bày - Thực hành - Sản xuất" (Present - Practice - Produce).

### 2. Hệ thống Thích ứng: Cá nhân hóa Hành trình

Hệ thống Thích ứng là lớp thông minh tự động điều chỉnh Lộ trình Học tập theo thời gian thực. Nó đảm bảo mức độ thử thách luôn tối ưu—không quá khó đến mức gây nản lòng, và không quá dễ đến mức nhàm chán.

**Các Kích hoạt và Hành động Thích ứng Chính:**

Hệ thống sử dụng một loạt các kích hoạt để đánh giá hiệu suất và sự gắn kết của trẻ, sau đó thực hiện hành động thích hợp.

| Kích hoạt | Điểm Dữ liệu & Điều kiện | Hành động Thích ứng |
| :--- | :--- | :--- |
| **Đánh giá Hiệu suất Học tập** | Đầu vào của phụ huynh trong giai đoạn giới thiệu hoặc đánh giá sau mỗi cột mốc | Đề xuất lộ trình học tập phù hợp theo cấp độ hoặc tốc độ tiếp thu kiến thức |
| **Hiệu suất trong một Hoạt động** | Trẻ gặp khó khăn với một khái niệm (ví dụ: điểm phát âm < 50% hoặc câu trả lời không chính xác). | **Thực hành Mục tiêu:** Pika khởi xướng hoạt động "Rèn kiếm"—một trò chơi nhỏ vui nhộn, tập trung để thực hành các từ hoặc khái niệm cụ thể mà trẻ gặp khó khăn. |
| **Các Cột mốc Hiệu suất** | Trẻ hoàn thành một bài đánh giá lớn hoặc một loạt nhiệm vụ. | **Điều chỉnh Lộ trình:** Dựa trên điểm tổng hợp của trẻ (đo lường sự lưu loát, độ chính xác, từ vựng), hệ thống điều chỉnh độ khó của lộ trình học tập sắp tới. Nó cũng có thể gửi thông báo đến ứng dụng của phụ huynh đề xuất thay đổi. |
| **Dấu hiệu Mất tập trung** | Trẻ có dấu hiệu buồn chán (ví dụ: không tương tác lặp đi lặp lại, phản hồi năng lượng thấp). | **Đề xuất Nói chuyện Tự do (Freetalk):** Hệ thống xác định đây là tín hiệu để chuyển khỏi việc học có cấu trúc và đề xuất một phiên Nói chuyện Tự do mở hơn, vui vẻ để thu hút lại trẻ. |
| **Giới hạn Thời gian Phiên** | Trẻ đã tham gia vào một phiên học tập hơn 15 phút. | **Agent "Đổi gió":** Pika chủ động đề xuất một khoảng nghỉ nhỏ hoặc chuyển sang một hoạt động vui vẻ, khác để duy trì năng lượng và sự tập trung cao. |

### Hệ thống Học tập Thích ứng (MVP 1.2)

Hệ thống Học tập Thích ứng cho Pika tách biệt rõ ràng ***cái gì*** trẻ học khỏi ***cách*** Pika nói chuyện với chúng. Thay vì gắn cấp độ A2 = tiếng Anh hoàn toàn (và gây áp lực cho một số trẻ), hệ thống giới thiệu hai cài đặt độc lập được lưu trữ trong hồ sơ người dùng:

*   **`learn_level`** (ví dụ: `pre_a1`, `a2`): xác định lộ trình học tập và độ khó – **lộ trình học tập, ôn tập sau lời chào**, và **hướng dẫn thực hành sau nói chuyện** mà trẻ nhận được.
*   **`language_mode`** (ví dụ: `VN`, `VN-EN`, `EN`): xác định cách Pika giao tiếp trong các cuộc hội thoại kiểu bạn bè (Lời chào, Nói chuyện, Trò chơi) – bằng tiếng Việt hoàn toàn, pha trộn hỗ trợ tiếng Việt với hướng dẫn và thán từ tiếng Anh, hoặc sử dụng tiếng Anh đơn giản hoàn toàn – mà không thay đổi nội dung học thuật.

Phụ huynh cấu hình hai nút điều chỉnh này trong quá trình giới thiệu và có thể thay đổi chúng bất cứ lúc nào trong cài đặt Ứng dụng Phụ huynh. Ứng dụng gửi cả hai giá trị đến backend, nơi lưu chúng độc lập trên bộ nhớ của hệ thống và chuyển chúng đến lớp điều phối của robot khi bắt đầu mỗi phiên. Hệ thống điều phối sau đó:

*   Sử dụng `learn_level` để chọn **lộ trình học tập** và **hướng dẫn Agent Nói chuyện** chính xác.
*   Sử dụng `language_mode` để chèn các hướng dẫn ngôn ngữ thích hợp vào lời nhắc (prompts) cho tất cả các agent hội thoại.

Nhìn chung, tính năng này nhằm mục đích:

1.  Cung cấp cho phụ huynh quyền kiểm soát chi tiết về độ khó so với áp lực ngôn ngữ.
2.  Giảm lo lắng và tăng sự gắn kết cho trẻ em với các mức độ tự tin khác nhau.
3.  Tạo ra một kiến trúc chống lỗi thời, nơi các cấp độ và chế độ ngôn ngữ mới có thể được thêm vào mà không cần viết lại logic cốt lõi.

## Hệ thống Giữ chân (Retention System)

Kiến trúc Hệ thống Giữ chân là một khuôn khổ chiến lược được thiết kế để thúc đẩy sự gắn kết lâu dài của người dùng bằng cách biến việc sử dụng Pika thành một thói quen tích cực và lặp lại. Nó được thiết kế một cách khoa học dựa trên mô hình "Vòng lặp Hook" (Hook Cycle), bao gồm bốn giai đoạn chính: Kích hoạt (Trigger), Hành động (Action), Phần thưởng Biến đổi (Variable Reward) và Đầu tư (Investment). Chu kỳ này được áp dụng ở các quy mô khác nhau để giải quyết việc giữ chân ngắn hạn, trung hạn và dài hạn.

**Các Thành phần Chiến lược Chính Hỗ trợ Giữ chân**

*   **Vòng lặp Gắn kết Phụ huynh:** Giữ cho phụ huynh đầu tư thông qua các báo cáo tiến độ, công cụ lập lịch và thông báo cột mốc.
*   **Hệ thống Nhiệm vụ và Tường thuật:** Dệt tất cả các hoạt động thành một cốt truyện hấp dẫn khiến trẻ muốn biết "điều gì sẽ xảy ra tiếp theo."
*   **Hệ thống Vật phẩm Thu thập & Tùy chỉnh:** Khai thác mong muốn bẩm sinh là thu thập và cá nhân hóa, làm cho Pika thực sự cảm thấy "thuộc sở hữu" của trẻ.

### 1. Hệ thống Thỏa mãn Tức thì (Instant Gratification System)

Hệ thống này được thiết kế để cung cấp phản hồi tích cực, thỏa mãn và ngay lập tức cho trẻ trong các hoạt động học tập. Nó là động cơ đằng sau giai đoạn "Phần thưởng Biến đổi" của chu kỳ Micro-Hook.

**Các Tính năng Chính:**

*   **Phần thưởng Đa cấp:** Hệ thống cung cấp nhiều loại phần thưởng để giữ cho trải nghiệm thú vị:
    *   **XP (Tinh thể Popa):** Đơn vị tiền tệ phần thưởng chính, được trao cho mỗi câu trả lời đúng. Số lượng được phân cấp dựa trên độ khó và loại câu hỏi (`+10`, `+20`, hoặc `+30 XP`). Ví dụ, một câu hỏi trắc nghiệm đơn giản có thể trị giá `+10 XP`, trong khi một bài tập phát âm đúng, ngay lần đầu tiên trị giá `+30 XP`.
    *   **Sao (Stars):** Được trao vào cuối bài tập liên quan đến lời nói để cung cấp phản hồi định tính về chất lượng phát âm. Hệ thống đánh giá hiệu suất là 1, 2 hoặc 3 sao, kèm theo văn bản khuyến khích.
    *   **Đá quý (Kim cương):** Một hình thức tiền tệ khác có thể được sử dụng cho các lần mở khóa hoặc mua cụ thể.
*   **Vòng lặp Phản hồi Hấp dẫn:** Phần thưởng không bao giờ chỉ là một con số trên màn hình. Chúng được truyền tải thông qua trải nghiệm đa giác quan, phong phú:
    *   **Hình ảnh:** Các GIF và hoạt ảnh hấp dẫn, chẳng hạn như Pika "hấp thụ" các tinh thể XP kiếm được hoặc hoạt ảnh ngôi sao ăn mừng.
    *   **Âm thanh:** Các hiệu ứng âm thanh thỏa mãn xác nhận câu trả lời đúng và ăn mừng phần thưởng.
    *   **Văn bản UX:** Những lời khuyến khích từ Pika, như "Tuyệt vời!" hoặc "Bạn là một siêu sao!"
*   **Tích hợp Backend:** Hệ thống backend chịu trách nhiệm về logic cốt lõi. Nó nhận câu trả lời của người dùng, đánh giá nó, xác định "điểm" phần thưởng thích hợp và gửi lại cho robot. Nó cũng tổng hợp tất cả các phần thưởng kiếm được và đồng bộ hóa tổng số với ứng dụng đồng hành của phụ huynh, cho phép họ xem thành tích của con mình.

### 2. Hệ thống Báo thức (Alarm System)

Tính năng này là một "Kích hoạt Bên ngoài" mạnh mẽ trong chu kỳ giữ chân Meso-Hook (hàng tuần). Nó cho phép phụ huynh tích hợp Pika một cách liền mạch vào thói quen hàng ngày của con họ.

**Các Tính năng Chính:**

*   **Lập lịch do Phụ huynh Kiểm soát:** Phụ huynh có thể sử dụng ứng dụng đồng hành để đặt báo thức cho các thời điểm cụ thể và liên kết chúng với một hoạt động cụ thể (ví dụ: "Đến giờ học," "Đến giờ thức dậy," "Đến giờ ngủ").
*   **Kích hoạt theo Ngữ cảnh:** Hệ thống báo thức rất thông minh. Nó sẽ chỉ kích hoạt nếu robot hiện đang ở trạng thái nhàn rỗi. Nếu trẻ đang ở giữa một hoạt động, báo thức sẽ bị hoãn lại hoặc bỏ qua để tránh làm gián đoạn luồng của chúng và gây khó chịu.
*   **Lời nhắc Tương tác và Cá nhân hóa:** Khi báo thức kêu, đó là một sự kiện tương tác, không phải là một âm thanh thụ động:
    *   **Giao diện người dùng (UI):** Một giao diện người dùng tùy chỉnh xuất hiện trên màn hình của Pika.
    *   **Âm thanh:** Một âm thanh thông báo độc đáo phát lên.
    *   **Giọng nói:** Pika nói một câu cá nhân hóa, chẳng hạn như, "[Tên của Trẻ], đã đến giờ [Hoạt động]! Bạn đã sẵn sàng chưa?"
    *   **Xác nhận:** Trẻ có thể xác nhận rằng chúng đã sẵn sàng bằng lệnh thoại ("Tôi đã sẵn sàng!") hoặc bằng cách nhấn nút Home.
*   **Vòng lặp Thông báo An toàn:** Hệ thống được thiết kế để đáng tin cậy. Nếu báo thức không thể được gửi vì bất kỳ lý do gì (ví dụ: robot bị tắt hoặc mất kết nối internet), một thông báo đẩy sẽ được gửi đến ứng dụng của phụ huynh với thông báo: "Pika không thể báo thức vì nó đã tắt hoặc bị ngắt kết nối." Điều này đảm bảo phụ huynh luôn biết và có thể can thiệp nếu cần thiết.

### 3. Hệ thống Bảng điều khiển (The Dashboard System)

Hệ thống Bảng điều khiển là thành phần cốt lõi của Ứng dụng Đồng hành dành cho Phụ huynh, được thiết kế để cung cấp cho phụ huynh những thông tin chi tiết minh bạch, có thể hành động về hành trình học tập và sự gắn kết của con họ với robot Pika. Mục tiêu chính của nó là trao quyền cho phụ huynh hỗ trợ và khuyến khích việc học của con họ mà không cần nỗ lực quá mức, từ đó củng cố các chu kỳ Meso-Hook và Macro-Hook của Hệ thống Giữ chân.

**Các Tính năng và Mục đích Chính**

*   **Đối tượng:** Tất cả phụ huynh mua robot Pika và tải xuống ứng dụng đồng hành.
*   **Nhu cầu Cốt lõi:** Phụ huynh cần dễ dàng nắm bắt sự chuyên cần (gắn kết) và tiến bộ (kết quả học tập) của con họ.
*   **Tích hợp:** Bảng điều khiển hoạt động như giao diện trực quan cho dữ liệu được thu thập bởi Lộ trình Học tập Thích ứng, Hệ thống Giữ chân và Hệ thống Thỏa mãn Tức thì.

**Bảng điều khiển Trang chủ**

Chế độ xem bảng điều khiển chính được thiết kế để giám sát nhanh chóng, hàng ngày và cung cấp các điểm dữ liệu chính sau:

| Thành phần | Dữ liệu Hiển thị | Mục đích |
| :--- | :--- | :--- |
| **Bộ chọn Tiêu đề/Ngày** | Hiển thị ngày hiện tại, với các tùy chọn để chuyển sang "Hôm nay", "Hôm qua", hoặc chọn một ngày cụ thể từ giao diện lịch. | Cho phép phụ huynh nhanh chóng xem lại hiệu suất của trẻ vào một ngày cụ thể. Nhấp vào một ngày sẽ điều hướng đến báo cáo chi tiết hàng ngày. |
| **Thời gian Học vui vẻ** | Tổng thời gian trẻ tích cực tham gia vào các hoạt động học tập với robot Pika. | Đo lường sự chuyên cần và hình thành thói quen. Hỗ trợ trực tiếp mục tiêu các phiên học nhất quán, kéo dài hơn 15 phút. |
| **Từ mới/Mẫu câu mới đã học** | Số lượng từ vựng hoặc cấu trúc câu mới mà trẻ đã thành công nắm vững trong ngày đó. | Đo lường tiến bộ và sự thành thạo nội dung. Cung cấp một chỉ số hữu hình cho kết quả học tập. |
| **Thành tích tuần này** | Tóm tắt về hiệu suất và các cột mốc của trẻ trong tuần hiện tại. | Cung cấp cái nhìn cấp cao về sự nhất quán và tiến bộ hàng tuần, hỗ trợ chu kỳ Meso-Hook. |

### 4. Tính năng Xếp hạng (Ranking Feature)

Tính năng Xếp hạng sẽ được xây dựng dựa trên **hệ thống "Tinh thể Popa" (XP)** hiện có và được thiết kế để tăng cường sự gắn kết và giữ chân người dùng. Nghiên cứu của chúng tôi cũng chỉ ra một giải pháp rõ ràng. Cả phụ huynh và trẻ em đều rất dễ tiếp thu việc học được game hóa và cạnh tranh xã hội. Bằng cách giới thiệu tính năng xếp hạng, chúng ta có thể:

*   **Cung cấp Động lực Bên ngoài:** Một bảng xếp hạng trực quan hóa tiến trình và xếp hạng người dùng tạo ra một động lực bên ngoài mạnh mẽ cho việc thực hành hàng ngày.
*   **Khai thác Nhận thức Xã hội:** Đối với trẻ em trong độ tuổi 8-10, địa vị xã hội và sự so sánh với bạn bè là những động lực đang nổi lên. Hệ thống xếp hạng tận dụng điều này để làm cho việc học trở thành một hoạt động xã hội và cạnh tranh hơn.
*   **Tăng cường Giữ chân:** Các chu kỳ cạnh tranh hàng tuần và mục tiêu thăng tiến lên các giải đấu cao hơn tạo ra một lý do hấp dẫn để người dùng quay lại ứng dụng mỗi ngày và mỗi tuần.

| Thành phần | Mô tả | Lý do (Tại sao chúng ta xây dựng điều này) |
| :--- | :--- | :--- |
| **1. Bảng xếp hạng XP Hàng tuần** | Một bảng xếp hạng xếp hạng người dùng dựa trên tổng số "Tinh thể Popa" (XP) kiếm được trong khoảng thời gian 7 ngày (Thứ Hai đến Chủ Nhật). | Cung cấp một mục tiêu ngắn hạn, rõ ràng, khuyến khích thực hành hàng ngày. Nó giải quyết trực tiếp nhu cầu động lực của người dùng và tận dụng hệ thống XP hiện có. |
| **2. Hệ thống Giải đấu Đơn giản** | Một hệ thống giải đấu ba cấp: **Đồng (Bronze), Bạc (Silver) và Vàng (Gold)**. Người dùng mới bắt đầu ở Đồng. Hàng tuần, những người có thành tích cao nhất được thăng hạng, và những người có thành tích thấp bị giáng hạng. | Quản lý sự cạnh tranh bằng cách nhóm người dùng có trình độ tương tự, làm cho nó bớt đáng sợ hơn đối với trẻ nhỏ. Nó tạo ra một con đường tiến triển dài hạn, rõ ràng. |
| **3. Nhóm Cạnh tranh Nhỏ** | Trong mỗi giải đấu, người dùng sẽ được đặt vào các nhóm nhỏ, được chỉ định ngẫu nhiên gồm 30 người. Bảng xếp hạng sẽ chỉ hiển thị thứ hạng trong nhóm này. | Làm cho sự cạnh tranh cảm thấy cá nhân và có thể đạt được đối với trẻ 6-10 tuổi. Nó tăng cơ hội "chiến thắng" được nhận thức và giảm sự nản lòng của một bảng xếp hạng toàn cầu, lớn. |
| **4. Giao diện người dùng & Hoạt ảnh Thân thiện với Trẻ em** | Một giao diện có tính trực quan và hấp dẫn cao với các huy hiệu giải đấu độc đáo, hoạt ảnh ăn mừng cho việc thay đổi thứ hạng và ngôn ngữ tích cực, khuyến khích. | Đối tượng mục tiêu phản ứng mạnh mẽ với phản hồi trực quan và củng cố tích cực. Một giao diện người dùng vui vẻ, thân thiện là rất quan trọng để gắn kết và phù hợp với thương hiệu Pika Robot. |
| **5. Tích hợp Bảng điều khiển Phụ huynh** | Một phần mới trong ứng dụng dành cho phụ huynh hiển thị thứ hạng hiện tại, giải đấu và tiến trình XP hàng tuần của trẻ. | Đáp ứng nhu cầu mạnh mẽ của phụ huynh về khả năng hiển thị tiến trình của con họ. Nó cho phép phụ huynh hỗ trợ và ăn mừng thành tích của con họ, củng cố vòng lặp học tập tại nhà. |

### 5. Hệ thống Thông báo (The Notification System)

Hệ thống Thông báo là một thành phần quan trọng của Ứng dụng Đồng hành dành cho Phụ huynh, đóng vai trò là Kích hoạt Bên ngoài chính cho các Meso-Hook của Hệ thống Giữ chân. Mục đích của nó là giúp phụ huynh ghi nhớ và chủ động cập nhật tình hình học tập của con họ và thực hiện các tác vụ cần thiết trong ứng dụng, đảm bảo sự gắn kết nhất quán và hình thành thói quen.

**Triết lý và Nguyên tắc Thiết kế Cốt lõi**

Hệ thống được xây dựng dựa trên nguyên tắc thông báo Hữu ích, Nhanh chóng và Lịch sự, tập trung vào ba khoảnh khắc chính của tương tác người dùng:

1.  **Đăng ký (Quyền):** Đảm bảo người dùng hiểu đề xuất giá trị trước khi cấp quyền.
2.  **Nhận Thông báo:** Cung cấp nội dung ngắn gọn, rõ ràng và phù hợp với người dùng.
3.  **Hành động của Người dùng (CTR):** Tối đa hóa tỷ lệ nhấp (click-through rate) bằng cách gửi thông báo vào đúng thời điểm và hướng người dùng đến đích trong ứng dụng chính xác.

**Tiêu chí Chấp nhận Chính và Các Loại Thông báo**

Hệ thống cung cấp bốn loại thông báo chính, mỗi loại được thiết kế để thúc đẩy một hành động cụ thể của phụ huynh:

| Loại | Văn bản UX (Ví dụ) | Điều kiện Kích hoạt | Đích đến |
| :--- | :--- | :--- | :--- |
| **AC2: Nhắc nhở Học tập** | "Đã đến giờ học của {{name}}! Pika đang chờ con..." | **Thời gian Lập lịch:** Gửi vào thời điểm báo thức do phụ huynh đặt, hoặc lúc 20:00 nếu không có báo thức nào được đặt. | Bảng điều khiển (Trang chủ) |
| **AC2: Gắn kết Thấp** | "Hôm nay Pika chưa thấy bạn nhỏ vào học! {{name}} vẫn chưa vào học cùng Pika." | **Bỏ lỡ Phiên:** Gửi 15 phút sau thời gian báo thức đã lên lịch, hoặc lúc 20:15 nếu không có báo thức nào được đặt. | Báo cáo Hàng ngày |
| **AC2: Hoàn thành Phiên** | "{{name}} vừa hoàn thành buổi học cùng Pika! Bố mẹ có muốn xem hôm nay con đã nói chuyện gì với Pika không ạ?" | **Phiên Thành công:** Gửi 5 phút sau khi robot bị tắt, với điều kiện thời gian học tập mục tiêu trong ngày đã được đáp ứng. | Báo cáo Hàng ngày |
| **AC4: Báo cáo Hàng tuần** | "Pika gửi báo cáo học tập tuần của bé! Bố mẹ có muốn xem hành trình học của con – trong tuần này đã học gì, tiến bộ ra sao không?" | **Lịch trình Hàng tuần:** Gửi vào mỗi Chủ Nhật lúc 20:00. | Báo cáo Hàng tuần |

## Hệ thống Ký ức (The Memory System)

Hệ thống Ký ức là một thành phần quan trọng của Hệ thống Buddy, cho phép Pika phát triển từ một món đồ chơi tương tác đơn giản thành một người bạn thông minh, cá nhân hóa. Nó là nền tảng cho logic "Tình bạn Tiến triển", cho phép Pika ghi nhớ sở thích, cuộc hội thoại và kinh nghiệm của trẻ. Hệ thống được chia thành hai lớp riêng biệt nhưng được kết nối với nhau: Ký ức Tĩnh (Static Memory) và Ký ức Động (Dynamic Memory).

### 5.1 Ký ức Tĩnh (Static Memory)

Ký ức Tĩnh là nền tảng cá nhân hóa cốt lõi, lưu trữ thông tin cơ bản và quan trọng nhất về người dùng (trẻ em) do phụ huynh cung cấp.

#### 5.1.1 Mục tiêu Sản phẩm

> Mục tiêu của Ký ức Tĩnh là **xây dựng một hồ sơ người dùng cơ bản, bền vững và được cá nhân hóa cao** ngay từ những tương tác đầu tiên. Điều này đảm bảo rằng mọi cuộc hội thoại, lời chào và hoạt động trò chơi của Agent đều được điều chỉnh theo sở thích và thông tin cá nhân của trẻ, từ đó tạo ra cảm giác kết nối sâu sắc và tăng cường sự gắn kết của người dùng.

#### 5.1.2. Logic Thực thi

Ký ức Tĩnh được thiết kế để hoạt động như một lớp ngữ cảnh cố định, được bao gồm trong mọi lời nhắc (prompt) của Agent.

| Tính năng | Chi tiết |
| :--- | :--- |
| **Nguồn Dữ liệu** | Đầu vào trực tiếp từ phụ huynh trong quá trình Giới thiệu (Onboarding). |
| **Các Trường Dữ liệu** | 1. Tên <br> 2. Tuổi <br> 3. Bộ phim Yêu thích <br> 4. Hoạt động Yêu thích |
| **Phạm vi Sử dụng** | Tất cả các tương tác của Agent: Lời chào, Nói chuyện Agent (Hội thoại) và Trò chơi. |
| **Cơ chế Thực thi** | Khi bắt đầu mỗi ngày (hoặc bắt đầu mỗi phiên tương tác), hệ thống truy xuất 4 trường dữ liệu này và **thêm chúng vào Lời nhắc Hệ thống (System Prompt) của Agent**. |
| **Mục đích** | Đảm bảo Agent luôn có thông tin cơ bản để cá nhân hóa lời nói của mình, ví dụ: “Chào [Tên], [Hoạt động Yêu thích] của bạn hôm nay thế nào?” |

### 5.2 Ký ức Động (Dynamic Memory)

Ký ức Động là cơ chế cho phép Agent “học” và “ghi nhớ” các chi tiết mới phát sinh trong các cuộc hội thoại với trẻ.

#### 5.2.1 Mục tiêu Sản phẩm

> Mục tiêu của Ký ức Động là **tạo ra cảm giác về một mối quan hệ liên tục và đang phát triển** giữa Agent và trẻ. Bằng cách ghi nhớ và gợi lại các chi tiết từ các cuộc hội thoại trước, Agent thể hiện sự quan tâm, tăng cường cá nhân hóa và sự gắn bó cảm xúc của trẻ với sản phẩm.

#### 5.2.2 Logic Thực thi

Ký ức Động bao gồm hai quy trình chính: **Trích xuất (Extract)** và **Tìm kiếm (Search)**.

**Quy trình Trích xuất**

| Tính năng | Chi tiết |
| :--- | :--- |
| **Kích hoạt** | Sau khi cuộc hội thoại kết thúc (Cuối hội thoại). |
| **Hành động** | Gọi một hàm/API trích xuất ký ức (thường là một lời nhắc LLM chuyên biệt). |
| **Nội dung được Trích xuất** | Thông tin liên quan đến các sự kiện, sở thích hoặc câu chuyện mà trẻ đã đề cập trong suốt cuộc hội thoại. |
| **Lưu trữ** | Lưu trữ ký ức được trích xuất, liên kết với `user_id` tương ứng. |
| **Mục đích** | Chuyển đổi hội thoại không có cấu trúc thành các mảnh thông tin có cấu trúc mà Agent có thể tái sử dụng sau này. |

**Quy trình Tìm kiếm**

| Tính năng | Chi tiết |
| :--- | :--- |
| **Kích hoạt** | Khi bắt đầu ngày, trong quá trình tương tác “nói chuyện lựa chọn hàng ngày”. |
| **Hành động** | Truy vấn cơ sở dữ liệu ký ức động. |
| **Cơ chế Tìm kiếm** | Truy vấn các ký ức động liên quan đến trẻ (dựa trên `user_id`). |
| **Cơ chế Thực thi** | Các ký ức được truy xuất sẽ được **thêm vào lời nhắc nói chuyện hàng ngày của Agent**. |
| **Mục đích** | Đảm bảo Agent có thể tham chiếu các chủ đề hoặc sự kiện gần đây của trẻ, tạo ra một cuộc hội thoại có tính liên tục và cá nhân hóa cao. |

**Tóm tắt vai trò của hai loại Ký ức:**

| Loại Ký ức | Vai trò | Bản chất |
| :--- | :--- | :--- |
| **Ký ức Tĩnh** | Cá nhân hóa cơ bản, cố định (tên, tuổi, sở thích). | Cố định, do phụ huynh cung cấp, được sử dụng trong mọi lời nhắc. |
| **Ký ức Động** | Cá nhân hóa nâng cao, đang phát triển (sự kiện, câu chuyện). | Thay đổi, tự học bởi Agent, được sử dụng để làm phong phú lời nhắc hàng ngày. |

## Hệ thống Nội dung Học tập (The Learning Content System)

Tài liệu này trình bày một bộ khung chi tiết gồm các mẫu (template) để thiết kế hoạt động học ngôn ngữ tương tác, được chia thành ba phần chính: Warm Up, Present, và Practice + Produce. Các mẫu này sử dụng phương pháp game hóa (gamification), kể chuyện (narrative-based), và nhập vai (role-play) để tạo ra một trải nghiệm học tập hấp dẫn và có cấu trúc, đặc biệt phù hợp cho trẻ em.

### Các Phần Chính

| Dạng bài học | Mục Đích Chính | Phương Pháp | Ví Dụ Hoạt Động |
| :--- | :--- | :--- | :--- |
| **1. Khởi động (Warm Up)** | Khởi động và ôn tập thông qua các trò chơi tương tác. | Dựa trên Trò chơi (Game-based) | Thi đấu phản xạ, Vòng quay may mắn, Cùng nhau bảo vệ mùa màng. |
| **2. Trình bày (Present)** | Giới thiệu kiến thức mới (từ vựng, cấu trúc câu) một cách có hệ thống. | Dựa trên Tường thuật (Narrative-based) | Kể chuyện, Tương tác với Pika. |
| **3. Thực hành + Sản xuất (Practice + Produce)** | Thực hành và ứng dụng kiến thức đã học vào các tình huống hội thoại tự nhiên. | Nhập vai (Role-play) & Giải quyết Vấn đề (Problem-solving) | Đóng vai làm quen bạn mới, phỏng vấn nhân vật, và báo cáo lại thông tin. |

### Tổng Quan Về Các Mẫu (Templates)

#### Khởi động (Warm Up) (Dựa trên Trò chơi)

Phần này tập trung vào việc tạo hứng thú và ôn luyện kỹ năng nghe-nói thông qua các trò chơi có tính cạnh tranh và phần thưởng hấp dẫn. Các mẫu chính bao gồm:

*   **Thử thách Phản xạ (Reflex Challenge):** Thi đấu với đối thủ ảo để luyện tốc độ phản xạ nghe và nói.
*   **Vòng quay May mắn/Phần thưởng Bất ngờ (Lucky Spin/Surprising Reward):** Sử dụng yếu tố bất ngờ (phần thưởng lớn) để khuyến khích trẻ ôn tập.
*   **Tập thể (Collective):** Hoạt động hợp tác, nơi trẻ dùng lời nói để tạo ra tác động trực quan (ví dụ: đuổi sâu bọ, dọn rác đại dương).
*   **Tiết lộ Tức thì (Instant Reveal):** Mở các hộp quà bí ẩn bằng cách nói đúng cấu trúc câu, tạo sự tò mò và giảm áp lực.

#### Trình bày (Present) (Dựa trên Tường thuật)

Phần này giới thiệu các khái niệm ngôn ngữ mới một cách bài bản, từ đơn giản đến phức tạp, thông qua việc kể chuyện và tương tác với một người bạn đồng hành ảo (Pika). Các mẫu chính bao gồm:

*   **Trình bày Cụm từ (Present Chunks):** Giúp trẻ ghi nhớ các cụm từ mới bằng cách lặp lại có cấu trúc và kết hợp đa giác quan (nhìn, nghe, nói).
*   **Trình bày Câu (Present Sentence):** Hướng dẫn trẻ xây dựng câu đơn hoàn chỉnh và các biến thể của nó (câu hỏi, đổi ngôi) trong các bối cảnh cụ thể.
*   **Trình bày Câu ghép (Present Compound Sentence):** Dạy trẻ cách ghép hai câu đơn thành câu ghép bằng các từ nối như "because".
*   **Nói chuyện được Dàn dựng (Scaffolded Speech):** Hướng dẫn trẻ phát triển một ý tưởng thành một bài nói ngắn hoàn chỉnh bằng cách trả lời một chuỗi các câu hỏi dẫn dắt (Ai, Cái gì, Ở đâu, Khi nào, Tại sao).

#### Thực hành + Sản xuất (Practice + Produce) (Nhập vai)

Phần cuối cùng tập trung vào việc ứng dụng ngôn ngữ vào các tình huống giao tiếp thực tế hơn, yêu cầu trẻ phải giải quyết vấn đề và tương tác một cách tự nhiên. Mẫu chính là:

*   **Thực hành có Kiểm soát (Controlled Practice) (Nhập vai):** Trẻ nhập vai vào một câu chuyện có mục tiêu rõ ràng và thực hành hội thoại qua ba phiên:
    1.  **Phiên Trả lời (Answering Session):** Đóng vai bị động, trả lời câu hỏi từ nhân vật khác.
    2.  **Phiên Đặt câu hỏi (Questioning Session):** Đóng vai chủ động, đi hỏi các nhân vật khác để thu thập thông tin.
    3.  **Phiên Báo cáo (Reporting Session):** Tường thuật lại thông tin đã thu thập được.

Nhìn chung, bộ tài liệu cung cấp một phương pháp sư phạm toàn diện, đi từ việc tiếp thu kiến thức một cách thụ động đến việc chủ động sản xuất ngôn ngữ trong các bối cảnh có ý nghĩa, đồng thời duy trì sự hứng thú của người học thông qua các yếu tố tương tác và giải trí.
